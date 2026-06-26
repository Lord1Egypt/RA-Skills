#!/usr/bin/env python3
"""
ModelPool Repair — One-click diagnostics and fix for OpenClaw model issues.
"""

import json
import os
import shlex
import shutil
import subprocess
import sys
import time
import urllib.request
import ssl

CONFIG_PATH = os.path.expanduser("~/.openclaw/openclaw.json")
SSL_CTX = ssl.create_default_context()


def log(msg):
    print(f"  {msg}", flush=True)


def run(cmd, timeout=30):
    """Run command safely (no shell=True)."""
    try:
        if isinstance(cmd, str):
            cmd = shlex.split(cmd)
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip(), r.returncode
    except subprocess.TimeoutExpired:
        return "TIMEOUT", -1
    except Exception:
        return "", -1


def load_config():
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        log("❌ Config file not found. Run 'openclaw daemon start' first.")
        sys.exit(1)
    except json.JSONDecodeError:
        log("❌ Config file corrupted. Will attempt fix in step 3.")
        return {"models": {"providers": {}}, "agents": {"defaults": {}}}


def save_config(config):
    backup_path = CONFIG_PATH + ".bak"
    if os.path.isfile(CONFIG_PATH):
        shutil.copy2(CONFIG_PATH, backup_path)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def step1_diagnose():
    """Basic diagnostics."""
    print("\n📋 [1/7] Diagnostics...")
    issues = 0

    out, _ = run("ss -tlnp")
    if "18789" in out:
        log("✅ Gateway port 18789 listening")
    else:
        log("❌ Gateway port 18789 NOT listening")
        issues += 1

    out, _ = run("openclaw config validate")
    if "valid" in out.lower() and "invalid" not in out.lower():
        log("✅ Config file valid")
    else:
        log("❌ Config file invalid")
        issues += 1

    out, _ = run("free -m")
    try:
        for line in out.splitlines():
            if line.startswith("Mem:"):
                free_mb = int(line.split()[3])
                if free_mb < 200:
                    log(f"⚠️  Low memory: {free_mb}MB free")
                    issues += 1
                else:
                    log(f"✅ Memory OK: {free_mb}MB free")
                break
    except Exception:
        pass

    out, _ = run("df /")
    try:
        lines = out.strip().splitlines()
        if len(lines) >= 2:
            usage = int(lines[-1].split()[4].replace("%", ""))
            if usage > 90:
                log(f"⚠️  Disk usage: {usage}%")
                issues += 1
            else:
                log(f"✅ Disk OK: {usage}%")
    except Exception:
        pass

    return issues


def step2_test_apis():
    """Test all provider APIs."""
    print("\n📋 [2/7] Testing model API connectivity...")
    dead = []

    try:
        config = load_config()
    except Exception:
        log("❌ Cannot read config")
        return dead

    providers = config.get("models", {}).get("providers", {})
    for name, info in providers.items():
        base_url = info.get("baseUrl", "")
        api_key = info.get("apiKey", "")
        models = info.get("models", [])
        if not models:
            continue
        model_id = models[0].get("id", "")
        url = base_url.rstrip("/") + "/chat/completions"

        try:
            req = urllib.request.Request(url, headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }, data=json.dumps({
                "model": model_id,
                "messages": [{"role": "user", "content": "hi"}],
                "max_tokens": 5
            }).encode())
            resp = urllib.request.urlopen(req, context=SSL_CTX, timeout=15)
            r = json.loads(resp.read())
            if r.get("choices"):
                log(f"✅ {name}/{model_id}")
            else:
                log(f"⚠️  {name}/{model_id} — empty response")
                dead.append(name)
        except Exception as e:
            log(f"❌ {name}/{model_id} — {str(e)[:50]}")
            dead.append(name)

    if dead:
        log(f"\n⚠️  {len(dead)} provider(s) unavailable")
    else:
        log("\n✅ All providers OK")
    return dead


def step3_fix_config():
    """Fix config with doctor."""
    print("\n📋 [3/7] Fixing config...")
    run("openclaw doctor --fix")
    log("✅ doctor --fix executed")


def step4_clean_sessions():
    """Clean stuck sessions."""
    print("\n📋 [4/7] Cleaning stuck sessions...")
    out, _ = run("openclaw sessions cleanup")
    log(f"✅ {out.split(chr(10))[-1] if out else 'Sessions cleaned'}")


def step5_rebuild_fallback(dead_providers):
    """Rebuild fallback chain, skip dead providers."""
    print("\n📋 [5/7] Rebuilding fallback chain...")
    try:
        config = load_config()
    except Exception:
        log("❌ Cannot read config")
        return

    model_config = config.get("agents", {}).get("defaults", {}).get("model", {})
    if isinstance(model_config, str):
        model_config = {"primary": model_config, "fallbacks": []}

    primary = model_config.get("primary", "")
    fallbacks = model_config.get("fallbacks", [])
    dead_set = set(dead_providers)

    primary_provider = primary.split("/")[0] if "/" in primary else ""
    if primary_provider in dead_set:
        log(f"⚠️  Primary {primary} is dead, finding replacement...")
        new_primary = None
        new_fallbacks = []
        for fb in fallbacks:
            fb_provider = fb.split("/")[0] if "/" in fb else ""
            if fb_provider not in dead_set and new_primary is None:
                new_primary = fb
            else:
                new_fallbacks.append(fb)
        if new_primary:
            new_fallbacks.append(primary)
            model_config["primary"] = new_primary
            model_config["fallbacks"] = new_fallbacks
            log(f"✅ Switched to: {new_primary}")
        else:
            log("❌ All models dead, keeping current config")
    else:
        log(f"✅ Primary {primary} is alive")

    config["agents"]["defaults"]["model"] = model_config
    save_config(config)
    log(f"📊 Chain: {model_config['primary']} + {len(model_config.get('fallbacks', []))} fallbacks")


def step6_cleanup():
    """Clean old log files."""
    print("\n📋 [6/7] Cleaning resources...")
    log_dir = "/tmp/openclaw"
    cleaned = 0
    if os.path.isdir(log_dir):
        now = time.time()
        for f in os.listdir(log_dir):
            fp = os.path.join(log_dir, f)
            if f.endswith(".log") and os.path.isfile(fp):
                if now - os.path.getmtime(fp) > 3 * 86400:
                    os.remove(fp)
                    cleaned += 1
    log(f"✅ Cleaned {cleaned} old log file(s)")


def step7_restart():
    """Restart OpenClaw gracefully."""
    print("\n📋 [7/7] Restarting OpenClaw...")
    run("openclaw daemon stop")
    time.sleep(5)
    run("openclaw daemon start")
    time.sleep(15)

    out, _ = run("ss -tlnp")
    if "18789" in out:
        log("✅ Gateway running")
    else:
        log("❌ Gateway still down")

    out, _ = run("openclaw config validate")
    log(out.split("\n")[0] if out else "Config check done")


def main():
    print("")
    print("🔧 ModelPool Repair v1.0")
    print("=" * 40)

    out, _ = run("openclaw --version")
    log(f"{'✅ ' + out if out else '❌ OpenClaw not found'}")

    issues = step1_diagnose()
    dead = step2_test_apis()
    step3_fix_config()
    step4_clean_sessions()
    step5_rebuild_fallback(dead)
    step6_cleanup()
    step7_restart()

    print("")
    print("=" * 40)
    print("🎉 Repair complete!")
    print("=" * 40)
    print("")


if __name__ == "__main__":
    main()
