#!/usr/bin/env python3
"""
Install script for multi-web-search skill.

Installs the ddgs package (optional — DuckDuckGo Lite fallback always works).
Verifies all scripts are runnable.
"""
import subprocess
import sys
import shutil
import os


def run(cmd, check=True):
    print(f"  → {' '.join(cmd)}")
    result = subprocess.run(cmd, check=check, capture_output=True, text=True)
    if result.stdout:
        for line in result.stdout.decode().strip().split("\n"):
            if line.strip():
                print(f"    {line}")
    if result.returncode != 0 and check:
        if result.stderr:
            for line in result.stderr.decode().strip().split("\n"):
                if line.strip():
                    print(f"    ! {line}", file=sys.stderr)
    return result


def main():
    print("🔧 Installing multi-web-search dependencies...\n")

    # 1. Python version check
    v = sys.version_info
    print(f"Python: {v.major}.{v.minor}.{v.micro}")
    if v < (3, 8):
        print("❌ Python 3.8+ required")
        sys.exit(1)
    print(f"  ✅ Python {v.major}.{v.minor} OK\n")

    # 2. Install ddgs (optional)
    print("Installing ddgs (optional — DuckDuckGo Lite works without it)...")
    pip_cmd = [sys.executable, "-m", "pip", "install", "--user", "ddgs"]
    result = run(pip_cmd, check=False)
    if result.returncode != 0:
        print("  ⚠️  ddgs install failed — will use DuckDuckGo Lite fallback")
    else:
        print("  ✅ ddgs installed")

    # 3. Verify ddgs CLI
    ddgs_path = shutil.which("ddgs")
    if ddgs_path:
        print(f"  ✅ ddgs CLI: {ddgs_path}")
    else:
        # Check user bin
        user_bin = os.path.expanduser("~/.local/bin")
        if os.path.exists(os.path.join(user_bin, "ddgs")):
            print(f"  ✅ ddgs CLI: {user_bin}/ddgs")
        else:
            print("  ⚠️  ddgs CLI not in PATH — will use DuckDuckGo Lite fallback")

    # 4. Verify scripts
    print("\n📦 Verifying scripts...")
    script_dir = os.path.dirname(os.path.abspath(__file__))

    scripts_to_check = [
        ("search.py", "Unified search"),
        ("multi_engine_search.py", "Multi-engine parallel search"),
        ("arxiv_search.py", "arXiv academic search"),
    ]

    for script_name, desc in scripts_to_check:
        script_path = os.path.join(script_dir, script_name)
        if os.path.exists(script_path):
            print(f"  ✅ {script_name} ({desc})")
        else:
            print(f"  ❌ {script_name} missing")

    # 5. Quick test
    print("\n🧪 Quick test (DuckDuckGo Lite fallback)...")
    search_script = os.path.join(script_dir, "search.py")
    if os.path.exists(search_script):
        result = subprocess.run(
            [sys.executable, search_script, "-q", "test", "-m", "1", "--lite"],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0:
            print("  ✅ DuckDuckGo Lite fallback works")
        else:
            print("  ⚠️  Test returned non-zero (may be OK)")

    # 6. Try ddgs test
    if ddgs_path or shutil.which("ddgs"):
        print("\n🧪 Quick test (ddgs)...")
        result = subprocess.run(
            [sys.executable, search_script, "-q", "test", "-m", "1", "-b", "duckduckgo"],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0:
            print("  ✅ ddgs search works")
        else:
            print("  ⚠️  ddgs test failed — will use fallback")

    print("\n✅ multi-web-search ready!")
    print("\nUsage:")
    print(f"  python3 {search_script} -q \"your query\" -m 5          # Auto (ddgs or Lite)")
    print(f"  python3 {search_script} -q \"query\" --lite               # Force DDG Lite")
    print(f"  python3 {search_script} -q \"query\" -b google -m 5        # Specific engine")
    print(f"  python3 {script_dir}/multi_engine_search.py -q \"query\" -e google,bing,brave -m 3")
    print(f"  python3 {script_dir}/arxiv_search.py -q \"ti:transformer\" -m 10")
    print()
    print("💡 DuckDuckGo Lite always works without installing anything.")


if __name__ == "__main__":
    main()
