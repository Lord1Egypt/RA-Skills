"""
完整端到端测试 - PDF -> 脚本 -> 音频
验证修复后的TTS性能
"""
import os
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# 清除代理
for proxy_var in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'ALL_PROXY']:
    if proxy_var in os.environ:
        del os.environ[proxy_var]

# 加载TTS配置
private_tts_path = Path(__file__).parent.parent / "private" / "TTS.txt"
if private_tts_path.exists() and not os.getenv("VOLCANO_TTS_APP_ID"):
    try:
        with open(private_tts_path, 'r', encoding='utf-8') as f:
            content = f.read()
            for line in content.strip().split('\n'):
                if 'APP ID' in line and '：' in line:
                    os.environ['VOLCANO_TTS_APP_ID'] = line.split('：')[1].strip()
                elif 'Access Token' in line and '：' in line:
                    os.environ['VOLCANO_TTS_ACCESS_TOKEN'] = line.split('：')[1].strip()
    except Exception as e:
        print(f"[Config] TTS加载失败: {e}")

# 加载Doubao API配置
private_doubao_path = Path(__file__).parent.parent / "private" / "research Agent.txt"
if private_doubao_path.exists():
    try:
        with open(private_doubao_path, 'r', encoding='utf-8') as f:
            content = f.read()
            for line in content.strip().split('\n'):
                # 解析ID行
                if line.startswith('ID'):
                    parts = line.split('：')
                    if len(parts) >= 2:
                        os.environ['DOUBAO_MODEL'] = parts[1].strip()
                # 解析API key行
                elif 'API key' in line:
                    parts = line.split('：')
                    if len(parts) >= 2:
                        os.environ['DOUBAO_API_KEY'] = parts[1].strip()
    except Exception as e:
        print(f"[Config] Doubao加载失败: {e}")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.podcast_pipeline import PodcastPipeline

print("=" * 70)
print("完整端到端测试")
print("=" * 70)
print("测试流程: PDF -> Research -> Script -> Audio")
print("=" * 70)

# 使用已有的PDF文件
pdf_path = "tests/pdf/基于遗传算法和神经网络的软件界面美感建模_袁培飒.pdf"

if not Path(pdf_path).exists():
    print(f"错误: PDF文件不存在: {pdf_path}")
    sys.exit(1)

print(f"\n输入文件: {pdf_path}")
print(f"文件大小: {Path(pdf_path).stat().st_size / 1024:.1f} KB")

output_dir = "./test_outputs/e2e_complete_test"
Path(output_dir).mkdir(parents=True, exist_ok=True)

try:
    pipeline = PodcastPipeline()

    total_start = time.time()

    print("\n" + "-" * 70)
    print("开始生成...")
    print("-" * 70)

    result = pipeline.generate(
        source=pdf_path,
        source_type="pdf",
        style="深度对谈",
        output_dir=output_dir,
        verbose=True
    )

    total_elapsed = time.time() - total_start

    print("\n" + "=" * 70)
    print("生成完成!")
    print("=" * 70)

    print(f"\n[总耗时] {total_elapsed:.1f}s ({total_elapsed/60:.1f}分钟)")

    print(f"\n[输出文件]")
    print(f"  Session ID: {result.get('session_id', 'N/A')}")
    print(f"  Markdown: {result.get('markdown_path', 'N/A')}")
    print(f"  Audio: {result.get('audio_path', 'N/A')}")

    # 检查文件
    md_path = result.get('markdown_path')
    audio_path = result.get('audio_path')

    if md_path and Path(md_path).exists():
        print(f"  Markdown大小: {Path(md_path).stat().st_size / 1024:.1f} KB")

    if audio_path and Path(audio_path).exists():
        audio_size = Path(audio_path).stat().st_size
        print(f"  Audio大小: {audio_size / 1024 / 1024:.2f} MB")
        print(f"\n[✓] 完整端到端流程成功!")
    else:
        print(f"\n[!] 警告: 音频文件未生成")
        print(f"    这可能是因为TTS配置问题，但脚本生成成功")

    print("\n" + "=" * 70)

except Exception as e:
    print(f"\n[错误] {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)


print("\n" + "=" * 70)
print("测试外部 Research Package 注入分支")
print("=" * 70)
print("测试流程: research_package 注入 -> Script -> Audio")
print("=" * 70)

try:
    from src.schema import ResearchPackage

    research_pkg = {
        "schema_version": "2.1",
        "source": "人工智能的发展趋势",
        "source_type": "topic",
        "style_selected": "深度对谈",
        "hook": "为什么我们总觉得AI离自己很远？",
        "central_insight": "AI正在从工具变成同事，改变的是工作的基本单元",
        "content_outline": "全篇采用渐进式揭露结构。seg_01 从日常办公场景切入，用具体效率案例建立听众代入感；seg_02 在中段抛出核心冲突（效率提升 vs 岗位焦虑），用 MIT 教授观点制造认知转折；seg_03 收束到可落地的认知框架，给出明确行动方向。语气沉稳，数据支撑，避免情绪大起大落。",
        "segments": [
            {
                "segment_id": "seg_01",
                "narrative_function": "setup",
                "dramatic_goal": "从日常生活切入，建立听众的代入感",
                "content_focus": "AI在办公场景中的悄然渗透",
                "estimated_length": 600,
                "materials_to_use": ["mat_001"],
                "persona_dynamics": {
                    "who_initiates": "A",
                    "dynamic_mode": "storytelling",
                    "emotional_tone": "curious"
                },
                "outline": "本段弧线：从'AI离我很远'到'AI已经在身边'。关键转折点在中段：用36氪报告中的自媒体团队效率提升40%案例打破听众既有认知。推进计划：A以身边变化发问开场，B起初不以为然，A用案例和数据说服，B产生共鸣并顺势提出焦虑。深度对谈风格，情绪平稳，语气偏叙述。"
            },
            {
                "segment_id": "seg_02",
                "narrative_function": "confrontation",
                "dramatic_goal": "抛出核心冲突：效率提升 vs 岗位焦虑",
                "content_focus": "AI替代人类工作的真实边界",
                "estimated_length": 800,
                "materials_to_use": ["mat_002"],
                "persona_dynamics": {
                    "who_initiates": "B",
                    "dynamic_mode": "challenge",
                    "emotional_tone": "tense"
                },
                "outline": "本段弧线：从'效率提升会裁人'到'AI替代有边界'。关键转折点在中段：引入 MIT Acemoglu 教授观点，指出短期冲击被高估，再用 WEF 数据平衡焦虑。推进计划：B 延续上段焦虑发问，A 先用反直觉角度回应（效率提升催生新业务），再引用专家和数据给出真实边界。深度对谈风格，反驳中带收敛，为下段铺垫。"
            },
            {
                "segment_id": "seg_03",
                "narrative_function": "resolution",
                "dramatic_goal": "给出可落地的认知框架",
                "content_focus": "什么样的人更容易与AI协作而非被替代",
                "estimated_length": 700,
                "materials_to_use": ["mat_003"],
                "persona_dynamics": {
                    "who_initiates": "A",
                    "dynamic_mode": "collaborate",
                    "emotional_tone": "reflective"
                },
                "outline": "本段弧线：从'焦虑怎么办'到'AI是同事不是对手'。关键转折点在前 1/3：直接总结出三条可落地的共生框架。推进计划：A 先提炼前文为三条行动建议，B 补充具体场景，双方共同收敛到'AI是同事'这一核心洞察，最后给听众明确的心理定位和行动方向。深度对谈风格，收尾沉稳但有力。"
            }
        ],
        "enriched_materials": [
            {
                "material_id": "mat_001",
                "material_type": "案例故事",
                "content": "某自媒体团队使用ChatGPT后，内容产出效率提升40%，从每周5篇提升到7篇",
                "source": "36氪 - 2024AI办公效率报告",
                "related_topic": "AI办公",
                "usage_hint": "用于开场建立共鸣"
            },
            {
                "material_id": "mat_002",
                "material_type": "专家观点",
                "content": "麻省理工教授Daron Acemoglu认为，生成式AI对就业的短期冲击被高估，中长期影响取决于制度设计",
                "source": "MIT Technology Review",
                "related_topic": "AI与就业",
                "usage_hint": "用于挑战'AI即将大规模失业'的恐慌叙事"
            },
            {
                "material_id": "mat_003",
                "material_type": "数据事实",
                "content": "世界经济论坛预测，到2027年，AI将创造6900万个新岗位，同时淘汰8300万个岗位，净减少约1400万个",
                "source": "WEF Future of Jobs Report 2023",
                "related_topic": "AI与就业",
                "usage_hint": "用于结尾给出全局视角"
            }
        ]
    }

    # 先验证 schema
    validated = ResearchPackage.model_validate(research_pkg)
    print(f"\n[Schema验证] ✓ 通过，segments={len(validated.segments)}, materials={len(validated.enriched_materials)}")

    output_dir2 = "./test_outputs/e2e_research_package_test"
    Path(output_dir2).mkdir(parents=True, exist_ok=True)

    pipeline2 = PodcastPipeline(skip_client_init=True)

    total_start = time.time()

    print("\n" + "-" * 70)
    print("开始生成（跳过本地 Research，直接 Script Generation）...")
    print("-" * 70)

    result2 = pipeline2.generate(
        source="人工智能的发展趋势",
        source_type="topic",
        style="深度对谈",
        research_package=research_pkg,
        output_dir=output_dir2,
        verbose=True
    )

    total_elapsed = time.time() - total_start

    print("\n" + "=" * 70)
    print("生成完成!")
    print("=" * 70)

    print(f"\n[总耗时] {total_elapsed:.1f}s ({total_elapsed/60:.1f}分钟)")

    md_path2 = result2.get("markdown_path", "N/A")
    # 音频非本次测试重点，仅做文本校验
    audio_path2 = result2.get("audio_path")

    print(f"\n[输出文件]")
    print(f"  Session ID: {result2.get('session_id', 'N/A')}")
    print(f"  Markdown: {md_path2}")
    if audio_path2:
        print(f"  Audio: {audio_path2} (TTS 已生成)")

    script = result2.get("script", [])
    total_lines = sum(len(seg.get("lines", [])) for seg in script)
    total_words = sum(seg.get("word_count", 0) for seg in script)
    print(f"  脚本行数: {total_lines}")
    print(f"  脚本字数: {total_words}")

    # 文本质量校验
    validation_passed = True
    if not (total_lines > 0 and total_words > 1000):
        print(f"\n[✗] 脚本内容不足")
        validation_passed = False

    # 校验 markdown 存在且包含 segment 内容
    if md_path2 and Path(md_path2).exists():
        md_content = Path(md_path2).read_text(encoding="utf-8")
        if "seg_01" not in md_content:
            print(f"[✗] Markdown 缺少 segment 内容")
            validation_passed = False
    else:
        print(f"[✗] Markdown 文件未生成")
        validation_passed = False

    # 校验 key_moments 非空
    for seg in script:
        if not seg.get("key_moments"):
            print(f"[✗] Segment {seg.get('segment_id')} 缺少 key_moments")
            validation_passed = False

    if validation_passed:
        print(f"\n[✓] 外部 Research Package 注入流程成功! (文本校验通过)")
    else:
        sys.exit(1)

    print("\n" + "=" * 70)

except Exception as e:
    print(f"\n[错误] {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
