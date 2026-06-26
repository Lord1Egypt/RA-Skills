#!/usr/bin/env python3
"""
Host Resource Watchdog -- Layer 2 of LLM Stream Guard.

Runs as a standalone daemon outside the Openclaw gateway process.
Monitors CPU / RAM / Disk redlines, detects poison-pill processes
and memory leaks in the gateway's child tree, and kills offenders
with a forensic incident snapshot.
"""
import os
import sys
import time
import json
import glob
import shutil
import logging
import subprocess
from logging.handlers import RotatingFileHandler
from collections import deque
from datetime import datetime

try:
    import psutil
except ImportError:
    sys.exit(
        "FATAL: Required library 'psutil' is missing.\n"
        "Install it with:  python3 -m pip install psutil\n"
        "or use deploy.sh to prepare the environment."
    )

# --- Paths (all under the Openclaw workspace) ---
WORKSPACE = os.environ.get(
    'OPENCLAW_WORKSPACE',
    os.path.expanduser('~/.openclaw/workspace')
)
CORE_DIR = os.path.join(WORKSPACE, 'memory', 'core')
LOG_FILE = os.path.join(CORE_DIR, 'resource-metrics.jsonl')
INCIDENTS_DIR = os.path.join(CORE_DIR, 'incidents')
AUDIT_LOG = os.path.join(CORE_DIR, 'system-supervisor-audit.md')
SESSIONS_DIR = os.path.expanduser('~/.openclaw/agents/main/sessions')


def ensure_dirs():
    os.makedirs(INCIDENTS_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    os.makedirs(SESSIONS_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(AUDIT_LOG), exist_ok=True)


class HeartbeatManager:
    def __init__(self):
        self.lock_file = '/dev/shm/watchdog_heartbeat.lock'
        try:
            if not os.path.exists(self.lock_file):
                with open(self.lock_file, 'w') as f:
                    pass
            os.utime(self.lock_file, None)
        except Exception:
            pass

    def tick(self):
        try:
            if not os.path.exists(self.lock_file):
                with open(self.lock_file, 'w') as f:
                    pass
            os.utime(self.lock_file, None)
        except Exception:
            pass


class TelemetryEngine:
    """Detects monotonically rising RSS (memory leak heuristic)."""

    def check_memory_leak(self, history):
        if len(history) < 2:
            return False
        now = time.time()
        window = 60
        window_history = [h for h in history if now - h['timestamp'] <= window]
        if len(window_history) < 5:
            return False

        start_rss = window_history[0].get('rss', 0)
        end_rss = window_history[-1].get('rss', 0)

        if end_rss - start_rss <= 100 * 1024 * 1024:
            return False

        prev_rss = start_rss
        for h in window_history[1:]:
            curr_rss = h.get('rss', 0)
            if curr_rss < prev_rss:
                return False
            prev_rss = curr_rss
            if h.get('cpu', 0) <= 30.0:
                return False

        return True


class SystemMonitor:
    """Logs host CPU / RAM / Disk to a JSONL rotating file."""

    def __init__(self):
        self.log_handler = RotatingFileHandler(
            LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=5
        )
        self.log_handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger = logging.getLogger('resource_metrics')
        self.logger.addHandler(self.log_handler)
        self.logger.setLevel(logging.INFO)

    def tick(self):
        try:
            cpu_pct = psutil.cpu_percent(interval=None)
            mem = psutil.virtual_memory()
            ram_pct = mem.percent
            disk = psutil.disk_usage('/')
            disk_pct = disk.percent

            self.logger.info(json.dumps({
                'ts': datetime.utcnow().isoformat(),
                'cpu': round(cpu_pct, 1),
                'ram': round(ram_pct, 1),
                'disk': round(disk_pct, 1),
            }))
            return cpu_pct, ram_pct, disk_pct
        except Exception:
            return 0.0, 0.0, 0.0


class ProcessMonitor:
    """Tracks the Openclaw gateway process tree for anomalies."""

    def __init__(self):
        self.history = {}
        self.procs = {}
        self.crash_history = deque()
        self.last_known_pid = None
        self.CRASH_THRESHOLD = 3
        self.TIME_WINDOW_SEC = 120

    def check_gateway_health(self, current_pid):
        now = time.time()
        while self.crash_history and (now - self.crash_history[0] > self.TIME_WINDOW_SEC):
            self.crash_history.popleft()

        if current_pid is None and self.last_known_pid is not None:
            self.crash_history.append(now)
            self.last_known_pid = None
        elif (current_pid is not None and self.last_known_pid is not None
              and current_pid != self.last_known_pid):
            self.crash_history.append(now)
            self.last_known_pid = current_pid
        elif current_pid is not None and self.last_known_pid is None:
            self.last_known_pid = current_pid

        if len(self.crash_history) >= self.CRASH_THRESHOLD:
            self.crash_history.clear()
            return True
        return False

    def update(self):
        now = time.time()
        gateway_pid = None

        # TOCTOU-resilient: outer try wraps the entire iteration
        try:
            for p in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmdline = p.info.get('cmdline', [])
                    name = p.info.get('name', '')
                    if cmdline is None:
                        cmdline = []
                    cmdline_str = ' '.join(cmdline)
                    if (('openclaw' in cmdline_str and 'gateway' in cmdline_str)
                            or 'openclaw.mjs' in cmdline_str
                            or 'openclaw-gateway' in name):
                        gateway_pid = p.info['pid']
                        break
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception:
            pass

        is_crash_looping = self.check_gateway_health(gateway_pid)
        active_keys = set()

        if gateway_pid:
            try:
                gateway_proc = psutil.Process(gateway_pid)
                try:
                    children = gateway_proc.children(recursive=True)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    children = []
                my_pid = os.getpid()

                for child in children:
                    try:
                        pid = child.pid
                        if pid == my_pid or pid <= 100:
                            continue

                        ctime = child.create_time()
                        key = (pid, ctime)
                        active_keys.add(key)

                        if key not in self.procs:
                            self.procs[key] = child
                            self.history[key] = deque()
                            try:
                                child.cpu_percent(interval=None)
                            except Exception:
                                pass

                            try:
                                io = child.io_counters()
                                io_total = io.read_bytes + io.write_bytes
                            except Exception:
                                io_total = 0
                            try:
                                rss = child.memory_info().rss
                            except Exception:
                                rss = 0
                            self.history[key].append({
                                'timestamp': now,
                                'cpu': 0.0,
                                'io_total': io_total,
                                'rss': rss,
                            })
                            continue

                        proc = self.procs[key]
                        try:
                            cpu = proc.cpu_percent(interval=None)
                        except Exception:
                            cpu = 0.0

                        try:
                            io = proc.io_counters()
                            io_total = io.read_bytes + io.write_bytes
                        except Exception:
                            io_total = 0

                        try:
                            rss = proc.memory_info().rss
                        except Exception:
                            rss = 0
                        self.history[key].append({
                            'timestamp': now,
                            'cpu': cpu,
                            'io_total': io_total,
                            'rss': rss,
                        })

                        while self.history[key] and now - self.history[key][0]['timestamp'] > 300:
                            self.history[key].popleft()

                    except (psutil.NoSuchProcess, psutil.AccessDenied, AttributeError):
                        continue
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        dead_keys = set(self.procs.keys()) - active_keys
        for k in dead_keys:
            del self.procs[k]
            if k in self.history:
                del self.history[k]

        return is_crash_looping

    def check_poison_pill(self, history, proc):
        """Detect CPU-bound process with zero I/O for 15 seconds."""
        if not history:
            return False
        POISON_WINDOW = 15
        CPU_THRESHOLD = 95.0
        now = time.time()
        window_start_time = now - POISON_WINDOW
        window_history = [h for h in history if h['timestamp'] >= window_start_time]
        if len(window_history) < 2:
            return False
        if now - window_history[0]['timestamp'] < (POISON_WINDOW - 1):
            return False
        start_io = window_history[0]['io_total']
        end_io = window_history[-1]['io_total']
        if end_io - start_io > 0:
            return False
        for entry in window_history:
            if entry['cpu'] <= CPU_THRESHOLD:
                return False
        return True


class WatchdogOrchestrator:
    def __init__(self):
        self.heartbeat_manager = HeartbeatManager()
        self.telemetry = TelemetryEngine()
        self.sys_monitor = SystemMonitor()
        self.process_monitor = ProcessMonitor()
        self.CPU_REDLINE = 90.0
        self.RAM_REDLINE = 90.0
        self.DISK_REDLINE = 90.0

    def kill_process_tree(self, proc):
        try:
            try:
                children = proc.children(recursive=True)
                for child in children:
                    try:
                        child.kill()
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
            proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    def capture_process_incident_snapshot(self, reason, target_process, extra_info=''):
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        report_path = os.path.join(INCIDENTS_DIR, f'incident_report_{timestamp}.md')
        try:
            # Collect system logs (journalctl -> syslog -> messages fallback)
            try:
                if shutil.which('journalctl'):
                    sys_logs = subprocess.check_output(
                        ['journalctl', '-u', 'openclaw', '-n', '50', '--no-pager'],
                        text=True, timeout=10, stderr=subprocess.DEVNULL
                    )
                else:
                    sys_logs = ''
                if not sys_logs:
                    try:
                        log_paths = ['/var/log/syslog', '/var/log/messages']
                        sys_logs = 'No system logs available.'
                        for p in log_paths:
                            if os.path.exists(p):
                                with open(p, 'r') as f:
                                    lines = f.readlines()[-50:]
                                    sys_logs = ''.join(lines)
                                    break
                    except Exception:
                        sys_logs = 'No system logs available.'
            except Exception:
                sys_logs = 'Error fetching system logs.'

            # Collect kernel segfault / OOM logs
            try:
                dmesg_result = subprocess.check_output(
                    ['dmesg', '-T'],
                    text=True, timeout=5, stderr=subprocess.DEVNULL
                )
                segfault_lines = [
                    line for line in dmesg_result.split('\n')
                    if any(kw in line.lower() for kw in ['segfault', 'error 4', 'killed'])
                ]
                dmesg_logs = ('\n'.join(segfault_lines[-10:])
                              if segfault_lines else 'No segfaults found in dmesg.')
            except Exception:
                dmesg_logs = 'Unable to read dmesg.'

            with open(report_path, 'w') as f:
                f.write(f'# Process Incident Report: {timestamp}\n')
                f.write(f'**Trigger**: {reason} for process `{target_process}`\n')
                if extra_info:
                    f.write(f'**Details**: {extra_info}\n')
                f.write('\n## 1. System/Process Error Tail\n```log\n')
                f.write(sys_logs + '\n```\n\n')
                f.write('## 2. Kernel Segfault/OOM Logs\n```bash\n')
                f.write(dmesg_logs + '\n```\n')

            with open(AUDIT_LOG, 'a') as f:
                f.write(f'\n\n**{timestamp} - SYSTEM CRITICAL EVENT**\n')
                f.write(f'{reason}. Snapshot saved to: `{report_path}`\n')
                if extra_info:
                    f.write(f'Details: {extra_info}\n')
            return report_path
        except Exception as e:
            print(f'Failed to capture snapshot: {e}', file=sys.stderr)
            return None

    def tick(self):
        self.heartbeat_manager.tick()
        cpu_pct, ram_pct, disk_pct = self.sys_monitor.tick()
        is_crash_looping = self.process_monitor.update()

        if is_crash_looping:
            print('[WARNING] Gateway Crash Loop Detected! Capturing logs.', file=sys.stderr)
            self.capture_process_incident_snapshot('CRASH LOOP DETECTED', 'openclaw')
            time.sleep(30)
            return

        redline_breached = []
        if cpu_pct >= self.CPU_REDLINE:
            redline_breached.append(f'CPU {cpu_pct:.1f}%')
        if ram_pct >= self.RAM_REDLINE:
            redline_breached.append(f'RAM {ram_pct:.1f}%')
        if disk_pct >= self.DISK_REDLINE:
            redline_breached.append(f'Disk {disk_pct:.1f}%')

        if redline_breached:
            timestamp = datetime.utcnow().isoformat()
            breach_msg = ', '.join(redline_breached)
            print(f'[WARNING] PHYSICAL REDLINE BREACH: {breach_msg}', file=sys.stderr)
            try:
                with open(AUDIT_LOG, 'a') as f:
                    f.write(f'\n- **{timestamp}**: PHYSICAL REDLINE BREACH: {breach_msg}')
            except Exception:
                pass

        poison_key = None
        for key, history in self.process_monitor.history.items():
            try:
                proc = self.process_monitor.procs[key]
                if self.process_monitor.check_poison_pill(history, proc):
                    poison_key = key
                    break
            except Exception:
                continue

        if poison_key:
            print(
                f'[CRITICAL] Poison Pill Detected on PID {poison_key[0]}! '
                f'(0 I/O, >95% CPU for 15s)',
                file=sys.stderr
            )
            self.capture_process_incident_snapshot(
                'POISON PILL DETECTED', f'PID {poison_key[0]}',
                extra_info='CPU >95% with 0 I/O for 15s'
            )
            try:
                proc = self.process_monitor.procs[poison_key]
                self.kill_process_tree(proc)
            except Exception:
                pass
            if poison_key in self.process_monitor.history:
                del self.process_monitor.history[poison_key]
            if poison_key in self.process_monitor.procs:
                del self.process_monitor.procs[poison_key]
            time.sleep(5)
            return

        leak_key = None
        for key, history in self.process_monitor.history.items():
            if self.telemetry.check_memory_leak(history):
                leak_key = key
                break

        if leak_key:
            print(
                f'[CRITICAL] RSS Dual-Lock (Monotonic + No GC + >100MB) '
                f'Triggered on PID {leak_key[0]}!',
                file=sys.stderr
            )
            self.capture_process_incident_snapshot(
                'RSS DUAL-LOCK TRIGGERED (MEMORY LEAK)', f'PID {leak_key[0]}'
            )
            try:
                proc = self.process_monitor.procs[leak_key]
                self.kill_process_tree(proc)
            except Exception:
                pass
            if leak_key in self.process_monitor.history:
                del self.process_monitor.history[leak_key]
            if leak_key in self.process_monitor.procs:
                del self.process_monitor.procs[leak_key]
            time.sleep(5)
            return


def main():
    ensure_dirs()
    orchestrator = WatchdogOrchestrator()
    print('Host Resource Watchdog (LLM Stream Guard Layer 2) Started...', flush=True)

    while True:
        try:
            orchestrator.tick()
            time.sleep(2)
        except Exception:
            import traceback
            traceback.print_exc(file=sys.stderr)
            time.sleep(2)


if __name__ == '__main__':
    main()
