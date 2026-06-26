#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(os.environ.get('MEMORY_ROOT', Path.cwd() / 'memory'))
SCRIPTS = Path(__file__).resolve().parent


def run(script, input_text=None, json_input=None, extra_env=None, args=None):
    cmd = [sys.executable, str(SCRIPTS / script)] + (args or [])
    env = os.environ.copy()
    env['MEMORY_ROOT'] = str(ROOT)
    if extra_env:
        env.update(extra_env)
    if json_input is not None:
        p = subprocess.run(cmd, input=json.dumps(json_input, ensure_ascii=False), text=True, capture_output=True, env=env)
    else:
        p = subprocess.run(cmd, input=input_text, text=True, capture_output=True, env=env)
    if p.returncode != 0:
        sys.stderr.write(p.stderr or p.stdout)
        raise SystemExit(p.returncode)
    sys.stdout.write(p.stdout)


def cmd_bootstrap(_):
    run('setup_memory_system.py')
    run('generate_memory_index.py')


def cmd_capture(args):
    events_json = subprocess.run(
        [sys.executable, str(SCRIPTS / 'extract_memory_events.py')],
        input=args.text,
        text=True,
        capture_output=True,
        env={**os.environ, 'MEMORY_ROOT': str(ROOT)},
    )
    if events_json.returncode != 0:
        sys.stderr.write(events_json.stderr or events_json.stdout)
        raise SystemExit(events_json.returncode)
    run('apply_memory_events.py', json_input=json.loads(events_json.stdout))
    run('generate_memory_index.py')


def cmd_gate(args):
    run('should_trigger_memory.py', input_text=args.text)


def cmd_turn(args):
    gate = subprocess.run(
        [sys.executable, str(SCRIPTS / 'should_trigger_memory.py')],
        input=args.text,
        text=True,
        capture_output=True,
        env={**os.environ, 'MEMORY_ROOT': str(ROOT)},
    )
    if gate.returncode != 0:
        sys.stderr.write(gate.stderr or gate.stdout)
        raise SystemExit(gate.returncode)
    gate_data = json.loads(gate.stdout)
    result = {'gate': gate_data}

    if gate_data.get('should_write'):
        events_json = subprocess.run(
            [sys.executable, str(SCRIPTS / 'extract_memory_events.py')],
            input=args.text,
            text=True,
            capture_output=True,
            env={**os.environ, 'MEMORY_ROOT': str(ROOT)},
        )
        if events_json.returncode != 0:
            sys.stderr.write(events_json.stderr or events_json.stdout)
            raise SystemExit(events_json.returncode)
        apply_p = subprocess.run(
            [sys.executable, str(SCRIPTS / 'apply_memory_events.py')],
            input=events_json.stdout,
            text=True,
            capture_output=True,
            env={**os.environ, 'MEMORY_ROOT': str(ROOT)},
        )
        if apply_p.returncode != 0:
            sys.stderr.write(apply_p.stderr or apply_p.stdout)
            raise SystemExit(apply_p.returncode)
        result['write'] = json.loads(apply_p.stdout)

    if gate_data.get('should_recall'):
        recall_p = subprocess.run(
            [sys.executable, str(SCRIPTS / 'recall_memory.py')],
            input=args.text,
            text=True,
            capture_output=True,
            env={**os.environ, 'MEMORY_ROOT': str(ROOT)},
        )
        if recall_p.returncode != 0:
            sys.stderr.write(recall_p.stderr or recall_p.stdout)
            raise SystemExit(recall_p.returncode)
        result['recall'] = json.loads(recall_p.stdout)

    if gate_data.get('should_reflect'):
        reflect_p = subprocess.run(
            [sys.executable, str(SCRIPTS / 'reflect_memory.py')],
            text=True,
            capture_output=True,
            env={**os.environ, 'MEMORY_ROOT': str(ROOT)},
        )
        if reflect_p.returncode != 0:
            sys.stderr.write(reflect_p.stderr or reflect_p.stdout)
            raise SystemExit(reflect_p.returncode)
        result['reflect'] = json.loads(reflect_p.stdout)

    if gate_data.get('should_process'):
        subprocess.run(
            [sys.executable, str(SCRIPTS / 'generate_memory_index.py')],
            text=True,
            capture_output=True,
            env={**os.environ, 'MEMORY_ROOT': str(ROOT)},
        )

    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_recall(args):
    run('recall_memory.py', input_text=args.query)


def cmd_reflect(_):
    run('reflect_memory.py')
    run('generate_memory_index.py')


def cmd_new_topic(args):
    run('new_topic_card.py', args=[
        '--slug', args.slug,
        '--title', args.title,
        '--summary', args.summary,
    ])
    run('generate_memory_index.py')


def cmd_new_object(args):
    argv = ['--type', args.type, '--domain', args.domain, '--slug', args.slug, '--title', args.title, '--summary', args.summary]
    run('new_memory_object.py', args=argv)
    run('generate_memory_index.py')


def main():
    ap = argparse.ArgumentParser(description='White-box memory orchestrator CLI')
    sub = ap.add_subparsers(dest='cmd', required=True)

    sub.add_parser('bootstrap').set_defaults(func=cmd_bootstrap)

    p_capture = sub.add_parser('capture')
    p_capture.add_argument('text')
    p_capture.set_defaults(func=cmd_capture)

    p_gate = sub.add_parser('gate')
    p_gate.add_argument('text')
    p_gate.set_defaults(func=cmd_gate)

    p_turn = sub.add_parser('turn')
    p_turn.add_argument('text')
    p_turn.set_defaults(func=cmd_turn)

    p_recall = sub.add_parser('recall')
    p_recall.add_argument('query')
    p_recall.set_defaults(func=cmd_recall)

    sub.add_parser('reflect').set_defaults(func=cmd_reflect)

    p_topic = sub.add_parser('new-topic')
    p_topic.add_argument('--slug', required=True)
    p_topic.add_argument('--title', required=True)
    p_topic.add_argument('--summary', required=True)
    p_topic.set_defaults(func=cmd_new_topic)

    p_obj = sub.add_parser('new-object')
    p_obj.add_argument('--type', required=True)
    p_obj.add_argument('--domain', required=True)
    p_obj.add_argument('--slug', required=True)
    p_obj.add_argument('--title', required=True)
    p_obj.add_argument('--summary', required=True)
    p_obj.set_defaults(func=cmd_new_object)

    args = ap.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
