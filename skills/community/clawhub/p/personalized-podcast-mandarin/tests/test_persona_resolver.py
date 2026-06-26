# -*- coding: utf-8 -*-
"""
PersonaResolver 测试
覆盖：首次使用、匹配、文档提取更新/创建、preset 优先级
"""

import sys
import os
import json
import shutil
from unittest import mock

sys.path.insert(0, '.')
sys.stdout.reconfigure(encoding='utf-8')

for k in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'ALL_PROXY']:
    os.environ.pop(k, None)

from src.persona_manager import PersonaManager, check_first_time
from src.persona_resolver import PersonaResolver

TEST_USER = "test_persona_resolver_user"


def _cleanup_user():
    base = os.path.join("config", "user_personas", TEST_USER)
    if os.path.exists(base):
        shutil.rmtree(base)


class FakeClient:
    """按顺序返回预定义响应的 mock LLM client"""
    def __init__(self, responses=None):
        self.responses = responses or []
        self.call_idx = 0

    def chat_completion(self, system_prompt, user_message, **kwargs):
        if self.call_idx < len(self.responses):
            resp = self.responses[self.call_idx]
            self.call_idx += 1
            return resp, 0
        # 默认：双人描述解析
        return json.dumps({
            "host_a": {
                "name": "默认A", "archetype": "观察者", "attitude": "curious",
                "voice_gender": "female", "signature_phrases": [], "pace": "normal"
            },
            "host_b": {
                "name": "默认B", "archetype": "讲故事的人", "attitude": "playful",
                "voice_gender": "male", "signature_phrases": [], "pace": "normal"
            }
        }), 0

    def chat_completion_stream(self, *args, **kwargs):
        raise NotImplementedError("Stream not used in these tests")


def test_resolve_first_time_no_input():
    print("\n[Test 1] 首次使用 + 无输入 -> is_first_time=True")
    _cleanup_user()

    resolver = PersonaResolver(TEST_USER, skip_client_init=True)
    result = resolver.resolve_first_time()
    assert result.is_first_time is True, f"期望 is_first_time=True, 实际 {result.is_first_time}"
    assert result.source == "first_time"
    print("  PASS")
    _cleanup_user()


def test_resolve_first_time_with_description():
    print("\n[Test 2] 首次使用 + description -> 新建并保存 default")
    _cleanup_user()

    resolver = PersonaResolver(TEST_USER, skip_client_init=True)
    resolver.client = FakeClient()
    result = resolver.resolve(explicit_description="郭德纲风格")
    assert result.source == "description_new", f"实际 source: {result.source}"
    assert PersonaManager(TEST_USER, "default").exists(), "default.json 应已生成"
    print("  PASS")
    _cleanup_user()


def test_resolve_existing_default_fallback():
    print("\n[Test 3] 非首次 + 无参数 -> 加载 existing_default")
    _cleanup_user()

    # 预置 default
    pm = PersonaManager(TEST_USER, "default")
    pm.save({
        "host_a": {
            "identity": {"name": "预设A", "archetype": "观察者"},
            "expression": {"pace": "normal", "signature_phrases": [], "attitude": "curious"},
            "memory_seed": []
        },
        "host_b": {
            "identity": {"name": "预设B", "archetype": "讲故事的人"},
            "expression": {"pace": "normal", "signature_phrases": [], "attitude": "playful"},
            "memory_seed": []
        }
    })

    resolver = PersonaResolver(TEST_USER, skip_client_init=True)
    result = resolver.resolve()
    assert result.source == "existing_default", f"实际 source: {result.source}"
    assert result.persona_config["host_a"]["identity"]["name"] == "预设A"
    print("  PASS")
    _cleanup_user()


def test_find_matching_persona_exact_name():
    print("\n[Test 4] 精确名称匹配 saved persona / preset")
    _cleanup_user()

    # 保存一个名为 guodegang 的 persona（单人格式）
    pm = PersonaManager(TEST_USER, "guodegang")
    pm.save({
        "identity": {"name": "郭德纲", "archetype": "吐槽者"},
        "expression": {"pace": "slow", "signature_phrases": ["说白了"], "attitude": "mournful"},
        "memory_seed": []
    })

    resolver = PersonaResolver(TEST_USER, skip_client_init=True)
    # 精确匹配 saved 名称
    match = resolver.find_matching_persona("guodegang")
    assert match is not None and match[0] == "guodegang", f"实际: {match}"

    # 精确匹配 preset 名称 "李诞"
    match2 = resolver.find_matching_persona("李诞")
    assert match2 is not None and match2[0] == "李诞", f"实际: {match2}"

    print("  PASS")
    _cleanup_user()


def test_find_matching_persona_no_match():
    print("\n[Test 5] LLM 返回 NO_MATCH -> None")
    _cleanup_user()

    pm = PersonaManager(TEST_USER, "saved_x")
    pm.save({
        "identity": {"name": "X", "archetype": "观察者"},
        "expression": {"pace": "normal", "signature_phrases": [], "attitude": "curious"},
        "memory_seed": []
    })

    resolver = PersonaResolver(TEST_USER, skip_client_init=True)
    resolver.client = FakeClient([json.dumps({"match_key": "NO_MATCH"})])
    match = resolver.find_matching_persona("完全不相关的宇航员风格")
    assert match is None, f"期望 None, 实际: {match}"
    print("  PASS")
    _cleanup_user()


def test_doc_extraction_creates_new():
    print("\n[Test 6] 文档输入 + 无匹配 -> 新建 extracted_new")
    _cleanup_user()

    extracted = {
        "identity": {"name": "张三", "archetype": "实践者", "core_drive": "", "chemistry": ""},
        "expression": {
            "pace": "normal", "sentence_length": "mixed",
            "signature_phrases": ["没问题"], "attitude": "curious"
        },
        "memory_seed": []
    }

    resolver = PersonaResolver(TEST_USER, skip_client_init=True)
    resolver.client = FakeClient([
        json.dumps(extracted),               # PersonaExtractor.extract
        json.dumps({"match_name": None})     # is_doc_persona_match
    ])

    result = resolver.resolve(document_text="这是一篇关于张三的访谈文章...")
    assert result.source == "extracted_new", f"实际 source: {result.source}"
    assert PersonaManager(TEST_USER, "张三_extracted").exists(), "应生成张三_extracted.json"
    print("  PASS")
    _cleanup_user()


def test_doc_extraction_updates_existing():
    print("\n[Test 7] 文档输入 + 匹配 -> 更新 extracted_updated（保留 voice_id）")
    _cleanup_user()

    # 先保存一个已有 persona，带 voice_id
    existing = {
        "identity": {"name": "张三", "archetype": "观察者"},
        "expression": {
            "pace": "fast", "signature_phrases": [" old"],
            "attitude": "skeptical", "voice_id": "my_custom_voice_123"
        },
        "memory_seed": [{"title": "旧记忆", "content": "旧内容", "tags": []}]
    }
    pm = PersonaManager(TEST_USER, "zhangsan_extracted")
    pm.save(existing)
    # 同时设为 default，使后续 resolver._resolve_default 能加载
    from src.setup_wizard import save_double_persona
    save_double_persona(TEST_USER, existing, {
        "identity": {"name": "搭档", "archetype": "讲故事的人"},
        "expression": {"pace": "normal", "signature_phrases": [], "attitude": "curious"},
        "memory_seed": []
    })

    extracted = {
        "identity": {"name": "张三", "archetype": "实践者", "core_drive": "新驱动力", "chemistry": "新互动"},
        "expression": {
            "pace": "normal", "sentence_length": "mixed",
            "signature_phrases": ["新口头禅"], "attitude": "curious"
        },
        "memory_seed": [{"title": "新记忆", "content": "新内容", "tags": ["新"]}]
    }

    resolver = PersonaResolver(TEST_USER, skip_client_init=True)
    resolver.client = FakeClient([
        json.dumps(extracted),                                          # PersonaExtractor.extract
        json.dumps({"match_name": "zhangsan_extracted", "confidence": "high"})  # is_doc_persona_match
    ])

    result = resolver.resolve(document_text="这是张三的最新访谈...")
    assert result.source == "extracted_updated", f"实际 source: {result.source}"
    assert result.matched_persona_name == "zhangsan_extracted"

    # 验证 voice_id 被保留
    updated = PersonaManager(TEST_USER, "zhangsan_extracted").load()
    # updated 现在可能是双人结构（因为 _merge_extracted_with_existing 返回单人，
    # 然后 pm.update(double_config) 保存了双人）
    host_a = updated.get("host_a", updated)
    assert host_a["expression"]["voice_id"] == "my_custom_voice_123", "voice_id 应被保留"

    # 验证 memory_seed 已合并（旧 + 新）
    mems = host_a.get("memory_seed", [])
    titles = [m.get("title") for m in mems]
    assert "旧记忆" in titles and "新记忆" in titles, f"memory_seed 应合并，实际: {titles}"

    print("  PASS")
    _cleanup_user()


def test_preset_priority_over_description():
    print("\n[Test 8] preset 与 description 同时传入时 preset 优先")
    _cleanup_user()

    resolver = PersonaResolver(TEST_USER, skip_client_init=True)
    resolver.client = FakeClient()
    result = resolver.resolve(explicit_description="某个描述", preset_name="李诞")
    assert result.source == "preset", f"实际 source: {result.source}"
    assert result.persona_config["host_a"]["identity"]["name"] == "李诞"
    print("  PASS")
    _cleanup_user()


def main():
    print("=" * 60)
    print("PersonaResolver Test Suite")
    print("=" * 60)

    tests = [
        test_resolve_first_time_no_input,
        test_resolve_first_time_with_description,
        test_resolve_existing_default_fallback,
        test_find_matching_persona_exact_name,
        test_find_matching_persona_no_match,
        test_doc_extraction_creates_new,
        test_doc_extraction_updates_existing,
        test_preset_priority_over_description,
    ]

    all_pass = True
    for t in tests:
        try:
            t()
        except AssertionError as e:
            print(f"  FAIL: {e}")
            all_pass = False
        except Exception as e:
            print(f"  ERROR: {e}")
            all_pass = False

    print("\n" + "=" * 60)
    print("全部通过" if all_pass else "存在失败")
    print("=" * 60)
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
