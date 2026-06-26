#!/usr/bin/env python3
"""
deploy.py — Deploy a custom OpenClaw repo to a Hostinger VPS via SSH.

Usage:
    python3 deploy.py --ip <IP> --key <SSH_KEY_PATH> [options]

Options:
    --ip          Server IP address (required)
    --key         Path to SSH private key (required)
    --user        SSH user (default: root)
    --port        SSH port (default: 22)
    --repo        OpenClaw npm package or git URL (default: openclaw)
                  Examples:
                    openclaw                     (official npm package)
                    my-fork@1.2.3               (scoped npm)
                    https://github.com/org/repo  (git clone + build)
    --name        Agent name (default: Koda)
    --gw-port     Gateway port (default: 18789)
    --token       Auth token (auto-generated if not provided)
    --anthropic   Anthropic API key (reads ANTHROPIC_API_KEY env if omitted)
    --openai      OpenAI API key (reads OPENAI_API_KEY env if omitted)
    --no-firewall Skip UFW configuration
"""

import argparse
import json
import os
import secrets
import subprocess
import sys
import time

try:
    import paramiko
except ImportError:
    print("Installing paramiko...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "paramiko", "--break-system-packages", "-q"])
    import paramiko


def run(client: paramiko.SSHClient, cmd: str, timeout: int = 120, show: bool = True) -> tuple[str, int]:
    """Run a remote command, return (stdout, exit_code)."""
    short = cmd[:90] + ("…" if len(cmd) > 90 else "")
    print(f"\n\033[36m$ {short}\033[0m")
    _, stdout, stderr = client.exec_command(cmd, timeout=timeout, get_pty=True)
    output = ""
    while True:
        line = stdout.readline()
        if not line:
            break
        output += line
        if show:
            print(line, end="", flush=True)
    code = stdout.channel.recv_exit_status()
    if code != 0:
        err = stderr.read().decode(errors="replace").strip()
        if err and show:
            print(f"\033[33m[stderr] {err[:300]}\033[0m")
    return output, code


def step(label: str) -> None:
    print(f"\n{'━'*56}\n  {label}\n{'━'*56}")


def connect(ip: str, port: int, user: str, key_path: str) -> paramiko.SSHClient:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print(f"🔌 Connecting to {user}@{ip}:{port} …")
    client.connect(ip, port=port, username=user, key_filename=key_path, timeout=30)
    print("✅ Connected")
    return client


def install_nodejs(client: paramiko.SSHClient) -> None:
    step("Installing Node.js 22")
    run(client, "apt-get update -qq", timeout=120)
    run(client, "apt-get install -y curl git ufw 2>&1 | tail -3", timeout=120)
    run(client, "curl -fsSL https://deb.nodesource.com/setup_22.x | bash - 2>&1 | tail -3", timeout=60)
    run(client, "apt-get install -y nodejs 2>&1 | tail -3", timeout=120)
    out, _ = run(client, "node --version && npm --version", show=True)
    print(f"  → {out.strip()}")


def install_openclaw(client: paramiko.SSHClient, repo: str) -> str:
    """Install OpenClaw. Returns the binary path."""
    step(f"Installing OpenClaw: {repo}")

    is_git = repo.startswith("http://") or repo.startswith("https://") or repo.startswith("git@")

    if is_git:
        # Clone and build from source
        run(client, "apt-get install -y git 2>&1 | tail -2", timeout=60)
        run(client, "npm install -g pnpm 2>&1 | tail -3", timeout=120)
        run(client, f"rm -rf /opt/openclaw && git clone --depth 1 {repo} /opt/openclaw", timeout=120)
        run(client, "cd /opt/openclaw && pnpm install --frozen-lockfile 2>&1 | tail -5", timeout=300)
        run(client, "cd /opt/openclaw && pnpm build 2>&1 | tail -5", timeout=300)
        # Link binary
        run(client, "ln -sf /opt/openclaw/dist/index.js /usr/local/bin/openclaw && chmod +x /usr/local/bin/openclaw", timeout=10)
        binary = "/usr/local/bin/openclaw"
    else:
        # npm install from registry
        run(client, f"npm install -g {repo} 2>&1 | tail -8", timeout=300)
        out, _ = run(client, "which openclaw", show=False)
        binary = out.strip() or "/usr/bin/openclaw"

    # Verify
    out, code = run(client, f"{binary} --version 2>&1 || {binary} version 2>&1 | head -2", show=True)
    if code != 0:
        print("⚠ Could not verify openclaw binary — continuing anyway")

    return binary


def write_config(client: paramiko.SSHClient, agent_name: str, gw_port: int,
                 token: str, anthropic_key: str, openai_key: str, ip: str) -> None:
    step("Writing openclaw.json")

    # IMPORTANT: agents.list[] format — NOT agents.default (causes schema error)
    config = {
        "agents": {
            "defaults": {
                "model": {"primary": "anthropic/claude-sonnet-4-6"}
            },
            "list": [
                {
                    "id": "main",
                    "default": True,
                    "name": agent_name,
                    "model": {"primary": "anthropic/claude-sonnet-4-6"}
                }
            ]
        },
        "env": {
            "ANTHROPIC_API_KEY": anthropic_key,
            **({"OPENAI_API_KEY": openai_key} if openai_key else {})
        },
        "gateway": {
            "port": gw_port,
            "bind": "lan",
            "mode": "remote",
            "auth": {
                "mode": "token",
                "token": token
            },
            "controlUi": {
                "allowedOrigins": [
                    f"http://localhost:{gw_port}",
                    f"http://127.0.0.1:{gw_port}",
                    f"http://{ip}:{gw_port}",
                ]
            }
        }
    }

    config_json = json.dumps(config, indent=2).replace('"', '\\"').replace('$', '\\$')

    run(client, "mkdir -p /root/.openclaw /root/.openclaw/agents/main/sessions", timeout=10)
    run(client, f'echo "{config_json}" > /root/.openclaw/openclaw.json', timeout=10)
    run(client, "chmod 600 /root/.openclaw/openclaw.json && chmod 700 /root/.openclaw", timeout=10)


def install_service(client: paramiko.SSHClient, binary: str, gw_port: int) -> None:
    step("Installing systemd service")

    # IMPORTANT:
    # - Use 'openclaw gateway --bind lan --auth token --allow-unconfigured'
    #   NOT 'openclaw gateway start' (that manages user-level systemd, fails in system service)
    # - Set XDG_RUNTIME_DIR=/run/user/0 (required to avoid D-Bus errors)
    # - Set OPENCLAW_NO_RESPAWN=1 (avoids extra startup overhead)
    # - Set NODE_COMPILE_CACHE for faster cold starts on small VPS

    service = f"""[Unit]
Description=OpenClaw Gateway
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root
ExecStart={binary} gateway --bind lan --port {gw_port} --auth token --allow-unconfigured
Restart=always
RestartSec=5
Environment=HOME=/root
Environment=NODE_ENV=production
Environment=OPENCLAW_NO_RESPAWN=1
Environment=NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache
Environment=XDG_RUNTIME_DIR=/run/user/0

[Install]
WantedBy=multi-user.target
"""

    run(client, f"mkdir -p /run/user/0 && chmod 700 /run/user/0", timeout=10)
    run(client, f"mkdir -p /var/tmp/openclaw-compile-cache", timeout=10)
    run(client, f"cat > /etc/systemd/system/openclaw.service << 'EOF'\n{service}\nEOF", timeout=10)
    run(client, "systemctl daemon-reload", timeout=15)
    run(client, "systemctl enable openclaw", timeout=10)
    run(client, "systemctl restart openclaw", timeout=30)


def configure_firewall(client: paramiko.SSHClient, gw_port: int) -> None:
    step("Configuring UFW firewall")
    run(client, f"ufw allow 22/tcp && ufw allow {gw_port}/tcp && ufw --force enable", timeout=30)


def wait_for_ready(client: paramiko.SSHClient, gw_port: int, attempts: int = 10) -> bool:
    step("Waiting for gateway to come online")
    for i in range(attempts):
        out, code = run(client, f"ss -tlnp | grep {gw_port}", show=False)
        if code == 0 and str(gw_port) in out:
            print(f"  ✅ Port {gw_port} is listening")
            return True
        print(f"  [{i+1}/{attempts}] Not ready yet — waiting 3s…")
        time.sleep(3)
    return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Deploy OpenClaw to Hostinger VPS")
    parser.add_argument("--ip", required=True, help="Server IP address")
    parser.add_argument("--key", required=True, help="Path to SSH private key")
    parser.add_argument("--user", default="root", help="SSH username")
    parser.add_argument("--port", type=int, default=22, help="SSH port")
    parser.add_argument("--repo", default="openclaw", help="npm package name or git URL")
    parser.add_argument("--name", default="Koda", help="Agent name")
    parser.add_argument("--gw-port", type=int, default=18789, help="Gateway port")
    parser.add_argument("--token", default="", help="Auth token (auto-generated if empty)")
    parser.add_argument("--anthropic", default="", help="Anthropic API key")
    parser.add_argument("--openai", default="", help="OpenAI API key")
    parser.add_argument("--no-firewall", action="store_true", help="Skip firewall config")
    args = parser.parse_args()

    # Resolve API keys
    anthropic_key = args.anthropic or os.environ.get("ANTHROPIC_API_KEY", "")
    openai_key = args.openai or os.environ.get("OPENAI_API_KEY", "")

    if not anthropic_key:
        # Try reading from OpenClaw vault
        vault_path = os.path.expanduser("~/.openclaw/secrets.json")
        if os.path.exists(vault_path):
            vault = json.load(open(vault_path))
            anthropic_key = vault.get("ANTHROPIC_API_KEY", "")
            openai_key = openai_key or vault.get("OPENAI_API_KEY", "")

    if not anthropic_key:
        print("❌ ANTHROPIC_API_KEY is required. Pass --anthropic or set the env var.", file=sys.stderr)
        sys.exit(1)

    # Generate token if not provided
    token = args.token or secrets.token_hex(24)

    print(f"""
╔══════════════════════════════════════════════════════╗
║          OpenClaw VPS Deployment                     ║
╠══════════════════════════════════════════════════════╣
║  Server:  {args.ip:<42} ║
║  Repo:    {args.repo:<42} ║
║  Agent:   {args.name:<42} ║
║  Port:    {args.gw_port:<42} ║
╚══════════════════════════════════════════════════════╝
""")

    client = connect(args.ip, args.port, args.user, args.key)

    try:
        install_nodejs(client)
        binary = install_openclaw(client, args.repo)
        write_config(client, args.name, args.gw_port, token, anthropic_key, openai_key, args.ip)
        install_service(client, binary, args.gw_port)

        if not args.no_firewall:
            configure_firewall(client, args.gw_port)

        ready = wait_for_ready(client, args.gw_port)

        print(f"""
{'━'*56}
  {'✅ DEPLOYMENT COMPLETE' if ready else '⚠ DEPLOYED — gateway may still be starting'}
{'━'*56}

  🌐 URL:    http://{args.ip}:{args.gw_port}
  🔑 Token:  {token}
  🐻 Agent:  {args.name}

  Manage:
    ssh {args.user}@{args.ip} "systemctl status openclaw"
    ssh {args.user}@{args.ip} "journalctl -u openclaw -f"
    ssh {args.user}@{args.ip} "systemctl restart openclaw"
""")

        # Save token to local vault if possible
        vault_path = os.path.expanduser("~/.openclaw/secrets.json")
        if os.path.exists(vault_path):
            vault = json.load(open(vault_path))
            key_name = f"OPENCLAW_VPS_{args.ip.replace('.', '_')}_TOKEN"
            vault[key_name] = token
            with open(vault_path, "w") as f:
                json.dump(vault, f, indent=2)
            print(f"  💾 Token saved to vault as {key_name}")

    finally:
        client.close()


if __name__ == "__main__":
    main()
