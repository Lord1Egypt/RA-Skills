#!/usr/bin/env python3
"""Demo: AI Memory Protocol v1.2.0 - Run with stdlib + sqlite3 only."""

import sys
import os
import tempfile
import importlib
import time

# Load the actual protocol
sys.path.insert(0, os.path.dirname(__file__))
from importlib.util import spec_from_file_location, module_from_spec
spec = spec_from_file_location("protocol", "ai_memory_protocol_v1.2.1.py")
mod = module_from_spec(spec)
spec.loader.exec_module(mod)

DB_PATH = tempfile.mktemp(suffix=".db")
SessionManager = mod.SessionManager


def test_basic_search():
    """TEST 1: add turns + search_count"""
    sm = SessionManager(DB_PATH)
    sm.start_conversation()
    sm.add_turn("user", "I love finance and glass bottles")
    sm.add_turn("assistant", "Interesting hobby")
    sm.end_conversation()          # v1.1.6: flushes buffer to DB
    time.sleep(0.05)
    c1 = sm.search_count("finance")
    c2 = sm.search_count("glass")
    ok = c1 == 1 and c2 == 1
    print(f"  [1] search_count finance={c1} glass={c2}  {'PASS' if ok else 'FAIL'}")
    return ok


def test_session_extended():
    """TEST 2: get_session_extended returns full turns"""
    sm = SessionManager(DB_PATH)
    sid = sm.start_conversation()
    sm.add_turn("user", "Hello world")
    sm.add_turn("assistant", "Hi there")
    sm.end_conversation()          # v1.1.6: flushes buffer to DB
    time.sleep(0.05)
    s = sm.get_session_extended(sid)
    ok = s.get("total_turns") == 2
    print(f"  [2] total_turns={s.get('total_turns')}  {'PASS' if ok else 'FAIL'}")
    return ok


def test_priority_persist():
    """TEST 3: priority_levels survive restart"""
    sm = SessionManager(DB_PATH)
    sm.add_priority_level("critical", 999)
    sm2 = SessionManager(DB_PATH)
    levels = sm2.get_priority_levels()
    ok = "critical" in levels
    print(f"  [3] priority_levels persist: {list(levels.keys())}  {'PASS' if ok else 'FAIL'}")
    return ok


def test_merge_duplicate():
    """TEST 4: merge_sessions duplicate strategy"""
    sm = SessionManager(DB_PATH)
    sid1 = sm.start_conversation()
    sid2 = sm.start_conversation()
    sm.add_turn("user", "msg A")
    sm.add_turn("user", "msg B")
    sm.end_conversation()          # v1.1.6: flushes buffer to DB
    time.sleep(0.05)
    sm.merge_sessions(sid2, sid1, conflict_strategy="duplicate")
    s = sm.get_session_extended(sid1)
    ok = s.get("total_turns", 0) >= 2
    print(f"  [4] merge duplicate total_turns={s.get('total_turns')}  {'PASS' if ok else 'FAIL'}")
    return ok


def test_heartbeat():
    """TEST 5: heartbeat() flushes buffer to DB"""
    sm = SessionManager(DB_PATH)
    sm.start_conversation()
    sm.add_turn("user", "heartbeat test message")
    sm.add_turn("assistant", "heartbeat reply")
    # heartbeat should flush the buffer
    sm.heartbeat()
    time.sleep(0.05)
    c = sm.search_count("heartbeat")
    ok = c == 2
    print(f"  [5] heartbeat flush count={c}  {'PASS' if ok else 'FAIL'}")
    sm.end_conversation()
    return ok


def main():
    print("=== AI Memory Protocol v1.2.0 Demo ===\n")

    results = [
        test_basic_search(),
        test_session_extended(),
        test_priority_persist(),
        test_merge_duplicate(),
        test_heartbeat(),
    ]

    print(f"\nDatabase: {DB_PATH}")
    print(f"Demo complete! ({sum(results)}/{len(results)}) PASS)")

    # Cleanup
    if os.path.exists(DB_PATH):
        os.unlink(DB_PATH)

    sys.exit(0 if all(results) else 1)


if __name__ == "__main__":
    main()
