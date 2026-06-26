# -*- coding: utf-8 -*-
"""
Agentic Persona 流程测试
验证：
1. setup_wizard 保存双人 persona 时同步生成 default.json
2. podcast_pipeline 在 default.json 缺失时能回退组合 host_a + host_b
3. _infer_persona_from_source 正则推断各类自然语言输入
"""

import sys
import os
import json
import shutil
from unittest.mock import patch

sys.path.insert(0, '.')
sys.stdout.reconfigure(encoding='utf-8')

# 清理代理
for k in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'ALL_PROXY']:
    os.environ.pop(k, None)

from src.setup_wizard import SetupWizard, save_double_persona
from src.persona_manager import PersonaManager
from src.podcast_pipeline import PodcastPipeline
from src import persona_resolver

TEST_USER = "test_agentic_flow_user"


def _cleanup_user():
    base = os.path.join("config", "user_personas", TEST_USER)
    if os.path.exists(base):
        shutil.rmtree(base)


def test_wizard_saves_default():
    print("\n[Test 1] SetupWizard 保存双人 persona 时同步生成 default.json")
    _cleanup_user()

    wizard = SetupWizard(TEST_USER)
    host_a = {
        "identity": {"name": "老炮", "archetype": "吐槽者", "core_drive": "吐槽", "chemistry": "怼"},
        "expression": {"pace": "fast", "sentence_length": "short", "signature_phrases": ["不是我杠啊"], "attitude": "skeptical"},
        "memory_seed": []
    }
    host_b = {
        "identity": {"name": "静姐", "archetype": "观察者", "core_drive": "理性", "chemistry": "引导"},
        "expression": {"pace": "slow", "sentence_length": "long", "signature_phrases": ["换个角度想"], "attitude": "curious"},
        "memory_seed": []
    }
    wizard._save_double_persona(host_a, host_b)

    # 验证 host_a / host_b / default 都存在
    assert PersonaManager(TEST_USER, "host_a").exists(), "host_a.json 应存在"
    assert PersonaManager(TEST_USER, "host_b").exists(), "host_b.json 应存在"
    assert PersonaManager(TEST_USER, "default").exists(), "default.json 应存在"

    default_data = PersonaManager(TEST_USER, "default").load()
    assert "host_a" in default_data, "default.json 应包含 host_a"
    assert "host_b" in default_data, "default.json 应包含 host_b"
    assert default_data["host_a"]["identity"]["name"] == "老炮"
    assert default_data["host_b"]["identity"]["name"] == "静姐"

    print("  PASS: default.json 已同步生成且结构正确")
    _cleanup_user()


def test_pipeline_fallback_to_host_ab():
    print("\n[Test 2] Pipeline 回退组合 host_a + host_b")
    _cleanup_user()

    # 仅保存 host_a 和 host_b，不保存 default
    pm_a = PersonaManager(TEST_USER, "host_a")
    pm_a.save({
        "identity": {"name": "A_name", "archetype": "TestA"},
        "expression": {"pace": "fast", "signature_phrases": [], "attitude": "curious"},
        "memory_seed": []
    })
    pm_b = PersonaManager(TEST_USER, "host_b")
    pm_b.save({
        "identity": {"name": "B_name", "archetype": "TestB"},
        "expression": {"pace": "slow", "signature_phrases": [], "attitude": "skeptical"},
        "memory_seed": []
    })

    pipeline = PodcastPipeline(skip_client_init=True, user_id=TEST_USER)
    persona = pipeline.default_persona
    assert "host_a" in persona, "应组合出 host_a"
    assert "host_b" in persona, "应组合出 host_b"
    assert persona["host_a"]["identity"]["name"] == "A_name"
    assert persona["host_b"]["identity"]["name"] == "B_name"
    assert pipeline.using_user_persona is True

    print("  PASS: Pipeline 正确回退组合 host_a + host_b")
    _cleanup_user()


def test_infer_persona_from_source():
    print("\n[Test 3] _infer_persona_from_source 正则推断")

    cases = [
        ("用郭德纲风格来讲量子力学", ("量子力学", "郭德纲")),
        ("像鲁豫那样讲人工智能", ("人工智能", "鲁豫")),
        ("以老炮吐槽的口吻聊聊为什么信号差", ("为什么信号差", "老炮吐槽")),
        ("让于谦风格的主持人来解读这篇文章", ("这篇文章", "于谦风格的主持人")),
        ("像郭德纲那样讲量子力学", ("量子力学", "郭德纲")),
        ("深度对谈", ("深度对谈", None)),
        ("用深度对谈风格来讲人工智能", ("人工智能", None)),  # 预定义风格应被过滤
    ]

    for source, expected in cases:
        result = PodcastPipeline._infer_persona_from_source(source)
        assert result == expected, f"输入: {source!r} 期望: {expected} 实际: {result}"
        print(f"  PASS: '{source}' -> {result}")


def test_pipeline_passes_document_text_to_resolver():
    print("\n[Test 4] PodcastPipeline._resolve_persona 正确传递 document_text")
    _cleanup_user()

    # 预置一个 default，使 resolver 在非首次下走默认分支也可
    save_double_persona(TEST_USER, {
        "identity": {"name": "DocA", "archetype": "观察者"},
        "expression": {"pace": "normal", "signature_phrases": [], "attitude": "curious"},
        "memory_seed": []
    }, {
        "identity": {"name": "DocB", "archetype": "讲故事的人"},
        "expression": {"pace": "normal", "signature_phrases": [], "attitude": "playful"},
        "memory_seed": []
    })

    pipeline = PodcastPipeline(skip_client_init=True, user_id=TEST_USER)
    calls = []
    original = persona_resolver.PersonaResolver.resolve

    def fake_resolve(self, explicit_description=None, document_text=None, preset_name=None, verbose=False):
        calls.append({"explicit_description": explicit_description, "document_text": document_text, "preset_name": preset_name})
        return persona_resolver.ResolveResult(
            persona_config={"host_a": {"identity": {"name": "MockA"}}, "host_b": {"identity": {"name": "MockB"}}},
            source="mock"
        )

    persona_resolver.PersonaResolver.resolve = fake_resolve
    try:
        result = pipeline._resolve_persona(
            persona_config=None,
            persona_description=None,
            preset=None,
            document_text="这是测试文档内容"
        )
        assert len(calls) == 1, f"期望 PersonaResolver.resolve 被调用 1 次，实际 {len(calls)}"
        assert calls[0]["document_text"] == "这是测试文档内容"
        assert result["host_a"]["identity"]["name"] == "MockA"
    finally:
        persona_resolver.PersonaResolver.resolve = original

    print("  PASS")
    _cleanup_user()


def test_cli_first_time_non_tty_exits():
    print("\n[Test 5] 非交互式 CLI 首次使用无 persona 参数时应报错")
    _cleanup_user()

    with patch("sys.stdin.isatty", return_value=False), \
         patch("src.podcast_pipeline.ensure_configured", return_value=True), \
         patch("sys.argv", ["podcast_pipeline", "量子力学", "--user-id", TEST_USER, "--skip-setup"]), \
         patch("builtins.print") as mock_print, \
         patch("sys.exit") as mock_exit:

        # 需要重新 import 以应用 patches
        from src import podcast_pipeline as pp_module
        pp_module.main()

        printed = " ".join(str(call) for call in mock_print.call_args_list)
        assert "首次使用必须指定" in printed or "--preset" in printed, f"未打印预期错误，实际输出: {printed}"

    print("  PASS")
    _cleanup_user()


def main():
    print("=" * 60)
    print("Agentic Persona Flow Test")
    print("=" * 60)

    all_pass = True
    tests = [
        test_wizard_saves_default,
        test_pipeline_fallback_to_host_ab,
        test_infer_persona_from_source,
        test_pipeline_passes_document_text_to_resolver,
        test_cli_first_time_non_tty_exits,
    ]
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
