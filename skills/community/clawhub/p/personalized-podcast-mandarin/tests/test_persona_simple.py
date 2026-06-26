# -*- coding: utf-8 -*-
"""
Persona系统简单测试
验证核心功能是否正常
"""

import sys
import os

# 清理代理
for k in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'ALL_PROXY']:
    os.environ.pop(k, None)

sys.path.insert(0, '.')

from src.persona_extractor import get_preset_persona
from src.persona_manager import PersonaManager, check_first_time
from src.memory_skill import MemorySkill


def test_preset():
    """测试预设Persona"""
    print("Test 1: Preset Persona")
    li_dan = get_preset_persona("李诞")
    if li_dan:
        print("  PASS: Got Li Dan persona")
        print(f"    archetype: {li_dan['identity']['archetype']}")
        return True
    else:
        print("  FAIL: Could not get preset")
        return False


def test_persona_manager():
    """测试Persona管理"""
    print("\nTest 2: Persona Manager")

    test_id = "test_user_123"
    manager = PersonaManager(test_id)

    # Test save
    test_persona = {
        "identity": {
            "name": "Test User",
            "archetype": "Observer",
            "core_drive": "Test drive",
            "chemistry": "Test chemistry"
        },
        "expression": {
            "pace": "normal",
            "sentence_length": "mixed",
            "signature_phrases": ["test phrase"],
            "attitude": "curious"
        },
        "memory_seed": []
    }

    if manager.save(test_persona):
        print("  PASS: Save persona")
    else:
        print("  FAIL: Save persona")
        return False

    # Test load
    loaded = manager.load()
    if loaded and loaded['identity']['name'] == 'Test User':
        print("  PASS: Load persona")
    else:
        print("  FAIL: Load persona")
        return False

    # Cleanup
    manager.delete()
    print("  PASS: Cleanup")
    return True


def test_memory():
    """测试Memory"""
    print("\nTest 3: Memory Skill")

    test_id = "test_user_456"
    skill = MemorySkill(test_id)

    # Add memories
    skill.add("Memory 1", "Content about startup", ["startup", "business"])
    skill.add("Memory 2", "Content about AI", ["AI", "tech"])

    # Retrieve
    results = skill.retrieve("startup business", top_k=2)
    if len(results) > 0:
        print("  PASS: Memory retrieve")
    else:
        print("  FAIL: Memory retrieve")
        return False

    # Cleanup
    import pathlib
    f = pathlib.Path(f"memory/{test_id}.md")
    if f.exists():
        f.unlink()
    print("  PASS: Cleanup")
    return True


def test_first_time():
    """测试首次使用检测"""
    print("\nTest 4: First Time Check")

    # Non-existent user
    is_first = check_first_time("nonexistent_xyz")
    if is_first:
        print("  PASS: Detect first time for new user")
    else:
        print("  FAIL: Should be first time")
        return False

    # Create user
    manager = PersonaManager("existing_user_abc")
    manager.save({"identity": {"name": "x"}, "expression": {}, "memory_seed": []})

    # Check again
    is_first = check_first_time("existing_user_abc")
    if not is_first:
        print("  PASS: Detect existing user")
    else:
        print("  FAIL: Should not be first time")
        return False

    # Cleanup
    manager.delete()
    print("  PASS: Cleanup")
    return True


def main():
    print("=" * 60)
    print("Persona System Simple Test")
    print("=" * 60)

    results = []

    try:
        results.append(("Preset", test_preset()))
    except Exception as e:
        print(f"  ERROR: {e}")
        results.append(("Preset", False))

    try:
        results.append(("Manager", test_persona_manager()))
    except Exception as e:
        print(f"  ERROR: {e}")
        results.append(("Manager", False))

    try:
        results.append(("Memory", test_memory()))
    except Exception as e:
        print(f"  ERROR: {e}")
        results.append(("Memory", False))

    try:
        results.append(("First Time", test_first_time()))
    except Exception as e:
        print(f"  ERROR: {e}")
        results.append(("First Time", False))

    print("\n" + "=" * 60)
    print("Summary:")
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        print(f"  {name}: {status}")

    all_passed = all(r[1] for r in results)
    print("=" * 60)

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
