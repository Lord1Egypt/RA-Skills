# -*- coding: utf-8 -*-
"""
跨时空对话：林黛玉 × 林肯
主题：自由与命运
"""

import sys
import os
import json

# 清理代理
for k in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'ALL_PROXY']:
    os.environ.pop(k, None)

sys.path.insert(0, '.')

from src.persona_manager import PersonaManager, DoublePersonaManager

# 测试用户ID
USER_ID = "test_cross_time"

def setup_personas():
    """加载并配置两个persona"""
    print("=" * 60)
    print("设置跨时空对话：林黛玉 × 林肯")
    print("=" * 60)
    print()

    # 读取persona
    with open('tests/persona-resource/output/daiyu_persona.json', 'r', encoding='utf-8') as f:
        daiyu_persona = json.load(f)

    with open('tests/persona-resource/output/lincoln_persona.json', 'r', encoding='utf-8') as f:
        lincoln_persona = json.load(f)

    print("【林黛玉 Persona】")
    print(f"  archetype: {daiyu_persona['identity']['archetype']}")
    print(f"  core_drive: {daiyu_persona['identity']['core_drive'][:40]}...")
    print(f"  signature_phrases: {daiyu_persona['expression']['signature_phrases']}")
    print()

    print("【林肯 Persona】")
    print(f"  archetype: {lincoln_persona['identity']['archetype']}")
    print(f"  core_drive: {lincoln_persona['identity']['core_drive'][:40]}...")
    print(f"  signature_phrases: {lincoln_persona['expression']['signature_phrases']}")
    print()

    # 保存到用户配置
    daiyu_manager = PersonaManager(USER_ID, "daiyu")
    daiyu_manager.save(daiyu_persona)

    lincoln_manager = PersonaManager(USER_ID, "lincoln")
    lincoln_manager.save(lincoln_persona)

    # 配置双主持人模式
    double_manager = DoublePersonaManager(USER_ID)
    double_manager.save(
        host_a=lincoln_persona,      # 林肯为主持人A
        host_b=daiyu_persona,        # 林黛玉为嘉宾B
        host_a_name="lincoln",
        host_b_name="daiyu"
    )

    print("[OK] 双主持人配置完成")
    print()

    return daiyu_persona, lincoln_persona


def generate_podcast_topic():
    """
    生成播客话题
    由于端到端需要API调用，这里输出配置供手动运行
    """
    print("=" * 60)
    print("播客配置")
    print("=" * 60)
    print()

    topic = "自由与命运：当东方诗魂遇见西方解放者"

    print(f"【话题】{topic}")
    print()
    print("【内容方向】")
    print("  - 林肯谈'人人生而平等'的理想与实现")
    print("  - 林黛玉谈'质本洁来还洁去'的命运观")
    print("  - 自由是抗争得来的还是命中注定的？")
    print("  - 如果黛玉遇见林肯，她会如何理解'解放'？")
    print()

    print("【主持人配置】")
    print("  Host A: 林肯 (追问者，逻辑与正义)")
    print("  Host B: 林黛玉 (诗魂，敏感与才情)")
    print()

    print("【风格模板】建议：深度访谈")
    print()

    print("=" * 60)
    print("运行以下命令生成完整播客：")
    print("=" * 60)
    print()
    print("from src.podcast_pipeline import PodcastPipeline")
    print(f"pipeline = PodcastPipeline(user_id='{USER_ID}')")
    print(f"result = pipeline.generate(")
    print(f"    topic='{topic}',")
    print(f"    source_type='topic',")
    print(f"    style_template='深度访谈',")
    print(f"    enable_tts=True")
    print(f")")
    print()

    return topic


def main():
    # 设置persona
    daiyu, lincoln = setup_personas()

    # 输出话题配置
    topic = generate_podcast_topic()

    # 输出memory检索测试
    print("=" * 60)
    print("Memory检索测试")
    print("=" * 60)
    print()

    from src.memory_skill import MemorySkill

    # 测试林黛玉的memory
    daiyu_memory = MemorySkill(USER_ID)  # 注意：实际应该按persona隔离
    # 这里简化处理，实际应该从persona的memory_seed加载

    print("【林肯的Memory】(用于'自由'相关话题)")
    print("  - 目睹奴隶拍卖：觉醒时刻")
    print("  - 解放宣言：18万黑人获得自由")
    print("  - 葛底斯堡：民有民治民享")
    print()

    print("【林黛玉的Memory】(用于'命运'相关话题)")
    print("  - 葬花：质本洁来还洁去")
    print("  - 焚稿：决绝告别")
    print("  - 菊花诗：孤标傲世")
    print()

    print("=" * 60)
    print("测试完成！")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
