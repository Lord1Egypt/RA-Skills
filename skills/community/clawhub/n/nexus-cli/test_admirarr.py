#!/usr/bin/env python3
"""
Test suite for admirarr CLI.
Runs all commands and reports pass/fail.

Usage: python3 test_admirarr.py
"""

import subprocess
import sys
import time

ADMIRARR = "/home/max/nexus-cli/admirarr"
PASS = "\033[92mPASS\033[0m"
FAIL = "\033[91mFAIL\033[0m"
SKIP = "\033[93mSKIP\033[0m"

results = {"pass": 0, "fail": 0, "skip": 0}


def run(cmd, timeout=30):
    """Run an admirarr command and return (exit_code, stdout, stderr)."""
    args = cmd.split() if cmd else []
    try:
        result = subprocess.run(
            ["python3", ADMIRARR] + args,
            capture_output=True, text=True, timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "TIMEOUT"
    except Exception as e:
        return -1, "", str(e)


def test(name, cmd, expect_exit=0, expect_in=None, expect_not_in=None, timeout=30):
    """Run a test and print result."""
    code, stdout, stderr = run(cmd, timeout)
    output = stdout + stderr
    passed = True
    reasons = []

    if code != expect_exit:
        passed = False
        reasons.append(f"exit={code} (expected {expect_exit})")

    if expect_in:
        for text in (expect_in if isinstance(expect_in, list) else [expect_in]):
            if text not in output:
                passed = False
                reasons.append(f"missing: '{text}'")

    if expect_not_in:
        for text in (expect_not_in if isinstance(expect_not_in, list) else [expect_not_in]):
            if text in output:
                passed = False
                reasons.append(f"unexpected: '{text}'")

    status = PASS if passed else FAIL
    if passed:
        results["pass"] += 1
    else:
        results["fail"] += 1

    detail = f"  ({', '.join(reasons)})" if reasons else ""
    print(f"  {status}  {name}{detail}")
    return passed


def test_skip(name, reason):
    """Skip a test with a reason."""
    results["skip"] += 1
    print(f"  {SKIP}  {name}  ({reason})")


def main():
    start = time.time()
    print("\n\033[33m  ⚓\033[0m \033[1mADMIRARR Test Suite\033[0m\n")
    print("  " + "━" * 50)

    # ── Help & basics ──
    print("\n  \033[33mBasics\033[0m")
    test("help command", "help", expect_in=["ADMIRARR", "USAGE", "EXAMPLES"])
    test("no args shows help", "", expect_in="ADMIRARR")
    test("--help flag", "--help", expect_in="ADMIRARR")
    test("--version flag", "--version", expect_in="admirarr v")
    test("unknown command", "asdfxyz", expect_in="Unknown command")

    # ── Status & Health ──
    print("\n  \033[33mStatus & Health\033[0m")
    test("status dashboard", "status", expect_in=["Fleet Status", "Health", "Disk"])
    test("health check", "health", expect_in="Health Check")
    test("doctor diagnostics", "doctor", expect_in=["Service Connectivity", "API Keys", "Disk Space"], timeout=60)

    # ── Library commands ──
    print("\n  \033[33mLibrary\033[0m")
    test("list movies", "movies", expect_in="Radarr")
    test("list shows", "shows", expect_in="Sonarr")
    test("missing content", "missing", expect_in="Missing Content")

    # ── Download commands ──
    print("\n  \033[33mDownloads\033[0m")
    test("download queue", "queue", expect_in="Download Queues")
    test("qbittorrent downloads", "downloads", expect_in="qBittorrent")

    # ── Indexers ──
    print("\n  \033[33mIndexers\033[0m")
    test("list indexers", "indexers", expect_in="Prowlarr")

    # ── Search ──
    print("\n  \033[33mSearch\033[0m")
    test("search no query", "search", expect_in="Usage")
    test("prowlarr search", "search interstellar", expect_in="Interstellar", timeout=45)
    test("find no query", "find", expect_in="Usage")
    test("find movie releases", "find silent hill", expect_in="Return to Silent Hill", timeout=45)

    # ── Plex ──
    print("\n  \033[33mPlex\033[0m")
    test("plex scan", "scan", expect_in="Scanning")
    test("plex recent", "recent", expect_in="Recently Added")

    # ── Infrastructure ──
    print("\n  \033[33mInfrastructure\033[0m")
    test("docker status", "docker", expect_in="seerr")
    test("disk space", "disk", expect_in="Disk Space")
    test("radarr logs", "logs radarr", expect_in="Radarr")
    test("invalid log service", "logs fakeservice", expect_in="only available for")

    # ── Restart (skip destructive) ──
    print("\n  \033[33mRestart\033[0m")
    test("restart no args", "restart", expect_in="Usage")
    test("restart unknown svc", "restart fakesvc", expect_in="Unknown service")

    # ── Interactive commands (skip — require user input) ──
    print("\n  \033[33mInteractive (skipped)\033[0m")
    test_skip("add-movie", "requires interactive input")
    test_skip("add-show", "requires interactive input")

    # ── History (may fail if tautulli is down) ──
    print("\n  \033[33mOptional\033[0m")
    code, out, _ = run("history")
    if "Cannot reach" in out or "No Tautulli" in out:
        test_skip("tautulli history", "tautulli is down")
    else:
        test("tautulli history", "history", expect_in="Watch History")

    # ── Summary ──
    elapsed = time.time() - start
    print("\n  " + "━" * 50)
    total = results["pass"] + results["fail"] + results["skip"]
    print(f"\n  \033[1mResults:\033[0m {results['pass']} passed, {results['fail']} failed, {results['skip']} skipped ({total} total)")
    print(f"  \033[2mCompleted in {elapsed:.1f}s\033[0m\n")

    sys.exit(1 if results["fail"] > 0 else 0)


if __name__ == "__main__":
    main()
