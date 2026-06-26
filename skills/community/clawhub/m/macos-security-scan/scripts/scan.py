#!/usr/bin/env python3
"""
macOS Security Scan Script
Part of the macos-security-scan skill for OpenClaw / ClawHub.

Read-only. Never modifies the system.
Usage:
    python3 scan.py [--sudo] [--out PATH] [--days N]
"""

import argparse
import datetime
import json
import os
import platform
import plistlib
import re
import socket
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Known-bad process / file name fragments (conservative list — well-documented
# malware families targeting macOS). Keep short to avoid false positives.
# ---------------------------------------------------------------------------
KNOWN_BAD_PATTERNS = [
    "keylogger", "spyagent", "mspy", "flexispy", "familytime",
    "hiddentear", "mshelper", "pplauncher", "crossrider",
    "genieo", "InstallMac", "VSearch", "Pirrit", "Bundlore",
    "Shlayer", "OSX.CookieMiner", "OSX.Dok", "OSX.Eleanor",
    "OSX.Proton", "OSX.Calisto", "OSX.Coldroot",
]

SUSPICIOUS_DIRS = [
    "/tmp/", "/var/tmp/", "/var/folders/",
]

LAUNCH_DIRS = [
    Path.home() / "Library/LaunchAgents",
    Path("/Library/LaunchAgents"),
    Path("/Library/LaunchDaemons"),
    Path("/System/Library/LaunchAgents"),
    Path("/System/Library/LaunchDaemons"),
]

PRIVACY_SERVICES = [
    "kTCCServiceAccessibility",
    "kTCCServiceScreenCapture",
    "kTCCServiceCamera",
    "kTCCServiceMicrophone",
    "kTCCServiceInputMonitoring",
    "kTCCServiceSystemPolicyAllFiles",
]

PRIVACY_LABELS = {
    "kTCCServiceAccessibility": "Accessibility",
    "kTCCServiceScreenCapture": "Screen Recording",
    "kTCCServiceCamera": "Camera",
    "kTCCServiceMicrophone": "Microphone",
    "kTCCServiceInputMonitoring": "Input Monitoring (Keylogger risk)",
    "kTCCServiceSystemPolicyAllFiles": "Full Disk Access",
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def run(cmd, use_sudo=False, timeout=15):
    """Run a shell command, return (stdout, stderr, returncode)."""
    if use_sudo:
        cmd = ["sudo", "-n"] + cmd
    try:
        r = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout
        )
        return r.stdout.strip(), r.stderr.strip(), r.returncode
    except subprocess.TimeoutExpired:
        return "", "timeout", 1
    except Exception as e:
        return "", str(e), 1


def section(title):
    bar = "=" * 60
    return f"\n{bar}\n  {title}\n{bar}\n"


def flag(level, message):
    icons = {"ok": "✅", "warn": "⚠️ ", "bad": "🚨"}
    return f"{icons.get(level, '  ')} {message}"


# ---------------------------------------------------------------------------
# Individual checks
# ---------------------------------------------------------------------------

def check_sip(use_sudo):
    lines = ["### System Integrity Protection (SIP)\n"]
    out, _, _ = run(["csrutil", "status"])
    if "enabled" in out.lower():
        lines.append(flag("ok", f"SIP is **enabled**. ({out})"))
    else:
        lines.append(flag("bad", f"SIP is **DISABLED** — this is a significant red flag. ({out})"))
    return "\n".join(lines)


def check_gatekeeper(use_sudo):
    lines = ["### Gatekeeper\n"]
    out, _, _ = run(["spctl", "--status"])
    if "enabled" in out.lower() or "assessments enabled" in out.lower():
        lines.append(flag("ok", "Gatekeeper is **enabled**."))
    else:
        lines.append(flag("bad", "Gatekeeper is **disabled** — unsigned apps can run freely."))
    return "\n".join(lines)


def check_filevault(use_sudo):
    lines = ["### FileVault (Disk Encryption)\n"]
    out, _, _ = run(["fdesetup", "status"])
    if "on" in out.lower():
        lines.append(flag("ok", "FileVault is **on**. Your disk is encrypted."))
    else:
        lines.append(flag("warn", f"FileVault is **off**. Anyone with physical access can read your disk. ({out})"))
    return "\n".join(lines)


def check_running_processes(use_sudo):
    lines = ["### Running Processes\n"]
    out, _, _ = run(["ps", "aux"])
    suspicious = []
    for line in out.splitlines()[1:]:
        parts = line.split()
        if len(parts) < 11:
            continue
        cmd_full = " ".join(parts[10:]).lower()
        pid = parts[1]
        user = parts[0]
        # Check known-bad patterns
        for pattern in KNOWN_BAD_PATTERNS:
            if pattern.lower() in cmd_full:
                suspicious.append(f"PID {pid} ({user}): `{cmd_full[:100]}` — matches known-bad pattern `{pattern}`")
        # Check suspicious directories
        for d in SUSPICIOUS_DIRS:
            if d in cmd_full and not cmd_full.startswith("/usr") and not cmd_full.startswith("/bin"):
                suspicious.append(f"PID {pid} ({user}): running from suspicious temp dir — `{cmd_full[:100]}`")

    if suspicious:
        lines.append(flag("bad", f"Found {len(suspicious)} suspicious process(es):\n"))
        for s in suspicious:
            lines.append(f"  - {s}")
    else:
        lines.append(flag("ok", "No obviously suspicious processes found."))
    return "\n".join(lines)


def check_launch_items(use_sudo):
    lines = ["### Launch Agents & Daemons (Startup Items)\n"]
    found = []
    for d in LAUNCH_DIRS:
        if not d.exists():
            continue
        for plist_path in d.glob("*.plist"):
            try:
                with open(plist_path, "rb") as f:
                    data = plistlib.load(f)
                label = data.get("Label", "?")
                program = data.get("Program") or (data.get("ProgramArguments") or ["?"])[0]
                run_at_load = data.get("RunAtLoad", False)
                found.append({
                    "path": str(plist_path),
                    "label": label,
                    "program": program,
                    "run_at_load": run_at_load,
                })
            except Exception:
                found.append({"path": str(plist_path), "label": "?", "program": "unreadable", "run_at_load": "?"})

    if not found:
        lines.append(flag("ok", "No launch items found."))
    else:
        lines.append(f"Found **{len(found)}** launch item(s). Review any you don't recognise:\n")
        for item in found:
            run_label = " *(runs at login)*" if item["run_at_load"] else ""
            suspicious = any(p.lower() in item["program"].lower() for p in KNOWN_BAD_PATTERNS)
            lvl = "bad" if suspicious else "warn"
            icon = "🚨" if suspicious else "  "
            lines.append(f"  {icon} `{item['label']}`{run_label}")
            lines.append(f"       Program: `{item['program']}`")
            lines.append(f"       Plist:   `{item['path']}`")
    return "\n".join(lines)


def check_login_items(use_sudo):
    lines = ["### Login Items\n"]
    out, _, rc = run(["osascript", "-e",
        'tell application "System Events" to get the name of every login item'])
    if rc == 0 and out:
        items = [i.strip() for i in out.split(",") if i.strip()]
        lines.append(f"Found **{len(items)}** login item(s):\n")
        for item in items:
            lines.append(f"  - {item}")
        lines.append("\n" + flag("warn", "Review any items you don't recognise."))
    else:
        lines.append(flag("ok", "No login items found (or could not be read without permission)."))
    return "\n".join(lines)


def check_network_connections(use_sudo):
    lines = ["### Network Connections (Active & Listening)\n"]
    cmd = ["lsof", "-i", "-n", "-P"]
    out, _, _ = run(cmd, use_sudo=use_sudo)
    listening = []
    established = []
    for line in out.splitlines()[1:]:
        parts = line.split()
        if len(parts) < 9:
            continue
        proc = parts[0]
        state = parts[-1] if parts[-1] in ("LISTEN", "(ESTABLISHED)") else ""
        addr = parts[8] if len(parts) > 8 else "?"
        if state == "LISTEN":
            listening.append(f"`{proc}` listening on `{addr}`")
        elif state == "(ESTABLISHED)":
            established.append(f"`{proc}` → `{addr}`")

    if listening:
        lines.append(f"**Listening ports** ({len(listening)}):\n")
        for l in listening[:20]:
            lines.append(f"  - {l}")
    else:
        lines.append(flag("ok", "No listening ports found."))

    if established:
        lines.append(f"\n**Active outbound connections** ({len(established)}):\n")
        for e in established[:20]:
            lines.append(f"  - {e}")
    else:
        lines.append(flag("ok", "\nNo active outbound connections found."))

    lines.append("\n" + flag("warn", "Review any connections to IPs/ports you don't recognise."))
    return "\n".join(lines)


def check_privacy_permissions(use_sudo):
    lines = ["### Privacy Permissions (Camera, Mic, Screen, Accessibility, etc.)\n"]
    # Read TCC databases
    tcc_paths = [
        Path.home() / "Library/Application Support/com.apple.TCC/TCC.db",
        Path("/Library/Application Support/com.apple.TCC/TCC.db"),
    ]
    results = []
    for tcc_path in tcc_paths:
        if not tcc_path.exists():
            continue
        cmd = ["sqlite3", str(tcc_path),
               "SELECT service, client, allowed FROM access WHERE allowed=1;"]
        out, err, rc = run(cmd, use_sudo=use_sudo)
        if rc == 0:
            for row in out.splitlines():
                parts = row.split("|")
                if len(parts) >= 2:
                    service, client = parts[0], parts[1]
                    label = PRIVACY_LABELS.get(service, service)
                    results.append((label, client))

    if results:
        # Group by service
        by_service = {}
        for label, client in results:
            by_service.setdefault(label, []).append(client)
        for service, clients in sorted(by_service.items()):
            risky = "Input Monitoring" in service or "Screen Recording" in service or "Accessibility" in service
            lvl = "warn" if risky else "ok"
            lines.append(f"\n**{service}** ({len(clients)} app(s)):")
            for c in clients:
                lines.append(f"  - `{c}`")
        lines.append("\n" + flag("warn",
            "Any app with Input Monitoring or Accessibility access that you don't recognise is a keylogger risk."))
    else:
        lines.append(flag("warn",
            "Could not read TCC database (try running with sudo for full results)."))
    return "\n".join(lines)


def check_kernel_extensions(use_sudo):
    lines = ["### Kernel Extensions (kexts)\n"]
    out, _, _ = run(["kextstat"])
    third_party = []
    for line in out.splitlines()[1:]:
        if "com.apple" not in line and "apple" not in line.lower():
            third_party.append(line.strip())
    if third_party:
        lines.append(flag("warn", f"Found **{len(third_party)}** third-party kernel extension(s):\n"))
        for k in third_party:
            lines.append(f"  - {k[:100]}")
        lines.append("\nKernel extensions have deep system access. Verify each is from a vendor you trust.")
    else:
        lines.append(flag("ok", "No third-party kernel extensions found."))
    return "\n".join(lines)


def check_recently_installed(use_sudo, days=14):
    lines = [f"### Recently Installed Software (last {days} days)\n"]
    cutoff = datetime.datetime.now() - datetime.timedelta(days=days)

    # Check /Applications
    apps = []
    for app in Path("/Applications").glob("*.app"):
        try:
            mtime = datetime.datetime.fromtimestamp(app.stat().st_mtime)
            if mtime > cutoff:
                apps.append((mtime, str(app)))
        except Exception:
            pass
    for app in (Path.home() / "Applications").glob("*.app"):
        try:
            mtime = datetime.datetime.fromtimestamp(app.stat().st_mtime)
            if mtime > cutoff:
                apps.append((mtime, str(app)))
        except Exception:
            pass

    # Check package receipts
    receipts_dir = Path("/var/db/receipts")
    receipts = []
    if receipts_dir.exists():
        for bom in receipts_dir.glob("*.bom"):
            try:
                mtime = datetime.datetime.fromtimestamp(bom.stat().st_mtime)
                if mtime > cutoff:
                    receipts.append((mtime, bom.stem))
            except Exception:
                pass

    if apps or receipts:
        lines.append(flag("warn",
            f"Found **{len(apps)}** app(s) and **{len(receipts)}** package(s) "
            f"installed/modified in the last {days} days:\n"))
        for mtime, path in sorted(apps, reverse=True):
            lines.append(f"  - {mtime.strftime('%Y-%m-%d')}  `{path}`")
        for mtime, name in sorted(receipts, reverse=True):
            lines.append(f"  - {mtime.strftime('%Y-%m-%d')}  package: `{name}`")
        lines.append("\nReview any items you didn't install yourself.")
    else:
        lines.append(flag("ok", f"No new software found in the last {days} days."))
    return "\n".join(lines)


def check_browser_extensions(use_sudo):
    lines = ["### Browser Extensions\n"]

    # Chrome
    chrome_dir = Path.home() / "Library/Application Support/Google/Chrome/Default/Extensions"
    if chrome_dir.exists():
        exts = [str(p) for p in chrome_dir.iterdir() if p.is_dir()]
        lines.append(f"**Google Chrome**: {len(exts)} extension(s) installed.")
        lines.append("  (To review: Chrome → Window → Extensions)")
    else:
        lines.append("**Google Chrome**: not found.")

    # Firefox
    ff_profiles = Path.home() / "Library/Application Support/Firefox/Profiles"
    if ff_profiles.exists():
        ext_count = sum(1 for p in ff_profiles.rglob("extensions/*.xpi"))
        lines.append(f"**Firefox**: ~{ext_count} extension file(s) found.")
        lines.append("  (To review: Firefox → Add-ons and Themes)")
    else:
        lines.append("**Firefox**: not found.")

    # Safari extensions listed via pluginkit
    out, _, _ = run(["pluginkit", "-mAvvv", "-p", "com.apple.Safari.extension"])
    safari_exts = [l.strip() for l in out.splitlines() if "Path" in l or "Bundle" in l]
    lines.append(f"**Safari**: {len(safari_exts)//2 if safari_exts else 0} extension(s).")
    lines.append("  (To review: Safari → Settings → Extensions)")

    lines.append("\n" + flag("warn", "Review all extensions. Remove any you didn't install."))
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Report assembly
# ---------------------------------------------------------------------------

def build_report(use_sudo, days):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hostname = socket.gethostname()
    macos_ver = platform.mac_ver()[0]

    parts = []
    parts.append(f"# macOS Security Scan Report")
    parts.append(f"\n**Date:** {now}  ")
    parts.append(f"**Host:** {hostname}  ")
    parts.append(f"**macOS:** {macos_ver}  ")
    parts.append(f"**Scan mode:** {'with sudo (deep)' if use_sudo else 'without sudo (standard)'}  \n")
    parts.append("> This report was generated by the `macos-security-scan` skill.")
    parts.append("> It is read-only — nothing on your system was changed.\n")
    parts.append("---\n")

    checks = [
        ("System Integrity & Encryption", [
            check_sip(use_sudo),
            check_gatekeeper(use_sudo),
            check_filevault(use_sudo),
        ]),
        ("Processes & Startup", [
            check_running_processes(use_sudo),
            check_launch_items(use_sudo),
            check_login_items(use_sudo),
        ]),
        ("Network", [
            check_network_connections(use_sudo),
        ]),
        ("Permissions & Extensions", [
            check_privacy_permissions(use_sudo),
            check_kernel_extensions(use_sudo),
            check_browser_extensions(use_sudo),
        ]),
        ("Recently Installed Software", [
            check_recently_installed(use_sudo, days),
        ]),
    ]

    for group_title, group_checks in checks:
        parts.append(section(group_title))
        for result in group_checks:
            parts.append(result)
            parts.append("")

    parts.append("---\n")
    parts.append("## What to do next\n")
    parts.append("- ✅ Items marked green are normal.")
    parts.append("- ⚠️  Items marked yellow are worth reviewing — they may be normal.")
    parts.append("- 🚨 Items marked red need immediate attention.")
    parts.append("\nIf you find anything concerning, consider:")
    parts.append("1. Contacting Apple Support (appleid.apple.com / 1-800-APL-CARE)")
    parts.append("2. Running a dedicated scanner such as Malwarebytes for Mac (free)")
    parts.append("3. Consulting a cybersecurity professional before using the device for sensitive tasks.")
    parts.append("\n---\n*End of report*\n")

    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="macOS security scan")
    parser.add_argument("--sudo", action="store_true",
                        help="Run privileged checks with sudo -n")
    parser.add_argument("--out", default="~/Desktop/security_report.md",
                        help="Output path for the report (default: ~/Desktop/security_report.md)")
    parser.add_argument("--days", type=int, default=14,
                        help="How many days back to check for recently installed software")
    args = parser.parse_args()

    if platform.system() != "Darwin":
        print("ERROR: This script only runs on macOS.", file=sys.stderr)
        sys.exit(1)

    print("🔍 Starting macOS security scan — this will take about 30–60 seconds…")
    report = build_report(use_sudo=args.sudo, days=args.days)

    out_path = Path(args.out).expanduser()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report, encoding="utf-8")

    print(f"\n✅ Scan complete. Report saved to: {out_path}")
    print("\n--- SUMMARY (first 60 lines) ---")
    for i, line in enumerate(report.splitlines()):
        if i >= 60:
            print("… (see full report file for details)")
            break
        print(line)


if __name__ == "__main__":
    main()
