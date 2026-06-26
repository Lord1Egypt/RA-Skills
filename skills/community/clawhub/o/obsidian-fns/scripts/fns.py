#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
import urllib.error
from pathlib import Path
from typing import Any, Dict, Optional

DEFAULT_TIMEOUT = 60
LOCAL_CONFIG = Path.home() / '.config' / 'fast-note-sync' / 'config.json'
OPENCALW_CONFIG = Path.home() / '.openclaw' / 'openclaw.json'
SKILL_KEY = 'fast-note-sync'


def eprint(*args: Any) -> None:
    print(*args, file=sys.stderr)


def load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def get_openclaw_skill_config() -> Dict[str, Any]:
    data = load_json(OPENCALW_CONFIG)
    skills = data.get('skills', {})
    entries = skills.get('entries', {}) if isinstance(skills, dict) else {}
    entry = entries.get(SKILL_KEY, {}) if isinstance(entries, dict) else {}
    return entry if isinstance(entry, dict) else {}


def get_local_config() -> Dict[str, Any]:
    return load_json(LOCAL_CONFIG)


def config_value(cli_value: Optional[str], env_key: str, key: str) -> Optional[str]:
    if cli_value is not None and str(cli_value).strip() != '':
        return str(cli_value).strip()
    env_value = os.environ.get(env_key, '').strip()
    if env_value:
        return env_value
    oc = get_openclaw_skill_config().get(key)
    if isinstance(oc, str) and oc.strip():
        return oc.strip()
    lc = get_local_config().get(key)
    if isinstance(lc, str) and lc.strip():
        return lc.strip()
    return None


def config_int(cli_value: Optional[int], env_key: str, key: str, default: int) -> int:
    if cli_value is not None:
        return int(cli_value)
    env_value = os.environ.get(env_key, '').strip()
    if env_value:
        return int(env_value)
    for source in (get_openclaw_skill_config(), get_local_config()):
        value = source.get(key)
        if isinstance(value, int):
            return value
        if isinstance(value, str) and value.strip().isdigit():
            return int(value.strip())
    return default


def save_local_config(updates: Dict[str, Any]) -> None:
    data = get_local_config()
    data.update({k: v for k, v in updates.items() if v is not None and v != ''})
    LOCAL_CONFIG.parent.mkdir(parents=True, exist_ok=True)
    LOCAL_CONFIG.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def build_url(base_url: str, path: str, query: Optional[Dict[str, Any]] = None) -> str:
    base = base_url.rstrip('/')
    if not path.startswith('/'):
        path = '/' + path
    url = base + path
    if query:
        clean = {k: v for k, v in query.items() if v is not None and v != ''}
        if clean:
            url += '?' + urllib.parse.urlencode(clean)
    return url


def request_json(method: str, url: str, *, token: Optional[str] = None, payload: Optional[Dict[str, Any]] = None, timeout: int = DEFAULT_TIMEOUT, accept_non_json: bool = False) -> Any:
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        headers['Content-Type'] = 'application/json'
    if token:
        headers['Authorization'] = token if token.lower().startswith('bearer ') else f'Bearer {token}'
    req = urllib.request.Request(url=url, data=data, method=method.upper(), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode('utf-8', errors='replace')
            if accept_non_json:
                return raw
            return json.loads(raw)
    except urllib.error.HTTPError as err:
        detail = err.read().decode('utf-8', errors='replace') if err.fp else ''
        eprint(f'HTTP {err.code} for {method.upper()} {url}')
        if detail:
            eprint(detail)
        raise SystemExit(2)
    except urllib.error.URLError as err:
        eprint(f'Network error: {err}')
        raise SystemExit(3)
    except json.JSONDecodeError:
        eprint('Response is not valid JSON')
        raise SystemExit(4)


def print_json(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def extract_data(data: Any) -> Any:
    return data.get('data') if isinstance(data, dict) and 'data' in data else data


def effective_config(args: argparse.Namespace) -> Dict[str, Any]:
    return {
        'baseUrl': config_value(getattr(args, 'base_url', None), 'FNS_BASE_URL', 'baseUrl'),
        'credentials': config_value(getattr(args, 'credentials', None), 'FNS_CREDENTIALS', 'credentials'),
        'password': config_value(getattr(args, 'password', None), 'FNS_PASSWORD', 'password'),
        'vault': config_value(getattr(args, 'vault', None), 'FNS_VAULT', 'vault'),
        'token': config_value(getattr(args, 'token', None), 'FNS_TOKEN', 'token'),
        'timeoutSeconds': config_int(getattr(args, 'timeout_seconds', None), 'FNS_TIMEOUT_SECONDS', 'timeoutSeconds', DEFAULT_TIMEOUT),
    }


def require(config: Dict[str, Any], *keys: str) -> None:
    missing = [k for k in keys if not config.get(k)]
    if missing:
        eprint('Missing required config:', ', '.join(missing))
        raise SystemExit(1)


def authed(args: argparse.Namespace, need_vault: bool = False) -> Dict[str, Any]:
    cfg = effective_config(args)
    require(cfg, 'baseUrl', 'token')
    if need_vault:
        require(cfg, 'vault')
    return cfg


def cmd_doctor(args: argparse.Namespace) -> None:
    cfg = effective_config(args)
    status = {
        'baseUrl': bool(cfg.get('baseUrl')),
        'credentials': bool(cfg.get('credentials')),
        'password': bool(cfg.get('password')),
        'vault': bool(cfg.get('vault')),
        'token': bool(cfg.get('token')),
        'timeoutSeconds': cfg.get('timeoutSeconds'),
        'openclawConfig': str(OPENCALW_CONFIG),
        'localConfig': str(LOCAL_CONFIG),
    }
    print_json(status)


def cmd_login(args: argparse.Namespace) -> None:
    cfg = effective_config(args)
    require(cfg, 'baseUrl', 'credentials', 'password')
    data = request_json(
        'POST',
        build_url(cfg['baseUrl'], '/user/login'),
        payload={'credentials': cfg['credentials'], 'password': cfg['password']},
        timeout=cfg['timeoutSeconds'],
    )
    token = None
    user_data = extract_data(data)
    if isinstance(user_data, dict):
        token = user_data.get('token')
    if not token and isinstance(data, dict):
        token = data.get('token')
    if not token:
        eprint('Login succeeded but token was not found in response')
        print_json(data)
        raise SystemExit(5)
    save_local_config({'token': token, 'baseUrl': cfg['baseUrl'], 'credentials': cfg['credentials'], 'vault': cfg.get('vault')})
    print(token if args.raw else json.dumps({'ok': True, 'token': token}, ensure_ascii=False, indent=2))


def cmd_user_info(args: argparse.Namespace) -> None:
    cfg = authed(args)
    data = request_json('GET', build_url(cfg['baseUrl'], '/user/info'), token=cfg['token'], timeout=cfg['timeoutSeconds'])
    print_json(data)


def cmd_vaults(args: argparse.Namespace) -> None:
    cfg = authed(args)
    data = request_json('GET', build_url(cfg['baseUrl'], '/vault'), token=cfg['token'], timeout=cfg['timeoutSeconds'])
    print_json(data)


def cmd_search(args: argparse.Namespace) -> None:
    cfg = authed(args, need_vault=True)
    query = {
        'vault': cfg['vault'],
        'keyword': args.keyword,
        'searchContent': 'true' if args.search_content else None,
        'searchMode': args.search_mode,
        'sortBy': args.sort_by,
        'sortOrder': args.sort_order,
        'page': args.page,
        'pageSize': args.page_size,
        'isRecycle': 'true' if args.is_recycle else None,
    }
    data = request_json('GET', build_url(cfg['baseUrl'], '/notes', query), token=cfg['token'], timeout=cfg['timeoutSeconds'])
    print_json(data)


def cmd_get(args: argparse.Namespace) -> None:
    cfg = authed(args, need_vault=True)
    data = request_json('GET', build_url(cfg['baseUrl'], '/note', {'vault': cfg['vault'], 'path': args.path}), token=cfg['token'], timeout=cfg['timeoutSeconds'])
    if args.content_only:
        note = extract_data(data)
        if isinstance(note, dict):
            print(note.get('content', ''))
            return
    print_json(data)


def write_note(args: argparse.Namespace, endpoint: str) -> None:
    cfg = authed(args, need_vault=True)
    payload = {'vault': cfg['vault'], 'path': args.path, 'content': args.content}
    if endpoint == '/note':
        payload['createOnly'] = args.create_only
    data = request_json('POST', build_url(cfg['baseUrl'], endpoint), token=cfg['token'], payload=payload, timeout=cfg['timeoutSeconds'])
    print_json(data)


def cmd_put(args: argparse.Namespace) -> None:
    write_note(args, '/note')


def cmd_append(args: argparse.Namespace) -> None:
    write_note(args, '/note/append')


def cmd_prepend(args: argparse.Namespace) -> None:
    write_note(args, '/note/prepend')


def cmd_replace(args: argparse.Namespace) -> None:
    cfg = authed(args, need_vault=True)
    payload = {
        'vault': cfg['vault'],
        'path': args.path,
        'find': args.find,
        'replace': args.replace_text,
        'regex': args.regex,
        'all': args.all,
        'failIfNoMatch': args.fail_if_no_match,
    }
    data = request_json('POST', build_url(cfg['baseUrl'], '/note/replace'), token=cfg['token'], payload=payload, timeout=cfg['timeoutSeconds'])
    print_json(data)


def cmd_rename(args: argparse.Namespace) -> None:
    cfg = authed(args, need_vault=True)
    payload = {'vault': cfg['vault'], 'oldPath': args.old_path, 'path': args.path}
    data = request_json('POST', build_url(cfg['baseUrl'], '/note/rename'), token=cfg['token'], payload=payload, timeout=cfg['timeoutSeconds'])
    print_json(data)


def cmd_move(args: argparse.Namespace) -> None:
    cfg = authed(args, need_vault=True)
    payload = {'vault': cfg['vault'], 'path': args.path, 'destination': args.destination, 'overwrite': args.overwrite}
    data = request_json('POST', build_url(cfg['baseUrl'], '/note/move'), token=cfg['token'], payload=payload, timeout=cfg['timeoutSeconds'])
    print_json(data)


def cmd_tree(args: argparse.Namespace) -> None:
    cfg = authed(args, need_vault=True)
    data = request_json('GET', build_url(cfg['baseUrl'], '/folder/tree', {'vault': cfg['vault']}), token=cfg['token'], timeout=cfg['timeoutSeconds'])
    print_json(data)


def cmd_histories(args: argparse.Namespace) -> None:
    cfg = authed(args, need_vault=True)
    data = request_json('GET', build_url(cfg['baseUrl'], '/note/histories', {'vault': cfg['vault'], 'path': args.path}), token=cfg['token'], timeout=cfg['timeoutSeconds'])
    print_json(data)


def cmd_restore_history(args: argparse.Namespace) -> None:
    cfg = authed(args, need_vault=True)
    payload = {'vault': cfg['vault'], 'path': args.path, 'historyId': args.history_id}
    data = request_json('PUT', build_url(cfg['baseUrl'], '/note/history/restore'), token=cfg['token'], payload=payload, timeout=cfg['timeoutSeconds'])
    print_json(data)


def cmd_set_config(args: argparse.Namespace) -> None:
    updates = {
        'baseUrl': args.base_url,
        'credentials': args.credentials,
        'password': args.password,
        'vault': args.vault,
        'token': args.token,
        'timeoutSeconds': args.timeout_seconds,
    }
    save_local_config(updates)
    print_json({'ok': True, 'savedTo': str(LOCAL_CONFIG), 'updatedKeys': [k for k, v in updates.items() if v is not None]})


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description='ObsidianFNS helper CLI')
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument('--base-url')
    common.add_argument('--credentials')
    common.add_argument('--password')
    common.add_argument('--vault')
    common.add_argument('--token')
    common.add_argument('--timeout-seconds', type=int)

    sub = p.add_subparsers(dest='command', required=True)

    doctor = sub.add_parser('doctor', parents=[common])
    doctor.set_defaults(func=cmd_doctor)

    login = sub.add_parser('login', parents=[common])
    login.add_argument('--raw', action='store_true')
    login.set_defaults(func=cmd_login)

    user_info = sub.add_parser('user-info', parents=[common])
    user_info.set_defaults(func=cmd_user_info)

    vaults = sub.add_parser('vaults', parents=[common])
    vaults.set_defaults(func=cmd_vaults)

    search = sub.add_parser('search', parents=[common])
    search.add_argument('--keyword', default='')
    search.add_argument('--search-content', action='store_true')
    search.add_argument('--search-mode', choices=['path', 'content', 'regex'])
    search.add_argument('--sort-by')
    search.add_argument('--sort-order', choices=['asc', 'desc'])
    search.add_argument('--page', type=int, default=1)
    search.add_argument('--page-size', type=int, default=20)
    search.add_argument('--is-recycle', action='store_true')
    search.set_defaults(func=cmd_search)

    getp = sub.add_parser('get', parents=[common])
    getp.add_argument('--path', required=True)
    getp.add_argument('--content-only', action='store_true')
    getp.set_defaults(func=cmd_get)

    put = sub.add_parser('put', parents=[common])
    put.add_argument('--path', required=True)
    put.add_argument('--content', required=True)
    put.add_argument('--create-only', action='store_true')
    put.set_defaults(func=cmd_put)

    append = sub.add_parser('append', parents=[common])
    append.add_argument('--path', required=True)
    append.add_argument('--content', required=True)
    append.set_defaults(func=cmd_append)

    prepend = sub.add_parser('prepend', parents=[common])
    prepend.add_argument('--path', required=True)
    prepend.add_argument('--content', required=True)
    prepend.set_defaults(func=cmd_prepend)

    replace = sub.add_parser('replace', parents=[common])
    replace.add_argument('--path', required=True)
    replace.add_argument('--find', required=True)
    replace.add_argument('--replace-text', required=True)
    replace.add_argument('--regex', action='store_true')
    replace.add_argument('--all', action='store_true')
    replace.add_argument('--fail-if-no-match', action='store_true')
    replace.set_defaults(func=cmd_replace)

    rename = sub.add_parser('rename', parents=[common])
    rename.add_argument('--old-path', required=True)
    rename.add_argument('--path', required=True)
    rename.set_defaults(func=cmd_rename)

    move = sub.add_parser('move', parents=[common])
    move.add_argument('--path', required=True)
    move.add_argument('--destination', required=True)
    move.add_argument('--overwrite', action='store_true')
    move.set_defaults(func=cmd_move)

    tree = sub.add_parser('tree', parents=[common])
    tree.set_defaults(func=cmd_tree)

    histories = sub.add_parser('histories', parents=[common])
    histories.add_argument('--path', required=True)
    histories.set_defaults(func=cmd_histories)

    restore = sub.add_parser('restore-history', parents=[common])
    restore.add_argument('--path', required=True)
    restore.add_argument('--history-id', required=True)
    restore.set_defaults(func=cmd_restore_history)

    setcfg = sub.add_parser('set-config')
    setcfg.add_argument('--base-url')
    setcfg.add_argument('--credentials')
    setcfg.add_argument('--password')
    setcfg.add_argument('--vault')
    setcfg.add_argument('--token')
    setcfg.add_argument('--timeout-seconds', type=int)
    setcfg.set_defaults(func=cmd_set_config)

    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
