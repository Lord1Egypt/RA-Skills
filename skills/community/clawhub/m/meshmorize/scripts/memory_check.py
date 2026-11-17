#!/usr/bin/env python3
"""Memory compliance check — run ALL checks with one command.
Usage: memory_check  (or just: memcheck)
"""
import subprocess, os, json, time
from datetime import datetime

HOME = os.path.expanduser("~")
WORKSPACE = os.environ.get("OPENCLAW_WORKSPACE", os.path.join(HOME, ".openclaw", "workspace"))
FRESH = os.path.join(WORKSPACE, "memory", "fresh")
MESH = os.path.join(WORKSPACE, "memory", "mesh.json")
RAW = os.path.join(WORKSPACE, "memory", "RAW_LOG.txt")
TODAY_FILE = os.path.join(FRESH, "today.md")

checks = {"✅": 0, "⚠️": 0, "❌": 0}
results = []

def ok(msg):
    checks["✅"] += 1
    results.append(f"  ✅ {msg}")

def warn(msg):
    checks["⚠️"] += 1
    results.append(f"  ⚠️  {msg}")

def fail(msg):
    checks["❌"] += 1
    results.append(f"  ❌ {msg}")

def run(cmd, timeout=10):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except Exception as e:
        return -1, "", str(e)

results.append(f"\n🧠 Memory Compliance Check — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
results.append("━" * 50)

# 1. LOG — auto_log
results.append(f"\n{'📝 1. LOG':>30}")
rc, out, _ = run("auto_log 'memcheck' 'memory compliance check'")
if rc == 0:
    ok("auto_log wrote entry ✅")
else:
    fail(f"auto_log failed ({rc})")

# 2. BRIDGE — mem-bridge init
results.append(f"\n{'🔗 2. BRIDGE':>30}")
rc, out, _ = run("mem-bridge init")
if rc == 0:
    ok("bridge initialized ✅")
else:
    fail(f"bridge init failed: {out[:80]}")

# 3. FRESH LAYER — today.md
results.append(f"\n{'📄 3. FRESH':>30}")
if os.path.exists(TODAY_FILE):
    size = os.path.getsize(TODAY_FILE)
    mtime = datetime.fromtimestamp(os.path.getmtime(TODAY_FILE))
    age = (datetime.now() - mtime).total_seconds()
    ok(f"today.md exists ({size}b, {age/60:.0f}m old) ✅")
    with open(TODAY_FILE) as f:
        first = f.readline().strip()
        results.append(f"     {first}")
else:
    fail("today.md missing!")

# 4. FRESH ROTATION — check all 5 fresh files
results.append(f"\n{'🔄 4. ROTATION':>30}")
expected = ["today.md", "yesterday.md", "2-days-ago.md", "3-days-ago.md", "4-days-ago.md"]
present = []
missing = []
for fname in expected:
    path = os.path.join(FRESH, fname)
    if os.path.exists(path):
        present.append(fname)
    else:
        missing.append(fname)
if len(present) >= 3:
    ok(f"{len(present)}/5 fresh files present ({', '.join(present)}) ✅")
else:
    warn(f"only {len(present)}/5 fresh files")

# 5. CORE FILES
results.append(f"\n{'📁 5. CORE FILES':>30}")
core = ["AGENTS.md", "SOUL.md", "MEMORY.md", "USER.md", "TOOLS.md", "IDENTITY.md"]
all_ok = True
for f in core:
    path = os.path.join(WORKSPACE, f)
    if not os.path.exists(path):
        fail(f"{f} missing!")
        all_ok = False
if all_ok:
    ok(f"all {len(core)} core files present ✅")

# 6. MESH
results.append(f"\n{'📎 6. MESH':>30}")
if os.path.exists(MESH):
    size = os.path.getsize(MESH)
    if size > 100:
        ok(f"mesh.json exists ({size}b) ✅")
    else:
        warn(f"mesh.json too small ({size}b)")
else:
    fail("mesh.json missing!")

# 7. RAW_LOG
results.append(f"\n{'📃 7. RAW_LOG':>30}")
if os.path.exists(RAW):
    size = os.path.getsize(RAW)
    ok(f"RAW_LOG.txt exists ({size}b) ✅")
else:
    fail("RAW_LOG.txt missing!")

# 8. SECRETS
results.append(f"\n{'🔐 8. SECRETS':>30}")
secrets_dir = os.path.join(WORKSPACE, "secrets")
if os.path.isdir(secrets_dir):
    count = len([f for f in os.listdir(secrets_dir) if os.path.isfile(os.path.join(secrets_dir, f))])
    ok(f"{count} secret files present ✅")
else:
    fail("secrets/ missing!")

# 9. TOOLS PATH
results.append(f"\n{'🔧 9. TOOLS ON PATH':>30}")
tools = {"auto_log": "auto_log", "memory_search": "memory_search", "mem-bridge": "mem-bridge"}
all_found = True
for name, cmd in tools.items():
    rc, out, _ = run(f"which {cmd}")
    if rc == 0:
        ok(f"{name} → {out}")
    else:
        fail(f"{name} not on PATH!")
        all_found = False

# 10. HEARTBEAT
results.append(f"\n{'❤️  10. HEARTBEAT':>30}")
hb = os.path.join(WORKSPACE, "HEARTBEAT.md")
if os.path.exists(hb):
    ok("HEARTBEAT.md present ✅")
else:
    fail("HEARTBEAT.md missing!")

# Summary
results.append("\n" + "━" * 50)
total = sum(checks.values())
results.append(f"📊 SUMMARY:  ✅ {checks['✅']}  ⚠️  {checks['⚠️']}  ❌ {checks['❌']}  out of {total} checks")
if checks['❌'] > 0:
    results.append("⚠️  Some checks failed — investigate above.")
elif checks['⚠️'] > 0:
    results.append("👍 Mostly OK, minor warnings.")
else:
    results.append("🎯 ALL CHECKS PASSED. Memory system healthy.")

print("\n".join(results))
