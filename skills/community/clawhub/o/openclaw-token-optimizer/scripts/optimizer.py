#!/usr/bin/env python3
"""Read-only CLI adapter. OpenClaw native reads or explicitly selected Hermes profile files."""
import argparse
import json
import math
import re
import subprocess
import sys
from pathlib import Path
from hermes_adapter import read_config, audit_hermes
from optimizer_core import VERSION, audit, route, context_report, budget

MAX_BYTES = 8 * 1024 * 1024

def read_json(path, default=None):
    if not path:
        return default
    p = Path(path)
    if p.stat().st_size > MAX_BYTES:
        raise ValueError('Input exceeds 8 MiB limit')
    value = json.loads(p.read_text())
    if not isinstance(value, dict):
        raise ValueError('Expected a JSON object')
    return value

def native(args, json_output=True):
    # No shell, no arbitrary executable/command option, no auth probe or mutation.
    result = subprocess.run(['openclaw', *args], capture_output=True, text=True, timeout=45, check=False)
    if result.returncode:
        raise ValueError('Native read command failed; inspect OpenClaw locally. Raw output withheld to protect secrets.')
    if len(result.stdout) > MAX_BYTES:
        raise ValueError('Native response exceeds limit')
    return json.loads(result.stdout) if json_output else result.stdout.strip()

def main():
    p = argparse.ArgumentParser(description='Token Optimizer v4: read-only evidence-based analysis')
    p.add_argument('--version', action='version', version=VERSION)
    sub = p.add_subparsers(dest='command', required=True)
    for cmd in ('audit', 'plan', 'route'):
        s = sub.add_parser(cmd)
        s.add_argument('--runtime', choices=['openclaw','hermes'], default='openclaw', help='Explicit runtime; default preserves OpenClaw compatibility')
        s.add_argument('--hermes-home', help='Explicit Hermes profile directory; reads config.yaml and cron/jobs.json only')
        s.add_argument('--hermes-model-env', help='Optional explicit HERMES_MODEL value; ambient environment is never read')
        s.add_argument('--catalog')
        s.add_argument('--status')
        s.add_argument('--live', action='store_true', help='Run fixed native read commands; may contact configured Gateway/providers')
        s.add_argument('--agent', default='oracle', help='Agent whose native model status is read')
        s.add_argument('--json', action='store_true')
        s.add_argument('--openclaw-version', help='Installed version for offline compatibility checks')
        if cmd == 'route':
            s.add_argument('--policy', required=True)
            s.add_argument('--tier', required=True)
            s.add_argument('--image', action='store_true')
            s.add_argument('--tools', action='store_true')
            s.add_argument('--context-tokens', type=int, default=0)
        else:
            s.add_argument('--config', help='Explicit local JSON config; never written or echoed')
            s.add_argument('--jobs')
            s.add_argument('--sessions', help='Normalized JSON object containing sessions array')
    s = sub.add_parser('context')
    s.add_argument('files', nargs='+', help='Explicit bootstrap files; no recursive traversal')
    s.add_argument('--json', action='store_true')
    s = sub.add_parser('budget')
    s.add_argument('--usage', help='JSON {costUSD, complete}; no native ingestion')
    s.add_argument('--limit', type=float)
    s.add_argument('--json', action='store_true')
    a = p.parse_args()
    try:
        if a.command in ('audit', 'plan', 'route'):
            if not re.fullmatch(r'[A-Za-z0-9_-]+', a.agent):
                raise ValueError('Invalid agent identifier')
            if a.runtime == 'hermes':
                if a.live and not a.hermes_home:
                    raise ValueError('Hermes live file mode needs an explicit profile directory')
                if a.command == 'route':
                    if a.live or a.hermes_home:
                        raise ValueError('Hermes route requires explicit normalized catalog/status exports; no native discovery')
                    if a.context_tokens < 0: raise ValueError('Context must not be negative')
                    result = route(read_json(a.catalog,{}),read_json(a.status,{}),read_json(a.policy),a.tier,a.image,a.tools,a.context_tokens)
                    result['runtime']='hermes'
                else:
                    if a.catalog or a.status or a.sessions:
                        raise ValueError('Hermes audit does not ingest catalog/status/session evidence')
                    if a.hermes_home and (a.config or a.jobs):
                        raise ValueError('Choose profile directory OR explicit exports, not both')
                    home=Path(a.hermes_home).expanduser() if a.hermes_home else None
                    config_path=home/'config.yaml' if home else a.config
                    jobs_path=home/'cron/jobs.json' if home else a.jobs
                    # Missing explicit profile files are errors, not empty successful audits.
                    config=read_config(config_path) if config_path else {}
                    jobs=read_json(jobs_path,{})
                    result=audit_hermes(config,jobs.get('jobs',[]),a.hermes_model_env,bool(config_path),bool(jobs_path))
                    if a.command == 'plan':
                        result['plan']=[{'action':f['message'],'automatic':False} for f in result['findings']]
                        result['patches']=[]
            else:
                if a.hermes_home or a.hermes_model_env:
                    raise ValueError('Hermes options require --runtime hermes')
                installed_version = native(['--version'], json_output=False) if a.live else a.openclaw_version
                cat = native(['models', 'list', '--agent', a.agent, '--all', '--json']) if a.live else read_json(a.catalog, {})
                status = native(['models', 'status', '--agent', a.agent, '--json']) if a.live else read_json(a.status, {})
                if a.command == 'route':
                    if a.context_tokens < 0:
                        raise ValueError('Context must not be negative')
                    result = route(cat, status, read_json(a.policy), a.tier, a.image, a.tools, a.context_tokens)
                else:
                    jobs = native(['cron', 'list', '--all', '--json']) if a.live else read_json(a.jobs, {})
                    sessions = read_json(a.sessions, {})
                    result = audit(cat, status, read_json(a.config, {}), jobs.get('jobs', []), sessions.get('sessions'))
                    result['coverage'] = {'config': bool(a.config), 'catalog': bool(a.live or a.catalog), 'status': bool(a.live or a.status), 'jobs': bool(a.live or a.jobs)}
                    if jobs.get('hasMore'):
                        result['limitations'].append('Automation response is paginated; this report covers only returned jobs.')
                    if a.command == 'plan':
                        result['plan'] = [{'action': f['message'], 'automatic': False} for f in result['findings']]
                        result['patches'] = []
                        result['limitations'].append('No schema-blind config patches: validate each proposed change against your installed OpenClaw schema.')
                match = re.search(r'(202[0-9])\.(\d+)\.(\d+)', installed_version or '')
                parsed = tuple(map(int, match.groups())) if match else None
                result['compatibility'] = {'installed': '.'.join(match.groups()) if match else None, 'adapterTested': '2026.9.4', 'status': 'tested_version' if parsed == (2026,9,4) else ('older_than_supported' if parsed and parsed < (2026,9,4) else 'unverified_version')}
        elif a.command == 'context':
            files = {}
            for i, path in enumerate(a.files):
                file = Path(path)
                if file.stat().st_size > MAX_BYTES:
                    raise ValueError('Context input exceeds limit')
                files[f'{i+1}:{file.name}'] = file.read_text()
            result = context_report(files)
        else:
            if a.limit is not None and (not math.isfinite(a.limit) or a.limit <= 0):
                raise ValueError('Limit must be positive')
            result = budget(read_json(a.usage), a.limit)
        # Reports are constructed from selected fields, never raw config/auth/prompts.
        if a.json:
            print(json.dumps(result, indent=2))
        else:
            print(f'Token Optimizer {VERSION} — {a.command} (read-only)')
            for key, value in result.items():
                if key != 'version':
                    print(f'{key}: {json.dumps(value, ensure_ascii=False)}')
        return 0
    except (ValueError, OSError, TypeError, AttributeError, KeyError, subprocess.TimeoutExpired):
        print('Unable to analyze input: invalid/missing JSON/YAML, unsupported shape, or native read failure. No changes made. Raw data withheld.', file=sys.stderr)
        return 2

if __name__ == '__main__':
    sys.exit(main())
