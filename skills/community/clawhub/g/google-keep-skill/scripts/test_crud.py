#!/usr/bin/env python3
"""E2E Test Suite for Google Keep Skill.
Safely runs in a real environment using UUIDs to avoid colliding with user data.
"""

import subprocess
import json
import os
import sys
import uuid

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEEP_PY = os.path.join(SKILL_ROOT, "scripts", "keep.py")

UID = uuid.uuid4().hex[:6]
TEST_TITLE = f"E2E Automated Test {UID}"

def run_keep(*args):
    """Executes the CLI with the provided arguments."""
    cmd = ["uv", "run", "python", KEEP_PY] + list(args)
    return subprocess.run(cmd, capture_output=True, text=True, cwd=SKILL_ROOT)

def parse_output(stdout):
    """Parses JSON safely from stdout."""
    stdout = stdout.strip()
    start = stdout.find("{")
    end = stdout.rfind("}")
    if start != -1 and end != -1:
        try:
            return json.loads(stdout[start:end+1])
        except Exception:
            return None
    return None

def step(name):
    print(f"\n\033[94m▶\033[0m {name}...", flush=True)

def ok(msg):
    print(f"  \033[92m[OK]\033[0m {msg}", flush=True)

def fail(msg):
    print(f"  \033[91m[FAIL]\033[0m {msg}", flush=True)
    sys.exit(1)

def main():
    print(f"Starting End-to-End Test Suite. Workspace: {SKILL_ROOT}")
    
    step("1. Checking Session")
    res = run_keep("check")
    data = parse_output(res.stdout)
    if not data or not data.get("success"):
        fail("Session inactive. Run 'uv run python scripts/keep.py login' first.")
    ok("Session is active.")
    
    step(f"2. Creating test note: '{TEST_TITLE}'")
    content = "Line 1\nLine 2"
    res = run_keep("create", "--title", TEST_TITLE, "--content", content)
    data = parse_output(res.stdout)
    if not data or not data.get("success"):
        fail(f"Failed to create note. Output: {res.stderr} | {res.stdout}")
    ok("Note created successfully.")
    
    step("3. Reading created note to verify content")
    res = run_keep("read", "--title", TEST_TITLE)
    data = parse_output(res.stdout)
    if not data or not data.get("success"):
        fail(f"Failed to read note. Output: {res.stdout}")
    read_data = data.get("data", {})
    if "Line 1" not in read_data.get("content", []) and "Line 1\nLine 2" not in str(read_data.get("content")):
        fail(f"Content mismatch! Got: {read_data.get('content')}")
    ok("Note content verified correctly.")
    
    step("4. Updating note")
    res = run_keep("update", "--title", TEST_TITLE, "--content", "Updated Line 1\nUpdated Line 2")
    data = parse_output(res.stdout)
    if not data or not data.get("success"):
        fail(f"Failed to update note. Output: {res.stderr} | {res.stdout}")
    ok("Note updated successfully.")
    
    step("5. Verifying update")
    res = run_keep("read", "--title", TEST_TITLE)
    data = parse_output(res.stdout)
    if not data or not data.get("success"):
        fail("Failed to find note by its original title.")
    read_data = data.get("data", {})
    if "Updated Line 1" not in read_data.get("content", []) and "Updated Line 1\nUpdated Line 2" not in str(read_data.get("content")):
        fail(f"Updated content mismatch! Got: {read_data.get('content')}")
    ok("Update verification passed.")
    
    step("6. Deleting note")
    res = run_keep("delete", "--title", TEST_TITLE)
    data = parse_output(res.stdout)
    if not data or not data.get("success"):
        fail(f"Failed to delete note. Output: {res.stderr} | {res.stdout}")
    ok("Note sent to trash.")
    
    print("\n\033[92m✔ All E2E Tests Passed Successfully!\033[0m")

if __name__ == "__main__":
    main()
