"""
Sub-Agent Research 注入模式示例

外部 Sub-Agent（如 Claude Code、OpenClaw）已完成真实网络检索后，
可直接将生成的 Research Package 注入 PodcastPipeline，跳过本地 Research 阶段。
"""
from src.podcast_pipeline import PodcastPipeline

research_pkg = {
    "schema_version": "2.1",
    "source": "人工智能的发展趋势",
    "source_type": "topic",
    "style_selected": "深度对谈",
    "hook": "为什么我们总觉得AI离自己很远？",
    "central_insight": "AI正在从工具变成同事，改变的不是岗位，而是工作的基本单元",
    "content_outline": "全篇采用渐进式揭露结构。seg_01 从日常办公切入建立共鸣；seg_02 抛出核心冲突并给出数据支撑；seg_03 收束到可落地的认知框架。深度对谈风格，语气沉稳。",
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
            "outline": "本段弧线：从'AI离我很远'到'AI已经在身边'。关键转折点在中段，用36氪报告案例打破既有认知。推进计划：A以身边变化发问，B起初不以为然，A用数据说服，B产生共鸣。"
        },
        {
            "segment_id": "seg_02",
            "narrative_function": "confrontation",
            "dramatic_goal": "抛出核心冲突：效率提升 vs 岗位焦虑",
            "content_focus": "AI替代人类工作的真实边界",
            "estimated_length": 800,
            "materials_to_use": ["mat_002", "mat_003"],
            "persona_dynamics": {
                "who_initiates": "B",
                "dynamic_mode": "challenge",
                "emotional_tone": "tense"
            },
            "outline": "本段弧线：从焦虑到厘清边界。关键转折点在中段，引用MIT教授观点纠正恐慌叙事。推进计划：B延续焦虑发问，A用反直觉角度回应，再引用专家和数据给出真实边界。"
        },
        {
            "segment_id": "seg_03",
            "narrative_function": "resolution",
            "dramatic_goal": "给出可落地的认知框架",
            "content_focus": "什么样的人更容易与AI协作而非被替代",
            "estimated_length": 700,
            "materials_to_use": ["mat_004"],
            "persona_dynamics": {
                "who_initiates": "A",
                "dynamic_mode": "collaborate",
                "emotional_tone": "reflective"
            },
            "outline": "本段弧线：从焦虑到行动。关键转折点在前1/3，直接总结三条共生框架。推进计划：A提炼行动建议，B补充场景，双方收敛到'AI是同事'的核心洞察。"
        }
    ],
    "enriched_materials": [
        {
            "material_id": "mat_001",
            "material_type": "案例故事",
            "content": "某自媒体团队使用ChatGPT后，内容产出效率提升40%",
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
        }
    ]
}

pipeline = PodcastPipeline(skip_client_init=True)
result = pipeline.generate(
    source="人工智能的发展趋势",
    source_type="topic",
    style="深度对谈",
    research_package=research_pkg,
    output_dir="./my_podcasts",
    verbose=True
)

print(f"Session ID: {result['session_id']}")
print(f"音频文件: {result['audio_path']}")
print(f"脚本行数: {sum(len(seg['lines']) for seg in result['script'])}")
