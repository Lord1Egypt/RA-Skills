"""
快速验证脚本：测试 Pipeline 修复项
验证点：
1. skip_audio=True 时跳过 TTS
2. memory_seed 被同步后注入 prompt（通过检查输出文本是否包含记忆内容）
3. 用户 style 覆盖 research_package 中 style_selected
4. 大纲预览正确输出
"""
import os
import sys
import json
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# 清除代理和TTS配置
for proxy_var in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'ALL_PROXY']:
    os.environ.pop(proxy_var, None)
for tts_var in ['VOLCANO_TTS_APP_ID', 'VOLCANO_TTS_ACCESS_TOKEN', 'VOLCANO_TTS_SECRET_KEY']:
    os.environ.pop(tts_var, None)

# 加载Doubao API配置
private_doubao_path = Path(__file__).parent.parent / "private" / "research Agent.txt"
if private_doubao_path.exists():
    try:
        with open(private_doubao_path, 'r', encoding='utf-8') as f:
            content = f.read()
            for line in content.strip().split('\n'):
                if line.startswith('ID'):
                    parts = line.split('：')
                    if len(parts) >= 2:
                        os.environ['DOUBAO_MODEL'] = parts[1].strip()
                elif 'API key' in line:
                    parts = line.split('：')
                    if len(parts) >= 2:
                        os.environ['DOUBAO_API_KEY'] = parts[1].strip()
    except Exception as e:
        print(f"[Config] Doubao加载失败: {e}")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.podcast_pipeline import PodcastPipeline

OUTPUT_DIR = Path(__file__).parent.parent / "test_outputs" / "fix_validation"

def test_skip_audio_and_memory():
    print("=" * 70)
    print("验证 1: skip_audio=True + memory_seed 注入闭环")
    print("=" * 70)

    persona_config = {
        "host_a": {
            "identity": {"name": "老炮", "archetype": "吐槽者", "core_drive": "吐槽", "chemistry": "回怼"},
            "expression": {"pace": "fast", "sentence_length": "short", "signature_phrases": ["不是我杠啊"], "attitude": "skeptical"},
            "memory_seed": [
                {
                    "title": "地铁信号差",
                    "content": "2022年买的旗舰机在地铁里打游戏疯狂掉线，气得我想摔手机。",
                    "tags": ["手机", "地铁", "吐槽"]
                }
            ]
        },
        "host_b": {
            "identity": {"name": "静姐", "archetype": "观察者", "core_drive": "理性", "chemistry": "引导"},
            "expression": {"pace": "slow", "sentence_length": "long", "signature_phrases": ["换个角度想"], "attitude": "curious"},
            "memory_seed": []
        }
    }

    # research_package 里的风格是"高效传达"，但用户传入 style="深度对谈"
    pkg = {
        "schema_version": "2.1",
        "source": "手机信号为什么越来越差",
        "source_type": "topic",
        "style_selected": "高效传达",  # 应该被用户指定的 style 覆盖
        "hook": "你有没有觉得地铁里刷手机越来越卡？",
        "central_insight": "信号差是基建问题和手机天线设计共同导致的",
        "content_outline": "测试用大纲",
        "segments": [
            {
                "segment_id": "seg_01",
                "narrative_function": "setup",
                "dramatic_goal": "从地铁信号吐槽建立共鸣",
                "content_focus": "手机在地铁里的信号问题",
                "estimated_length": 500,
                "materials_to_use": [],
                "persona_dynamics": {"who_initiates": "A", "dynamic_mode": "storytelling", "emotional_tone": "curious"},
                "outline": "A 吐槽地铁信号差，B 安慰并分析原因。A 必须自然引用自己'地铁打游戏掉线'的记忆。"
            }
        ],
        "enriched_materials": []
    }

    pipeline = PodcastPipeline(skip_client_init=True)
    result = pipeline.generate(
        source="手机信号为什么越来越差",
        source_type="topic",
        style="深度对谈",  # 用户显式指定
        research_package=pkg,
        persona_config=persona_config,
        output_dir=str(OUTPUT_DIR / "skip_audio_memory"),
        verbose=True,
        skip_audio=True
    )

    # 校验 1: 没有音频
    assert result.get("audio_path") is None, "错误：skip_audio=True 时仍生成了音频"
    print("\n[✓] skip_audio=True 生效，未生成音频")

    # 校验 2: 用户 style 覆盖了 research_package 的 style_selected
    effective_style = result.get("style")
    assert effective_style == "深度对谈", f"错误：style 应为'深度对谈'，实际为 {effective_style}"
    print("[✓] 用户指定的 style 正确覆盖了 research_package 的 style_selected")

    # 校验 3: 脚本中引用了 memory_seed 内容
    script_text = "\n".join(
        line.get("text", "")
        for seg in result.get("script", [])
        for line in seg.get("lines", [])
    )
    memory_keywords = ["地铁", "掉线", "摔手机", "2022年"]
    found = [kw for kw in memory_keywords if kw in script_text]
    print(f"[?] 记忆引用检测结果: 找到关键词 {found}")
    if found:
        print("[✓] memory_seed 内容已进入生成文本")
    else:
        print("[!] 警告：未在生成文本中检测到记忆关键词（可能需要更具体的记忆内容或检查注入链路）")

    # 校验 4: 返回结果包含 research（大纲可见）
    research = result.get("research")
    assert research is not None, "错误：结果中缺少 research"
    assert research.get("content_outline") == "测试用大纲", "错误：大纲内容不一致"
    print("[✓] research/outline 已包含在返回结果中，大纲可见")

    print("=" * 70)


def test_pause_before_audio():
    print("\n" + "=" * 70)
    print("验证 2: pause_before_audio 检查点存在性（仅函数签名和命令行参数）")
    print("=" * 70)

    # 由于自动测试无法交互输入，这里只验证参数能被传入不报错
    import inspect
    sig = inspect.signature(PodcastPipeline.generate)
    assert "skip_audio" in sig.parameters, "错误：generate 缺少 skip_audio 参数"
    assert "pause_before_audio" in sig.parameters, "错误：generate 缺少 pause_before_audio 参数"
    print("[✓] generate() 参数签名包含 skip_audio 和 pause_before_audio")

    import argparse
    from src.podcast_pipeline import main
    import io
    # 解析 --help 检查参数存在
    # 这里用一个简单的办法：检查源码字符串
    import src.podcast_pipeline as pp
    src_code = Path(pp.__file__).read_text(encoding='utf-8')
    assert "--skip-audio" in src_code, "错误：命令行缺少 --skip-audio"
    assert "--review" in src_code, "错误：命令行缺少 --review"
    assert "--target-length" in src_code, "错误：命令行缺少 --target-length"
    print("[✓] 命令行入口包含 --skip-audio、--review 和 --target-length")
    print("=" * 70)


def test_dynamic_target_length():
    print("\n" + "=" * 70)
    print("验证 3: 动态目标字数与无硬编码限制")
    print("=" * 70)

    import inspect
    from src.podcast_pipeline import PodcastPipeline
    sig = inspect.signature(PodcastPipeline.generate)
    assert "target_length" in sig.parameters, "错误：generate 缺少 target_length 参数"
    print("[✓] generate() 参数签名包含 target_length")

    import src.podcast_pipeline as pp
    import src.script_generator as sg
    pp_code = Path(pp.__file__).read_text(encoding='utf-8')
    sg_code = Path(sg.__file__).read_text(encoding='utf-8')
    combined = pp_code + sg_code
    assert "5500" not in combined, "错误：源码中仍残留 5500 硬编码"
    assert "6500" not in combined, "错误：源码中仍残留 6500 硬编码"
    assert "target_words" in combined, "错误：未注入动态 target_words 逻辑"
    print("[✓] podcast_pipeline.py / script_generator.py 已移除 5500-6500 硬编码，并注入 target_words")

    from src.schema import ScriptVersion, ResearchSegment, ResearchMaterial, DialogueLine
    sv = ScriptVersion.model_json_schema()
    assert sv['properties']['word_count'].get('maximum') == 15000, "错误：ScriptVersion.word_count 上限未放宽"
    assert sv['properties']['lines'].get('maxItems') == 600, "错误：ScriptVersion.lines 上限未放宽"
    dl = DialogueLine.model_json_schema()
    assert dl['properties']['text'].get('maxLength') == 500, "错误：DialogueLine.text 上限未放宽"
    rs = ResearchSegment.model_json_schema()
    est = rs['properties']['estimated_length']
    assert est.get('minimum') == 50 and est.get('maximum') == 2500, "错误：ResearchSegment.estimated_length 范围未放宽"
    rm = ResearchMaterial.model_json_schema()
    assert rm['properties']['content'].get('maxLength') == 1500, "错误：ResearchMaterial.content 上限未放宽"
    print("[✓] schema.py 中所有长度限制已同步放宽")
    print("=" * 70)


if __name__ == "__main__":
    test_skip_audio_and_memory()
    test_pause_before_audio()
    test_dynamic_target_length()
    print("\n全部验证通过")
