#!/usr/bin/env python3
"""
infoseek_host.py — 远程托管一级形态 CLI（v1.0.0）
=================================================================

把 infoseek MCP server 托管为远程 SSE 服务（一级部署形态）：
- start：后台拉起 SSE server（--require-token 强制鉴权），自动生成 token，
  轮询 /health 直到就绪，输出每生态连接信息（Claude/Coze/Dify 等 remote 形态）。
- status：读取托管状态 + 存活检查 + 健康检查。
- stop：停止托管进程。
- token：打印当前 token（配置客户端用）。

状态文件：~/.infoseek/host_state.json（状态中立目录）。
日志文件：~/.infoseek/host.log

用法：
  python scripts/infoseek_host.py start [--port 8765] [--host 0.0.0.0] [--token <secret>]
  python scripts/infoseek_host.py status
  python scripts/infoseek_host.py stop
  python scripts/infoseek_host.py token
"""

from __future__ import annotations

import argparse
import json
import os
import secrets
import signal
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

SKILL_ROOT = Path(__file__).parent.parent
SERVER = SKILL_ROOT / 'scripts' / 'infoseek_mcp_server.py'
STATE_FILE = Path.home() / '.infoseek' / 'host_state.json'
LOG_FILE = Path.home() / '.infoseek' / 'host.log'
HEALTH_PATH = '/health'


def _state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding='utf-8'))
        except Exception:
            return {}
    return {}


def _save_state(s: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding='utf-8')


def _pid_alive(pid: int) -> bool:
    if not pid:
        return False
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def _health_ok(host: str, port: int) -> bool:
    try:
        with urllib.request.urlopen(f'http://{host}:{port}{HEALTH_PATH}', timeout=3) as r:
            return r.status == 200
    except Exception:
        return False


def _terminate(pid: int) -> None:
    if not _pid_alive(pid):
        return
    try:
        if os.name == 'nt':
            subprocess.run(['taskkill', '/PID', str(pid), '/F'],
                           capture_output=True, timeout=10)
        else:
            os.kill(pid, signal.SIGTERM)
    except Exception as e:
        print(f"[warn] 终止进程 {pid} 失败: {e}")


def cmd_start(args) -> int:
    st = _state()
    if _pid_alive(st.get('pid')):
        print(f"[start] 已存在托管实例 (pid={st['pid']}, port={st.get('port')})，无需重复启动")
        return 0

    token = args.token or os.environ.get('INFOSEEK_AUTH_TOKEN') or secrets.token_urlsafe(32)
    port = args.port
    host = args.host
    log_f = open(LOG_FILE, 'a', encoding='utf-8', buffering=1)

    cmd = [sys.executable, str(SERVER), '--transport', 'sse',
           '--port', str(port), '--require-token', '--token', token]
    # 脱离父进程组，保证父 CLI 退出后托管进程存活（真实部署关键）
    popen_kwargs = dict(
        stdout=log_f, stderr=log_f, cwd=str(SKILL_ROOT),
        stdin=subprocess.DEVNULL,
    )
    if os.name == 'nt':
        popen_kwargs['creationflags'] = (
            subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS)
    else:
        popen_kwargs['start_new_session'] = True
    proc = subprocess.Popen(cmd, **popen_kwargs)

    # 轮询健康检查（最多 30s）
    ok = False
    for _ in range(30):
        time.sleep(1)
        if _health_ok(host, port):
            ok = True
            break
        if proc.poll() is not None:
            break

    if not ok:
        print(f"[start] 托管启动失败（health 未就绪，进程退出码 {proc.poll()}）。")
        print(f"        日志: {LOG_FILE}")
        print(f"        请检查端口占用或运行: python {SERVER} --transport sse --port {port} 前台验证")
        return 1

    _save_state({
        'pid': proc.pid, 'host': host, 'port': port, 'token': token,
        'transport': 'sse', 'started_at': time.strftime('%Y-%m-%d %H:%M:%S'),
        'log': str(LOG_FILE),
    })
    print(f"[start] 托管已就绪  http://{host}:{port}/sse  (pid={proc.pid})")
    print(f"[start] 日志: {LOG_FILE}")
    print()
    print_connections(host, port, token)
    return 0


def print_connections(host: str, port: int, token: str) -> None:
    url = f'http://{host}:{port}/sse'
    print("=" * 62)
    print("各生态 remote 连接信息")
    print("=" * 62)
    print(f"  MCP 端点 : {url}")
    print(f"  认证头   : Authorization: Bearer {token}")
    print()
    print("  Claude/通用 MCP 客户端配置（加入 mcpServers）:")
    print(json.dumps({
        "mcpServers": {
            "infoseek-remote": {
                "url": url,
                "headers": {"Authorization": f"Bearer {token}"},
            }
        }
    }, ensure_ascii=False, indent=2))
    print()
    print(f"  设置环境变量（无 Python 平台直连）:")
    print(f"    INFOSEEK_AUTH_TOKEN={token}")
    print("    INFOSEEK_HOST / INFOSEEK_PORT 可用于 ecosystem.Config.from_env()")


def cmd_status(args) -> int:
    st = _state()
    if not st:
        print("[status] 无托管状态（~/.infoseek/host_state.json 不存在）")
        return 1
    # 存活判定：健康检查为准（Windows 分离进程 os.kill(pid,0) 可能误判）；
    # pid 检查仅作辅助
    health = _health_ok(st.get('host', '127.0.0.1'), st.get('port', 0))
    pid_alive = _pid_alive(st.get('pid'))
    alive = health or pid_alive
    print(f"  pid       : {st.get('pid')}  ({'存活' if alive else '已退出'})")
    print(f"  endpoint  : http://{st.get('host')}:{st.get('port')}/sse")
    print(f"  health    : {'OK' if health else '不可达'}")
    print(f"  started_at: {st.get('started_at')}")
    print(f"  log       : {st.get('log')}")
    if health:
        print(f"  token     : {st.get('token')}")
    return 0 if health else 1


def cmd_stop(args) -> int:
    st = _state()
    if not st:
        print("[stop] 无托管状态，无需停止")
        return 0
    _terminate(st.get('pid'))
    # 清空状态：unlink 可能被沙箱回收站拦截 → 降级为空状态
    try:
        STATE_FILE.unlink(missing_ok=True)
    except OSError:
        _save_state({})
    print(f"[stop] 已停止托管实例 (pid={st.get('pid')})")
    return 0


def cmd_token(args) -> int:
    st = _state()
    if st.get('token'):
        print(st['token'])
        return 0
    print("[token] 无托管实例（先 start 或设置 INFOSEEK_AUTH_TOKEN）", file=sys.stderr)
    return 1


def main():
    ap = argparse.ArgumentParser(description='infoseek 远程托管 CLI（P2 一级部署形态）')
    sub = ap.add_subparsers(dest='cmd', required=True)

    p_start = sub.add_parser('start', help='启动托管 SSE 服务')
    p_start.add_argument('--port', type=int, default=8765)
    p_start.add_argument('--host', default='0.0.0.0')
    p_start.add_argument('--token', default=None, help='固定 token（缺省自动生成）')
    p_start.set_defaults(func=cmd_start)

    p_status = sub.add_parser('status', help='托管状态 + 健康检查')
    p_status.set_defaults(func=cmd_status)

    p_stop = sub.add_parser('stop', help='停止托管')
    p_stop.set_defaults(func=cmd_stop)

    p_token = sub.add_parser('token', help='打印当前 token')
    p_token.set_defaults(func=cmd_token)

    args = ap.parse_args()
    sys.exit(args.func(args))


if __name__ == '__main__':
    main()
