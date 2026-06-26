"""
Interactive setup wizard for PVM.

Run with: pvm init [--config config.yaml]

Detects OS, checks prerequisites, walks through channel configuration,
and sets up the service manager.
"""

from __future__ import annotations

import argparse
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import questionary as q
    HAS_QUESTIONARY = True
except ImportError:
    HAS_QUESTIONARY = False

WELCOME = """
╔══════════════════════════════════════════════════════════════╗
║         Permission Vending Machine — Setup Wizard            ║
╚══════════════════════════════════════════════════════════════╝

This wizard will:
  1. Detect your OS and check prerequisites
  2. Configure which notification channels to enable
  3. Collect credentials for each channel
  4. Set up the service to run automatically

Let's get started.
"""


def check_prerequisites() -> dict:
    """Check what tools are available. Returns dict of found/missing tools."""
    return {
        "python": shutil.which("python3") or shutil.which("python"),
        "git": shutil.which("git"),
        "sendblue": shutil.which("sendblue"),
        "sqlite": shutil.which("sqlite3"),
    }


def detect_os() -> str:
    system = platform.system().lower()
    if system == "darwin":
        return "macos"
    elif system == "linux":
        return "linux"
    elif system == "windows" or os.name == "nt":
        return "windows"
    return "unknown"


def check_sendblue() -> bool:
    """Check if sendblue CLI is installed and configured."""
    try:
        result = subprocess.run(
            ["sendblue", "whoami"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.returncode == 0
    except Exception:
        return False


def detect_existing_config(config_path: str) -> dict | None:
    """Check if config.yaml already exists."""
    p = Path(config_path)
    if p.exists():
        import yaml
        try:
            return yaml.safe_load(p.read_text())
        except Exception:
            return {}
    return None


def run_wizard(config_path: str) -> dict:
    """Run the interactive setup wizard. Returns final config dict."""
    if not HAS_QUESTIONARY:
        print("questionary not installed. Run: pip install questionary")
        sys.exit(1)

    print(WELCOME)

    # ── OS Detection ──────────────────────────────────────────────────────
    os_name = detect_os()
    os_display = {"macos": "macOS", "linux": "Linux", "windows": "Windows"}.get(os_name, os_name)
    print(f"Detected OS: {os_display}")

    # ── Prerequisites ───────────────────────────────────────────────────────
    prereqs = check_prerequisites()
    print("\n📋 Prerequisites:")
    for tool, found in prereqs.items():
        status = "✅" if found else "❌"
        print(f"  {status} {tool}")

    if not prereqs.get("python"):
        print("\n❌ Python 3 not found. Please install Python 3.9+ first.")
        sys.exit(1)

    # ── Existing config? ──────────────────────────────────────────────────
    existing = detect_existing_config(config_path)
    if existing:
        print(f"\n⚠️  Config already exists at {config_path}")
        print("   Will update existing channels only.")
        start_config = existing
    else:
        print(f"\n📄 Creating new config at {config_path}")
        start_config = {
            "vault": {
                "db_path": str(Path(config_path).parent / "grants.db"),
                "default_ttl_minutes": 30,
                "max_ttl_minutes": 480,
            },
            "channels": {},
            "permissions": {
                "guarded_operations": [
                    {"operation": "rm", "scope_type": "path", "require_approval": True},
                    {"operation": "git push --force", "scope_type": "repo", "require_approval": True},
                    {"operation": "trash", "scope_type": "path", "require_approval": False},
                ]
            },
        }

    # ── Channels ──────────────────────────────────────────────────────────
    print("\n📡 Notification Channels")
    print("Enable the channels you want to use. You can enable multiple.")

    channel_questions = {
        "sendblue": "iMessage / SMS (macOS only — uses sendblue CLI)",
        "email": "Email (SMTP + IMAP — works on all platforms)",
        "discord": "Discord (webhook — works on all platforms)",
        "telegram": "Telegram (bot API — works on all platforms)",
        "slack": "Slack (webhook — works on all platforms)",
    }

    if os_name == "macos":
        # macOS: offer all channels
        enabled = q.checkbox(
            "Which channels should PVM use?",
            choices=[q.Choice(display, value=k) for k, display in channel_questions.items()],
            default=["sendblue", "discord"] if check_sendblue() else ["discord"],
        ).ask()
    else:
        # Non-macOS: disable sendblue (CLI only works on macOS)
        non_macos = {k: v for k, v in channel_questions.items() if k != "sendblue"}
        enabled = q.checkbox(
            "Which channels should PVM use? (Sendblue unavailable on this OS)",
            choices=[q.Choice(display, value=k) for k, display in non_macos.items()],
            default=["discord"],
        ).ask()

    if not enabled:
        print("No channels selected — cannot set up PVM without any notification channel.")
        sys.exit(1)

    # ── Per-channel configuration ───────────────────────────────────────────
    channels = {}
    approver_numbers = []

    # Discord
    if "discord" in enabled:
        print("\n🔔 Discord")
        webhook_url = q.text(
            "Discord webhook URL:",
            default=existing.get("channels", {}, {}).get("discord", {}).get("webhook_url", ""),
            validator=lambda v: q.Validation(
                q.ValidationType.PATTERN,
                "Must be a Discord webhook URL" if not v.startswith("https://discord.com/api/webhooks/") else q.ValidationResult.SUCCESS,
            ) if v else q.ValidationResult(success=True, text=""),
        ).ask()

        if os_name == "macos":
            default_base = "http://192.168.0.1:7823"
        else:
            default_base = "http://YOUR_SERVER_IP:7823"

        http_base = q.text(
            "Public URL for approval links (enter your server IP or domain):",
            default=existing.get("channels", {}, {}).get("discord", {}).get("http_approval_base", default_base),
        ).ask()

        channels["discord"] = {
            "enabled": True,
            "webhook_url": webhook_url,
            "http_approval_base": http_base,
        }

    # Sendblue (macOS only)
    if "sendblue" in enabled:
        print("\n📱 Sendblue (iMessage / SMS)")
        if not check_sendblue():
            print("⚠️  sendblue CLI not found. Install with: brew install sendblue")
            install = q.confirm("Continue without Sendblue?", default=False).ask()
            if not install:
                sys.exit(0)
        else:
            print("✅ sendblue CLI detected and configured.")

        from_number = q.text(
            "Sendblue iMessage number (from your sendblue account):",
            default=existing.get("channels", {}, {}).get("sendblue", {}).get("from_number", "+1"),
        ).ask()
        approver_raw = q.text(
            "Approver phone numbers (comma-separated, e.g. +1234567890, +0987654321):",
            default="",
        ).ask()
        if approver_raw:
            approver_numbers = [n.strip() for n in approver_raw.split(",") if n.strip()]

        channels["sendblue"] = {
            "enabled": True,
            "api_key": existing.get("channels", {}, {}).get("sendblue", {}).get("api_key", ""),
            "from_number": from_number,
            "approver_numbers": approver_numbers,
            "poll_interval_seconds": 15,
        }

    # Email
    if "email" in enabled:
        print("\n📧 Email")
        smtp_host = q.text(
            "SMTP host (e.g. smtp.mail.me.com for iCloud):",
            default=existing.get("channels", {}, {}).get("email", {}).get("smtp_host", "smtp.mail.me.com"),
        ).ask()
        smtp_port = q.text(
            "SMTP port:",
            default=existing.get("channels", {}, {}).get("email", {}).get("smtp_port", "465"),
        ).ask()
        imap_host = q.text(
            "IMAP host:",
            default=existing.get("channels", {}, {}).get("email", {}).get("imap_host", smtp_host.replace("smtp", "imap")),
        ).ask()
        imap_port = q.text(
            "IMAP port:",
            default=existing.get("channels", {}, {}).get("email", {}).get("imap_port", "993"),
        ).ask()
        username = q.text(
            "Email username (your email address):",
            default=existing.get("channels", {}, {}).get("email", {}).get("username", ""),
        ).ask()
        password = q.password(
            "Email password or app-specific password:",
        ).ask()
        approver_emails_raw = q.text(
            "Approver email addresses (comma-separated):",
            default="",
        ).ask()

        channels["email"] = {
            "enabled": True,
            "smtp_host": smtp_host,
            "smtp_port": int(smtp_port),
            "imap_host": imap_host,
            "imap_port": int(imap_port),
            "username": username,
            "password": password,
            "from_addr": username,
            "approver_emails": [e.strip() for e in approver_emails_raw.split(",") if e.strip()],
        }

    # Telegram
    if "telegram" in enabled:
        print("\n✈️  Telegram")
        bot_token = q.password("Telegram bot token:").ask()
        approver_chats_raw = q.text(
            "Approver Telegram chat IDs (comma-separated):",
            default="",
        ).ask()
        channels["telegram"] = {
            "enabled": True,
            "bot_token": bot_token,
            "approver_chat_ids": [c.strip() for c in approver_chats_raw.split(",") if c.strip()],
        }

    # Slack
    if "slack" in enabled:
        print("\n💬 Slack")
        webhook_url = q.text(
            "Slack webhook URL:",
            default=existing.get("channels", {}, {}).get("slack", {}).get("webhook_url", "https://hooks.slack.com/..."),
        ).ask()
        channels["slack"] = {
            "enabled": True,
            "webhook_url": webhook_url,
        }

    # ── Default disabled channels ─────────────────────────────────────────
    all_channels = ["sendblue", "email", "discord", "telegram", "slack"]
    for ch in all_channels:
        if ch not in channels:
            channels[ch] = {"enabled": False}

    # ── Server settings ────────────────────────────────────────────────────
    print("\n🌐 Server")
    default_port = existing.get("server", {}).get("port", "7823")
    port = q.text(f"HTTP server port (default: {default_port}):", default=default_port).ask()
    try:
        port = int(port) if port else 7823
    except ValueError:
        port = 7823

    if os_name == "macos":
        default_db = str(Path.home() / "flume" / "permission-vending-machine" / "grants.db")
    else:
        default_db = str(Path.home() / "permission-vending-machine" / "grants.db")
    db_path = q.text(f"Database path:", default=existing.get("vault", {}).get("db_path", default_db)).ask()

    # ── Summary ───────────────────────────────────────────────────────────
    print("\n╔══════════════════════════════════════════════════════════════╗")
    print("║                      Setup Summary                            ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print(f"  Config file: {config_path}")
    print(f"  OS: {os_display}")
    print(f"  Channels: {', '.join(enabled)}")
    print(f"  Server port: {port}")
    print(f"  Database: {db_path}")

    confirm = q.confirm("\n✅ Write config and set up service?", default=True).ask()
    if not confirm:
        print("Aborted.")
        sys.exit(0)

    # ── Write config ──────────────────────────────────────────────────────
    import yaml

    config = {
        "vault": {
            "db_path": db_path,
            "default_ttl_minutes": 30,
            "max_ttl_minutes": 480,
        },
        "channels": channels,
        "permissions": start_config.get("permissions", {}),
    }

    config_p = Path(config_path)
    config_p.parent.mkdir(parents=True, exist_ok=True)
    config_p.write_text(yaml.dump(config, default_flow_style=False, sort_keys=False))
    print(f"\n✅ Config written to {config_path}")

    # ── Service setup ─────────────────────────────────────────────────────
    service_dir = Path.home() / "Library" / "LaunchAgents" if os_name == "macos" else Path("/etc/systemd/system") if os_name == "linux" else Path.home() / "pvm"

    print(f"\n⚙️  Setting up service ({os_display})...")

    if os_name == "macos":
        setup_macos_service(config_path, port, db_path)
    elif os_name == "linux":
        setup_linux_service(config_path, port, db_path)
    else:
        print("⚠️  Service setup for Windows not yet automated.")
        print("   Run manually: pvm serve --port", port)

    print("\n╔══════════════════════════════════════════════════════════════╗")
    print("║  ✅ Setup complete!                                           ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print(f"\n  Start:   launchctl load ~/Library/LaunchAgents/ai.flume.pvm.plist")
    print(f"  Status:  curl http://localhost:{port}/health")
    print(f"  Logs:    tail -f ~/flume/permission-vending-machine/pvm.err.log")
    print(f"\n  After adding API keys to {config_path}, restart the service.")

    return config


def setup_macos_service(config_path: str, port: int, db_path: str) -> None:
    """Generate and install launchd plist for macOS."""
    plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>ai.flume.pvm</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Library/Developer/CommandLineTools/usr/bin/python3</string>
        <string>-m</string>
        <string>pvm</string>
        <string>serve</string>
        <string>--port</string>
        <string>{port}</string>
    </array>
    <key>WorkingDirectory</key>
    <string>{Path(config_path).parent.absolute()}</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PYTHONPATH</key>
        <string>{Path(config_path).parent.absolute()}/src</string>
        <key>PATH</key>
        <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    </dict>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>{Path(db_path).parent.absolute()}/pvm.log</string>
    <key>StandardErrorPath</key>
    <string>{Path(db_path).parent.absolute()}/pvm.err.log</string>
    <key>ProcessType</key>
    <string>Background</string>
</dict>
</plist>
"""
    plist_path = Path.home() / "Library" / "LaunchAgents" / "ai.flume.pvm.plist"
    plist_path.parent.mkdir(parents=True, exist_ok=True)
    plist_path.write_text(plist_content)
    print(f"✅ Created launchd plist at {plist_path}")
    print(f"   To start: launchctl load {plist_path}")


def setup_linux_service(config_path: str, port: int, db_path: str) -> None:
    """Generate systemd unit for Linux."""
    unit_content = f"""[Unit]
Description=PVM Approval Daemon
After=network.target

[Service]
Type=simple
User={os.environ.get('USER', 'root')}
WorkingDirectory={Path(config_path).parent.absolute()}
ExecStart=/usr/bin/python3 -m pvm serve --port {port}
Restart=always
RestartSec=10
StandardOutput=append:{Path(db_path).parent.absolute()}/pvm.log
StandardError=append:{Path(db_path).parent.absolute()}/pvm.err.log
Environment=PYTHONPATH={Path(config_path).parent.absolute()}/src

[Install]
WantedBy=multi-user.target
"""
    unit_path = Path("/tmp/pvm.service")
    unit_path.write_text(unit_content)
    print(f"✅ Systemd unit written to {unit_path}")
    print("   To install (requires sudo):")
    print(f"   sudo mv {unit_path} /etc/systemd/system/pvm.service")
    print("   sudo systemctl daemon-reload")
    print("   sudo systemctl enable pvm")
    print("   sudo systemctl start pvm")


def main() -> int:
    parser = argparse.ArgumentParser(prog="pvm init")
    parser.add_argument(
        "--config",
        default=os.environ.get("PVM_CONFIG", "./config.yaml"),
        help="Path to config file (default: ./config.yaml or $PVM_CONFIG)",
    )
    args = parser.parse_args()

    if not HAS_QUESTIONARY:
        print("This command requires questionary.")
        print("Install it with: pip install questionary")
        return 1

    run_wizard(args.config)
    return 0
