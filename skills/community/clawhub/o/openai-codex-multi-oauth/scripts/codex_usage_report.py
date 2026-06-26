#!/usr/bin/env python3
import argparse
import base64
import json
import socket
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any

USAGE_URL = 'https://chatgpt.com/backend-api/wham/usage'
DEFAULT_ACTIVE_SLOT_ID = 'openai-codex:default'


def load_json(path: Path | None):
    if path is None or not path.exists():
        return None
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)


def decode_email(profile: dict[str, Any] | None):
    access = (profile or {}).get('access') or (profile or {}).get('token')
    if not isinstance(access, str) or access.count('.') < 2:
        return None
    try:
        payload = access.split('.')[1]
        payload += '=' * (-len(payload) % 4)
        decoded = json.loads(base64.urlsafe_b64decode(payload.encode()).decode())
        return ((decoded.get('https://api.openai.com/profile') or {}).get('email'))
    except Exception:
        return None


def default_paths(state_dir: Path, agent: str, repo_path: str | None):
    return {
        'repo': Path(repo_path).expanduser() if repo_path else state_dir / 'codex-oauth-profiles.json',
        'auth': state_dir / 'agents' / agent / 'agent' / 'auth-profiles.json',
    }


def load_repo(paths: dict[str, Path | None], auth: dict[str, Any]):
    repo = load_json(paths['repo'])
    if isinstance(repo, dict):
        return repo
    profiles = {
        pid: cred
        for pid, cred in ((auth.get('profiles') or {}).items())
        if isinstance(pid, str) and pid.startswith('openai-codex:') and isinstance(cred, dict)
    }
    return {'profiles': profiles}


def profile_signature(profile: dict[str, Any] | None):
    if not isinstance(profile, dict):
        return None
    return (
        profile.get('accountId'),
        profile.get('workspaceName') or profile.get('workspaceId') or profile.get('workspace'),
        profile.get('access') or profile.get('token'),
        profile.get('refreshToken'),
    )


def detect_active_profile_id(auth: dict[str, Any], repo: dict[str, Any], active_slot_id: str):
    active = ((auth.get('profiles') or {}).get(active_slot_id))
    active_sig = profile_signature(active)
    if active_sig is None:
        return None
    for pid, profile in (repo.get('profiles') or {}).items():
        if not isinstance(pid, str) or not pid.startswith('openai-codex:'):
            continue
        if profile_signature(profile) == active_sig:
            return pid
    return None


def collect_profiles(auth: dict[str, Any], repo: dict[str, Any]):
    repo_profiles = repo.get('profiles') or {}
    auth_profiles = auth.get('profiles') or {}
    seen = set(repo_profiles) | {pid for pid in auth_profiles if str(pid).startswith('openai-codex:')}
    profiles = []
    for pid in sorted(seen):
        source = repo_profiles.get(pid) or auth_profiles.get(pid) or {}
        profiles.append({
            'profileId': pid,
            'accountId': source.get('accountId'),
            'email': source.get('email') or decode_email(source),
            'workspace': source.get('workspaceName') or source.get('workspaceId') or source.get('workspace'),
            'access': source.get('access') or source.get('token'),
        })
    return profiles


def select_profiles(items: list[dict[str, Any]], targets: list[str] | None):
    if not targets:
        return items
    wanted = set(targets)
    out = []
    for item in items:
        pid = item['profileId']
        short = pid.split(':', 1)[1] if ':' in pid else pid
        if pid in wanted or short in wanted:
            out.append(item)
    return out


def fetch_usage(item: dict[str, Any], timeout_seconds: int):
    token = item.get('access')
    if not token:
        return {'error': 'missing token'}
    headers = {
        'Authorization': f'Bearer {token}',
        'User-Agent': 'CodexBar',
        'Accept': 'application/json',
    }
    if item.get('accountId'):
        headers['ChatGPT-Account-Id'] = item['accountId']
    req = urllib.request.Request(USAGE_URL, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout_seconds) as res:
            return json.loads(res.read().decode())
    except urllib.error.HTTPError as exc:
        return {'error': f'HTTP {exc.code}'}
    except socket.timeout:
        return {'error': 'timeout'}
    except Exception as exc:
        return {'error': exc.__class__.__name__}


def window_line(window: dict[str, Any] | None):
    if not isinstance(window, dict) or not window:
        return None
    seconds = int(window.get('limit_window_seconds') or 0)
    if seconds >= 604800:
        label = 'Week'
    elif seconds >= 86400:
        label = 'Day'
    elif seconds > 0:
        label = f'{round(seconds / 3600)}h'
    else:
        label = 'Window'
    used = float(window.get('used_percent') or 0)
    left = max(0, min(100, round(100 - used)))
    reset_at = window.get('reset_at')
    reset_txt = '-'
    if reset_at:
        try:
            reset_txt = datetime.fromtimestamp(int(reset_at)).isoformat(sep=' ', timespec='minutes')
        except Exception:
            reset_txt = str(reset_at)
    return f'{label} {left}% left (reset {reset_txt})'


def summarize_usage(data: dict[str, Any]):
    if data.get('error'):
        return {'error': data['error']}
    usage_windows = []
    for key in ('primary_window', 'secondary_window'):
        line = window_line(((data.get('rate_limit') or {}).get(key) or {}))
        if line:
            usage_windows.append(line)
    review_windows = []
    for key in ('primary_window', 'secondary_window'):
        line = window_line(((data.get('code_review_rate_limit') or {}).get(key) or {}))
        if line:
            review_windows.append(line)
    return {
        'user_id': data.get('user_id'),
        'account_id': data.get('account_id'),
        'email': data.get('email'),
        'plan_type': data.get('plan_type'),
        'usage_windows': usage_windows,
        'code_review_windows': review_windows,
        'raw': data,
    }


def print_human(rows: list[dict[str, Any]], active_profile_id: str | None):
    if not rows:
        print('No openai-codex profiles selected.')
        return
    print('Codex usage report')
    if active_profile_id:
        print(f'active_profile: {active_profile_id}')
    duplicate_accounts: dict[str, list[str]] = {}
    for row in rows:
        acct = row.get('accountId') or row.get('usage', {}).get('account_id')
        if acct:
            duplicate_accounts.setdefault(acct, []).append(row['profileId'])
    for idx, row in enumerate(rows, start=1):
        usage = row['usage']
        suffix = ' [active]' if row['profileId'] == active_profile_id else ''
        print(f"{idx}. {row['profileId']}{suffix}")
        print(f"   store_email={row.get('email') or '-'}")
        print(f"   store_accountId={row.get('accountId') or '-'}")
        if usage.get('error'):
            print(f"   error={usage['error']}")
            continue
        print(f"   api_email={usage.get('email') or '-'}")
        print(f"   api_user_id={usage.get('user_id') or '-'}")
        print(f"   api_account_id={usage.get('account_id') or '-'}")
        print(f"   plan={usage.get('plan_type') or '-'}")
        if usage.get('usage_windows'):
            print('   usage=' + ' · '.join(usage['usage_windows']))
        if usage.get('code_review_windows'):
            print('   code_review=' + ' · '.join(usage['code_review_windows']))
    dup_groups = {acct: ids for acct, ids in duplicate_accounts.items() if len(ids) > 1}
    if dup_groups:
        print('\nshared_account_ids:')
        for acct, ids in sorted(dup_groups.items()):
            print(f"  {acct}: {', '.join(ids)}")


def main():
    parser = argparse.ArgumentParser(description='Fetch live wham/usage data for each OpenClaw Codex OAuth profile.')
    parser.add_argument('--state-dir', default='~/.openclaw', help='OpenClaw state directory (default: ~/.openclaw)')
    parser.add_argument('--agent', default='main', help='Agent id to inspect (default: main)')
    parser.add_argument('--repo-path', default=None, help='Optional external profile repo path')
    parser.add_argument('--active-slot-id', default=DEFAULT_ACTIVE_SLOT_ID, help='Active slot profile id used by router setups')
    parser.add_argument('--profile', action='append', default=[], help='Profile id or short slot name; repeat to select multiple')
    parser.add_argument('--timeout', type=int, default=10, help='Per-request timeout in seconds (default: 10)')
    parser.add_argument('--json', action='store_true', help='Print JSON output')
    parser.add_argument('--raw', action='store_true', help='Include raw API payloads in JSON output')
    args = parser.parse_args()

    state_dir = Path(args.state_dir).expanduser()
    paths = default_paths(state_dir, args.agent, args.repo_path)
    auth = load_json(paths['auth']) or {}
    repo = load_repo(paths, auth)
    active_profile_id = detect_active_profile_id(auth, repo, args.active_slot_id)
    profiles = select_profiles(collect_profiles(auth, repo), args.profile)

    rows = []
    for item in profiles:
        raw = fetch_usage(item, timeout_seconds=args.timeout)
        usage = summarize_usage(raw)
        row = {
            'profileId': item['profileId'],
            'email': item.get('email'),
            'accountId': item.get('accountId'),
            'workspace': item.get('workspace'),
            'isActiveProfile': item['profileId'] == active_profile_id,
            'usage': usage,
        }
        if args.raw and not usage.get('error'):
            row['raw'] = usage.get('raw')
        rows.append(row)

    payload = {
        'stateDir': str(state_dir),
        'agent': args.agent,
        'activeProfileId': active_profile_id,
        'profiles': rows,
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print_human(rows, active_profile_id)


if __name__ == '__main__':
    main()
