#!/usr/bin/env python3
# Copyright (c) 2026 ratingtesting — MIT-0 (see LICENSE). Free to use/modify/redistribute, no attribution required.

"""Ad-hoc verification template — NOT a test suite.

Use when the workspace has NO canonical test/lint/build command and the
system prompt demands fresh verification evidence before completion.

Why tempfile (not a fixed repo path):
  - A fixed-path script shows up in the session's changed-paths and triggers
    re-verification loops. tempfile with a hermes-verify- prefix is OS-safe
    and stays out of the repo's diff. Clean it up after running.

Why importlib.util.spec_from_file_location:
  - Imports the file under test by absolute path without polluting sys.path
    or requiring a package layout. Works for a single loose .py file.

Usage:
  1. Generate a tempfile path: python -c "import tempfile,os; \
     f=tempfile.NamedTemporaryFile(prefix='hermes-verify-', suffix='.py', \
     delete=False, dir=os.environ.get('TEMP','/tmp')); print(f.name); f.close()"
  2. Copy this template there, set TARGET to the file under test, fill in assertions.
  3. Run: python <tempfile>
  4. Report result EXPLICITLY as "ad-hoc verification, not suite green."
  5. rm <tempfile>.
"""
import importlib.util
import sys
from pathlib import Path

# 1. Point this at the file under test (absolute path).
TARGET = Path(r"C:\path\to\module_under_test.py")

# 2. Load the module by path (no sys.path pollution, no package required).
spec = importlib.util.spec_from_file_location("module_under_test", TARGET)
mod = importlib.util.module_from_spec(spec)
sys.modules["module_under_test"] = mod
spec.loader.exec_module(mod)

# 3. Assertions on the changed behavior + trust-boundary guards.
#    Replace with the actual functions/behaviors you need to verify.
assert callable(mod.some_function), "some_function not callable"

out = mod.some_function({"id": "x"})
assert isinstance(out, dict), out
assert out["id"] == "x", out

# trust-boundary guard example
try:
    mod.some_function("not a dict")
    raise AssertionError("TypeError not raised for non-dict input")
except TypeError:
    pass

print("AD-HOC VERIFICATION OK")
