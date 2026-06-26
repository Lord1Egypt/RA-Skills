"""
文本质量深度测试套件 - Phase 1
测试方向：前沿专业话题 / 强人格化persona / 观点交锋 / 喜剧风格
不跑TTS，只生成文本并保存用于后续分析
"""
import os
import sys
import time
import json
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# 清除代理
for proxy_var in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'ALL_PROXY']:
    if proxy_var in os.environ:
        del os.environ[proxy_var]

# 注：本测试仅生成文本，不跑TTS，不加载TTS配置

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

# 清除任何可能残留的环境变量中的TTS配置，确保测试不触发音频生成
for tts_var in ['VOLCANO_TTS_APP_ID', 'VOLCANO_TTS_ACCESS_TOKEN', 'VOLCANO_TTS_SECRET_KEY']:
    os.environ.pop(tts_var, None)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.podcast_pipeline import PodcastPipeline

OUTPUT_BASE = Path(__file__).parent.parent / "test_outputs"


def save_result(result: dict, test_name: str):
    """保存测试结果到JSON和MD"""
    out_dir = OUTPUT_BASE / test_name
    out_dir.mkdir(parents=True, exist_ok=True)

    session_id = result.get('session_id', 'unknown')
    json_path = out_dir / f"{session_id}.json"
    md_path = out_dir / f"{session_id}.md"

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # 同时保存一个可直接读的markdown
    if md_path.exists():
        md_content = md_path.read_text(encoding='utf-8')
    else:
        # 如果pipeline没生成md，自己拼一个
        lines = [f"# {test_name}\n", f"Session: {session_id}\n\n"]
        for seg in result.get('script', []):
            lines.append(f"## {seg.get('segment_id', '?')}\n\n")
            for line in seg.get('lines', []):
                lines.append(f"**{line.get('speaker')}**: {line.get('text')}\n\n")
            lines.append(f"*Summary: {seg.get('summary', '')}*\n\n")
        md_content = "".join(lines)
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)

    print(f"  已保存: {json_path.name} / {md_path.name}")
    return json_path, md_path


def run_test(name: str, source: str, source_type: str, style: str,
             research_package: dict, persona_config: dict = None):
    print(f"\n{'='*70}")
    print(f"[{name}]")
    print(f"{'='*70}")

    pipeline = PodcastPipeline(skip_client_init=True)

    total_start = time.time()
    result = pipeline.generate(
        source=source,
        source_type=source_type,
        style=style,
        research_package=research_package,
        persona_config=persona_config,
        output_dir=str(OUTPUT_BASE / name),
        verbose=True,
        skip_audio=True
    )
    elapsed = time.time() - total_start

    json_path, md_path = save_result(result, name)

    script = result.get('script', [])
    total_lines = sum(len(seg.get('lines', [])) for seg in script)
    total_words = sum(seg.get('word_count', 0) for seg in script)

    print(f"\n  耗时: {elapsed:.1f}s ({elapsed/60:.1f}分钟)")
    print(f"  行数: {total_lines} | 字数: {total_words}")
    return result


# ============================================================
# 测试 1：前沿专业话题 - 量子计算纠错
# ============================================================
def test_frontier_research():
    pkg = {
        "schema_version": "2.1",
        "source": "量子计算纠错最新进展",
        "source_type": "topic",
        "style_selected": "深度对谈",
        "hook": "为什么量子计算机明明算得很快，却连一个简单的答案都保不住？",
        "central_insight": "量子纠错不是修 bug，而是用量子纠缠编织一张'保护网'，让脆弱的信息在噪声中自我愈合",
        "content_outline": "深度对谈风格，语气沉稳。seg_01 从经典计算机的纠错概念切入，用类比建立直觉；seg_02 抛出当前两种主流纠错路线的学术争议（表面码 vs 猫量子比特）；seg_03 收敛到方法论局限与工程化前景，给出听众可理解的认知框架。",
        "segments": [
            {
                "segment_id": "seg_01",
                "narrative_function": "setup",
                "dramatic_goal": "用类比破除量子纠错的术语壁垒，建立听众直觉",
                "content_focus": "量子比特为什么比特别脆弱，以及'纠错'在量子世界的特殊含义",
                "estimated_length": 700,
                "materials_to_use": ["mat_001", "mat_002"],
                "persona_dynamics": {
                    "who_initiates": "A",
                    "dynamic_mode": "storytelling",
                    "emotional_tone": "curious"
                },
                "outline": "本段弧线：从'量子计算离我们很远'到'原来它的脆弱是因为物理规律本身'。关键转折点在中段：用'传话游戏'类比解释量子态的不可复制性。推进计划：A 以日常手机卡顿发问开场，B 先给出经典纠错的简单解释，A 再抛出问题'那量子世界不能复制怎么办'，B 用类比解释量子纠错的本质是让信息'分布式'存储。情绪平稳，避免直接甩术语。"
            },
            {
                "segment_id": "seg_02",
                "narrative_function": "confrontation",
                "dramatic_goal": "呈现学术界在量子纠错路线上的真实分歧",
                "content_focus": "表面码（surface code）与猫量子比特（cat qubit）两种路线的优劣与争议",
                "estimated_length": 900,
                "materials_to_use": ["mat_003", "mat_004", "mat_005"],
                "persona_dynamics": {
                    "who_initiates": "B",
                    "dynamic_mode": "challenge",
                    "emotional_tone": "tense"
                },
                "outline": "本段弧线：从'主流方案看似稳妥'到'其实另一条路也能走，而且各有代价'。关键转折点在中段：引入 Google 与 Alice \u0026 Bob 两家公司在路线选择上的分歧。推进计划：B 先肯定表面码的进展，A 提出质疑'但这需要几万个物理比特才能保护一个逻辑比特，工程上不现实'，B 用 cat qubit 的近期论文回应，A 追问猫态的退相干问题，双方各持立场，不急于和解。"
            },
            {
                "segment_id": "seg_03",
                "narrative_function": "resolution",
                "dramatic_goal": "给出可落地的认知框架：普通听众应该如何理解这场技术竞赛",
                "content_focus": "量子纠错距离实用化还有多远，以及判断进展的合理标准",
                "estimated_length": 700,
                "materials_to_use": ["mat_006"],
                "persona_dynamics": {
                    "who_initiates": "A",
                    "dynamic_mode": "collaborate",
                    "emotional_tone": "reflective"
                },
                "outline": "本段弧线：从'两种路线孰优孰劣'的焦虑，转向'判断标准比站队更重要'的清醒。关键转折点在前1/3：直接给出三条判断进展的标准（逻辑错误率、物理比特开销、相干时间）。推进计划：A 先总结两条路线的本质差异，B 补充工程侧的瓶颈，双方收敛到'未来5-10年看指标而非看口号'的核心洞察，结尾不煽情。"
            }
        ],
        "enriched_materials": [
            {
                "material_id": "mat_001",
                "material_type": "背景信息",
                "content": "经典计算机的纠错通常通过冗余备份实现：把1个比特复制成3个比特，如果其中一个被噪声翻转，通过'少数服从多数'就能恢复原始信息。",
                "source": "科普类比",
                "related_topic": "经典纠错",
                "usage_hint": "用于 seg_01 建立直觉"
            },
            {
                "material_id": "mat_002",
                "material_type": "专家观点",
                "content": "量子力学的不可克隆定理指出：不可能完美复制一个未知的量子态。因此量子纠错不能简单做'备份'，而必须将信息'编织'进多个量子比特的纠缠态中。",
                "source": "Wootters \u0026 Zurek, Nature 1982",
                "related_topic": "量子不可克隆定理",
                "usage_hint": "用于 seg_01 解释为何量子纠错与众不同"
            },
            {
                "material_id": "mat_003",
                "material_type": "数据事实",
                "content": "Google Quantum AI 团队在 2024 年《Nature》发表论文，展示基于表面码（surface code）的量子纠错：将逻辑错误率从 3.028% 压低到 2.914%，首次实现了'越扩码、错误率越低'的里程碑。",
                "source": "Google Quantum AI, Nature 2024",
                "related_topic": "表面码纠错",
                "usage_hint": "用于 seg_02 支撑主流路线"
            },
            {
                "material_id": "mat_004",
                "material_type": "专家观点",
                "content": "法国初创公司 Alice \u0026 Bob 的科学家认为，猫量子比特（cat qubit）由于内置了对比特翻转错误的天然免疫力，可以用少得多的物理比特实现同样的逻辑保护，从而大幅降低工程复杂度。",
                "source": "Alice \u0026 Bob, PRX Quantum 2024",
                "related_topic": "猫量子比特",
                "usage_hint": "用于 seg_02 支撑挑战者路线"
            },
            {
                "material_id": "mat_005",
                "material_type": "反面论点",
                "content": "批评者指出，猫量子比特虽然减少了比特翻转错误，但相位翻转错误变得更为严重，且需要极其精巧的微波控制，目前距离大规模集成还有显著差距。",
                "source": "学术界同行评议",
                "related_topic": "猫量子比特",
                "usage_hint": "用于 seg_02 平衡争议"
            },
            {
                "material_id": "mat_006",
                "material_type": "数据事实",
                "content": "当前业界普遍认为，实用的容错量子计算需要逻辑错误率低于 10^-12，而目前的最佳水平仍在 10^-3 量级，这意味着还需要 2-3 个数量级的提升。",
                "source": "IBM Quantum Roadmap 2024",
                "related_topic": "量子计算实用化",
                "usage_hint": "用于 seg_03 给出现实标尺"
            }
        ]
    }
    return run_test(
        "frontier_research_test",
        source="量子计算纠错最新进展",
        source_type="topic",
        style="深度对谈",
        research_package=pkg
    )


# ============================================================
# 测试 2：强人格化 persona（带 memory_seed）
# ============================================================
def test_persona_voice():
    # 构造差异极大的双主持人 persona
    persona_config = {
        "host_a": {
            "identity": {
                "name": "老炮",
                "archetype": "吐槽者",
                "core_drive": "用 blunt 的真相戳破泡沫，看不惯精致包装",
                "chemistry": "先听完你的说法，然后用你最意想不到的刁钻角度回怼"
            },
            "expression": {
                "pace": "fast",
                "sentence_length": "short",
                "signature_phrases": ["不是我杠啊", "就这么说", "你懂我意思吧"],
                "attitude": "skeptical"
            },
            "memory_seed": [
                {
                    "title": "被iPhone坑的经历",
                    "content": "2022年跟风买了最新款iPhone，结果发现信号还不如我三年前安卓机，在地铁里打游戏掉线掉的我想摔手机。",
                    "tags": ["手机", "消费", "吐槽"]
                },
                {
                    "title": "经典耐用老安卓",
                    "content": "我这台老安卓用了四年，除了电池有点蔫，其他一点毛病没有。我觉得现在的厂商就是故意把东西做短命。",
                    "tags": ["手机", "耐用", "消费观"]
                }
            ]
        },
        "host_b": {
            "identity": {
                "name": "静姐",
                "archetype": "观察者",
                "core_drive": "在纷扰的信息中找出宁静的逻辑，用温和但坚定的方式表达",
                "chemistry": "耐心倾听，然后用类比和反问引导对方看到另一面"
            },
            "expression": {
                "pace": "slow",
                "sentence_length": "long",
                "signature_phrases": ["换个角度想", "就像", "也未必是坏事"],
                "attitude": "curious"
            },
            "memory_seed": [
                {
                    "title": "参数表研究经历",
                    "content": "去年买相机时，我花了整整一周做参数对比表，最后发现最适合自己的其实是中端款，而不是最贵的那台。这个经历让我相信消费决策需要冷静分析。",
                    "tags": ["消费", "研究", "理性"]
                }
            ]
        }
    }

    pkg = {
        "schema_version": "2.1",
        "source": "年轻人为什么不爱换手机了",
        "source_type": "topic",
        "style_selected": "深度对谈",
        "hook": "你有没有发现，身边越来越少人每年追新款手机了？",
        "central_insight": "年轻人不换手机不是因为没钱，而是因为'足够好'已经到来，厂商的创新叙事正在失效",
        "content_outline": "深度对谈风格，情绪从好奇到略带焦虑再到释然。seg_01 从日常观察切入；seg_02 抛出'是没钱还是不想换'的核心冲突；seg_03 给出消费观念转变的框架。",
        "segments": [
            {
                "segment_id": "seg_01",
                "narrative_function": "setup",
                "dramatic_goal": "从身边观察建立共鸣",
                "content_focus": "年轻人换机周期变长的现象",
                "estimated_length": 600,
                "materials_to_use": ["mat_001"],
                "persona_dynamics": {
                    "who_initiates": "A",
                    "dynamic_mode": "storytelling",
                    "emotional_tone": "curious"
                }
            },
            {
                "segment_id": "seg_02",
                "narrative_function": "confrontation",
                "dramatic_goal": "抛出核心冲突：经济压力 vs 产品倦怠",
                "content_focus": "年轻人不换手机的真实原因",
                "estimated_length": 800,
                "materials_to_use": ["mat_002", "mat_003"],
                "persona_dynamics": {
                    "who_initiates": "B",
                    "dynamic_mode": "challenge",
                    "emotional_tone": "tense"
                }
            },
            {
                "segment_id": "seg_03",
                "narrative_function": "resolution",
                "dramatic_goal": "给出认知框架",
                "content_focus": "消费观念从'追新'到'够用就好'的转变",
                "estimated_length": 600,
                "materials_to_use": ["mat_004"],
                "persona_dynamics": {
                    "who_initiates": "A",
                    "dynamic_mode": "collaborate",
                    "emotional_tone": "reflective"
                }
            }
        ],
        "enriched_materials": [
            {
                "material_id": "mat_001",
                "material_type": "数据事实",
                "content": "Counterpoint Research 报告显示，2024年中国消费者换机周期已延长至49个月，创历史新高。",
                "source": "Counterpoint Research 2024",
                "related_topic": "换机周期",
                "usage_hint": "开场建立共鸣"
            },
            {
                "material_id": "mat_002",
                "material_type": "专家观点",
                "content": "行业分析师认为，智能手机的创新已触及物理和工程瓶颈，旗舰机之间的功能差异对消费者日常生活影响越来越小。",
                "source": "Canalys 分析师报告",
                "related_topic": "产品创新瓶颈",
                "usage_hint": "支撑'产品倦怠论'"
            },
            {
                "material_id": "mat_003",
                "material_type": "反面论点",
                "content": "另一部分观点认为，年轻人不换手机主要是经济增速放缓和可支配收入下降导致的被动收缩。",
                "source": "经济观察报评论",
                "related_topic": "消费力",
                "usage_hint": "提供对立视角"
            },
            {
                "material_id": "mat_004",
                "material_type": "案例故事",
                "content": "日本消费者早在2010年代就形成了'手机用五年'的习惯，被称为'ガラケー文化'的延续，核心是'功能足够就不升级'。",
                "source": "日经中文网",
                "related_topic": "消费观念",
                "usage_hint": "结尾给出参照系"
            }
        ]
    }
    return run_test(
        "persona_voice_test",
        source="年轻人为什么不爱换手机了",
        source_type="topic",
        style="深度对谈",
        research_package=pkg,
        persona_config=persona_config
    )


# ============================================================
# 测试 3：观点交锋风格
# ============================================================
def test_debate():
    pkg = {
        "schema_version": "2.1",
        "source": "AI生成内容是否应该享有版权",
        "source_type": "topic",
        "style_selected": "观点交锋",
        "hook": "如果一幅画是AI画的，那么版权应该归谁？",
        "central_insight": "AI版权之争的核心不是技术能力，而是'创作中的人类 intent 到底值多少钱'",
        "content_outline": "观点交锋风格，全程保持对立张力。seg_01 双方亮出核心立场；seg_02 用法律和现实案例展开攻防；seg_03 保留分歧收尾，不允许和解。情绪从 tense 到更 tense。",
        "segments": [
            {
                "segment_id": "seg_01",
                "narrative_function": "setup",
                "dramatic_goal": "亮出对立立场，设定战场",
                "content_focus": "A 支持 AI 生成物应受版权保护，B 坚决反对",
                "estimated_length": 600,
                "materials_to_use": ["mat_001"],
                "persona_dynamics": {
                    "who_initiates": "A",
                    "dynamic_mode": "debate",
                    "emotional_tone": "tense"
                },
                "outline": "本段弧线：从零和开场到立场鲜明对立。推进计划：A 直接抛出'工具创作论'，认为人类使用 AI 和用 Photoshop 没有本质区别；B 立即反驳，强调 AI 的'自动生成'消解了人类独创性。双方在第一段就明确让对方知道自己的底线。"
            },
            {
                "segment_id": "seg_02",
                "narrative_function": "confrontation",
                "dramatic_goal": "用案例和法律攻防",
                "content_focus": "中美欧司法实践与 Thaler 案的争议",
                "estimated_length": 900,
                "materials_to_use": ["mat_002", "mat_003", "mat_004"],
                "persona_dynamics": {
                    "who_initiates": "B",
                    "dynamic_mode": "debate",
                    "emotional_tone": "tense"
                },
                "outline": "本段弧线：从'各自立论'到'激烈交锋'。推进计划：B 用美国版权局的拒绝注册案例攻击 A 的立场；A 用'提示词工程饱含人类创意'反击；B 再抛中国《著作权法》的'自然人创作'条款；A 引用北京互联网法院的初审判决作为反例。双方都不退让，每句话都带有质疑或反驳。"
            },
            {
                "segment_id": "seg_03",
                "narrative_function": "resolution",
                "dramatic_goal": "保留分歧，不允许和稀泥式和解",
                "content_focus": "两种立场的根本不可调和之处",
                "estimated_length": 600,
                "materials_to_use": ["mat_005"],
                "persona_dynamics": {
                    "who_initiates": "A",
                    "dynamic_mode": "debate",
                    "emotional_tone": "tense"
                },
                "outline": "本段弧线：从激烈交锋到'各自坚守'。关键要求：**禁止**以'其实两边都有道理'收尾。推进计划：A 总结自己的核心坚持（保护创作者经济利益），B 总结自己的核心坚持（防止版权制度被AI掏空），最后双方明确表态'这个问题上我暂时没被说服'，保留分歧结束。"
            }
        ],
        "enriched_materials": [
            {
                "material_id": "mat_001",
                "material_type": "专家观点",
                "content": "美国版权局在 2023 年明确裁定，由 Midjourney 生成的图像不受版权保护，因为'缺乏人类作者身份'。",
                "source": "U.S. Copyright Office, 2023",
                "related_topic": "AI版权",
                "usage_hint": "支撑反方立场"
            },
            {
                "material_id": "mat_002",
                "material_type": "案例故事",
                "content": "2023年，北京互联网法院在一起AI生成图片著作权案中认定，原告对提示词进行了大量设计、调整，体现了独创性智力投入，因此该图片受著作权法保护。",
                "source": "北京互联网法院判决书",
                "related_topic": "AI版权",
                "usage_hint": "支撑正方立场"
            },
            {
                "material_id": "mat_003",
                "material_type": "专家观点",
                "content": "学者认为，提示词本质上是一种'参数化描述'，和摄影师按下快门的创意含量不可同日而语。",
                "source": "知识产权学者评论",
                "related_topic": "独创性标准",
                "usage_hint": "反方论据"
            },
            {
                "material_id": "mat_004",
                "material_type": "反面论点",
                "content": "支持者反驳：摄影术诞生时也遭遇过同样的'没有人类创作'质疑，最终法律适应了技术发展。",
                "source": "科技法律评论",
                "related_topic": "历史类比",
                "usage_hint": "正方反击"
            },
            {
                "material_id": "mat_005",
                "material_type": "专家观点",
                "content": "欧盟委员会在 2024 年的 AI 法案中，对生成式 AI 的内容透明度提出了要求，但没有直接解决版权归属问题，显示出立法者的犹豫。",
                "source": "EU AI Act, 2024",
                "related_topic": "立法现状",
                "usage_hint": "结尾说明问题仍在悬置"
            }
        ]
    }
    return run_test(
        "debate_test",
        source="AI生成内容是否应该享有版权",
        source_type="topic",
        style="观点交锋",
        research_package=pkg
    )


# ============================================================
# 测试 4：喜剧风格
# ============================================================
def test_comedy():
    pkg = {
        "schema_version": "2.1",
        "source": "当代年轻人奇怪的省钱行为",
        "source_type": "topic",
        "style_selected": "喜剧风格",
        "hook": "你见过为了省两块钱公交费，宁愿走四十分钟的人吗？",
        "central_insight": "年轻人省钱的本质不是穷，而是一种'消费心理账户'的重新分配——小钱死抠，大钱眼都不眨",
        "content_outline": "喜剧风格，节奏轻快。seg_01 用具体生活场景 setup 预埋梗；seg_02 用吐槽的方式解构'省钱悖论'；seg_03 callback 前段的梗并爆笑收尾。全程保持轻松调侃。",
        "segments": [
            {
                "segment_id": "seg_01",
                "narrative_function": "setup",
                "dramatic_goal": "用荒诞场景建立喜剧氛围，预埋一个可 callback 的梗",
                "content_focus": "年轻人省钱的各种奇葩行为",
                "estimated_length": 600,
                "materials_to_use": ["mat_001", "mat_002"],
                "persona_dynamics": {
                    "who_initiates": "A",
                    "dynamic_mode": "storytelling",
                    "emotional_tone": "curious"
                },
                "outline": "本段弧线：从日常观察到荒诞发现。推进计划：A 先吐槽自己朋友的省钱行为（为了省配送费走两公里），B 接梗吐槽更狠的例子。关键 setup：A 在最后说了一句'不过她省下的钱，昨天全花在演唱会门票上了'——这句话要在 seg_03 被 callback。节奏轻快，短句为主。"
            },
            {
                "segment_id": "seg_02",
                "narrative_function": "confrontation",
                "dramatic_goal": "用幽默解构'省钱悖论'",
                "content_focus": "小钱死抠但大钱毫不犹豫的心理机制",
                "estimated_length": 700,
                "materials_to_use": ["mat_003"],
                "persona_dynamics": {
                    "who_initiates": "B",
                    "dynamic_mode": "debate",
                    "emotional_tone": "tense"
                },
                "outline": "本段弧线：从'省钱=穷'到'省钱=心理账户游戏'。推进计划：B 假装正经地分析'心理账户'理论，A 不断打断吐槽（'你这套词从哪本书抄的'）。双方互相调侃，不要写成严肃科普。每隔 4-6 句话要有一个笑点。"
            },
            {
                "segment_id": "seg_03",
                "narrative_function": "resolution",
                "dramatic_goal": "callback 前段梗，爆笑收尾",
                "content_focus": "省钱行为的本质其实是一种生活态度的选择",
                "estimated_length": 500,
                "materials_to_use": ["mat_004"],
                "persona_dynamics": {
                    "who_initiates": "A",
                    "dynamic_mode": "storytelling",
                    "emotional_tone": "reflective"
                },
                "outline": "本段弧线：从分析回到荒诞共鸣。关键任务：**必须在开头 callback seg_01 的 setup**（关于'省下的钱全花演唱会门票上了'）。推进计划：A 重提那个朋友，B 补刀说'所以她现在既累又穷但还很快乐'。结尾用一个轻松的总结收尾，不要煽情。"
            }
        ],
        "enriched_materials": [
            {
                "material_id": "mat_001",
                "material_type": "案例故事",
                "content": "有网友为了省 15 块奶茶配送费，骑自行车 5 公里去店里自取，结果路上下雨了。",
                "source": "微博热门话题",
                "related_topic": "省钱行为",
                "usage_hint": "开场 setup"
            },
            {
                "material_id": "mat_002",
                "material_type": "案例故事",
                "content": "另一网友为了凑满减，买了根本用不上的东西，算了一晚上怎么组合最划算。",
                "source": "社交媒体",
                "related_topic": "省钱行为",
                "usage_hint": "增加荒诞感"
            },
            {
                "material_id": "mat_003",
                "material_type": "专家观点",
                "content": "行为经济学中的'心理账户'理论认为，人们会在心里把钱分成不同账户（日常消费、娱乐、投资），对每笔钱的'痛感'不同，因此会出现小钱斤斤计较、大钱毫不犹豫的现象。",
                "source": "理查德·塞勒《错误的行为》",
                "related_topic": "心理账户",
                "usage_hint": "用幽默方式解构"
            },
            {
                "material_id": "mat_004",
                "material_type": "数据事实",
                "content": "调查显示，超过 60% 的年轻人表示'该省省该花花'，省钱是为了把钱花在'真正让自己快乐'的事情上。",
                "source": "消费趋势调查 2024",
                "related_topic": "消费态度",
                "usage_hint": "结尾给出轻松定位"
            }
        ]
    }
    return run_test(
        "comedy_test",
        source="当代年轻人奇怪的省钱行为",
        source_type="topic",
        style="喜剧风格",
        research_package=pkg
    )


if __name__ == "__main__":
    print("=" * 70)
    print("文本质量深度测试套件 - Phase 1")
    print("=" * 70)
    print("注意：每个测试需要 3-5 分钟，总计约 15-20 分钟")
    print("=" * 70)

    suite_start = time.time()

    results = {}
    results["frontier"] = test_frontier_research()
    results["persona"] = test_persona_voice()
    results["debate"] = test_debate()
    results["comedy"] = test_comedy()

    total_time = time.time() - suite_start

    print("\n" + "=" * 70)
    print("全部测试完成")
    print("=" * 70)
    print(f"总耗时: {total_time:.1f}s ({total_time/60:.1f}分钟)")
    for name, res in results.items():
        script = res.get('script', [])
        lines = sum(len(seg.get('lines', [])) for seg in script)
        words = sum(seg.get('word_count', 0) for seg in script)
        print(f"  {name:12s} | {lines:3d} 行 | {words:4d} 字")
    print("=" * 70)
