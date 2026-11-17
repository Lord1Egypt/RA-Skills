#!/usr/bin/env python3
"""Regression guard: the shared model resolver (llm_resolution.py, v4.0).

Supersedes the narrower v3.6.x guard that only checked the two arbiters. The
v4.0 refactor routes EVERY caller through one module, so the contract this test
pins is the whole precedence chain, in order:

  1. explicit `*=LLM_MODEL` / `OLLAMA_MODEL` env var wins (decision #2: the
     escape hatch that saved v3.6.0/v3.6.1 stays, but visible and logged);
  2. otherwise the gateway default (`agents.defaults.model.primary`);
  3. otherwise the configured fallback (`agents.defaults.model.fallbacks[0]`);
  4. otherwise the local safety net (`qwen2.5:7b`), presence-checked.

It also pins the no-silent-failure invariant (spec v4.0 section 6): a missing
local safety model must RAISE a clear error, never let Ollama start a
synchronous multi-GB pull that would hang the run.

Every caller must resolve to a name the daemon actually serves (or a tagged
explicit override) — never an invented model name.

Usage:
    python3 hybrid-search/test_model_resolution.py
Exit 0 = all guards hold; exit 1 = at least one regression.
"""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

# (module, env var) — each module resolves its model at import time.
MODULES = [
    ("conflict_resolver", "CONFLICT_LLM_MODEL"),
    ("consolidate_advisor", "OLLAMA_MODEL"),
]

# The shared module itself, for the precedence-chain assertions.
SHARED = "llm_resolution"


def _run(module, env, code=None):
    """Import `module` in a clean subprocess and print its resolved model."""
    code = code or (
        "import sys; sys.path.insert(0, %r);"
        "import %s as m;"
        "print(getattr(m, 'LLM_MODEL', None) or getattr(m, 'OLLAMA_MODEL', ''))"
        % (HERE, module)
    )
    return subprocess.run(
        [sys.executable, "-c", code],
        env={**os.environ, **env},
        capture_output=True, text=True, timeout=60,
    )


def _served():
    import urllib.request
    try:
        with urllib.request.urlopen("http://localhost:11434/api/tags", timeout=5) as r:
            return {m.get("name", "") for m in json.loads(r.read()).get("models", [])}
    except Exception:
        return set()


def _write_config(tmpdir, model=None, fallbacks=None):
    """Write a minimal openclaw.json and return its path."""
    cfg = {"agents": {"defaults": {}}}
    if model is not None or fallbacks is not None:
        cfg["agents"]["defaults"]["model"] = {}
        if model is not None:
            cfg["agents"]["defaults"]["model"]["primary"] = model
        if fallbacks is not None:
            cfg["agents"]["defaults"]["model"]["fallbacks"] = fallbacks
    path = os.path.join(tmpdir, "openclaw.json")
    with open(path, "w") as f:
        json.dump(cfg, f)
    return path


def test_explicit_env_wins():
    failures = []
    for module, var in MODULES:
        proc = _run(module, {var: "my-explicit-model:tag"})
        got = proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else ""
        if got != "my-explicit-model:tag":
            failures.append(f"{module}: explicit {var} ignored (got {got!r})")
        else:
            print(f"  OK  {module}: explicit {var} honoured")
    return failures


def test_resolves_to_served_model():
    """No env var: the returned name must be one the daemon serves."""
    failures = []
    served = _served()
    if not served:
        print("  !  daemon unreachable — skipping served-model assertion")
        return failures
    for module, var in MODULES:
        env = {k: v for k, v in os.environ.items() if k != var}
        proc = _run(module, env)
        got = proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else ""
        if got not in served:
            failures.append(f"{module}: resolved {got!r} which the daemon does not serve")
        else:
            print(f"  OK  {module}: resolved served model {got!r}")
    return failures


def test_unreachable_daemon_still_tagged():
    """Daemon down: must return a tagged preference, never crash/blank/bare."""
    failures = []
    for module, var in MODULES:
        env = {k: v for k, v in os.environ.items() if k != var}
        env["OLLAMA_URL"] = "http://127.0.0.1:59999"  # closed port
        proc = _run(module, env)
        if proc.returncode != 0:
            failures.append(f"{module}: crashed when daemon unreachable: {proc.stderr.strip()[-160:]}")
            continue
        got = proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else ""
        if not got or ":" not in got:
            failures.append(f"{module}: returned unusable model {got!r} when daemon down")
        else:
            print(f"  OK  {module}: offline fallback {got!r}")
    return failures


# ─── v4.0: precedence chain of the shared resolver ────────────────────────────

def _explain(env, shared_code=None):
    """Run explain_resolution() in a clean subprocess, return its dict."""
    code = shared_code or (
        "import sys, json; sys.path.insert(0, %r);"
        "import llm_resolution as L;"
        "print(json.dumps(L.explain_resolution()))" % HERE
    )
    proc = subprocess.run(
        [sys.executable, "-c", code],
        env={**os.environ, **env},
        capture_output=True, text=True, timeout=60,
    )
    if proc.returncode != 0:
        return {"_error": proc.stderr.strip()[-200:]}
    try:
        return json.loads(proc.stdout.strip().splitlines()[-1])
    except Exception:
        return {"_error": proc.stdout.strip()[-200:]}


def test_gateway_primary_wins():
    """No override: source must be gateway:primary and match the config."""
    failures = []
    with tempfile.TemporaryDirectory() as td:
        cfg = _write_config(td, model="ollama/gateway-pick:cloud",
                            fallbacks=["ollama/backup-pick:cloud"])
        env = {k: v for k, v in os.environ.items()
               if k not in ("OLLAMA_MODEL", "TRACE_LLM_MODEL",
                            "CONFLICT_LLM_MODEL", "AUTO_CAPTURE_MODEL")}
        env["OPENCLAW_CONFIG"] = cfg
        info = _explain(env)
        if info.get("source") != "gateway:primary" or info.get("model") != "gateway-pick:cloud":
            failures.append(f"gateway primary not honoured: {info}")
        else:
            print(f"  OK  gateway:primary -> {info['model']}")
    return failures


def test_gateway_fallback_used_when_primary_missing():
    """Primary absent: source must be gateway:fallback."""
    failures = []
    with tempfile.TemporaryDirectory() as td:
        cfg = _write_config(td, model=None, fallbacks=["ollama/backup-pick:cloud"])
        env = {k: v for k, v in os.environ.items()
               if k not in ("OLLAMA_MODEL", "TRACE_LLM_MODEL",
                            "CONFLICT_LLM_MODEL", "AUTO_CAPTURE_MODEL")}
        env["OPENCLAW_CONFIG"] = cfg
        info = _explain(env)
        if info.get("source") != "gateway:fallback" or info.get("model") != "backup-pick:cloud":
            failures.append(f"gateway fallback not honoured: {info}")
        else:
            print(f"  OK  gateway:fallback -> {info['model']}")
    return failures


def test_local_safety_when_config_missing():
    """No config at all: must land on the local safety net, visibly."""
    failures = []
    env = {k: v for k, v in os.environ.items()
           if k not in ("OLLAMA_MODEL", "TRACE_LLM_MODEL",
                        "CONFLICT_LLM_MODEL", "AUTO_CAPTURE_MODEL")}
    env["OPENCLAW_CONFIG"] = "/tmp/does-not-exist-openclaw.json"
    info = _explain(env)
    if info.get("source") != "local_safety" or info.get("model") != "qwen2.5:7b":
        failures.append(f"local safety net not reached: {info}")
    else:
        print(f"  OK  local_safety -> {info['model']}")
    return failures


def test_explicit_beats_gateway():
    """An explicit env var must outrank the gateway config."""
    failures = []
    with tempfile.TemporaryDirectory() as td:
        cfg = _write_config(td, model="ollama/gateway-pick:cloud")
        env = {k: v for k, v in os.environ.items() if k not in ("OLLAMA_MODEL",)}
        env["OPENCLAW_CONFIG"] = cfg
        env["OLLAMA_MODEL"] = "explicit-beats-gateway:cloud"
        info = _explain(env)
        if info.get("source") != "override_env:OLLAMA_MODEL" or info.get("model") != "explicit-beats-gateway:cloud":
            failures.append(f"explicit override did not beat gateway: {info}")
        else:
            print(f"  OK  explicit beats gateway -> {info['model']}")
    return failures


def test_missing_local_safety_raises():
    """No-silent-failure (spec 6.1): a missing local safety model RAISES."""
    failures = []
    code = (
        "import sys; sys.path.insert(0, %r);"
        "import llm_resolution as L;"
        "L._served_models = lambda: frozenset();"
        "L._read_gateway_config = lambda: {};\n"
        "try:\n"
        "    L.resolve_llm_model(require_local_presence=True)\n"
        "    print('NO-RAISE')\n"
        "except RuntimeError as e:\n"
        "    print('RAISED:', str(e)[:60])\n" % HERE
    )
    proc = subprocess.run(
        [sys.executable, "-c", code],
        env={**os.environ},
        capture_output=True, text=True, timeout=60,
    )
    out = proc.stdout.strip()
    if "RAISED:" not in out:
        failures.append(f"missing local safety model did not raise: {out!r} / {proc.stderr.strip()[-160:]}")
    else:
        print(f"  OK  missing local safety raises -> {out}")
    return failures


def main():
    print("== test_model_resolution ==")
    print("[1/7] explicit env var wins")
    f1 = test_explicit_env_wins()
    print("[2/7] no env var -> a model the daemon actually serves")
    f2 = test_resolves_to_served_model()
    print("[3/7] daemon unreachable -> tagged fallback, no crash")
    f3 = test_unreachable_daemon_still_tagged()
    print("[4/7] gateway primary honoured")
    f4 = test_gateway_primary_wins()
    print("[5/7] gateway fallback used when primary missing")
    f5 = test_gateway_fallback_used_when_primary_missing()
    print("[6/7] local safety net when config missing")
    f6 = test_local_safety_when_config_missing()
    print("[7/7] explicit beats gateway; missing local safety raises")
    f7 = test_explicit_beats_gateway()
    f8 = test_missing_local_safety_raises()

    failures = f1 + f2 + f3 + f4 + f5 + f6 + f7 + f8
    if failures:
        print("\nFAILURES:")
        for f in failures:
            print("  ✗", f)
        return 1
    print("\nAll model-resolution guards hold.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
