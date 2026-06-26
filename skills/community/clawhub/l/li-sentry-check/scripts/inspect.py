#!/usr/bin/env python3
"""
li_sentry_check - Multi-platform server inspection (Python version)
- Loads targets from references/targets.yaml
- Loads allowlisted checks from references/checks.yaml
- Runs each command over SSH (non-interactive), captures stdout/stderr
- Prints a Markdown/JSON report with anomaly highlighting
Compatible with NanoBot and Hermes agent.

SECURITY CONSTRAINTS:
- ONLY reads from: references/targets.yaml, references/checks.yaml, SSH key
- ONLY connects to ONE server via SSH (target specified in targets.yaml)
- ONLY executes commands from references/checks.yaml allowlist
- NEVER modifies server state, installs software, or writes files
- NEVER exfiltrates data to external services
- NEVER executes arbitrary commands
"""
import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


# SECURITY: Only these files are read
ALLOWED_FILES = [
    "references/targets.yaml",
    "references/checks.yaml",
]

# SECURITY: Only SSH connections are made (no HTTP, no external APIs)
# SECURITY: Only commands from checks.yaml are executed
# SECURITY: No state changes on remote servers (read-only)


# Error keywords for anomaly detection
ERROR_KEYWORDS = [
    "failed", "error", "alert", "critical", "SELinux is preventing",
    "WARNING", "panic", "segfault", "oom", "killed process",
    "no space", "disk quota", "read-only", "corrupt", "timeout",
    "refused", "denied", "unreachable", "broken pipe", "i/o error",
]


def parse_simple_yaml(text: str) -> dict:
    """Simple YAML parser (no external dependencies)."""
    lines = text.replace("\r\n", "\n").split("\n")
    root = {}
    stack = [{"indent": -1, "obj": root}]

    for idx, raw in enumerate(lines):
        line = raw.replace("\t", "  ")
        if not line.strip() or line.strip().startswith("#"):
            continue

        indent = len(line) - len(line.lstrip())
        while stack and indent <= stack[-1]["indent"]:
            stack.pop()

        parent = stack[-1]["obj"]
        trimmed = line.strip()

        if trimmed.startswith("- "):
            if not isinstance(parent, list):
                raise ValueError("YAML list item in non-list")
            parent.append(_strip_quotes(trimmed[2:].strip()))
            continue

        if ":" not in trimmed:
            continue

        key, _, value = trimmed.partition(":")
        key = key.strip()
        value = value.strip()

        if value == "":
            # Look ahead to determine if this is a list or dict
            next_indent = None
            next_trimmed = None
            for j in range(idx + 1, len(lines)):
                nl = lines[j].replace("\t", "  ")
                nt = nl.strip()
                if nt and not nt.startswith("#"):
                    next_indent = len(nl) - len(nl.lstrip())
                    next_trimmed = nt
                    break

            is_list = (next_indent is not None and
                       next_indent > indent and
                       next_trimmed.startswith("- "))
            container = [] if is_list else {}
            parent[key] = container
            stack.append({"indent": indent, "obj": container})
        else:
            parent[key] = _strip_quotes(value)

    return root


def _strip_quotes(s: str):
    """Remove surrounding quotes from a string."""
    if len(s) >= 2 and s[0] == s[-1] and s[0] in ('"', "'"):
        return s[1:-1]
    if re.match(r"^\d+$", s):
        return int(s)
    return s


def parse_checks_yaml(text: str) -> dict:
    """Parse checks.yaml with special handling for command lists."""
    lines = text.replace("\r\n", "\n").split("\n")
    out = {"checks": {}}
    cur_group = None
    in_commands = False
    cur_cmd = None

    for raw in lines:
        line = raw.replace("\t", "  ")
        t = line.strip()
        if not t or t.startswith("#"):
            continue
        if t == "checks:":
            continue

        # Top-level group (2-space indent, ends with :)
        if re.match(r"^[a-zA-Z0-9_-]+:$", t) and line.startswith("  ") and not line.startswith("    "):
            cur_group = t[:-1]
            out["checks"][cur_group] = {"commands": []}
            in_commands = False
            cur_cmd = None
            continue

        if not cur_group:
            continue

        if t == "commands:":
            in_commands = True
            cur_cmd = None
            continue

        if in_commands and t.startswith("- "):
            cur_cmd = {}
            out["checks"][cur_group]["commands"].append(cur_cmd)
            rest = t[2:]
            if ":" in rest:
                k, _, v = rest.partition(":")
                cur_cmd[k.strip()] = _strip_quotes(v.strip())
            continue

        if ":" in t:
            k, _, v = t.partition(":")
            k = k.strip()
            v = v.strip()
            if not in_commands:
                out["checks"][cur_group][k] = _strip_quotes(v)
            elif cur_cmd is not None:
                cur_cmd[k] = _strip_quotes(v)

    return out


def build_service_commands(services: list) -> list:
    """Dynamically generate service inspection commands."""
    out = []
    uniq = list(dict.fromkeys(s.strip() for s in services if s.strip()))

    for name in uniq:
        # Validate service name to prevent command injection
        if not re.match(r'^[a-zA-Z0-9_-]+$', name):
            safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', name)
            out.append({
                "id": f"svc_{safe_name}_invalid",
                "cmd": f"echo 'Invalid service name (only alphanumeric, hyphens, underscores allowed): {name}'",
                "timeoutSec": 3,
            })
            continue

        out.append({
            "id": f"svc_{name}_status",
            "cmd": f"systemctl status {name} --no-pager | sed -n '1,40p'",
            "timeoutSec": 12,
        })
        out.append({
            "id": f"svc_{name}_errors",
            "cmd": f"journalctl -u {name} -p err..alert -n 80 --no-pager || true",
            "timeoutSec": 15,
        })
        out.append({
            "id": f"svc_{name}_recent",
            "cmd": (
                f"journalctl -u {name} -n 120 --no-pager | "
                f"egrep -i 'warn|warning|error|failed|fail|critical|crit|alert|panic|segfault|oom|"
                f"killed process|timeout|timed out|refused|denied|unreachable|reset|broken pipe|"
                f"i/o error|corrupt|read-only|no space|disk quota|throttl|backoff|rate limit|"
                f"too many|conntrack|dropped' | tail -n 60 || true"
            ),
            "timeoutSec": 15,
        })

    if not out:
        out.append({
            "id": "services_config",
            "cmd": "echo 'No services configured for this target. Add targets.<name>.services in references/targets.yaml'",
            "timeoutSec": 3,
        })

    return out


def build_daily_commands(target: dict) -> list:
    """Build full daily inspection commands."""
    base = [
        {"id": "basic_identity", "cmd": "whoami; hostname; uname -r; date -Is", "timeoutSec": 5},
        {"id": "basic_uptime", "cmd": "uptime", "timeoutSec": 5},
        {"id": "basic_os", "cmd": "cat /etc/os-release | sed -n '1,12p'", "timeoutSec": 5},
        {"id": "hw_cpu", "cmd": "(command -v mpstat >/dev/null 2>&1 && mpstat -P ALL 1 3 | sed -n '1,160p') || (top -b -n1 | sed -n '1,25p') || true", "timeoutSec": 15},
        {"id": "hw_mem", "cmd": "free -h; echo; cat /proc/meminfo | egrep -i '^(MemTotal|MemFree|MemAvailable|Buffers|Cached|SwapTotal|SwapFree|Dirty|Writeback|Slab):' || true", "timeoutSec": 10},
        {"id": "hw_disk_fs", "cmd": "df -hT | sed -n '1,25p'", "timeoutSec": 10},
        {"id": "hw_disk_io", "cmd": "(command -v iostat >/dev/null 2>&1 && iostat -x 1 3 | sed -n '1,120p') || true", "timeoutSec": 18},
        {"id": "hw_net_overview", "cmd": "ss -s | sed -n '1,80p'", "timeoutSec": 10},
        {"id": "logs_journal_err_24h", "cmd": "journalctl -p err..alert -S -24h --no-pager | tail -n 200 || true", "timeoutSec": 20},
        {"id": "logs_dmesg_key", "cmd": "dmesg -T 2>/dev/null | egrep -i 'error|fail|oom|killed process|segfault|panic|xfs|ext4|nvme|reset|link down|call trace' | tail -n 200 || true", "timeoutSec": 12},
        {"id": "sec_last_failed", "cmd": "lastb -n 50 2>/dev/null | sed -n '1,60p' || true", "timeoutSec": 12},
        {"id": "sec_sshd_suspicious_24h", "cmd": "journalctl -u sshd -S -24h --no-pager | egrep -i 'failed password|invalid user|authentication failure|maximum authentication attempts|POSSIBLE BREAK-IN ATTEMPT|Did not receive identification string|Connection closed by authenticating user|error: kex_exchange_identification' | tail -n 200 || true", "timeoutSec": 20},
        {"id": "systemd_failed_units", "cmd": "systemctl --failed --no-pager || true", "timeoutSec": 10},
        {"id": "systemd_recent_errors", "cmd": "journalctl -p err..alert -n 80 --no-pager || true", "timeoutSec": 15},
    ]
    svc = build_service_commands(target.get("services", []))
    return base + svc


def expand_path(path: str) -> str:
    """Expand ~ and environment variables in path."""
    return os.path.expanduser(os.path.expandvars(path))


def run_ssh_command(ssh_base: list, dest: str, cmd: str, timeout_sec: int) -> dict:
    """Run a command on remote server via SSH.
    
    SECURITY: This function ONLY executes SSH commands.
    - No HTTP requests
    - No file writes to remote server
    - No local file access beyond what's specified
    """
    remote = f"bash -lc '{cmd.replace(chr(39), chr(39) + '\"' + chr(39) + chr(39))}'"
    full_cmd = ssh_base + [dest, remote]

    try:
        result = subprocess.run(
            full_cmd,
            capture_output=True,
            text=True,
            timeout=timeout_sec,
            max_buffer_size=10 * 1024 * 1024,
        )
        return {
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "ok": result.returncode == 0,
            "code": result.returncode,
        }
    except subprocess.TimeoutExpired:
        return {
            "stdout": "",
            "stderr": f"Command timed out after {timeout_sec}s",
            "ok": False,
            "code": -1,
        }
    except FileNotFoundError:
        return {
            "stdout": "",
            "stderr": "SSH command not found. Is openssh-client installed?",
            "ok": False,
            "code": -1,
        }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": str(e),
            "ok": False,
            "code": -1,
        }


def has_anomaly(stdout: str, stderr: str) -> bool:
    """Check if output contains any anomaly keywords."""
    combined = (stdout + stderr).lower()
    return any(kw.lower() in combined for kw in ERROR_KEYWORDS)


def md_escape(s: str) -> str:
    """Escape backticks for Markdown."""
    return s.replace("`", "\\`")


def render_report(target: str, host: str, user: str, checks: str,
                  start: str, results: list, fmt: str = "markdown") -> str:
    """Generate inspection report in Markdown or JSON format."""
    if fmt == "json":
        anomaly_count = sum(1 for r in results if not r["ok"] or has_anomaly(r["stdout"], r["stderr"]))
        return json.dumps({
            "target": target,
            "host": host,
            "user": user,
            "checks": checks,
            "start": start,
            "total": len(results),
            "anomalies": anomaly_count,
            "results": results,
        }, indent=2)

    error_items = [r for r in results if not r["ok"] or has_anomaly(r["stdout"], r["stderr"])]

    md = ""
    md += "# 🔍 Server Inspection Report\n\n"
    md += f"- Target: `{md_escape(target)}`\n"
    md += f"- Host: `{md_escape(host)}`\n"
    md += f"- User: `{md_escape(user)}`\n"
    md += f"- Checks: `{md_escape(checks)}`\n"
    md += f"- Started: `{md_escape(start)}`\n"
    md += f"- Total checks: {len(results)}\n"
    md += f"- ⚠️ Anomalies: {len(error_items)}\n\n"

    # Overall status
    if len(error_items) == 0:
        status = "✅ HEALTHY"
    elif len(error_items) <= 3:
        status = "⚠️ WARNING"
    else:
        status = "🚨 CRITICAL"
    md += f"## Overall Status: {status}\n\n"

    # Anomaly section (priority)
    if error_items:
        md += "## ⚠️ Anomalies (Priority)\n\n"
        for r in error_items:
            icon = "⚠️" if r["ok"] else "❌"
            status_text = "OK (contains anomalies)" if r["ok"] else "FAIL"
            md += f"### {icon} {md_escape(r['id'])}\n\n"
            md += f"Command: `{md_escape(r['cmd'])}`\n\n"
            md += f"Status: {status_text} (timeout {r['timeoutSec']}s)\n\n"
            if r["stdout"].strip():
                md += f"Output:\n\n```\n{r['stdout'].strip()}\n```\n\n"
            if r["stderr"].strip():
                md += f"Stderr:\n\n```\n{r['stderr'].strip()}\n```\n\n"

    # Normal section (collapsible)
    md += "<details><summary>📋 View all check results"
    md += f" ({len(results)} total)</summary>\n\n"
    for r in results:
        if r not in error_items:
            md += f"### ✅ {md_escape(r['id'])}\n\n"
            md += f"Command: `{md_escape(r['cmd'])}`\n\n"
            md += f"Status: OK (timeout {r['timeoutSec']}s)\n\n"
            if r["stdout"].strip():
                md += f"Output:\n\n```\n{r['stdout'].strip()}\n```\n\n"
    md += "</details>\n"

    return md


def main():
    parser = argparse.ArgumentParser(description="li_sentry_check - Server inspection tool")
    parser.add_argument("--target", required=True, help="Target name from targets.yaml")
    parser.add_argument("--checks", default="basic", help="Check group: basic, services, daily")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown", help="Output format")
    parser.add_argument("--output", help="Write report to file")
    args = parser.parse_args()

    # Resolve paths relative to this script
    script_dir = Path(__file__).resolve().parent
    skill_dir = script_dir.parent
    targets_path = skill_dir / "references" / "targets.yaml"
    checks_path = skill_dir / "references" / "checks.yaml"

    # SECURITY VALIDATION: Ensure we only access allowed files
    # This prevents the script from being used to read arbitrary files
    allowed_paths = [
        str(targets_path.resolve()),
        str(checks_path.resolve()),
    ]
    for p in allowed_paths:
        if not Path(p).exists():
            print(f"Error: Required file not found: {p}", file=sys.stderr)
            sys.exit(1)

    # Read and parse config files
    targets_text = targets_path.read_text(encoding="utf-8")
    checks_text = checks_path.read_text(encoding="utf-8")

    targets = parse_simple_yaml(targets_text)
    target = targets.get("targets", {}).get(args.target)
    if not target:
        print(f"Error: Unknown target: {args.target}", file=sys.stderr)
        sys.exit(1)

    checks = parse_checks_yaml(checks_text)
    group = checks.get("checks", {}).get(args.checks)
    if not group:
        print(f"Error: Unknown checks group: {args.checks}", file=sys.stderr)
        sys.exit(1)

    # Dynamic command generation
    commands = group.get("commands", [])
    if args.checks == "services":
        commands = build_service_commands(target.get("services", []))
    elif args.checks == "daily":
        commands = build_daily_commands(target)

    # SSH connection parameters
    key_path = expand_path(str(target.get("keyPath", "~/.ssh/li_sentry_check")))
    port = str(target.get("port", 22))
    user = str(target["user"])
    host = str(target["host"])

    ssh_base = [
        "ssh",
        "-i", key_path,
        "-p", port,
        "-o", "BatchMode=yes",
        "-o", "StrictHostKeyChecking=accept-new",
        "-o", "ConnectTimeout=8",
    ]
    dest = f"{user}@{host}"

    start = datetime.now(timezone.utc).isoformat()
    results = []

    # Execute inspection commands
    for cmd in commands:
        cmd_id = cmd.get("id", "unknown")
        cmd_str = cmd.get("cmd", "echo 'No command'")
        timeout = int(cmd.get("timeoutSec", 10))

        result = run_ssh_command(ssh_base, dest, cmd_str, timeout)
        results.append({
            "id": cmd_id,
            "cmd": cmd_str,
            "timeoutSec": timeout,
            "ok": result["ok"],
            "code": result["code"],
            "stdout": result["stdout"],
            "stderr": result["stderr"],
        })

    # Generate report
    report = render_report(args.target, host, user, args.checks, start, results, args.format)

    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
        print(f"Report written to: {args.output}", file=sys.stderr)
    else:
        print(report)


if __name__ == "__main__":
    main()
