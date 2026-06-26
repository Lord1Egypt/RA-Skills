#!/usr/bin/env python3
"""
Test: ChromaDB Singleton Verification (Fix 3)
==============================================

Verifies that:
1. Multiple ChromaIntegration() calls return the same instance (id() check)
2. get_chroma() returns the same instance as ChromaIntegration.get_instance()
3. ChromaIntegration() constructor redirects to singleton (not a new instance)
4. shutdown() properly resets the singleton
5. After shutdown, a new instance is created (different id)
6. ChromaIntegrationV2 does NOT share the singleton
7. ChromaIntegrationV2 reuses the singleton's PersistentClient when available
8. Thread safety: concurrent access returns same instance

Run:
    cd ~/projects/kb-framework
    python -m tests.test_chroma_singleton
"""

import sys
import threading
from pathlib import Path

# Add project root to path
_project_root = Path(__file__).parent.parent
sys.path.insert(0, str(_project_root))
sys.path.insert(0, str(_project_root))

from kb.framework.chroma_integration import (
    ChromaIntegration,
    ChromaIntegrationV2,
    get_chroma,
)


def test_singleton_identity():
    """Multiple constructor calls return the same object."""
    ChromaIntegration.reset_instance()
    a = ChromaIntegration()
    b = ChromaIntegration()
    assert a is b, f"Expected same instance, got id(a)={id(a)} id(b)={id(b)}"
    assert id(a) == id(b), f"id mismatch: {id(a)} != {id(b)}"
    print("  ✅ Constructor calls return same instance")


def test_get_chroma_same_as_constructor():
    """get_chroma() returns same instance as ChromaIntegration()."""
    ChromaIntegration.reset_instance()
    a = ChromaIntegration()
    c = get_chroma()
    assert a is c, f"get_chroma() returned different instance: {id(a)} != {id(c)}"
    print("  ✅ get_chroma() == ChromaIntegration() singleton")


def test_get_instance_same_as_constructor():
    """get_instance() returns same instance."""
    ChromaIntegration.reset_instance()
    a = ChromaIntegration()
    d = ChromaIntegration.get_instance()
    assert a is d, f"get_instance() returned different instance"
    print("  ✅ get_instance() == ChromaIntegration() singleton")


def test_shutdown_resets():
    """After shutdown, next call creates a new instance."""
    ChromaIntegration.reset_instance()
    a = ChromaIntegration()
    id_before = id(a)
    ChromaIntegration.shutdown()
    b = ChromaIntegration()
    id_after = id(b)
    assert id_before != id_after, f"shutdown() did not reset: {id_before} == {id_after}"
    print("  ✅ shutdown() resets singleton — new instance created after")


def test_reset_instance_resets():
    """reset_instance() also resets the singleton."""
    ChromaIntegration.reset_instance()
    a = ChromaIntegration()
    id_before = id(a)
    ChromaIntegration.reset_instance()
    b = ChromaIntegration()
    id_after = id(b)
    assert id_before != id_after, "reset_instance() did not reset"
    print("  ✅ reset_instance() resets singleton")


def test_v2_not_singleton():
    """ChromaIntegrationV2 is NOT a singleton — each call creates new instance."""
    ChromaIntegration.reset_instance()
    v2_a = ChromaIntegrationV2()
    v2_b = ChromaIntegrationV2()
    assert v2_a is not v2_b, f"V2 instances should differ, got same id={id(v2_a)}"
    print("  ✅ ChromaIntegrationV2 is non-singleton (different instances)")


def test_v2_different_from_v1():
    """V2 instance is NOT the same as the V1 singleton."""
    ChromaIntegration.reset_instance()
    v1 = ChromaIntegration()
    v2 = ChromaIntegrationV2()
    assert v1 is not v2, "V1 and V2 should be different objects"
    print("  ✅ V2 instance ≠ V1 singleton")


def test_thread_safety():
    """Concurrent thread access returns same singleton."""
    ChromaIntegration.reset_instance()
    results = []
    errors = []

    def create_instance():
        try:
            inst = ChromaIntegration()
            results.append(id(inst))
        except Exception as e:
            errors.append(e)

    threads = [threading.Thread(target=create_instance) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert not errors, f"Thread errors: {errors}"
    assert len(set(results)) == 1, f"Got multiple instance ids: {set(results)}"
    print("  ✅ Thread-safe: 10 concurrent calls → 1 unique instance")


def test_single_persistent_client():
    """All code paths share one PersistentClient (no duplicate connections)."""
    ChromaIntegration.reset_instance()
    a = get_chroma()
    # Access the client to trigger lazy init
    _ = a.client
    # Create another reference
    b = ChromaIntegration()
    _ = b.client
    assert a._client is b._client, "PersistentClient should be shared"
    print("  ✅ Single PersistentClient across all references")


def main():
    print("=" * 60)
    print("ChromaDB Singleton Verification (Fix 3)")
    print("=" * 60)

    # Clean up before starting
    ChromaIntegration.reset_instance()

    tests = [
        ("Singleton Identity", test_singleton_identity),
        ("get_chroma() ≡ Constructor", test_get_chroma_same_as_constructor),
        ("get_instance() ≡ Constructor", test_get_instance_same_as_constructor),
        ("shutdown() Resets", test_shutdown_resets),
        ("reset_instance() Resets", test_reset_instance_resets),
        ("V2 Non-Singleton", test_v2_not_singleton),
        ("V2 ≠ V1", test_v2_different_from_v1),
        ("Thread Safety", test_thread_safety),
        ("Single PersistentClient", test_single_persistent_client),
    ]

    passed = 0
    failed = 0

    for name, test_fn in tests:
        print(f"\n[{name}]")
        try:
            test_fn()
            passed += 1
        except AssertionError as e:
            print(f"  ❌ FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"  ❌ ERROR: {e}")
            failed += 1

    # Clean up
    ChromaIntegration.shutdown()

    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())