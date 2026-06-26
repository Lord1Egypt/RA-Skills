#!/usr/bin/env python3
"""One-shot launcher for the Go Next Move HTTP interaction mode.

What the skill (the agent) does here is intentionally small:

1. Load or create a long-lived secret.
2. Mint a short-lived signed token (default 5 hours).
3. Start the local web server.
4. Start a public tunnel (Cloudflare quick tunnel by default) so the user can
   reach the page from anywhere.
5. Print the final link `https://<tunnel-host>/?token=<token>` to hand to the
   user.

After that the agent is done. When the token expires, run this again to mint a
new link. To force every old link dead, pass `--rotate-secret` (this rotates
the shared secret). If the tunnel host changes between runs, just send the new
link.

The original CLI workflow (`scripts/next_move.py`) is unaffected; this is an
additional entry point.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import socket
import subprocess
import sys
import threading
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from skill_token import (  # noqa: E402
    DEFAULT_SECRET_PATH,
    DEFAULT_STATE_DIR,
    DEFAULT_TTL_SECONDS,
    load_or_create_secret,
    mint_token,
    rotate_secret,
)
from web_server import build_next_move_args, run_server  # noqa: E402

TRYCLOUDFLARE_RE = re.compile(r"https://[a-z0-9-]+\.trycloudflare\.com")


def find_free_port(host: str, preferred: int) -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.bind((host, preferred))
            return preferred
        except OSError:
            pass
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, 0))
        return sock.getsockname()[1]


def start_cloudflared(local_url: str, timeout: float = 40.0) -> tuple[subprocess.Popen, str | None]:
    """Start a Cloudflare quick tunnel and return (process, public_url)."""
    binary = shutil.which("cloudflared")
    if not binary:
        return None, None
    proc = subprocess.Popen(
        [binary, "tunnel", "--no-autoupdate", "--url", local_url],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    public_url: list[str | None] = [None]

    def reader() -> None:
        assert proc.stdout is not None
        for line in proc.stdout:
            sys.stderr.write("[cloudflared] " + line)
            if public_url[0] is None:
                match = TRYCLOUDFLARE_RE.search(line)
                if match:
                    public_url[0] = match.group(0)

    thread = threading.Thread(target=reader, daemon=True)
    thread.start()

    deadline = time.time() + timeout
    while time.time() < deadline:
        if public_url[0]:
            return proc, public_url[0]
        if proc.poll() is not None:
            return proc, None
        time.sleep(0.3)
    return proc, public_url[0]


def daemonize(log_file: Path) -> None:
    """Detach into a new session so the service survives the spawning shell.

    macOS has no `setsid` binary and `nohup &` keeps the child in the caller's
    process group, so it gets reaped when the launching shell / elevated
    system.run command returns. A classic double-fork + setsid makes the daemon
    a session leader that outlives its parent.
    """
    if os.fork() > 0:
        os._exit(0)  # original process returns to the caller immediately
    os.setsid()
    if os.fork() > 0:
        os._exit(0)  # first child exits; grandchild is fully detached
    log_file.parent.mkdir(parents=True, exist_ok=True)
    sys.stdout.flush()
    sys.stderr.flush()
    log_fd = os.open(str(log_file), os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644)
    null_fd = os.open(os.devnull, os.O_RDONLY)
    os.dup2(null_fd, 0)
    os.dup2(log_fd, 1)
    os.dup2(log_fd, 2)
    os.close(null_fd)
    os.close(log_fd)


def main() -> int:
    parser = argparse.ArgumentParser(description="Launch the Go Next Move web server behind a public tunnel.")
    parser.add_argument("--host", default="127.0.0.1", help="Local bind host, default: 127.0.0.1")
    parser.add_argument("--port", type=int, default=8848, help="Preferred local port, default: 8848")
    parser.add_argument("--ttl-hours", type=float, default=DEFAULT_TTL_SECONDS / 3600, help="Link validity in hours, default: 5")
    parser.add_argument("--secret-path", type=Path, default=DEFAULT_SECRET_PATH, help="Secret file path")
    parser.add_argument("--rotate-secret", action="store_true", help="Rotate the secret first, invalidating all existing links")
    parser.add_argument("--no-tunnel", action="store_true", help="Skip the tunnel and only print the local link")
    parser.add_argument("--tunnel", choices=["cloudflare", "none"], default="cloudflare", help="Tunnel provider")
    parser.add_argument("--visits", type=int, help="Forward a KataGo visit budget to next_move.py")
    parser.add_argument("--coordinate-style", choices=["gtp", "sequential"], help="Forward coordinate style to next_move.py")
    parser.add_argument("--katago", help="Forward an explicit katago executable path to next_move.py")
    parser.add_argument("--model", help="Forward an explicit KataGo model path to next_move.py")
    parser.add_argument("--analysis-config", help="Forward an explicit KataGo analysis config to next_move.py")
    parser.add_argument("--skill-config", help="Forward an explicit project analysis override config to next_move.py")
    parser.add_argument("--state-dir", type=Path, default=DEFAULT_STATE_DIR, help="Directory for the public tunnel URL state file")
    parser.add_argument("--daemonize", action="store_true", help="Detach into a new session (double-fork) and keep running in the background")
    parser.add_argument("--log-file", type=Path, help="Log file when daemonizing (default: <state-dir>/serve.log)")
    parser.add_argument("--pid-file", type=Path, help="Write the running PID to this file")
    args = parser.parse_args()

    if args.daemonize:
        log_file = args.log_file or (Path(args.state_dir) / "serve.log")
        daemonize(log_file)

    if args.pid_file:
        args.pid_file.parent.mkdir(parents=True, exist_ok=True)
        args.pid_file.write_text(str(os.getpid()) + "\n", encoding="utf-8")

    if args.rotate_secret:
        secret = rotate_secret(args.secret_path)
        sys.stderr.write("[launch] rotated secret; all previous links are now invalid\n")
    else:
        secret = load_or_create_secret(args.secret_path)

    port = find_free_port(args.host, args.port)
    extra = build_next_move_args(args)

    httpd = run_server(args.host, port, secret, extra)
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()
    local_url = f"http://{args.host}:{port}"
    sys.stderr.write(f"[launch] resident web server on {local_url}\n")

    state_dir = Path(args.state_dir)
    state_dir.mkdir(parents=True, exist_ok=True)
    tunnel_url_file = state_dir / "tunnel_url"
    (state_dir / "port").write_text(str(port) + "\n", encoding="utf-8")

    use_tunnel = not args.no_tunnel and args.tunnel == "cloudflare"
    if not use_tunnel:
        tunnel_url_file.write_text(local_url + "\n", encoding="utf-8")
        sys.stderr.write(f"[launch] tunnel disabled; serving local URL only: {local_url}\n")
        _print_startup_link(local_url, secret, args.ttl_hours)
        try:
            while True:
                time.sleep(3600)
        except KeyboardInterrupt:
            pass
        finally:
            httpd.shutdown()
        return 0

    # Resident supervision: keep a Cloudflare quick tunnel alive and keep the
    # public URL state file current. Quick-tunnel hostnames change whenever
    # cloudflared restarts, which is exactly why the agent re-reads this file
    # each time it mints a link.
    printed_first = False
    try:
        while True:
            tunnel_proc, public_url = start_cloudflared(local_url)
            if tunnel_proc is None:
                sys.stderr.write(
                    "[launch] cloudflared not found. Install it (`brew install cloudflared`) "
                    "or run with --no-tunnel.\n"
                )
                tunnel_url_file.write_text(local_url + "\n", encoding="utf-8")
                return 1
            if public_url:
                tunnel_url_file.write_text(public_url + "\n", encoding="utf-8")
                sys.stderr.write(f"[launch] tunnel ready: {public_url}\n")
                if not printed_first:
                    _print_startup_link(public_url, secret, args.ttl_hours)
                    printed_first = True
            else:
                sys.stderr.write("[launch] tunnel did not report a public URL; retrying.\n")
            tunnel_proc.wait()
            sys.stderr.write("[launch] tunnel exited; restarting in 3s.\n")
            time.sleep(3)
    except KeyboardInterrupt:
        pass
    finally:
        httpd.shutdown()
        try:
            if tunnel_proc is not None and tunnel_proc.poll() is None:
                tunnel_proc.terminate()
        except NameError:
            pass
    return 0


def _print_startup_link(public_base: str, secret: str, ttl_hours: float) -> None:
    token = mint_token(secret, ttl_seconds=int(ttl_hours * 3600))
    print("=" * 72)
    print("围棋下一手 · HTTP 交互链接（启动样例，token 每次重新签发）")
    print(f"有效期：约 {ttl_hours:g} 小时")
    print("")
    print(f"{public_base}/?token={token}")
    print("=" * 72)
    sys.stdout.flush()


if __name__ == "__main__":
    raise SystemExit(main())
