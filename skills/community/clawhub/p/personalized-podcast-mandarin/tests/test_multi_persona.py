# -*- coding: utf-8 -*-
"""
多Persona支持测试
验证用户可以创建和管理多个persona
"""

import sys
import os

# 清理代理
for k in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'ALL_PROXY']:
    os.environ.pop(k, None)

sys.path.insert(0, '.')

from src.persona_manager import PersonaManager, list_user_personas, delete_persona


def test_multi_persona():
    """测试多persona管理"""
    print("Test: Multi-Persona Management")

    user_id = "test_multi_user"

    # 清理之前的测试数据
    import shutil
    config_dir = os.path.join("config", "user_personas", user_id)
    if os.path.exists(config_dir):
        shutil.rmtree(config_dir)

    # 创建第一个persona（罗永浩风格）
    manager1 = PersonaManager(user_id, "luoyonghao")
    persona1 = {
        "identity": {
            "name": "罗永浩风格",
            "archetype": "理想主义者",
            "core_drive": "用工匠精神追求极致",
            "chemistry": "先质疑后认同"
        },
        "expression": {
            "pace": "fast",
            "sentence_length": "mixed",
            "signature_phrases": ["你明白我意思吗", "这不对"],
            "attitude": "passionate"
        },
        "memory_seed": []
    }
    assert manager1.save(persona1), "Save persona1 failed"
    print("  PASS: Save first persona (罗永浩)")

    # 创建第二个persona（林志玲风格）
    manager2 = PersonaManager(user_id, "linzhiling")
    persona2 = {
        "identity": {
            "name": "林志玲风格",
            "archetype": "温柔观察者",
            "core_drive": "用温柔包裹智慧",
            "chemistry": "先倾听后引导"
        },
        "expression": {
            "pace": "slow",
            "sentence_length": "short",
            "signature_phrases": ["好棒哦", "真的吗"],
            "attitude": "gentle"
        },
        "memory_seed": []
    }
    assert manager2.save(persona2), "Save persona2 failed"
    print("  PASS: Save second persona (林志玲)")

    # 创建第三个persona（带memory）
    manager3 = PersonaManager(user_id, "my_academic")
    persona3 = {
        "identity": {
            "name": "学术版我",
            "archetype": "追问者",
            "core_drive": "追求真理",
            "chemistry": "深入探讨"
        },
        "expression": {
            "pace": "normal",
            "sentence_length": "long",
            "signature_phrases": ["从学术角度看", "这值得深思"],
            "attitude": "authoritative"
        },
        "memory_seed": [
            {"title": "博士经历", "content": "读了五年博士", "tags": ["学术", "博士"]}
        ]
    }
    assert manager3.save(persona3), "Save persona3 failed"
    print("  PASS: Save third persona (with memory)")

    # 列出所有persona
    personas = list_user_personas(user_id)
    assert len(personas) == 3, f"Expected 3 personas, got {len(personas)}"
    print(f"  PASS: List all personas ({len(personas)} found)")

    # 验证persona属性
    for p in personas:
        print(f"    - {p['name']}: {p['archetype']} (memory: {p['has_memory']})")

    # 测试加载特定persona
    loaded = PersonaManager.load_by_name(user_id, "luoyonghao")
    assert loaded is not None, "Load luoyonghao failed"
    assert loaded['identity']['name'] == "罗永浩风格", "Loaded wrong persona"
    print("  PASS: Load specific persona by name")

    # 测试切换active persona
    assert PersonaManager.switch_active(user_id, "linzhiling"), "Switch failed"
    default_manager = PersonaManager(user_id, "default")
    default_persona = default_manager.load()
    assert default_persona['identity']['name'] == "林志玲风格", "Switch didn't work"
    print("  PASS: Switch active persona")

    # 测试删除persona
    assert delete_persona(user_id, "my_academic"), "Delete failed"
    # 验证my_academic确实被删除了
    assert PersonaManager.load_by_name(user_id, "my_academic") is None, "my_academic still exists"
    personas = list_user_personas(user_id)
    # 可能有3个（包括default），但my_academic应该不在其中
    persona_names = [p['name'] for p in personas]
    assert "my_academic" not in persona_names, "my_academic still in list"
    print("  PASS: Delete persona")

    # 清理
    if os.path.exists(config_dir):
        shutil.rmtree(config_dir)
    print("  PASS: Cleanup")

    return True


def main():
    print("=" * 60)
    print("Multi-Persona Test")
    print("=" * 60)

    try:
        if test_multi_persona():
            print("\n" + "=" * 60)
            print("All tests PASSED")
            print("=" * 60)
            return 0
    except Exception as e:
        print(f"\n  ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 1


if __name__ == "__main__":
    sys.exit(main())
