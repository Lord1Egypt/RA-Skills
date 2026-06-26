# -*- coding: utf-8 -*-
"""
生成跨时空播客：林黛玉 × 林肯
需要设置 DOUBAO_API_KEY 环境变量
"""

import sys
import os

# 清理代理
for k in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'ALL_PROXY']:
    os.environ.pop(k, None)

sys.path.insert(0, '.')

import json
from pathlib import Path


def generate_script():
    """生成播客脚本（使用Script Generator）"""

    # 读取persona
    with open('tests/persona-resource/output/daiyu_persona.json', 'r', encoding='utf-8') as f:
        daiyu = json.load(f)

    with open('tests/persona-resource/output/lincoln_persona.json', 'r', encoding='utf-8') as f:
        lincoln = json.load(f)

    topic = "自由与命运：当东方诗魂遇见西方解放者"

    print("=" * 70)
    print("跨时空播客生成")
    print("=" * 70)
    print()
    print(f"话题: {topic}")
    print()

    # 构建大纲
    outline = {
        "title": topic,
        "segments": [
            {
                "segment_id": "seg_01",
                "estimated_duration_min": 3,
                "content_focus": "两位来自不同时空的灵魂初次相遇，互相介绍自己的时代与背景",
                "key_points": ["林肯介绍19世纪的美国与废奴运动", "黛玉介绍大观园与封建礼教", "初步的文化冲击与好奇"]
            },
            {
                "segment_id": "seg_02",
                "estimated_duration_min": 5,
                "content_focus": "探讨'自由'的含义：林肯的政治自由 vs 黛玉的精神自由",
                "key_points": ["林肯谈解放黑奴与《解放宣言》", "黛玉谈'质本洁来还洁去'的精神追求", "两种自由观的对比"]
            },
            {
                "segment_id": "seg_03",
                "estimated_duration_min": 5,
                "content_focus": "探讨'命运'：是可以抗争的还是注定的？",
                "key_points": ["黛玉谈命运的无常与悲剧", "林肯谈通过抗争改变命运", "如果黛玉有选择的机会"]
            },
            {
                "segment_id": "seg_04",
                "estimated_duration_min": 4,
                "content_focus": "跨时空的共鸣与告别",
                "key_points": ["两位灵魂发现共同的理想主义内核", "对自由、尊严、人性的共识", "诗意告别"]
            }
        ]
    }

    # 构建persona注入
    persona_injection = f"""
【双主持人Persona配置】

主持人A - 林肯：
- 身份: {lincoln['identity']['archetype']}
- 核心驱动力: {lincoln['identity']['core_drive']}
- 互动方式: {lincoln['identity']['chemistry']}
- 语速: {lincoln['expression']['pace']}
- 口头禅: {', '.join(lincoln['expression']['signature_phrases'])}
- 态度: {lincoln['expression']['attitude']}

主持人B - 林黛玉：
- 身份: {daiyu['identity']['archetype']}
- 核心驱动力: {daiyu['identity']['core_drive']}
- 互动方式: {daiyu['identity']['chemistry']}
- 语速: {daiyu['expression']['pace']}
- 口头禅: {', '.join(daiyu['expression']['signature_phrases'])}
- 态度: {daiyu['expression']['attitude']}
"""

    # 可用记忆
    lincoln_memories = "\n".join([f"- [{m['title']}] {m['content']}" for m in lincoln['memory_seed']])
    daiyu_memories = "\n".join([f"- [{m['title']}] {m['content']}" for m in daiyu['memory_seed']])

    print("【可用记忆 - 林肯】")
    print(lincoln_memories)
    print()
    print("【可用记忆 - 林黛玉】")
    print(daiyu_memories)
    print()

    # 准备生成脚本的prompt
    script_prompt = f"""你是一个跨时空播客编剧。请根据以下信息生成一个完整的播客脚本。

{persona_injection}

【话题大纲】
标题: {outline['title']}

共{len(outline['segments'])}段:
"""

    for seg in outline['segments']:
        script_prompt += f"""
段落 {seg['segment_id']}:
- 时长: 约{seg['estimated_duration_min']}分钟
- 焦点: {seg['content_focus']}
- 要点: {', '.join(seg['key_points'])}
"""

    script_prompt += """
【输出格式】
请输出JSON格式:
{
  "lines": [
    {"speaker": "Host A", "text": "..."},
    {"speaker": "Host B", "text": "..."}
  ],
  "word_count": 总字数,
  "estimated_duration_sec": 预估秒数
}

【要求】
1. Host A 是林肯，Host B 是林黛玉
2. 严格遵循各自persona的表达风格
3. 林肯用逻辑、案例、历史事实
4. 黛玉用诗词、隐喻、情感表达
5. 保持跨时空对话的文化张力
6. 每段之间要有自然的过渡
7. 全文约4000-5000字

请直接输出JSON，不要其他解释。
"""

    print("=" * 70)
    print("正在生成脚本...")
    print("=" * 70)
    print()

    # 调用API生成
    try:
        from src.volcano_client_requests import create_ark_client_requests

        api_key = os.getenv("DOUBAO_API_KEY")
        if not api_key:
            print("[ERROR] 需要设置 DOUBAO_API_KEY 环境变量")
            print()
            print("请先设置环境变量:")
            print("  set DOUBAO_API_KEY=your_api_key")
            return None

        client = create_ark_client_requests(api_key=api_key)

        result, usage = client.chat_completion(
            system_prompt=script_prompt,
            user_message="请生成这个跨时空播客的完整脚本。",
            temperature=0.7,
            max_tokens=8192
        )

        # 解析结果
        if isinstance(result, str):
            script_data = json.loads(result)
        else:
            script_data = result

        # 保存脚本
        os.makedirs('tests/persona-resource/output', exist_ok=True)
        with open('tests/persona-resource/output/cross_time_script.json', 'w', encoding='utf-8') as f:
            json.dump(script_data, f, ensure_ascii=False, indent=2)

        print(f"[OK] 脚本生成完成")
        print(f"  行数: {len(script_data['lines'])}")
        print(f"  字数: {script_data.get('word_count', 'N/A')}")
        print(f"  预估时长: {script_data.get('estimated_duration_sec', 'N/A')}秒")
        print()
        print("脚本已保存到: tests/persona-resource/output/cross_time_script.json")
        print()

        # 显示前10行预览
        print("=" * 70)
        print("脚本预览（前10行）")
        print("=" * 70)
        for line in script_data['lines'][:10]:
            speaker = line['speaker']
            text = line['text'][:60] + '...' if len(line['text']) > 60 else line['text']
            print(f"{speaker}: {text}")
        print("...")

        return script_data

    except Exception as e:
        print(f"[ERROR] 生成失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def generate_audio(script_data=None):
    """生成音频"""
    print()
    print("=" * 70)
    print("音频生成")
    print("=" * 70)
    print()

    if script_data is None:
        # 尝试加载已有脚本
        script_path = 'tests/persona-resource/output/cross_time_script.json'
        if not Path(script_path).exists():
            print(f"[ERROR] 脚本文件不存在: {script_path}")
            return False

        with open(script_path, 'r', encoding='utf-8') as f:
            script_data = json.load(f)

    # 分离两位主持人的台词
    host_a_lines = [line['text'] for line in script_data['lines'] if line['speaker'] == 'Host A']
    host_b_lines = [line['text'] for line in script_data['lines'] if line['speaker'] == 'Host B']

    print(f"Host A (林肯) 台词数: {len(host_a_lines)}")
    print(f"Host B (林黛玉) 台词数: {len(host_b_lines)}")
    print()

    # 配置语音
    voice_config = {
        'Host A': {  # 林肯 - 成熟男性，权威
            'voice_type': 'BV005',  # 磁性男声
            'speed': 1.0,
        },
        'Host B': {  # 林黛玉 - 年轻女性，柔弱
            'voice_type': 'BV001',  # 温柔女声
            'speed': 0.9,  # 稍慢，体现黛玉的慢性
        }
    }

    print("语音配置:")
    print(f"  林肯 (Host A): {voice_config['Host A']['voice_type']}, speed={voice_config['Host A']['speed']}")
    print(f"  黛玉 (Host B): {voice_config['Host B']['voice_type']}, speed={voice_config['Host B']['speed']}")
    print()

    print("[INFO] 音频生成需要TTS服务")
    print("[INFO] 如需生成音频，请确保:")
    print("  1. 已配置火山引擎TTS")
    print("  2. 有足够的API配额")
    print()

    # 这里可以接入TTS生成
    # from src.tts_controller import VolcanoTTSController
    # tts = VolcanoTTSController(api_key=os.getenv("DOUBAO_API_KEY"))
    # ...

    print("[OK] 音频生成配置完成（未实际调用TTS）")
    print()
    print("输出文件将保存到:")
    print("  tests/persona-resource/output/cross_time_host_a.mp3")
    print("  tests/persona-resource/output/cross_time_host_b.mp3")

    return True


def main():
    print("\n" + "=" * 70)
    print("跨时空播客生成器：林黛玉 × 林肯")
    print("=" * 70)
    print()

    # 检查persona文件
    if not Path('tests/persona-resource/output/daiyu_persona.json').exists():
        print("[ERROR] 请先运行 test_cross_time_podcast.py 设置persona")
        return 1

    # 生成脚本
    script = generate_script()

    if script:
        # 生成音频配置
        generate_audio(script)
        print()
        print("=" * 70)
        print("全部完成！")
        print("=" * 70)
        return 0
    else:
        print()
        print("=" * 70)
        print("脚本生成失败")
        print("=" * 70)
        return 1


if __name__ == "__main__":
    sys.exit(main())
