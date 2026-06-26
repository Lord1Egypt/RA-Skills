# -*- coding: utf-8 -*-
"""
Persona系统测试
测试Persona提取、管理和Memory功能
"""

import sys
sys.path.insert(0, '.')

import os
from pathlib import Path

# 清理环境变量中的代理设置
for k in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'ALL_PROXY']:
    os.environ.pop(k, None)

from src.persona_extractor import PersonaExtractor, get_preset_persona
from src.persona_manager import PersonaManager, check_first_time
from src.memory_skill import MemorySkill, quick_retrieve


def test_preset_persona():
    """测试预设Persona"""
    print("\n" + "=" * 60)
    print("测试1: 预设Persona获取")
    print("=" * 60)

    li_dan = get_preset_persona("李诞")
    if li_dan:
        print("[OK] 李诞Persona获取成功")
        print(f"  archetype: {li_dan['identity']['archetype']}")
        print(f"  signature_phrases: {li_dan['expression']['signature_phrases']}")
    else:
        print("[FAIL] 获取失败")


def test_persona_extraction():
    """测试Persona提取（需要API Key）"""
    print("\n" + "=" * 60)
    print("测试2: Persona提取")
    print("=" * 60)

    # 检查API Key
    if not os.getenv("DOUBAO_API_KEY"):
        print("跳过（需要DOUBAO_API_KEY环境变量）")
        return None

    # 示例文本
    sample_text = """
    说实话，我做这个播客不是为了当专家，就是觉得有些东西想不明白，找人聊聊。
    我2020年那次创业失败让我学到，时机比努力重要。很多人问我怎么看AI，
    我觉得吧，AI就是个杠杆，不会用的人被替代，会用的人被放大。
    说白了，技术是中性的，关键看你怎么用。
    """

    extractor = PersonaExtractor()
    persona = extractor.extract(sample_text)

    print(f"提取结果:")
    print(f"  archetype: {persona['identity']['archetype']}")
    print(f"  core_drive: {persona['identity']['core_drive'][:50]}...")
    print(f"  signature_phrases: {persona['expression']['signature_phrases']}")
    print(f"  memory_seed数量: {len(persona['memory_seed'])}")

    return persona


def test_persona_manager():
    """测试Persona管理"""
    print("\n" + "=" * 60)
    print("测试3: Persona管理")
    print("=" * 60)

    test_user_id = "test_user_001"
    manager = PersonaManager(test_user_id)

    # 检查是否存在
    exists = manager.exists()
    print(f"Persona是否存在: {exists}")

    # 创建一个测试Persona
    test_persona = {
        "identity": {
            "name": "测试用户",
            "archetype": "追问者",
            "core_drive": "测试核心驱动力",
            "chemistry": "测试互动方式"
        },
        "expression": {
            "pace": "normal",
            "sentence_length": "mixed",
            "signature_phrases": ["测试口头禅1", "测试口头禅2"],
            "attitude": "curious"
        },
        "memory_seed": [
            {"title": "测试记忆", "content": "测试内容", "tags": ["测试", "记忆"]}
        ]
    }

    # 保存
    if manager.save(test_persona):
        print("[OK] Persona保存成功")
    else:
        print("[FAIL] Persona保存失败")

    # 加载
    loaded = manager.load()
    if loaded:
        print("[OK] Persona加载成功")
        print(f"  name: {loaded['identity']['name']}")
    else:
        print("[FAIL] Persona加载失败")

    # 格式化展示
    display = manager.format_for_display(loaded)
    print(f"\n格式化展示:\n{display[:300]}...")

    # 清理
    manager.delete()
    print("\n[OK] 测试数据已清理")


def test_memory_skill():
    """测试Memory子Skill"""
    print("\n" + "=" * 60)
    print("测试4: Memory子Skill")
    print("=" * 60)

    test_user_id = "test_user_002"
    skill = MemorySkill(test_user_id)

    # 添加记忆
    skill.add(
        title="2020年创业失败",
        content="2020年做AI教育项目，获客成本过高导致失败",
        tags=["创业", "失败", "2020", "AI教育"]
    )

    skill.add(
        title="对AI的看法",
        content="AI是杠杆而非替代品，不会用的人被替代",
        tags=["AI", "观点", "工具观"]
    )

    skill.add(
        title="远程工作经验",
        content="坚持远程工作3年，认为关键是异步沟通",
        tags=["远程工作", "效率", "工作方式"]
    )

    print(f"✓ 添加了3条记忆")

    # 检索测试
    print("\n检索测试:")

    results1 = skill.retrieve("创业相关的话题", top_k=2)
    print(f"Query: '创业相关的话题' -> 找到 {len(results1)} 条")
    for r in results1:
        print(f"  - {r[:60]}...")

    results2 = skill.retrieve("AI人工智能", top_k=2)
    print(f"\nQuery: 'AI人工智能' -> 找到 {len(results2)} 条")
    for r in results2:
        print(f"  - {r[:60]}...")

    # 统计
    stats = skill.get_stats()
    print(f"\nMemory统计: {stats}")

    # 清理
    memory_file = Path(f"memory/{test_user_id}.md")
    if memory_file.exists():
        memory_file.unlink()
    print("✓ 测试数据已清理")


def test_first_time_check():
    """测试首次使用检测"""
    print("\n" + "=" * 60)
    print("测试5: 首次使用检测")
    print("=" * 60)

    # 不存在的用户
    is_first = check_first_time("non_existent_user_xyz")
    print(f"不存在用户检测: {is_first} (应为True)")

    # 创建用户后再检测
    manager = PersonaManager("test_existing_user")
    manager.save({"identity": {"name": "test"}, "expression": {}, "memory_seed": []})

    is_first = check_first_time("test_existing_user")
    print(f"存在用户检测: {is_first} (应为False)")

    # 清理
    manager.delete()
    print("✓ 测试数据已清理")


def main():
    """运行所有测试"""
    print("=" * 60)
    print("Persona系统测试套件")
    print("=" * 60)

    try:
        test_preset_persona()
    except Exception as e:
        print(f"[FAIL] 预设Persona测试失败: {e}")

    try:
        persona = test_persona_extraction()
    except Exception as e:
        print(f"[FAIL] Persona提取测试失败: {e}")

    try:
        test_persona_manager()
    except Exception as e:
        print(f"[FAIL] Persona管理测试失败: {e}")

    try:
        test_memory_skill()
    except Exception as e:
        print(f"[FAIL] Memory测试失败: {e}")

    try:
        test_first_time_check()
    except Exception as e:
        print(f"[FAIL] 首次使用检测测试失败: {e}")

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
