#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
SERVICE_DIR = CURRENT_DIR.parent / 'service'
if str(SERVICE_DIR) not in sys.path:
    sys.path.insert(0, str(SERVICE_DIR))

from config import build_ssh_tunnel_command, build_web_url, save_install_info  # noqa: E402
from generate_web_credentials import build_credentials  # noqa: E402
from paths import ensure_skill_dirs, get_runtime_dir  # noqa: E402
from pick_port import pick_port  # noqa: E402
from web_process_lib import detect_systemd_user, read_unit_env, systemd_unit_exists, systemd_unit_status, systemd_user_available, wait_for_port, write_unit_file  # noqa: E402


DEFAULT_SYSTEMD_TEMPLATE = """[Unit]\nDescription=OpenAI Auth Switcher Public Web Preview\nAfter=default.target\n\n[Service]\nType=simple\nWorkingDirectory=__WORKSPACE__\nEnvironment=PYTHONUNBUFFERED=1\nEnvironment=OPENAI_AUTH_SWITCHER_HOST=127.0.0.1\nEnvironment=OPENAI_AUTH_SWITCHER_PORT=8765\nExecStart=/usr/bin/env python3 __WORKSPACE__/skills/openai-auth-switcher-public/service/app.py\nRestart=on-failure\nRestartSec=2\n\n[Install]\nWantedBy=default.target\n"""


SYSTEMD_PREVIEW_UNIT = 'openai-auth-switcher-web-preview.service'


def wait_for_systemd_ready(unit_name: str, host: str, port: int, timeout_seconds: float = 20.0, interval_seconds: float = 0.5) -> tuple[bool, dict]:
    deadline = __import__('time').time() + timeout_seconds
    last_status: dict = {}
    while __import__('time').time() < deadline:
        last_status = systemd_unit_status(unit_name)
        ready = wait_for_port(host, port, timeout_seconds=interval_seconds, interval_seconds=min(0.2, interval_seconds))
        if last_status.get('is_active') and ready:
            return True, last_status
    return False, last_status


def start_background_service(host: str, port: int) -> dict:
    ensure_skill_dirs()
    runtime_dir = get_runtime_dir()
    log_path = runtime_dir / 'web-preview.log'
    pid_path = runtime_dir / 'web-preview.pid'
    app_path = CURRENT_DIR.parent / 'service' / 'app.py'
    env = os.environ.copy()
    env['OPENAI_AUTH_SWITCHER_HOST'] = host
    env['OPENAI_AUTH_SWITCHER_PORT'] = str(port)
    with log_path.open('a', encoding='utf-8') as log:
        proc = subprocess.Popen(['python3', str(app_path)], stdout=log, stderr=log, env=env)
    pid_path.write_text(str(proc.pid), encoding='utf-8')
    ready = wait_for_port(host, port)
    return {'ok': ready, 'pid': proc.pid, 'pid_path': str(pid_path), 'log_path': str(log_path), 'mode': 'background-process', 'ready': ready}


def ensure_systemd_template(template_path: Path) -> tuple[Path, bool]:
    if template_path.exists():
        return template_path, False
    template_path.parent.mkdir(parents=True, exist_ok=True)
    template_path.write_text(DEFAULT_SYSTEMD_TEMPLATE, encoding='utf-8')
    return template_path, True


def start_systemd_service(host: str, port: int) -> dict:
    workspace = CURRENT_DIR.parent.parent.parent
    template_path = CURRENT_DIR.parent / 'assets' / 'systemd' / 'openai-auth-switcher-web.service.template'
    template_path, generated_template = ensure_systemd_template(template_path)
    unit_name = SYSTEMD_PREVIEW_UNIT
    unit_path = Path.home() / '.config' / 'systemd' / 'user' / unit_name
    log_path = get_runtime_dir() / 'web-preview.log'
    had_existing_unit = systemd_unit_exists(unit_name)
    write_unit_file(template_path, unit_path, workspace=workspace, host=host, port=port)
    subprocess.run(['systemctl', '--user', 'daemon-reload'], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if had_existing_unit:
        subprocess.run(['systemctl', '--user', 'reset-failed', unit_name], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['systemctl', '--user', 'enable', unit_name], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['systemctl', '--user', 'restart', unit_name], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    status_ok, status = wait_for_systemd_ready(unit_name, host, port)
    env = read_unit_env(unit_name)
    ready = bool(status_ok or wait_for_port(host, port, timeout_seconds=2.0, interval_seconds=0.2))
    result = {
        'ok': status_ok,
        'mode': 'systemd-user',
        'unit': str(unit_path),
        'unit_name': unit_name,
        'ready': ready,
        'status': status,
        'runtime_env': env,
        'log_path': str(log_path),
    }
    if generated_template:
        result['warning'] = f'systemd template was missing and has been regenerated at {template_path}'
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description='Install and bootstrap the web preview for openai-auth-switcher-public')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--username', default='admin')
    parser.add_argument('--password-length', type=int, default=18)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    creds = build_credentials(username=args.username, length=args.password_length)
    port_info = pick_port(host=args.host)
    port = int(port_info['port'])
    install_info = {
        'ok': True,
        'host': args.host,
        'port': port,
        'username': creds['username'],
        'password': creds['password'],
        'local_url': build_web_url(args.host, port),
        'ssh_tunnel': build_ssh_tunnel_command(port),
        'port_source': port_info['source'],
    }
    save_install_info(install_info)
    systemd_probe = detect_systemd_user()
    install_info['systemd_probe'] = systemd_probe
    service = start_systemd_service(args.host, port) if systemd_probe.get('available') else start_background_service(args.host, port)
    attempted_systemd = service if service.get('mode') == 'systemd-user' else None
    if not service.get('ok') and service.get('mode') == 'systemd-user':
        fallback_reason = service.get('error') or 'systemd-user not active or port not ready within startup window'
        service = start_background_service(args.host, port)
        service['fallback_reason'] = fallback_reason
        service['attempted_systemd'] = attempted_systemd
    elif service.get('mode') == 'background-process' and not systemd_probe.get('available') and systemd_probe.get('reason'):
        service['fallback_reason'] = systemd_probe.get('reason')
    install_info['service'] = service
    install_info['ready'] = bool(service.get('ready') or service.get('ok'))
    save_install_info(install_info)

    if args.json:
        print(json.dumps(install_info, ensure_ascii=False, indent=2))
    else:
        print('Install complete.')
        print(f"Web URL (local): {install_info['local_url']}")
        print(f"Port: {port}")
        print(f"Username: {creds['username']}")
        print(f"Password: {creds['password']}")
        print('')
        print('SSH tunnel:')
        print(install_info['ssh_tunnel'])
        print('')
        print(f"Service mode: {service['mode']}")
        print(f"Service ready: {service.get('ready')}")
        if service.get('unit_name'):
            print(f"Systemd unit: {service['unit_name']}")
        print(f"Log file: {service.get('log_path', '<none>')}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
