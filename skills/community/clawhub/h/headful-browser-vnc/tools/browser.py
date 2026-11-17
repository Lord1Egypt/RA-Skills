#!/usr/bin/env python3
"""Linux session lifecycle and CLI. No privileged installs or shell evaluation."""
import argparse
import contextlib
import fcntl
import json
import os
from pathlib import Path
import re
import secrets
import shutil
import signal
import socket
import stat
import subprocess
import sys
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
CONFIG_KEYS = {
    'VNC_PASSFILE', 'VNC_DISPLAY', 'VNC_RESOLUTION', 'VNC_PORT',
    'REMOTE_DEBUG_PORT', 'PROXY_URL', 'OUT_DIR', 'BROWSER_STATE_DIR',
    'CHROME_BIN', 'NOVNC_PORT', 'NOVNC_WEB',
}


class BrowserError(Exception):
    pass


def private_dir(path):
    path = Path(path).absolute()
    path.mkdir(mode=0o700, parents=True, exist_ok=True)
    info = path.lstat()
    if not stat.S_ISDIR(info.st_mode) or info.st_uid != os.getuid():
        raise BrowserError(f'Not an owned directory: {path}')
    path.chmod(0o700)
    return path


def private_file(path):
    info = Path(path).lstat()
    if not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid() or info.st_mode & 0o077:
        raise BrowserError(f'Expected an owned regular file with mode 0600/0400: {path}')


def load_config(path):
    """Literal KEY=value only; quotes remove delimiters, never expand shell syntax."""
    values = {}
    if not path.exists():
        return values
    private_file(path)
    for number, raw in enumerate(path.read_text().splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        key, sep, value = line.partition('=')
        key, value = key.strip(), value.strip()
        if not sep or key not in CONFIG_KEYS:
            raise BrowserError(f'{path}:{number}: unknown configuration key {key!r}')
        if value.startswith(('"', "'")):
            if len(value) < 2 or value[-1] != value[0]:
                raise BrowserError(f'{path}:{number}: unmatched quote')
            value = value[1:-1]
        if any(char in value for char in ('$', '`', '\x00')):
            raise BrowserError(f'{path}:{number}: use literal values, no shell expansion')
        values[key] = value
    return values


def config():
    result = load_config(ROOT / '.env')
    result.update({k: os.environ[k] for k in CONFIG_KEYS if k in os.environ})
    return {k: v for k, v in result.items() if v != ''}


def state_root(cfg):
    default = Path(os.environ.get('XDG_STATE_HOME', Path.home() / '.local/state')) / 'headful-browser-vnc'
    return private_dir(cfg.get('BROWSER_STATE_DIR', default))


@contextlib.contextmanager
def locked(path):
    fd = os.open(path, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    try:
        if os.fstat(fd).st_uid != os.getuid():
            raise BrowserError(f'Lock is not owned by current user: {path}')
        os.fchmod(fd, 0o600)
        fcntl.flock(fd, fcntl.LOCK_EX)
        yield
    finally:
        os.close(fd)


def save(path, value):
    temporary = path.with_name(path.name + '.' + secrets.token_hex(8))
    fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    try:
        with os.fdopen(fd, 'w') as stream:
            json.dump(value, stream, indent=2)
            stream.write('\n')
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def read_state(directory):
    path = directory / 'session.json'
    if not path.exists():
        return None
    private_file(path)
    try:
        state = json.loads(path.read_text())
        required = {'schema', 'sessionId', 'token', 'display', 'resolution', 'vncPort',
                    'novncPort', 'cdpPort', 'profileDir', 'state', 'processes'}
        if not isinstance(state, dict) or not required.issubset(state) or state['schema'] != 1:
            raise ValueError('unsupported or incomplete schema')
        if state['sessionId'] != directory.name or state['profileDir'] != str(directory / 'profile'):
            raise ValueError('session identity or profile path mismatch')
        if not isinstance(state['token'], str) or not re.fullmatch(r'[0-9a-f]{48}', state['token']):
            raise ValueError('invalid session token')
        if not isinstance(state['processes'], list):
            raise ValueError('invalid process inventory')
        for process in state['processes']:
            if (not isinstance(process, dict) or process.get('role') not in ('xvfb', 'wm', 'vnc', 'novnc', 'chrome')
                    or not isinstance(process.get('pid'), int) or process['pid'] <= 1
                    or process.get('pgid') != process['pid']
                    or not isinstance(process.get('start'), str) or not process['start'].isdigit()):
                raise ValueError('invalid process identity')
        return state
    except (ValueError, TypeError) as error:
        raise BrowserError(f'Invalid session state at {path}: {error}')


def proc_info(pid):
    try:
        # comm may contain spaces or parentheses.
        fields = Path(f'/proc/{pid}/stat').read_text().rsplit(')', 1)[1].split()
        return {'pid': int(pid), 'start': fields[19], 'pgid': int(fields[2]), 'status': fields[0]}
    except (OSError, ValueError, IndexError):
        return None


def alive(record):
    actual = proc_info(record['pid'])
    return bool(actual and actual['start'] == record['start'] and actual['status'] != 'Z')


def members(record, token):
    result = []
    for entry in Path('/proc').iterdir():
        if not entry.name.isdigit():
            continue
        info = proc_info(entry.name)
        if not info or info['pgid'] != record['pgid'] or info['status'] == 'Z':
            continue
        try:
            env = (entry / 'environ').read_bytes().split(b'\0')
            if f'HF_SESSION_TOKEN={token}'.encode() in env:
                result.append(info)
        except OSError:
            continue
    return result


def stop_processes(state, roles=None):
    records = [p for p in reversed(state['processes']) if roles is None or p['role'] in roles]
    for sig, duration in ((signal.SIGTERM, 4), (signal.SIGKILL, 2)):
        for record in records:
            if members(record, state['token']):
                with contextlib.suppress(ProcessLookupError):
                    os.killpg(record['pgid'], sig)
        deadline = time.monotonic() + duration
        while time.monotonic() < deadline:
            if not any(members(p, state['token']) for p in records):
                return
            time.sleep(0.1)
    raise BrowserError('Some session processes did not exit; state retained for retry')


def launch(state, directory, role, command, environment=None):
    log_path = directory / f'{role}.log'
    fd = os.open(log_path, os.O_WRONLY | os.O_CREAT | os.O_APPEND | os.O_NOFOLLOW, 0o600)
    os.fchmod(fd, 0o600)
    env = {**os.environ, 'HF_SESSION_TOKEN': state['token'], 'DISPLAY': state['display'],
           'XAUTHORITY': str(directory / 'Xauthority')}
    env.update(environment or {})
    try:
        process = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=fd, stderr=fd,
                                   env=env, start_new_session=True, close_fds=True)
    finally:
        os.close(fd)
    record = proc_info(process.pid)
    if not record or record['status'] == 'Z':
        process.wait(timeout=1)
        raise BrowserError(f'{role} exited during startup; inspect {log_path}')
    record['role'] = role
    state['processes'].append(record)
    save(directory / 'session.json', state)
    return record


def port_available(port):
    with socket.socket() as sock:
        try:
            sock.bind(('127.0.0.1', port))
            return True
        except OSError:
            return False


def port_number(value):
    try:
        port = int(value)
    except (ValueError, TypeError):
        raise BrowserError(f'Invalid port: {value}')
    if not 1024 <= port <= 65535:
        raise BrowserError('Ports must be between 1024 and 65535')
    return port


def choose_port(requested, start, reserved):
    if requested is not None:
        port = port_number(requested)
        if port in reserved or not port_available(port):
            raise BrowserError(f'Port {port} is already in use')
        return port
    for port in range(start, start + 200):
        if port not in reserved and port_available(port):
            return port
    raise BrowserError('No available port in allocation range')


def listener_owned(port, record, token):
    """Require a loopback-only listener belonging to the launched process group."""
    inodes = set()
    for process in members(record, token):
        try:
            for fd in Path(f"/proc/{process['pid']}/fd").iterdir():
                with contextlib.suppress(OSError):
                    link = os.readlink(fd)
                    if link.startswith('socket:['):
                        inodes.add(link[8:-1])
        except OSError:
            continue
    found = False
    for table in ('tcp', 'tcp6'):
        path = Path('/proc/net') / table
        if not path.exists():
            continue
        for line in path.read_text().splitlines()[1:]:
            columns = line.split()
            address, hex_port = columns[1].split(':')
            if int(hex_port, 16) != port or columns[3] != '0A':
                continue
            loopback = address in ('0100007F', '00000000000000000000000001000000')
            if not loopback or columns[9] not in inodes:
                return False
            found = True
    return found


def local_json(port, path):
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(f'http://127.0.0.1:{port}{path}', timeout=2) as response:
        return json.load(response)


def wait_ready(record, check, label, timeout=15):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if not alive(record):
            raise BrowserError(f'{label} exited; inspect session logs')
        try:
            if check():
                return
        except (OSError, ValueError, subprocess.SubprocessError):
            pass
        time.sleep(0.1)
    raise BrowserError(f'{label} readiness timed out; inspect session logs')


def require_tools(*names):
    missing = [name for name in names if not shutil.which(name)]
    if missing:
        raise BrowserError('Missing dependencies: ' + ', '.join(missing))


def chrome_binary(cfg):
    candidates = [cfg['CHROME_BIN']] if cfg.get('CHROME_BIN') else ['google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser']
    for name in candidates:
        if shutil.which(name):
            return shutil.which(name)
    raise BrowserError('Chrome/Chromium not found; set CHROME_BIN to an executable')


def display_free(display):
    number = display[1:]
    return not Path(f'/tmp/.X11-unix/X{number}').exists() and not Path(f'/tmp/.X{number}-lock').exists()


def start_vnc(args, cfg, directory):
    require_tools('Xvfb', 'xdpyinfo', 'x11vnc', 'xauth')
    passfile = Path(args.passfile or cfg.get('VNC_PASSFILE', ''))
    if not str(args.passfile or cfg.get('VNC_PASSFILE', '')):
        raise BrowserError('Set VNC_PASSFILE or pass --passfile first')
    private_file(passfile)
    if passfile.stat().st_size != 8:
        raise BrowserError('VNC passfile must contain an 8-byte binary rfbauth password')
    requested = args.display or cfg.get('VNC_DISPLAY')
    if requested and not re.fullmatch(r':[0-9]{1,4}', requested):
        raise BrowserError('Display must have the form :99')
    display = requested or next((f':{n}' for n in range(99, 299) if display_free(f':{n}')), None)
    if not display or not display_free(display):
        raise BrowserError(f'Display {display} is unavailable; existing displays are never adopted')
    resolution = args.resolution or cfg.get('VNC_RESOLUTION', '1366x768')
    match = re.fullmatch(r'([0-9]{3,4})x([0-9]{3,4})', resolution)
    if not match or not all(320 <= int(v) <= 7680 for v in match.groups()):
        raise BrowserError('Resolution must be WIDTHxHEIGHT, dimensions 320..7680')
    port = choose_port(args.port or cfg.get('VNC_PORT'), 5901, set())
    novnc_requested = args.novnc_port or cfg.get('NOVNC_PORT')
    novnc = None
    web = None
    if novnc_requested:
        require_tools('websockify')
        web = Path(args.novnc_web or cfg.get('NOVNC_WEB', '/usr/share/novnc')).resolve()
        if not (web / 'vnc.html').is_file():
            raise BrowserError(f'noVNC vnc.html not found in {web}')
        novnc = choose_port(novnc_requested, 6080, {port})
    state = {'schema': 1, 'sessionId': args.session, 'token': secrets.token_hex(24),
             'display': display, 'resolution': resolution, 'vncPort': port,
             'novncPort': novnc, 'cdpPort': None, 'profileDir': str(directory / 'profile'),
             'state': 'starting', 'processes': [], 'createdAt': time.time()}
    save(directory / 'session.json', state)
    try:
        auth = directory / 'Xauthority'
        auth.unlink(missing_ok=True)
        auth.touch(mode=0o600, exist_ok=False)
        subprocess.run(['xauth', '-f', str(auth), 'add', display, '.', secrets.token_hex(16)],
                       check=True, capture_output=True, timeout=5)
        record = launch(state, directory, 'xvfb', ['Xvfb', display, '-screen', '0', resolution + 'x24',
                        '-nolisten', 'tcp', '-auth', str(auth)])
        def x_ready():
            return subprocess.run(['xdpyinfo', '-display', display], stdout=subprocess.DEVNULL,
                                  stderr=subprocess.DEVNULL, timeout=2,
                                  env={**os.environ, 'XAUTHORITY': str(auth)}).returncode == 0
        wait_ready(record, x_ready, 'Xvfb')
        if shutil.which('fluxbox'):
            launch(state, directory, 'wm', ['fluxbox'])
        record = launch(state, directory, 'vnc', ['x11vnc', '-display', display, '-localhost',
                        '-rfbport', str(port), '-rfbauth', str(passfile.resolve()), '-forever', '-shared'])
        wait_ready(record, lambda: listener_owned(port, record, state['token']), 'x11vnc')
        if novnc:
            record = launch(state, directory, 'novnc', ['websockify', '--web', str(web),
                            f'127.0.0.1:{novnc}', f'127.0.0.1:{port}'])
            wait_ready(record, lambda: listener_owned(novnc, record, state['token']), 'noVNC')
        state['state'] = 'vnc-ready'
        save(directory / 'session.json', state)
        return state
    except BaseException:
        stop_processes(state)
        state['state'] = 'failed'
        save(directory / 'session.json', state)
        raise


def start_chrome(args, cfg, directory, state):
    if os.getuid() == 0:
        raise BrowserError('Run Chrome as a non-root user; sandbox remains enabled')
    binary = chrome_binary(cfg)
    if state['state'] != 'vnc-ready':
        raise BrowserError('Session must be vnc-ready before Chrome is started')
    if any(not alive(p) for p in state['processes'] if p['role'] in ('vnc', 'xvfb')):
        raise BrowserError('VNC/display process is no longer running; stop the session first')
    reserved = {state['vncPort'], state.get('novncPort')}
    port = choose_port(args.remote_debug_port or cfg.get('REMOTE_DEBUG_PORT'), 9222, reserved)
    profile = private_dir(state['profileDir'])
    command = [binary, f'--user-data-dir={profile}', '--remote-debugging-address=127.0.0.1',
               f'--remote-debugging-port={port}', '--no-first-run', '--no-default-browser-check',
               '--disable-dev-shm-usage', f"--window-size={state['resolution'].replace('x', ',')}"]
    proxy = args.proxy or cfg.get('PROXY_URL')
    if proxy:
        if not re.match(r'^(https?|socks5)://[^\s]+$', proxy):
            raise BrowserError('Proxy must be an http(s) or socks5 URL without spaces')
        command.append('--proxy-server=' + proxy)
    command.append('about:blank')
    try:
        record = launch(state, directory, 'chrome', command)
        def ready():
            return listener_owned(port, record, state['token']) and bool(local_json(port, '/json/version').get('webSocketDebuggerUrl'))
        wait_ready(record, ready, 'Chrome', timeout=25)
        state['cdpPort'], state['state'] = port, 'running'
        save(directory / 'session.json', state)
        return state
    except BaseException:
        stop_processes(state, {'chrome'})
        state['processes'] = [p for p in state['processes'] if p['role'] != 'chrome']
        save(directory / 'session.json', state)
        raise


def public_state(state, directory):
    result = {k: v for k, v in state.items() if k not in ('token', 'processes')}
    result['sessionDir'] = str(directory)
    result['processes'] = [{'role': p['role'], 'pid': p['pid'], 'alive': alive(p)} for p in state['processes']]
    if state['state'] not in ('stopped', 'failed') and any(not p['alive'] for p in result['processes'] if p['role'] != 'wm'):
        result['state'] = 'degraded'
    result['vncAddress'] = f"127.0.0.1:{state['vncPort']}"
    if state.get('novncPort'):
        result['operatorUrl'] = f"http://127.0.0.1:{state['novncPort']}/vnc.html"
    if state.get('cdpPort'):
        result['cdpEndpoint'] = f"http://127.0.0.1:{state['cdpPort']}"
    return result


def require_browser(state):
    if not state or state['state'] not in ('running', 'paused'):
        raise BrowserError('Session has no running browser')
    chrome = next(p for p in state['processes'] if p['role'] == 'chrome')
    if not alive(chrome) or not listener_owned(state['cdpPort'], chrome, state['token']):
        raise BrowserError('Browser or its loopback CDP listener is no longer healthy')


def export(args, cfg, directory, state):
    require_browser(state)
    if args.command == 'navigate-and-capture' and state['state'] == 'paused':
        raise BrowserError('Session is paused for operator control; resume before navigation')
    require_tools('node')
    base = private_dir(cfg.get('OUT_DIR', ROOT / 'out'))
    session_out = private_dir(base / args.session)
    output = session_out / (time.strftime('%Y%m%dT%H%M%SZ', time.gmtime()) + '-' + secrets.token_hex(6))
    output.mkdir(mode=0o700)
    command = ['node', str(ROOT / 'tools/playwright_export.js'), args.command,
               '--port', str(state['cdpPort']), '--out', str(output), '--session', args.session]
    if args.command in ('capture', 'navigate-and-capture', 'storage-state'):
        command += ['--target', args.target]
    if args.command == 'navigate-and-capture':
        command += ['--url', args.url]
    if args.command == 'cookies':
        command += ['--url', args.url]
    completed = subprocess.run(command, capture_output=True, text=True, timeout=100)
    try:
        result = json.loads(completed.stdout)
    except ValueError:
        raise BrowserError('Exporter failed: ' + completed.stderr.strip()[-500:])
    return result, completed.returncode


def parser():
    cli = argparse.ArgumentParser(description=__doc__)
    commands = cli.add_subparsers(dest='command', required=True)
    for name in ('start', 'start-vnc', 'start-chrome', 'status', 'pages', 'capture',
                 'navigate-and-capture', 'cookies', 'storage-state', 'pause', 'resume', 'stop'):
        sub = commands.add_parser(name)
        sub.add_argument('session', help='Session identifier: letters, digits, underscore, hyphen')
        if name in ('start', 'start-vnc'):
            sub.add_argument('--display')
            sub.add_argument('--resolution')
            sub.add_argument('--port', type=int, help='VNC port')
            sub.add_argument('--passfile')
            sub.add_argument('--novnc-port', type=int)
            sub.add_argument('--novnc-web')
        if name in ('start', 'start-chrome'):
            sub.add_argument('--proxy')
            sub.add_argument('--remote-debug-port', type=int)
        if name in ('capture', 'navigate-and-capture', 'storage-state'):
            sub.add_argument('--target', required=True, help='Exact CDP targetId from pages')
        if name in ('navigate-and-capture', 'cookies'):
            sub.add_argument('--url', required=True, help='http(s) URL; cookies are scoped to this URL')
    commands.add_parser('doctor')
    return cli


def doctor(cfg):
    checks = {name: bool(shutil.which(name)) for name in ('python3', 'node', 'Xvfb', 'xdpyinfo', 'x11vnc', 'xauth')}
    checks['linux'] = sys.platform == 'linux'
    checks['nonRoot'] = os.getuid() != 0
    try:
        chrome_binary(cfg)
        checks['chrome'] = True
    except BrowserError:
        checks['chrome'] = False
    try:
        pf = Path(cfg.get('VNC_PASSFILE', ''))
        private_file(pf)
        checks['passfile'] = pf.stat().st_size == 8
    except (OSError, BrowserError):
        checks['passfile'] = False
    if shutil.which('node'):
        check = subprocess.run(['node', '-e', "require('playwright'); if(Number(process.versions.node.split('.')[0]) < 22) process.exit(1)"],
                               cwd=ROOT, capture_output=True, timeout=10)
        checks['node22AndPlaywright'] = check.returncode == 0
    else:
        checks['node22AndPlaywright'] = False
    return {'success': all(checks.values()), 'checks': checks}


def main(argv=None):
    os.umask(0o077)
    args = parser().parse_args(argv)
    cfg = config()
    if args.command == 'doctor':
        result = doctor(cfg)
        print(json.dumps(result))
        return 0 if result['success'] else 1
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,63}', args.session):
        raise BrowserError('Invalid session identifier')
    if sys.platform != 'linux':
        raise BrowserError('Session lifecycle requires Linux; use the documented Linux host setup')
    root = state_root(cfg)
    directory = private_dir(root / args.session)
    with locked(directory / 'session.lock'):
        state = read_state(directory)
        if args.command in ('start', 'start-vnc', 'start-chrome', 'stop'):
            with locked(root / 'allocation.lock'):
                if args.command == 'stop':
                    if state:
                        stop_processes(state)
                        state['state'] = 'stopped'
                        save(directory / 'session.json', state)
                    print(json.dumps({'success': True, 'sessionId': args.session, 'state': 'stopped'}))
                    return 0
                if state and state['state'] not in ('stopped', 'failed'):
                    if args.command != 'start-chrome':
                        # Explicitly fail instead of silently ignoring changed flags.
                        raise BrowserError('Session already exists; use status or stop before changing startup options')
                if args.command == 'start-chrome':
                    if not state:
                        raise BrowserError('Start VNC first')
                    state = start_chrome(args, cfg, directory, state)
                else:
                    if state and any(members(p, state['token']) for p in state['processes']):
                        raise BrowserError('Session still owns processes; stop it before restarting')
                    if args.command == 'start':
                        # Validate browser before allocating display processes.
                        chrome_binary(cfg)
                        if os.getuid() == 0:
                            raise BrowserError('Run as a non-root user with Chrome sandbox enabled')
                    state = start_vnc(args, cfg, directory)
                    if args.command == 'start':
                        try:
                            state = start_chrome(args, cfg, directory, state)
                        except BaseException:
                            stop_processes(state)
                            state['state'] = 'failed'
                            save(directory / 'session.json', state)
                            raise
            print(json.dumps({'success': True, **public_state(state, directory)}))
            return 0
        if not state:
            raise BrowserError('Session not found')
        if args.command == 'status':
            print(json.dumps({'success': True, **public_state(state, directory)}))
        elif args.command in ('pause', 'resume'):
            require_browser(state)
            state['state'] = 'paused' if args.command == 'pause' else 'running'
            save(directory / 'session.json', state)
            print(json.dumps({'success': True, **public_state(state, directory)}))
        elif args.command == 'pages':
            require_browser(state)
            pages = local_json(state['cdpPort'], '/json/list')
            print(json.dumps({'success': True, 'pages': [{'targetId': p['id'], 'url': p['url'],
                             'title': p.get('title', '')} for p in pages if p['type'] == 'page']}))
        else:
            result, code = export(args, cfg, directory, state)
            print(json.dumps(result))
            return code
    return 0


if __name__ == '__main__':
    def interrupted(signum, frame):
        raise KeyboardInterrupt
    signal.signal(signal.SIGTERM, interrupted)
    try:
        sys.exit(main())
    except (BrowserError, OSError, ValueError, subprocess.SubprocessError) as error:
        print(json.dumps({'success': False, 'error': str(error)}))
        sys.exit(1)
    except KeyboardInterrupt:
        print(json.dumps({'success': False, 'error': 'Interrupted'}))
        sys.exit(130)
