#!/usr/bin/env python3
"""Read-only, Python 3.6-compatible site and task state for agents."""
import argparse
import base64
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import uuid

SITE = "@SITE@"
PREFIX = "@PREFIX@"
ADAPTER = '@ADAPTER@'


def capture(argv, timeout=30):
    try:
        return subprocess.check_output(argv, stderr=subprocess.STDOUT,
                                       universal_newlines=True, timeout=timeout).strip(), None
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as error:
        return None, str(error)


def task(state, request):
    if not re.match(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$", request):
        raise ValueError("invalid request ID")
    directory = state / "requests" / request
    result = {"schema_version": 1, "cluster": SITE, "request_id": request,
              "phase": "not_found", "exit_code": None}
    if not (directory / "identity").exists():
        return result
    job, window, payload = (directory / "identity").read_text().strip().split("\t", 2)
    result.update(job_id=job, window=window, command=base64.b64decode(payload).decode(),
                  log_path=str(directory / "output.log"), phase="unknown")
    if (directory / "state").exists():
        fields = (directory / "state").read_text().strip().split("\t")
        result.update(phase=fields[0], updated_at=fields[1])
        if len(fields) == 3:
            result["exit_code"] = int(fields[2])
    # A durable running record alone does not prove a live process.
    result["liveness"] = "not_checked"
    return result


def status(state, doctor=False, verify_backup=False):
    queue, error = capture(["squeue", "-h", "-u", os.environ["USER"], "-o", "%i|%T|%j|%N"])
    result = {"schema_version": 1, "cluster": SITE, "host": os.uname().nodename,
              "queue_state": "unknown" if error else "known", "jobs": [],
              "routes": [], "allocations": [], "errors": [error] if error else []}
    names = ('compute_storage', 'autosave_liveness', 'snapshot_integrity', 'toolchain')
    result['checks'] = {name: dict(state='not_checked', reason='No compute observation') for name in names}
    result['checks']['scheduler'] = dict(state='unknown' if error else 'passed', reason=error or 'Queue query succeeded')
    if queue:
        for line in queue.splitlines():
            job, phase, name, node = line.split("|", 3)
            result["jobs"].append(dict(job_id=job, slurm_state=phase, name=name, node=node))
    for path in sorted((state / 'allocations').glob('*.json')):
        try:
            record = json.loads(path.read_text())
            active = next((item for item in result['jobs'] if item['job_id'] == record.get('job_id') or item['name'] == record.get('job_name')), None)
            result['allocations'].append(dict(request_id=record['request_id'], job_id=record.get('job_id') or (active['job_id'] if active else None),
                phase=record.get('phase'), scheduler_observation='unknown' if error else active['slurm_state'] if active else 'not_in_queue',
                log_path=record.get('log_path'), record_path=str(path)))
        except (OSError, ValueError, KeyError) as record_error:
            result['errors'].append('invalid allocation record: ' + str(record_error))
    for path in sorted((state / "routes").glob("*.route")):
        fields = path.read_text().strip().split("\t")
        if len(fields) < 4:
            result["errors"].append("invalid route: " + str(path))
            continue
        job, host = fields[:2]
        if not re.match(r"^[0-9]+$", job) or not re.match(r"^[A-Za-z0-9][A-Za-z0-9.-]*$", host):
            result["errors"].append("invalid route identity: " + str(path))
            continue
        active_job = next((item for item in result["jobs"] if item["job_id"] == job), None)
        route = dict(job_id=job, node=host, phase="unknown", route_path=str(path))
        if not error:
            route["phase"] = "candidate" if active_job and active_job["slurm_state"] == "RUNNING" else "inactive"
        if doctor and route["phase"] == "candidate":
            route['checks'] = {name: dict(state='not_checked', reason='Compute route unavailable') for name in names}
            if ADAPTER == "psc":
                argv = ["tmux", "-S", fields[2], "display-message", "-p", "-t", fields[3], "#{pane_dead}|#{pane_pid}"]
            else:
                argv = ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10", host,
                        "tmux -L gpu-" + job + " has-session -t work"]
            output, probe_error = capture(argv)
            healthy = not probe_error
            if ADAPTER == "psc" and healthy:
                healthy = output.startswith("0|") and (len(fields) < 6 or output.split("|")[1] == fields[5])
            route["phase"] = "reachable" if healthy else "unreachable"
            if probe_error:
                result["errors"].append(probe_error)
            if healthy:
                core_bin = Path(os.environ.get('HPC_CORE_BIN', str(Path.home() / '.local/bin')))
                argv = [str(core_bin / (SITE + '-gpu')), 'run', '--job', job, '--request', 'health-' + uuid.uuid4().hex,
                        '--wait', 'hpc-health', '--', str(core_bin / (SITE + '-health')), '--job', job]
                if verify_backup:
                    argv.append('--verify')
                output, health_error = capture(argv, int(os.environ.get('HPC_HEALTH_VERIFY_SECONDS', '300')) + 45 if verify_backup else 45)
                if health_error:
                    route['health'] = dict(healthy=False, observation='unknown', error=health_error)
                    result['errors'].append(health_error)
                else:
                    try:
                        records = [line[len('HPC_HEALTH_JSON='):] for line in output.splitlines() if line.startswith('HPC_HEALTH_JSON=')]
                        route['health'] = json.loads(records[-1])
                        if route['health'].get('job_id') != job:
                            raise ValueError('compute health job identity mismatch')
                        if not route['health'].get('healthy'):
                            result['errors'].append('unhealthy backup on job ' + job)
                        health = route['health']
                        storage = health.get('compute_storage')
                        if storage is not None:
                            route['checks']['compute_storage'] = dict(state='passed' if storage.get('writable') else 'failed',
                                                                      reason='Job-local path writability')
                        if 'autosave_state' in health:
                            route['checks']['autosave_liveness'] = dict(state='passed' if health['autosave_state'] == 'alive' else 'failed',
                                                                        reason=health['autosave_state'])
                        if health.get('integrity') not in (None, 'not_checked'):
                            route['checks']['snapshot_integrity'] = dict(state='passed' if health['integrity'] == 'verified' else
                                                                        'unknown' if health['integrity'] == 'unknown' else 'failed',
                                                                        reason=health.get('integrity_output', health['integrity']))
                    except (IndexError, ValueError) as health_error:
                        route['health'] = dict(healthy=False, observation='unknown', error=str(health_error))
                        result['errors'].append(str(health_error))
        result["routes"].append(route)
    for name in names:
        observed = [r.get('checks', {}).get(name, {}) for r in result['routes'] if r['phase'] in ('reachable', 'unreachable')]
        if observed:
            states = [c.get('state', 'not_checked') for c in observed]
            selected = next((s for s in ('failed', 'unknown', 'not_checked', 'passed') if s in states))
            result['checks'][name] = dict(state=selected, reason='See per-route checks')
    result['checks_not_performed'] = [name for name in names if result['checks'][name]['state'] == 'not_checked']
    result['next_actions'] = []
    if error: result['next_actions'].append('Retry scheduler observation; do not submit a replacement allocation')
    if doctor and not any(r['phase'] == 'reachable' for r in result['routes']):
        result['next_actions'].append('Inspect the recorded allocation and login pane; compute checks have not run')
    if doctor and not verify_backup:
        result['next_actions'].append('Use doctor --verify-backup when archive integrity needs verification')
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["task", "status", "doctor"])
    parser.add_argument("request", nargs="?")
    parser.add_argument('--verify-backup', action='store_true')
    args = parser.parse_args()
    state = Path(os.environ.get(PREFIX + "_GPU_STATE_DIR", str(Path.home() / ".local/state" / (SITE + "-gpu"))))
    try:
        if args.verify_backup and args.mode != 'doctor':
            raise ValueError('--verify-backup requires doctor')
        result = task(state, args.request or "") if args.mode == "task" else status(state, args.mode == "doctor", args.verify_backup)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 1 if result.get("errors") or result.get("phase") == "not_found" else 0
    except (ValueError, OSError) as error:
        print(json.dumps({"schema_version": 1, "cluster": SITE, "error": str(error)}))
        return 2


if __name__ == "__main__":
    sys.exit(main())
