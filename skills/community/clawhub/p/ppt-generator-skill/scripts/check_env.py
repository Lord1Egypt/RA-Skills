#!/usr/bin/env python3
"""
check_env.py — Environment dependency checker for ppt-generator skill.

Run this once after installation to verify all required tools are available.
Outputs a clear pass/fail report with exact install commands for missing items.

Usage:
  python3 scripts/check_env.py
  python3 scripts/check_env.py --json   # machine-readable output
  python3 scripts/check_env.py --fix    # auto-install missing Python packages

Exit codes:
  0 — all dependencies satisfied
  1 — one or more dependencies missing (details printed to stdout)
"""

import sys
import os
import json
import shutil
import subprocess
import argparse
import platform


# ── Dependency definitions ────────────────────────────────────────────────────

# Each entry: (check_fn, display_name, install_commands_by_platform, critical)
# critical=True  → skill will not work at all without this
# critical=False → degrades gracefully (e.g. QA steps skipped)

def _run(cmd: list) -> tuple[bool, str]:
    """Run a command, return (success, output)."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return result.returncode == 0, (result.stdout + result.stderr).strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False, ""


def check_python3():
    v = sys.version_info
    ok = v.major == 3 and v.minor >= 9
    ver = f"{v.major}.{v.minor}.{v.micro}"
    return ok, ver


def check_node():
    ok, out = _run(["node", "--version"])
    return ok, out.strip()


def check_npm():
    ok, out = _run(["npm", "--version"])
    return ok, out.strip()


def check_pptxgenjs():
    # Check global npm install
    ok, out = _run(["node", "-e", "require('pptxgenjs'); console.log('ok')"])
    if ok and "ok" in out:
        return True, "installed"
    # Also check local node_modules
    local = os.path.join(os.getcwd(), "node_modules", "pptxgenjs")
    if os.path.isdir(local):
        return True, f"installed (local: {local})"
    return False, "not found"


def check_pip_package(pkg_import: str, pkg_name: str):
    try:
        __import__(pkg_import)
        # Get version if available
        try:
            import importlib.metadata
            ver = importlib.metadata.version(pkg_name)
            return True, ver
        except Exception:
            return True, "installed"
    except ImportError:
        return False, "not installed"


def check_markitdown():
    return check_pip_package("markitdown", "markitdown")


def check_pypdf():
    return check_pip_package("pypdf", "pypdf")


def check_python_pptx():
    return check_pip_package("pptx", "python-pptx")


def check_soffice():
    # Try the skill's wrapper first, then system soffice
    wrapper = os.path.join(os.path.dirname(__file__), "office", "soffice.py")
    if os.path.exists(wrapper):
        ok, out = _run([sys.executable, wrapper, "--version"])
        if ok:
            return True, "available via scripts/office/soffice.py"
    if shutil.which("soffice"):
        ok, out = _run(["soffice", "--version"])
        return ok, out.strip()
    if shutil.which("libreoffice"):
        ok, out = _run(["libreoffice", "--version"])
        return ok, out.strip()
    return False, "not found"


def check_pdftoppm():
    ok, out = _run(["pdftoppm", "-v"])
    if ok or "pdftoppm" in out.lower():
        return True, out.split("\n")[0].strip()
    return False, "not found"


# ── Platform-aware install instructions ──────────────────────────────────────

def _os_type() -> str:
    s = platform.system().lower()
    if s == "darwin":
        return "macos"
    if s == "windows":
        return "windows"
    return "linux"


INSTALL_INSTRUCTIONS = {
    "python3": {
        "linux":   ["sudo apt install python3  # Ubuntu/Debian",
                    "sudo yum install python3  # CentOS/RHEL"],
        "macos":   ["brew install python3"],
        "windows": ["winget install Python.Python.3",
                    "# or download from https://www.python.org/downloads/"],
        "note":    "Python 3.9+ required",
    },
    "node": {
        "linux":   ["curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -",
                    "sudo apt install -y nodejs",
                    "# or: sudo snap install node --classic"],
        "macos":   ["brew install node",
                    "# or: nvm install --lts"],
        "windows": ["winget install OpenJS.NodeJS",
                    "# or download from https://nodejs.org/"],
        "note":    "Node.js 16+ required for pptxgenjs",
    },
    "npm": {
        "linux":   ["sudo apt install npm   # included with Node.js on most systems"],
        "macos":   ["brew install node      # npm is bundled with node"],
        "windows": ["# npm is bundled with Node.js installer"],
        "note":    "Usually installed automatically with Node.js",
    },
    "pptxgenjs": {
        "linux":   ["npm install -g pptxgenjs"],
        "macos":   ["npm install -g pptxgenjs",
                    "# If permission error: sudo npm install -g pptxgenjs"],
        "windows": ["npm install -g pptxgenjs"],
        "note":    "Required for from-scratch PPT generation",
    },
    "markitdown": {
        "linux":   ['pip install "markitdown[pptx]" --break-system-packages',
                    "# or in virtualenv: pip install 'markitdown[pptx]'"],
        "macos":   ['pip3 install "markitdown[pptx]"'],
        "windows": ['pip install "markitdown[pptx]"'],
        "note":    "Required for reading uploaded .pdf/.docx/.pptx reference files",
    },
    "pypdf": {
        "linux":   ["pip install pypdf --break-system-packages"],
        "macos":   ["pip3 install pypdf"],
        "windows": ["pip install pypdf"],
        "note":    "PDF fallback reader when markitdown fails",
    },
    "python-pptx": {
        "linux":   ["pip install python-pptx --break-system-packages"],
        "macos":   ["pip3 install python-pptx"],
        "windows": ["pip install python-pptx"],
        "note":    "Required for template-based PPT generation (from-template mode)",
    },
    "soffice": {
        "linux":   ["sudo apt install libreoffice    # Ubuntu/Debian",
                    "sudo yum install libreoffice    # CentOS/RHEL",
                    "sudo snap install libreoffice   # snap"],
        "macos":   ["brew install --cask libreoffice",
                    "# or download from https://www.libreoffice.org/download/"],
        "windows": ["winget install TheDocumentFoundation.LibreOffice",
                    "# or download from https://www.libreoffice.org/download/"],
        "note":    "Optional — needed for QA visual inspection (PDF conversion)",
    },
    "pdftoppm": {
        "linux":   ["sudo apt install poppler-utils    # Ubuntu/Debian",
                    "sudo yum install poppler-utils    # CentOS/RHEL"],
        "macos":   ["brew install poppler"],
        "windows": ["# Download poppler for Windows from:",
                    "# https://github.com/oschwartz10612/poppler-windows/releases",
                    "# Then add bin/ to PATH"],
        "note":    "Optional — needed for QA visual inspection (PDF to images)",
    },
}

# ── Check registry ────────────────────────────────────────────────────────────

CHECKS = [
    # (key, label, check_fn, critical)
    ("python3",      "Python 3.9+",    check_python3,    True),
    ("node",         "Node.js",        check_node,       True),
    ("npm",          "npm",            check_npm,        True),
    ("pptxgenjs",    "pptxgenjs",      check_pptxgenjs,  True),
    ("markitdown",   "markitdown",     check_markitdown, True),
    ("pypdf",        "pypdf",          check_pypdf,      False),
    ("python-pptx",  "python-pptx",    check_python_pptx, True),
    ("soffice",      "LibreOffice",    check_soffice,    False),
    ("pdftoppm",     "pdftoppm",       check_pdftoppm,   False),
]


# ── Runner ────────────────────────────────────────────────────────────────────

def run_checks() -> list:
    results = []
    for key, label, check_fn, critical in CHECKS:
        ok, detail = check_fn()
        results.append({
            "key":      key,
            "label":    label,
            "ok":       ok,
            "detail":   detail,
            "critical": critical,
        })
    return results


def print_report(results: list, os_type: str):
    print()
    print("═" * 58)
    print("  PPT Generator Skill — Environment Check")
    print("═" * 58)

    all_ok      = True
    missing_critical = []
    missing_optional = []

    for r in results:
        icon = "✅" if r["ok"] else ("❌" if r["critical"] else "⚠️ ")
        detail = f"  ({r['detail']})" if r["detail"] else ""
        print(f"  {icon}  {r['label']:<18}{detail}")
        if not r["ok"]:
            all_ok = False
            if r["critical"]:
                missing_critical.append(r["key"])
            else:
                missing_optional.append(r["key"])

    print("─" * 58)

    if all_ok:
        print("  ✅  All dependencies satisfied. Ready to generate PPTs!")
        print("═" * 58)
        print()
        return

    # Print install instructions for missing items
    if missing_critical:
        print(f"\n  ❌  REQUIRED — skill will not work without these:\n")
        for key in missing_critical:
            _print_install(key, os_type)

    if missing_optional:
        print(f"\n  ⚠️   OPTIONAL — QA features will be unavailable:\n")
        for key in missing_optional:
            _print_install(key, os_type)

    print("═" * 58)
    print()


def _print_install(key: str, os_type: str):
    info = INSTALL_INSTRUCTIONS.get(key, {})
    note = info.get("note", "")
    cmds = info.get(os_type, info.get("linux", []))

    label_map = {r[0]: r[1] for r in CHECKS}
    label = label_map.get(key, key)

    print(f"  ▸ {label}" + (f"  — {note}" if note else ""))
    for cmd in cmds:
        if cmd.startswith("#"):
            print(f"      {cmd}")
        else:
            print(f"      $ {cmd}")
    print()


def auto_fix(results: list):
    """Attempt to pip-install missing Python packages."""
    pip_keys = {"markitdown", "pypdf", "python-pptx"}
    pip_pkg_map = {
        "markitdown":  "markitdown[pptx]",
        "pypdf":       "pypdf",
        "python-pptx": "python-pptx",
    }

    to_install = [
        pip_pkg_map[r["key"]]
        for r in results
        if not r["ok"] and r["key"] in pip_keys
    ]

    if not to_install:
        print("  Nothing to auto-install (only pip packages can be auto-fixed).")
        return

    print(f"\n  Installing: {', '.join(to_install)} ...\n")
    cmd = [sys.executable, "-m", "pip", "install"] + to_install + ["--break-system-packages"]
    result = subprocess.run(cmd)
    if result.returncode == 0:
        print("\n  ✅  Installation complete. Re-run check_env.py to verify.")
    else:
        print("\n  ❌  Installation failed. Try running manually:")
        print(f"      $ pip install {' '.join(to_install)} --break-system-packages")


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Check ppt-generator skill dependencies")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of formatted report")
    parser.add_argument("--fix",  action="store_true", help="Auto-install missing Python pip packages")
    args = parser.parse_args()

    os_type = _os_type()
    results = run_checks()
    all_ok  = all(r["ok"] for r in results if r["critical"])

    if args.json:
        print(json.dumps({
            "os":       os_type,
            "all_ok":   all_ok,
            "results":  results,
        }, indent=2))
    else:
        print_report(results, os_type)
        if args.fix:
            auto_fix(results)

    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
