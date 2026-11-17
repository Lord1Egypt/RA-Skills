#!/usr/bin/env python3
"""
upload_to_pinme.py — Upload files/dirs to PinMe (IPFS) and return a short shareable URL.

USAGE:
    python3 upload_to_pinme.py <path> [--verbose] [--yes] [--timeout SEC]
    python3 upload_to_pinme.py --list [--limit N] [--raw]
    python3 upload_to_pinme.py --rm <hash>
    python3 upload_to_pinme.py --set-appkey <KEY>
    python3 upload_to_pinme.py --show-appkey
    python3 upload_to_pinme.py --wallet
    python3 upload_to_pinme.py --logout

STDOUT CONTRACT:
    The final line of stdout is always a single JSON object:
        {"success": true|false, "error_type": "...", "url": "...", ...}
    All progress / warnings / debug output goes to stderr.

ERROR TYPES:
    auth_required   - AppKey not configured (run --set-appkey)
    invalid_path    - File/dir not found or unreadable
    oversize        - File > 200MB or dir > 1GB
    cli_missing     - pinme CLI failed to install / not found
    network         - Timeout / connection error
    quota_exceeded  - PinMe quota / wallet empty
    url_not_found   - Upload OK but no shareable URL parsed
    unknown         - Fallback (raw stderr included in `error`)

EXIT CODES:
    0 - success
    1 - generic failure
    2 - structured failure (see error_type in JSON)

ENV OVERRIDES (advanced):
    PINME_APPKEY       Directly use this AppKey (highest priority, doesn't persist)
    PINME_APPKEY_FILE  Override AppKey storage path (defaults to XDG_DATA_HOME/pinme-share/appkey.json)

REQUIREMENTS:
    Node.js >= 16.13.0, pinme CLI (auto-installed), PinMe AppKey.
"""

import sys
import os
import json
import subprocess
import re
import argparse
from pathlib import Path


# ──────────────────────────────────────────────────────────────────
# Paths / constants
# ──────────────────────────────────────────────────────────────────
def _default_appkey_path() -> Path:
    """Resolve AppKey storage path.

    Priority:
      1. $PINME_APPKEY_FILE (explicit override)
      2. $XDG_DATA_HOME/pinme-share/appkey.json
      3. ~/.local/share/pinme-share/appkey.json
    """
    env_override = os.environ.get("PINME_APPKEY_FILE")
    if env_override:
        return Path(os.path.expanduser(env_override))
    xdg = os.environ.get("XDG_DATA_HOME")
    if xdg:
        base = Path(os.path.expanduser(xdg))
    else:
        base = Path(os.path.expanduser("~/.local/share"))
    return base / "pinme-share" / "appkey.json"


APPKEY_FILE = _default_appkey_path()
NPM_GLOBAL_BIN = os.path.expanduser("~/.npm-global/bin")

MAX_FILE_SIZE = 200 * 1024 * 1024          # 200MB
MAX_DIR_SIZE = 1024 * 1024 * 1024          # 1GB
DEFAULT_UPLOAD_TIMEOUT = 180
MAX_UPLOAD_TIMEOUT = 1800

URL_DOMAINS_WHITELIST = (
    "pinit.eth.limo",
    "pinme.eth.limo",
    "ipfs.io",
    "dweb.link",
)


# ──────────────────────────────────────────────────────────────────
# Output helpers
# ──────────────────────────────────────────────────────────────────
def stderr(msg: str):
    print(msg, file=sys.stderr, flush=True)


def emit(obj: dict, exit_code: int = 0):
    """Print final JSON to stdout and exit."""
    print(json.dumps(obj, ensure_ascii=False))
    sys.exit(exit_code)


def emit_error(error_type: str, message: str, **extra):
    obj = {"success": False, "error_type": error_type, "error": message, **extra}
    emit(obj, exit_code=2)


# ──────────────────────────────────────────────────────────────────
# Environment / PATH
# ──────────────────────────────────────────────────────────────────
def env_with_npm_bin() -> dict:
    """Subprocess env with ~/.npm-global/bin prepended to PATH."""
    env = os.environ.copy()
    cur_path = env.get("PATH", "")
    if NPM_GLOBAL_BIN not in cur_path.split(os.pathsep):
        env["PATH"] = f"{NPM_GLOBAL_BIN}{os.pathsep}{cur_path}"
    return env


def check_node_version():
    try:
        result = subprocess.run(
            ["node", "--version"],
            capture_output=True, text=True, timeout=10,
            env=env_with_npm_bin(),
        )
        major = int(result.stdout.strip().lstrip("v").split(".")[0])
        if major < 16:
            return False, f"Node.js too old (need >=16.13.0, got {result.stdout.strip()})"
        return True, None
    except FileNotFoundError:
        return False, "Node.js not found in PATH"
    except Exception as e:
        return False, f"Node.js check failed: {e}"


# ──────────────────────────────────────────────────────────────────
# pinme CLI install & invoke
# ──────────────────────────────────────────────────────────────────
def find_pinme():
    env = env_with_npm_bin()
    try:
        r = subprocess.run(["which", "pinme"], capture_output=True, text=True, env=env, timeout=10)
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
    except Exception:
        pass
    for path in [
        os.path.join(NPM_GLOBAL_BIN, "pinme"),
        "/usr/local/bin/pinme",
        "/usr/bin/pinme",
    ]:
        if os.path.isfile(path):
            return path
    return None


def ensure_pinme():
    if find_pinme():
        return True, None
    stderr("ℹ️  pinme CLI not found, installing via npm...")
    npm_global = os.path.expanduser("~/.npm-global")
    try:
        r = subprocess.run(
            ["npm", "install", "-g", "pinme", "--prefix", npm_global],
            capture_output=True, text=True, timeout=180,
        )
    except Exception as e:
        return False, f"npm install failed: {e}"
    if r.returncode != 0:
        try:
            r2 = subprocess.run(
                ["npm", "install", "-g", "pinme"],
                capture_output=True, text=True, timeout=180,
            )
        except Exception as e:
            return False, (r.stderr or "") + f"\nfallback npm install failed: {e}"
        if r2.returncode != 0:
            return False, (r.stderr or "") + "\n" + (r2.stderr or "")
    return find_pinme() is not None, None


def run_pinme(args_list, timeout=180, input_text=None):
    pinme = find_pinme()
    if not pinme:
        return None, "pinme CLI not found"
    try:
        result = subprocess.run(
            [pinme] + args_list,
            capture_output=True, text=True, timeout=timeout,
            env=env_with_npm_bin(),
            input=input_text,
        )
        return result, None
    except subprocess.TimeoutExpired:
        return None, f"timeout after {timeout}s"
    except Exception as e:
        return None, f"subprocess error: {e}"


# ──────────────────────────────────────────────────────────────────
# AppKey management (XDG-compliant local file)
# ──────────────────────────────────────────────────────────────────
def read_appkey_file():
    """Read AppKey from XDG-standard local file."""
    if not APPKEY_FILE.exists():
        return None
    try:
        data = json.loads(APPKEY_FILE.read_text())
        key = data.get("appkey", "").strip()
        return key or None
    except Exception:
        return None


def write_appkey_file(key: str):
    """Persist AppKey to local file with 0600 perms (parent dir auto-created)."""
    APPKEY_FILE.parent.mkdir(parents=True, exist_ok=True)
    APPKEY_FILE.write_text(json.dumps({"appkey": key}, indent=2))
    try:
        os.chmod(APPKEY_FILE, 0o600)
    except Exception:
        pass


def has_pinme_appkey_configured():
    """Check if pinme CLI already has an AppKey set."""
    r, _ = run_pinme(["show-appkey"], timeout=15)
    if not r:
        return False
    out = (r.stdout or "") + (r.stderr or "")
    # CLI prints "No AppKey found" when missing
    if "No AppKey" in out or "no appkey" in out.lower():
        return False
    # Otherwise it prints a masked key
    return r.returncode == 0


def set_pinme_appkey(key: str):
    """Configure pinme CLI with given AppKey."""
    r, _ = run_pinme(["set-appkey", key], timeout=30)
    if not r:
        return False, "failed to invoke pinme"
    if r.returncode != 0:
        return False, (r.stderr or r.stdout or "set-appkey failed").strip()
    return True, None


def ensure_appkey():
    """Three-tier lookup: $PINME_APPKEY env → pinme CLI → local file → fail."""
    # Highest priority: explicit env override (doesn't persist)
    env_key = os.environ.get("PINME_APPKEY", "").strip()
    if env_key:
        if not has_pinme_appkey_configured():
            stderr("ℹ️  Using PINME_APPKEY from env to configure pinme CLI...")
            ok, err = set_pinme_appkey(env_key)
            if not ok:
                return False, f"failed to apply PINME_APPKEY env: {err}"
        return True, None

    if has_pinme_appkey_configured():
        return True, None

    file_key = read_appkey_file()
    if file_key:
        stderr(f"ℹ️  Using AppKey from {APPKEY_FILE} to configure pinme CLI...")
        ok, err = set_pinme_appkey(file_key)
        if ok:
            return True, None
        return False, f"failed to write AppKey to pinme CLI: {err}"

    return False, (
        "PinMe AppKey not configured.\n"
        "  Option 1 (recommended): run `python3 upload_to_pinme.py --set-appkey <YOUR_KEY>`\n"
        "  Option 2: register at https://pinme.eth.limo to get an AppKey, then run option 1\n"
        "  Option 3 (advanced): export PINME_APPKEY=<YOUR_KEY> for one-shot / CI use"
    )


# ──────────────────────────────────────────────────────────────────
# Size / timeout
# ──────────────────────────────────────────────────────────────────
def get_path_size(path: str) -> int:
    p = Path(path)
    if p.is_file():
        return p.stat().st_size
    total = 0
    for f in p.rglob("*"):
        if f.is_file():
            try:
                total += f.stat().st_size
            except OSError:
                pass
    return total


def check_size_limits(path: str):
    """Return (ok, err_message). err_message is None when ok."""
    p = Path(path)
    size = get_path_size(path)
    size_mb = size / (1024 * 1024)
    if p.is_file() and size > MAX_FILE_SIZE:
        return False, f"single file too large: {size_mb:.1f}MB > 200MB"
    if p.is_dir() and size > MAX_DIR_SIZE:
        return False, f"directory too large: {size_mb:.1f}MB > 1024MB"
    return True, None


def compute_upload_timeout(path: str, override: int = None) -> int:
    if override:
        return min(override, MAX_UPLOAD_TIMEOUT)
    size_mb = get_path_size(path) / (1024 * 1024)
    # 60s base + 2s/MB, floor 180s, ceiling 1800s
    t = int(max(DEFAULT_UPLOAD_TIMEOUT, 60 + size_mb * 2))
    return min(t, MAX_UPLOAD_TIMEOUT)


# ──────────────────────────────────────────────────────────────────
# URL extraction
# ──────────────────────────────────────────────────────────────────
def extract_url(output: str):
    """Extract first URL whose host is in whitelist. Prefer short *.pinit.eth.limo."""
    short = re.search(r"https://[a-zA-Z0-9\-]+\.pinit\.eth\.limo[^\s\n]*", output)
    if short:
        return short.group(0).rstrip(".,)")
    preview = re.search(r"https://pinme\.eth\.limo/#/preview/[^\s\n]+", output)
    if preview:
        return preview.group(0).rstrip(".,)")
    for domain in URL_DOMAINS_WHITELIST:
        m = re.search(rf"https://[a-zA-Z0-9.\-/]*{re.escape(domain)}[^\s\n]*", output)
        if m:
            return m.group(0).rstrip(".,)")
    return None


# ──────────────────────────────────────────────────────────────────
# Output parsers
# ──────────────────────────────────────────────────────────────────
def parse_list_output(text: str):
    """Parse `pinme list` output into structured records.

    pinme prints blocks like:
        Name: foo.html
        CID:  Qm...
        ENS URL: https://xxxx.pinit.eth.limo
        Size: 12 KB
        Date: 2026-05-21 09:30
    Be defensive: missing fields → None.
    """
    # Strip ANSI escape codes
    text = re.sub(r"\x1b\[[0-9;]*[mK]", "", text)
    records = []
    cur = {}
    for line in text.splitlines():
        line = line.strip()
        if not line:
            if cur:
                records.append(cur)
                cur = {}
            continue
        m = re.match(r"^([A-Za-z][A-Za-z ]*?):\s+(.+)$", line)
        if not m:
            continue
        key, val = m.group(1).strip().lower(), m.group(2).strip()
        if key in ("name", "filename"):
            cur["name"] = val
        elif key == "cid":
            cur["cid"] = val
        elif "url" in key:
            cur["url"] = val
        elif key == "size":
            cur["size"] = val
        elif key in ("date", "time", "uploaded"):
            cur["time"] = val
    if cur:
        records.append(cur)
    return records


def classify_error(stderr_text: str, stdout_text: str = "", default: str = "unknown") -> str:
    """Map stderr/stdout patterns to error_type."""
    blob = (stderr_text + "\n" + stdout_text).lower()
    if "please login" in blob or "no appkey" in blob or "unauthorized" in blob or "401" in blob or "403" in blob:
        return "auth_required"
    if "quota" in blob or "insufficient balance" in blob or "402" in blob or ("wallet" in blob and "empty" in blob):
        return "quota_exceeded"
    if "too large" in blob or "size limit" in blob or "413" in blob:
        return "oversize"
    network_markers = (
        "timeout", "timed out", "etimedout",
        "enotfound", "econnrefused", "econnreset", "eai_again",
        "network", "dns",
        "status code 408", "status code 502", "status code 503", "status code 504",
        "session initialization failed",
        "chunk/init failed",
        "request failed with status code 5",
    )
    if any(m in blob for m in network_markers):
        return "network"
    return default


# ──────────────────────────────────────────────────────────────────
# Warnings (privacy + quota notice)
# ──────────────────────────────────────────────────────────────────
def print_upload_warnings(skip: bool):
    if skip:
        return
    stderr("⚠️  PinMe = public IPFS: uploads are world-readable and hard to truly delete")
    stderr("⚠️  Do NOT upload: internal docs / client data / credentials / private info / unreleased material")
    stderr("💰  PinMe may charge after free quota (~500 uploads); see https://pinme.eth.limo console")


# ──────────────────────────────────────────────────────────────────
# Subcommands
# ──────────────────────────────────────────────────────────────────
def cmd_set_appkey(key: str):
    if not key or len(key) < 20:
        emit_error("invalid_appkey", f"AppKey looks too short / malformed (length {len(key)}, need >=20)")
    ok, err = ensure_pinme()
    if not ok:
        emit_error("cli_missing", f"cannot install pinme CLI: {err}")
    ok, err = set_pinme_appkey(key)
    if not ok:
        emit_error("auth_required", f"pinme set-appkey failed: {err}")
    write_appkey_file(key)
    emit({
        "success": True,
        "message": f"AppKey configured (written to pinme CLI + {APPKEY_FILE})",
        "appkey_file": str(APPKEY_FILE),
    })


def cmd_show_appkey():
    ok, err = ensure_pinme()
    if not ok:
        emit_error("cli_missing", f"pinme CLI not installed: {err}")
    r, _ = run_pinme(["show-appkey"], timeout=15)
    if not r:
        emit_error("unknown", "cannot invoke pinme show-appkey")
    output = (r.stdout or "") + (r.stderr or "")
    file_key = read_appkey_file()
    env_key = os.environ.get("PINME_APPKEY", "").strip()
    emit({
        "success": True,
        "pinme_cli": output.strip(),
        "env_override_set": bool(env_key),
        "local_file_configured": bool(file_key),
        "local_file_path": str(APPKEY_FILE),
    })


def cmd_logout():
    ok, err = ensure_pinme()
    if not ok:
        emit_error("cli_missing", f"pinme CLI not installed: {err}")
    r, _ = run_pinme(["logout"], timeout=15)
    out = ((r.stdout or "") + (r.stderr or "")).strip() if r else ""
    removed_file = False
    if APPKEY_FILE.exists():
        try:
            APPKEY_FILE.unlink()
            removed_file = True
        except Exception:
            pass
    emit({
        "success": True,
        "pinme_cli_output": out,
        "local_file_removed": removed_file,
        "local_file_path": str(APPKEY_FILE),
    })


def cmd_wallet():
    ok, err = ensure_pinme()
    if not ok:
        emit_error("cli_missing", f"pinme CLI not installed: {err}")
    ok, err = ensure_appkey()
    if not ok:
        emit_error("auth_required", err)
    r, _ = run_pinme(["wallet"], timeout=30)
    if not r or r.returncode != 0:
        out = ((r.stdout if r else "") + (r.stderr if r else "")).strip()
        emit_error("unknown", f"pinme wallet failed: {out}")
    emit({"success": True, "wallet": (r.stdout or "").strip()})


def cmd_rm(cid: str):
    ok, err = ensure_pinme()
    if not ok:
        emit_error("cli_missing", f"pinme CLI not installed: {err}")
    ok, err = ensure_appkey()
    if not ok:
        emit_error("auth_required", err)
    # `pinme rm` is interactive; feed the CID + confirmation via stdin
    r, _ = run_pinme(["rm"], timeout=60, input_text=f"{cid}\ny\n")
    out = ((r.stdout or "") + (r.stderr or "")).strip() if r else ""
    if not r or r.returncode != 0:
        et = classify_error(r.stderr if r else "", r.stdout if r else "")
        emit_error(et, f"pinme rm failed: {out}")
    emit({"success": True, "cid": cid, "output": out})


def cmd_list(limit: int, raw: bool):
    ok, err = ensure_pinme()
    if not ok:
        emit_error("cli_missing", f"pinme CLI not installed: {err}")
    ok, err = ensure_appkey()
    if not ok:
        emit_error("auth_required", err)
    r, _ = run_pinme(["list", "-l", str(limit)], timeout=30)
    if not r:
        emit_error("unknown", "cannot invoke pinme list")
    out = (r.stdout or "") + (r.stderr or "")
    if r.returncode != 0:
        et = classify_error(r.stderr or "", r.stdout or "")
        emit_error(et, out.strip())
    if raw:
        emit({"success": True, "raw": r.stdout})
    records = parse_list_output(r.stdout)
    emit({"success": True, "count": len(records), "history": records})


def cmd_upload(path: str, verbose: bool, skip_warnings: bool, timeout_override: int):
    if not os.path.exists(path):
        emit_error("invalid_path", f"path does not exist: {path}")
    if not os.access(path, os.R_OK):
        emit_error("invalid_path", f"path not readable: {path}")

    ok, err = ensure_pinme()
    if not ok:
        emit_error("cli_missing", f"cannot install pinme CLI: {err}")

    ok, err = ensure_appkey()
    if not ok:
        emit_error("auth_required", err)

    ok, err = check_size_limits(path)
    if not ok:
        emit_error("oversize", err)

    print_upload_warnings(skip_warnings)

    timeout = compute_upload_timeout(path, timeout_override)
    stderr(f"ℹ️  Uploading {path} (timeout={timeout}s)...")

    # pinme v2 CLI does not accept --verbose on `upload`; map to local logging only
    upload_args = ["upload", path]
    if verbose:
        stderr(f"[verbose] cmd: pinme {' '.join(upload_args)}")

    result, err = run_pinme(upload_args, timeout=timeout)
    if err == f"timeout after {timeout}s":
        emit_error("network", f"upload timed out after {timeout}s; file may be too large or network unstable")
    if not result:
        emit_error("unknown", err or "unknown error")

    output = (result.stdout or "") + (result.stderr or "")
    if result.returncode != 0:
        et = classify_error(result.stderr or "", result.stdout or "")
        emit_error(et, output.strip())

    url = extract_url(output)
    if not url:
        emit_error("url_not_found", f"upload OK but no URL parsed\n{output}")

    # Try to upgrade preview URL → short ENS URL via list
    short_url = url
    if "pinit.eth.limo" not in url:
        list_result, _ = run_pinme(["list", "-l", "1"], timeout=15)
        if list_result and list_result.returncode == 0:
            ens = re.search(
                r"ENS URL:\s*(https://[a-zA-Z0-9\-]+\.pinit\.eth\.limo[^\s\n]*)",
                list_result.stdout,
            )
            if ens:
                short_url = ens.group(1).strip()

    emit({
        "success": True,
        "url": short_url,
        "preview_url": url if url != short_url else None,
        "size_bytes": get_path_size(path),
        "timeout_used": timeout,
    })


# ──────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Upload to PinMe / manage AppKey / list / rm",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("path", nargs="?", help="File or directory to upload")
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--yes", "-y", action="store_true", help="Skip privacy warnings")
    parser.add_argument("--timeout", type=int, help="Upload timeout in seconds")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--raw", action="store_true", help="Return raw output for --list")
    parser.add_argument("--rm", metavar="CID", help="Remove a pinned file by CID")
    parser.add_argument("--set-appkey", metavar="KEY", dest="set_appkey",
                        help="Configure PinMe AppKey (persists to pinme CLI + local file)")
    parser.add_argument("--show-appkey", action="store_true", dest="show_appkey")
    parser.add_argument("--wallet", action="store_true", help="Show PinMe wallet balance")
    parser.add_argument("--logout", action="store_true")
    args = parser.parse_args()

    ok, err = check_node_version()
    if not ok:
        emit_error("cli_missing", err)

    # Mutual-exclusion guard: exactly one action at a time.
    # Without this, `path` + `--list` (etc.) would silently run only the first
    # matched branch and drop the rest — a silent-failure trap.
    action_flags = {
        "--set-appkey": bool(args.set_appkey),
        "--show-appkey": args.show_appkey,
        "--logout": args.logout,
        "--wallet": args.wallet,
        "--rm": bool(args.rm),
        "--list": args.list,
        "<path>": bool(args.path),
    }
    active = [name for name, on in action_flags.items() if on]
    if len(active) > 1:
        emit_error(
            "conflicting_args",
            f"only one operation allowed at a time, got multiple: {', '.join(active)}. "
            "Please call them separately.",
        )

    if args.set_appkey:
        cmd_set_appkey(args.set_appkey)
    if args.show_appkey:
        cmd_show_appkey()
    if args.logout:
        cmd_logout()
    if args.wallet:
        cmd_wallet()
    if args.rm:
        cmd_rm(args.rm)
    if args.list:
        cmd_list(args.limit, args.raw)
    if args.path:
        cmd_upload(args.path, args.verbose, args.yes, args.timeout)

    emit_error("usage", "no operation specified. Use --help for usage.")


if __name__ == "__main__":
    main()
