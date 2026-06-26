# -*- coding: utf-8 -*-
"""端到端测试：提取 Persona 并生成播客"""

import os
import sys
import json
import requests

os.chdir('d:/vscode/AI-podcast/ai-podcast-dual-host')
sys.path.insert(0, '.')

# 清理代理
for k in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'ALL_PROXY']:
    os.environ.pop(k, None)

# API 配置
API_KEY = 'bea84e03-aa7f-4d9c-9a24-60f70493da11'
MODEL = 'ep-20260330183110-h92rj'
API_BASE = 'https://ark.cn-beijing.volces.com/api/v3'

session = requests.Session()
session.trust_env = False
session.proxies = {}
session.headers.update({
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
})

def call_api(system_prompt, user_message, temperature=0.7, max_tokens=4096):
    """调用火山引擎 API"""
    payload = {
        'model': MODEL,
        'messages': [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_message}
        ],
        'temperature': temperature,
        'max_tokens': max_tokens
    }
    response = session.post(f'{API_BASE}/chat/completions', json=payload, timeout=300)
    response.raise_for_status()
    data = response.json()
    content = data['choices'][0]['message']['content']
    return content

def extract_persona(text, name_hint=""):
    """从文本提取 Persona"""
    with open('agents/persona-extractor.md', 'r', encoding='utf-8') as f:
        system_prompt = f.read()

    user_message = f'''请从以下材料提取Persona：

【用户补充说明】
{name_hint if name_hint else "无"}

【材料内容】
{text[:6000]}

请只输出JSON，不要其他解释。'''

    content = call_api(system_prompt, user_message, temperature=0.5, max_tokens=2048)

    # 解析 JSON
    try:
        return json.loads(content)
    except:
        # 清理 markdown
        if '```json' in content:
            content = content.split('```json')[1].split('```')[0]
        elif '```' in content:
            content = content.split('```')[1].split('```')[0]
        return json.loads(content.strip())

def generate_script(daiyu_persona, lincoln_persona, topic):
    """生成播客脚本"""
    with open('agents/script-generator.md', 'r', encoding='utf-8') as f:
        system_prompt = f.read()

    # 构建输入
    script_prompt = f"""你是播客脚本生成器。基于以下信息生成双人对话脚本。

【双主持人Persona配置】

主持人A - 林肯：
- 身份: {lincoln_persona['identity']['archetype']}
- 核心驱动力: {lincoln_persona['identity']['core_drive']}
- 互动方式: {lincoln_persona['identity']['chemistry']}
- 语速: {lincoln_persona['expression']['pace']}
- 口头禅: {', '.join(lincoln_persona['expression']['signature_phrases'][:3])}
- 态度: {lincoln_persona['expression']['attitude']}

主持人B - 林黛玉：
- 身份: {daiyu_persona['identity']['archetype']}
- 核心驱动力: {daiyu_persona['identity']['core_drive']}
- 互动方式: {daiyu_persona['identity']['chemistry']}
- 语速: {daiyu_persona['expression']['pace']}
- 口头禅: {', '.join(daiyu_persona['expression']['signature_phrases'][:3])}
- 态度: {daiyu_persona['expression']['attitude']}

【话题】
{topic}

【大纲】
1. 开场：两位来自不同时空的灵魂初次相遇
2. 探讨"自由"的含义：林肯的政治自由 vs 黛玉的精神自由
3. 探讨"命运"：是可以抗争的还是注定的？
4. 跨时空的共鸣与告别

【可用记忆 - 林肯】
{chr(10).join([f"- [{m['title']}] {m['content'][:50]}..." for m in lincoln_persona['memory_seed'][:3]])}

【可用记忆 - 林黛玉】
{chr(10).join([f"- [{m['title']}] {m['content'][:50]}..." for m in daiyu_persona['memory_seed'][:3]])}

【输出格式】
请输出JSON格式:
{{
  "lines": [
    {{"speaker": "A", "text": "..."}},
    {{"speaker": "B", "text": "..."}}
  ],
  "word_count": 总字数,
  "estimated_duration_sec": 预估秒数
}}

【要求】
1. Host A 是林肯，Host B 是林黛玉
2. 严格遵循各自persona的表达风格
3. 林肯用逻辑、案例、历史事实
4. 黛玉用诗词、隐喻、情感表达
5. 全文约3000-4000字
6. 对话自然流畅，有情感交流

请直接输出JSON。"""

    content = call_api(system_prompt, script_prompt, temperature=0.8, max_tokens=8192)

    try:
        return json.loads(content)
    except:
        if '```json' in content:
            content = content.split('```json')[1].split('```')[0]
        elif '```' in content:
            content = content.split('```')[1].split('```')[0]
        return json.loads(content.strip())

def main():
    print('=' * 70)
    print('端到端测试：林黛玉 × 林肯 跨时空对话')
    print('=' * 70)
    print()

    # 读取文档
    with open('tests/persona-resource/林黛玉.txt', 'r', encoding='utf-8') as f:
        daiyu_text = f.read()
    with open('tests/persona-resource/林肯.txt', 'r', encoding='utf-8') as f:
        lincoln_text = f.read()

    # Step 1: 提取 Persona
    print('Step 1: 提取林黛玉 Persona')
    print('-' * 70)
    daiyu_persona = extract_persona(daiyu_text, "林黛玉")
    print(f"  Name: {daiyu_persona['identity']['name']}")
    print(f"  Archetype: {daiyu_persona['identity']['archetype']}")
    print(f"  Core Drive: {daiyu_persona['identity']['core_drive'][:50]}...")
    print(f"  Phrases: {daiyu_persona['expression']['signature_phrases']}")
    print(f"  Memory: {len(daiyu_persona['memory_seed'])} items")
    print()

    print('Step 2: 提取林肯 Persona')
    print('-' * 70)
    lincoln_persona = extract_persona(lincoln_text, "林肯")
    print(f"  Name: {lincoln_persona['identity']['name']}")
    print(f"  Archetype: {lincoln_persona['identity']['archetype']}")
    print(f"  Core Drive: {lincoln_persona['identity']['core_drive'][:50]}...")
    print(f"  Phrases: {lincoln_persona['expression']['signature_phrases']}")
    print(f"  Memory: {len(lincoln_persona['memory_seed'])} items")
    print()

    # 保存 Persona
    os.makedirs('tests/persona-resource/output', exist_ok=True)
    with open('tests/persona-resource/output/daiyu_e2e.json', 'w', encoding='utf-8') as f:
        json.dump(daiyu_persona, f, ensure_ascii=False, indent=2)
    with open('tests/persona-resource/output/lincoln_e2e.json', 'w', encoding='utf-8') as f:
        json.dump(lincoln_persona, f, ensure_ascii=False, indent=2)
    print('[OK] Persona 已保存')
    print()

    # Step 3: 生成脚本
    print('Step 3: 生成播客脚本')
    print('-' * 70)
    topic = "自由与命运：当东方诗魂遇见西方解放者"
    script = generate_script(daiyu_persona, lincoln_persona, topic)

    print(f"  Lines: {len(script['lines'])}")
    print(f"  Word count: {script.get('word_count', 'N/A')}")
    print(f"  Duration: {script.get('estimated_duration_sec', 'N/A')} sec")
    print()

    # 保存脚本
    with open('tests/persona-resource/output/cross_time_script_e2e.json', 'w', encoding='utf-8') as f:
        json.dump(script, f, ensure_ascii=False, indent=2)
    print('[OK] 脚本已保存')
    print()

    # 显示预览
    print('=' * 70)
    print('脚本预览（前15行）')
    print('=' * 70)
    for line in script['lines'][:15]:
        speaker = '林肯' if line['speaker'] == 'A' else '黛玉'
        text = line['text'][:60] + '...' if len(line['text']) > 60 else line['text']
        print(f"{speaker}: {text}")
    print('...')
    print()

    # 保存文本版本
    with open('tests/persona-resource/output/cross_time_script.txt', 'w', encoding='utf-8') as f:
        f.write(f'话题: {topic}\n')
        f.write('=' * 70 + '\n\n')
        for line in script['lines']:
            speaker = '林肯' if line['speaker'] == 'A' else '黛玉'
            f.write(f'{speaker}: {line["text"]}\n\n')

    print('[OK] 文本版脚本已保存')
    print()
    print('=' * 70)
    print('端到端测试完成！')
    print('=' * 70)
    print()
    print('输出文件:')
    print('  - tests/persona-resource/output/daiyu_e2e.json')
    print('  - tests/persona-resource/output/lincoln_e2e.json')
    print('  - tests/persona-resource/output/cross_time_script_e2e.json')
    print('  - tests/persona-resource/output/cross_time_script.txt')

if __name__ == '__main__':
    main()
