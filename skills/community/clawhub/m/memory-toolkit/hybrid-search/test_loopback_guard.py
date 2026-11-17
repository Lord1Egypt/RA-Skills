#!/usr/bin/env python3
"""Import-time guard test: every OLLAMA URL must be loopback.

Catches the class of bug fixed in v3.0.2 (OLLAMA_GEN_URL read directly from the
environment, bypassing get_safe_ollama_url()). A non-loopback OLLAMA_* URL must
raise at import — the process must not start.

Usage:
    python3 hybrid-search/test_loopback_guard.py
Exit 0 = all guards hold; exit 1 = at least one bypass.
"""
import importlib
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# (module, env var, non-loopback value) — each must FAIL to import.
URL_GUARDS = [
    ("hybrid_search", "OLLAMA_URL", "http://evil.example.com:11434"),
    ("hybrid_search", "OLLAMA_EMBED_URL", "http://evil.example.com:11434"),
    ("conflict_resolver", "OLLAMA_URL", "http://evil.example.com:11434"),
    ("conflict_resolver", "OLLAMA_GEN_URL", "http://evil.example.com/api/generate"),
    # v4.0.1: llm_resolution.py was previously exempted from the static scan
    # (`if fn == "llm_resolution.py": continue`) while reading OLLAMA_URL
    # unguarded — a real SSRF gap. It now uses get_safe_ollama_url() like the
    # others, and is guarded here so the exemption can never come back.
    ("llm_resolution", "OLLAMA_URL", "http://evil.example.com:11434"),
]

# Every OLLAMA_* variable name that reaches a network sink in this codebase.
# A new one must be added here AND guarded; the test fails otherwise.
KNOWN_OLLAMA_VARS = {"OLLAMA_URL", "OLLAMA_EMBED_URL", "OLLAMA_GEN_URL", "OLLAMA_MODEL", "OLLAMA_API_KEY"}


def _interpreter():
    """Prefer an interpreter that has sqlite_vec, else the current one."""
    for cand in ("/tmp/v22-vec/bin/python", sys.executable):
        if cand and os.path.exists(cand) if cand.startswith("/") else True:
            try:
                r = subprocess.run([cand, "-c", "import sqlite_vec"],
                                   capture_output=True, timeout=15)
                if r.returncode == 0:
                    return cand
            except Exception:
                pass
    return sys.executable


def _run_import(module, env):
    code = (
        "import sys; sys.path.insert(0, %r); import %s"
        % (HERE, module)
    )
    proc = subprocess.run(
        [_interpreter(), "-c", code],
        env={**os.environ, **env},
        capture_output=True, text=True, timeout=30,
    )
    return proc


def test_non_loopback_refused():
    failures = []
    for module, var, value in URL_GUARDS:
        proc = _run_import(module, {var: value})
        if proc.returncode == 0:
            failures.append(f"{module}: {var}={value} imported WITHOUT error (guard bypassed)")
        else:
            print(f"  OK  {module}.{var} refused non-loopback")
    return failures


def test_loopback_accepted():
    failures = []
    for module, var, _ in URL_GUARDS:
        proc = _run_import(module, {var: "http://127.0.0.1:11434"})
        if proc.returncode != 0:
            failures.append(f"{module}: {var}=loopback REFUSED (should import): {proc.stderr.strip()[-160:]}")
        else:
            print(f"  OK  {module}.{var} accepts loopback")
    return failures


def test_no_unguarded_ollama_reads():
    """Static scan: no os.environ.get(\"OLLAMA_*\") that is a URL bypass."""
    import re
    failures = []
    for root, _dirs, files in os.walk(os.path.dirname(HERE)):
        if "__pycache__" in root:
            continue
        for fn in files:
            if not fn.endswith(".py"):
                continue
            path = os.path.join(root, fn)
            with open(path, encoding="utf-8") as fh:
                for i, line in enumerate(fh, 1):
                    code = line.split("#", 1)[0]  # ignore comments
                    m = re.search(r'os\.environ(?:\.get)?[\(\[]\s*"(OLLAMA_[A-Z_]+)"', code)
                    if not m:
                        continue
                    var = m.group(1)
                    # API keys/models are not URLs — allowed.
                    if var in ("OLLAMA_API_KEY", "OLLAMA_MODEL"):
                        continue
                    if "get_safe_ollama_url" in line:
                        continue
                    failures.append(f"{os.path.relpath(path, os.path.dirname(HERE))}:{i}: unguarded {var} read")
    return failures


def main():
    print("== test_loopback_guard ==")
    print("[1/3] non-loopback OLLAMA_* must be refused at import")
    f1 = test_non_loopback_refused()
    print("[2/3] loopback OLLAMA_* must still import")
    f2 = test_loopback_accepted()
    print("[3/3] no unguarded OLLAMA_* URL reads (static)")
    f3 = test_no_unguarded_ollama_reads()

    failures = f1 + f2 + f3
    if failures:
        print("\nFAILURES:")
        for f in failures:
            print("  ✗", f)
        return 1
    print("\nAll loopback guards hold.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
