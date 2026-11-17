#!/usr/bin/env python3
"""Dependency handling shared by every script in this skill.

Why this exists: the scripts auto-`pip install` what they need so the skill "just
works" on a fresh machine. That fails in exactly the environments a non-Claude agent
often runs in — a sandbox with no network, or a PEP 668 "externally-managed" Python
(Homebrew / Debian / many CI images) — and the failure used to surface as a raw
CalledProcessError traceback with no guidance at all.

So: try the import, try to install it, and if that doesn't work say plainly WHICH
package is missing, HOW to install it, and WHAT degrades without it. A required dep
exits 2 with that message; an optional one returns None and the caller degrades
honestly (which is the skill's rule anyway: degrade loudly, never silently).

Set LIFE_COMPANION_NO_AUTOINSTALL=1 to skip the install attempt entirely (useful in
sandboxes, and in tests).
"""
import os
import subprocess
import sys

# pkg (pip name) -> (import name, what it powers, required?)
DEPS = {
    "PyYAML":       ("yaml",         "the private profile / journal / continuity store", True),
    "lunar-python": ("lunar_python", "the BaZi 八字 engine (四柱/十神/大运)", True),
    "sxtwl":        ("sxtwl",        "the independent 立春 year-pillar cross-check", False),
    "pyswisseph":   ("swisseph",     "astro.py only — the Western natal chart 星盘 / 星座 daily (real ephemeris). BaZi, journal and career all work without it.", False),
}


def _pip_install(pkg):
    if os.environ.get("LIFE_COMPANION_NO_AUTOINSTALL"):
        return False, "auto-install disabled (LIFE_COMPANION_NO_AUTOINSTALL=1)"
    try:
        r = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--quiet", pkg],
            capture_output=True, text=True, timeout=300,
        )
    except Exception as e:  # pip missing, sandbox kill, ...
        return False, str(e)
    if r.returncode == 0:
        return True, ""
    err = (r.stderr or r.stdout or "").strip()
    if "externally-managed-environment" in err:
        err = ("this Python is externally managed (PEP 668) — install into a venv, "
               "or use `pip install --user` / `pipx` / your OS package manager")
    return False, err.splitlines()[-1] if err else f"pip exited {r.returncode}"


def ensure(pkg, import_name=None, feature=None, optional=False):
    """Import `import_name`, installing `pkg` if needed.

    Returns the module, or None when an OPTIONAL dep can't be had. A REQUIRED dep
    that can't be had exits(2) with an actionable message — never a bare traceback.
    """
    import_name = import_name or pkg
    known = DEPS.get(pkg)
    feature = feature or (known[1] if known else pkg)
    try:
        return __import__(import_name)
    except ImportError:
        pass

    ok, why = _pip_install(pkg)
    if ok:
        try:
            return __import__(import_name)
        except ImportError as e:
            why = f"installed but not importable: {e}"

    msg = (f"[life-companion] missing dependency: {pkg} (import `{import_name}`)\n"
           f"  needed for: {feature}\n"
           f"  auto-install failed: {why}\n"
           f"  fix: {sys.executable} -m pip install {pkg}\n")
    if optional:
        print(msg + "  continuing WITHOUT it — say so in the reply rather than "
                    "papering over the gap.", file=sys.stderr)
        return None
    print(msg + "  this script cannot run without it.", file=sys.stderr)
    sys.exit(2)


def report():
    """Machine- and human-readable dependency status. Never installs anything."""
    rows = []
    for pkg, (import_name, feature, required) in DEPS.items():
        try:
            __import__(import_name)
            state, detail = "ok", None
        except ImportError as e:
            state = "missing"
            detail = (f"{sys.executable} -m pip install {pkg}"
                      if required else
                      f"optional — without it: {feature} is unavailable; "
                      f"install with {sys.executable} -m pip install {pkg}")
        rows.append({"package": pkg, "import": import_name, "powers": feature,
                     "required": required, "status": state, "fix": detail})
    py_ok = sys.version_info >= (3, 9)
    return {
        "python": sys.version.split()[0],
        "python_ok": py_ok,
        "python_note": None if py_ok else "Python 3.9+ required (zoneinfo, dict ordering)",
        "executable": sys.executable,
        "dependencies": rows,
        "all_required_present": all(r["status"] == "ok" for r in rows if r["required"]) and py_ok,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(report(), ensure_ascii=False, indent=2))
