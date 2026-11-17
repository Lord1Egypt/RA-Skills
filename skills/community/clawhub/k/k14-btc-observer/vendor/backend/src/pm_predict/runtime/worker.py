"""Single writer of strategy state, isolated from HTTP/WebSocket and SQLite."""
from collections import deque
from dataclasses import asdict
import os
import queue
import time
from pm_predict.engine import PaperEngine
from pm_predict.research.scenarios import scenarios


def percentiles(values):
    v = sorted(values)
    if not v:
        return {'samples': 0, 'p50_us': None, 'p95_us': None, 'p99_us': None}
    def p(q):
        return round(v[min(len(v)-1, int((len(v)-1)*q))] / 1000, 3)
    return {'samples': len(v), 'p50_us': p(.5), 'p95_us': p(.95), 'p99_us': p(.99)}


def describe_cases():
    return [{'id': name, 'title': title, 'events': len(events), 'source': 'SYNTHETIC'}
            for name, title, events, expected in scenarios()]


def snapshot(engine, run_id, scenario, status, done, total, timings, curve, error=None):
    windows = []
    for w in engine.windows.values():
        windows.append({'id': w.id, 'start': w.start, 'side': w.side, 'k14': w.k, 'fair_up': w.fair,
                        'blocked': w.blocked, 'closed': w.closed,
                        'holdings': {k: str(v) for k,v in w.qty.items()},
                        'books': {side: {'bid': str(b[2]), 'asks': [[str(p), str(q)] for p,q in b[3]],
                                         'source_ms': b[1], 'sequence': b[0]} for side,b in w.books.items()}})
    return {'run_id': run_id, 'scenario': scenario, 'status': status, 'source': 'SYNTHETIC',
            'mode': 'OFFLINE_PAPER', 'worker_pid': os.getpid(), 'progress': {'done': done, 'total': total},
            'account': engine.summary(), 'orders': [asdict(o) for o in engine.orders.values()],
            'fills': [asdict(f) for f in engine.fills.values()], 'windows': windows,
            'events': engine.journal[-100:], 'intents': engine.intents[-50:], 'curve': list(curve),
            'latency': percentiles(timings), 'error': error, 'updated_wall_ms': int(time.time()*1000)}


def worker_main(commands, output):
    engine = PaperEngine()
    cases = {n: (title, events) for n,title,events,expected in scenarios()}
    run_id = current = None
    pending, seen = [], {}
    i = 0
    status = 'idle'
    delay = .18
    due = 0
    timings = deque(maxlen=10000)
    curve = deque(maxlen=2000)

    def send(payload):
        # Never discard an accounting event to make a dashboard look fast.
        # If the consumer fails, stop this paper process rather than keep generating actions.
        output.put(payload, timeout=.5)

    send({'kind': 'ready', 'pid': os.getpid()})
    while True:
        try:
            timeout = max(0, min(.2, due-time.monotonic())) if status == 'running' else .2
            cmd = commands.get(timeout=timeout)
        except queue.Empty:
            cmd = None
        if cmd:
            action = cmd['action']
            if action == 'shutdown':
                return
            if action == 'start':
                if status in ('running', 'paused'):
                    send({'kind': 'command_rejected', 'reason': 'run is active'})
                    continue
                current, run_id = cmd['scenario'], cmd['run_id']
                engine, pending, seen, i = PaperEngine(), cases[current][1], {}, 0
                timings.clear(); curve.clear()
                delay, due, status = cmd['delay_ms']/1000, time.monotonic(), 'running'
                send({'kind': 'run_started', 'run_id': run_id, 'scenario': current,
                      'title': cases[current][0], 'created_ms': int(time.time()*1000)})
            elif action == 'pause' and status == 'running':
                status = 'paused'
            elif action == 'resume' and status == 'paused':
                status, due = 'running', time.monotonic()
            elif action == 'stop' and status in ('running', 'paused'):
                status = 'stopped'
            send({'kind': 'snapshot', 'payload': snapshot(engine, run_id, current, status, i, len(pending), timings, curve)})
        if status != 'running' or time.monotonic() < due:
            continue
        try:
            event = pending[i]
            stamp = time.perf_counter_ns()
            event_id = event['event_id']
            if event_id in seen:
                if seen[event_id] != event:
                    raise ValueError('conflicting event id')
                duplicate = True
            else:
                getattr(engine, event['method'])(**event['args'])
                seen[event_id] = event
                duplicate = False
            timings.append(time.perf_counter_ns()-stamp)
            i += 1
            curve.append({'step': i, 'cash': float(engine.cash), 'reserved': float(engine.reserve()),
                          'realized': float(engine.realized)})
            if i == len(pending):
                status = 'completed'
            state = snapshot(engine, run_id, current, status, i, len(pending), timings, curve)
            send({'kind': 'event', 'run_id': run_id, 'sequence': i, 'payload': event, 'duplicate': duplicate})
            send({'kind': 'snapshot', 'payload': state})
            due = time.monotonic()+delay
        except Exception as ex:
            status = 'error'
            send({'kind': 'runtime_error', 'run_id': run_id, 'reason': str(ex)})

