#!/usr/bin/env python3
"""
弘脑记忆系统 - 核心模块快速测试
HongNao Memory OS - Core Modules Quick Test

测试核心功能的关键路径，运行时间 <5 分钟
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from memory_api import HongNaoMemorySystem, MemorySystemConfig
from openclaw_integration import OpenClawMemorySync, OpenClawTools
from preference_learning import UserPreferenceLearner, PreferencePatterns


def test_memory_extraction():
    """测试记忆抽取"""
    print("\n" + "=" * 60)
    print("📝 测试 1: 记忆抽取")
    print("=" * 60)
    
    config = MemorySystemConfig()
    system = HongNaoMemorySystem(config)
    
    text = "我叫唐锋，在燧弘华创担任执行总裁。我喜欢简洁的沟通风格，偏好使用 Python 开发。"
    result = system.add_memories_from_text(text, source="test")
    
    success = result['success'] and result['extracted_count'] > 0
    print(f"  抽取结果：{'✅ 通过' if success else '❌ 失败'}")
    print(f"  抽取数量：{result['extracted_count']} 条")
    
    return success


def test_memory_retrieval():
    """测试记忆检索"""
    print("\n" + "=" * 60)
    print("🔍 测试 2: 记忆检索")
    print("=" * 60)
    
    config = MemorySystemConfig()
    system = HongNaoMemorySystem(config)
    
    # 添加测试记忆
    system.add_memories_from_text("用户喜欢 Python 开发", source="test")
    system.add_memories_from_text("用户在燧弘华创工作", source="test")
    
    # 检索
    result = system.retrieve_memories("Python 编程", top_k=3)
    
    success = result['success'] and result['count'] > 0
    print(f"  检索结果：{'✅ 通过' if success else '❌ 失败'}")
    print(f"  找到记忆：{result['count']} 条")
    
    return success


def test_session_sync():
    """测试 Session 同步"""
    print("\n" + "=" * 60)
    print("🔄 测试 3: Session 同步")
    print("=" * 60)
    
    config = MemorySystemConfig()
    system = HongNaoMemorySystem(config)
    sync = OpenClawMemorySync(system)
    
    messages = [
        {"role": "user", "content": "我叫唐锋"},
        {"role": "user", "content": "我喜欢简洁的沟通"},
    ]
    
    result = sync.sync_session_to_memory(
        session_id="test_001",
        messages=messages,
        auto_extract=True
    )
    
    success = result['success'] and result['memories_extracted'] >= 0
    print(f"  同步结果：{'✅ 通过' if success else '❌ 失败'}")
    print(f"  抽取记忆：{result['memories_extracted']} 条")
    
    return success


def test_preference_learning():
    """测试偏好学习"""
    print("\n" + "=" * 60)
    print("🧠 测试 4: 偏好学习")
    print("=" * 60)
    
    # 直接测试模式识别，不依赖完整模块
    from preference_learning import PreferencePatterns
    
    test_texts = [
        "我喜欢简洁的回复风格",
        "我偏好使用 Python",
        "我讨厌冗长的会议",
    ]
    
    total_extracted = 0
    for text in test_texts:
        prefs = PreferencePatterns.extract_preferences(text)
        total_extracted += len(prefs)
        print(f"  '{text}' -> {len(prefs)} 条偏好")
    
    success = total_extracted >= 2  # 至少识别 2 条
    print(f"  识别结果：{'✅ 通过' if success else '❌ 失败'}")
    print(f"  识别偏好：{total_extracted} 条")
    
    return success


def test_user_profile():
    """测试用户画像"""
    print("\n" + "=" * 60)
    print("👤 测试 5: 用户画像")
    print("=" * 60)
    
    config = MemorySystemConfig()
    system = HongNaoMemorySystem(config)
    tools = OpenClawTools(system)
    
    # 添加一些记忆
    system.add_memory("用户喜欢 Python", "preference", ["编程"])
    system.add_memory("用户在燧弘华创工作", "fact", ["工作"])
    
    profile = tools.get_user_preference()
    
    has_data = len(profile.get('facts', [])) > 0 or len(profile.get('preferences', [])) > 0
    success = has_data
    print(f"  画像结果：{'✅ 通过' if success else '❌ 失败'}")
    print(f"  事实：{len(profile.get('facts', []))} 条")
    print(f"  偏好：{len(profile.get('preferences', []))} 条")
    
    return success


def test_persistence():
    """测试记忆持久化"""
    print("\n" + "=" * 60)
    print("💾 测试 6: 记忆持久化")
    print("=" * 60)
    
    config = MemorySystemConfig()
    system = HongNaoMemorySystem(config)
    
    # 添加记忆
    system.add_memory("测试记忆 1", "fact", ["test"])
    system.add_memory("测试记忆 2", "preference", ["test"])
    
    # 导出
    json_str = system.export_to_json()
    
    # 导入到新系统
    system2 = HongNaoMemorySystem(config)
    system2.import_from_json(json_str)
    
    stats = system2.get_stats()
    success = stats['total_memories'] >= 2
    print(f"  持久化：{'✅ 通过' if success else '❌ 失败'}")
    print(f"  恢复记忆：{stats['total_memories']} 条")
    
    return success


def main():
    """运行所有测试"""
    print("=" * 60)
    print("弘脑记忆系统 - 核心模块快速测试")
    print("=" * 60)
    print("预计运行时间：<5 分钟\n")
    
    tests = [
        ("记忆抽取", test_memory_extraction),
        ("记忆检索", test_memory_retrieval),
        ("Session 同步", test_session_sync),
        ("偏好学习", test_preference_learning),
        ("用户画像", test_user_profile),
        ("记忆持久化", test_persistence),
    ]
    
    results = {}
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except Exception as e:
            print(f"\n❌ {name} 测试异常：{e}")
            results[name] = False
    
    # 总结
    print("\n" + "=" * 60)
    print("📋 测试总结")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, result in results.items():
        status = "✅" if result else "❌"
        print(f"  {status} {name}")
    
    print(f"\n总计：{passed}/{total} 通过 ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n✅ 所有核心测试通过！系统功能正常。")
        return 0
    else:
        print(f"\n⚠️ {total - passed} 个测试失败，请检查。")
        return 1


if __name__ == "__main__":
    sys.exit(main())
