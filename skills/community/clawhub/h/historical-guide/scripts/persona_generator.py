#!/usr/bin/env python3
"""
动态生成人物画像
当召唤的人物不在库中时，自动生成画像
"""

from __future__ import annotations

import json
import sys
import requests
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from api_config import load_api_config
from character_loader import CharacterLoader


def call_api(config: dict, system_prompt: str, user_prompt: str, temperature: float, max_tokens: int) -> str:
    """通用API调用函数"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config['api_key']}"
    }
    
    payload = {
        "model": config['model'],
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    response = requests.post(
        config['api_base'],
        headers=headers,
        json=payload
    )
    
    response.raise_for_status()
    data = response.json()
    return data['choices'][0]['message']['content']


def check_if_positive_figure(character_name: str, config: dict) -> bool:
    """通过API判断是否为适合加载的历史人物"""
    system_prompt = """你是一个历史人物评判专家。
请判断用户输入的历史人物是否适合作为博物馆伴游讲解人物。

适合的人物标准：
1. 中国历史上的正面人物或有积极贡献的人物
2. 公认的文化名人、思想家、艺术家、科学家等
3. 在民间有正面形象和影响力的人物

不适合的人物：
1. 历史上有较大争议的人物（如权臣、奸臣等）
2. 可能在讲解中产生不当言论的人物
3. 未被广泛认可的历史人物

请只回答"适合"或"不适合"，不要做过多解释。"""
    
    user_prompt = f"请判断「{character_name}」是否适合作为博物馆伴游讲解人物？"
    
    result = call_api(config, system_prompt, user_prompt, 0.3, 50)
    return "适合" in result


def generate_persona(character_name: str) -> dict:
    """生成人物画像"""
    config = load_api_config()
    
    is_positive = check_if_positive_figure(character_name, config)
    
    if not is_positive:
        raise ValueError(f"抱歉，暂无法为「{character_name}」生成画像。或许可以尝试其他著名的历史人物，如王羲之、陶渊明等。")
    
    system_prompt = """你是一个中国历史人物画像生成专家。

请根据给定的历史人物姓名，生成符合以下JSON结构的人物画像：

{
  "id": "人物拼音缩写（小写）",
  "name": "姓名",
  "title": "尊称/称号",
  "era": "朝代",
  "dynasty_context": "具体时期",
  "personality": {
    "traits": ["性格特点1", "性格特点2", "..."],
    "values": ["核心价值观1", "核心价值观2", "..."]
  },
  "speaking_style": {
    "tone": "说话语气特点",
    "vocabulary": ["常用词汇1", "常用词汇2", "..."],
    "sentence_patterns": ["典型句式1", "典型句式2", "..."],
    "moods": ["常见情绪1", "常见情绪2"]
  },
  "knowledge": {
    "periods": ["活跃时期1", "..."],
    "domains": ["擅长领域1", "..."],
    "relevant_artifacts": ["可能相关的文物类型1", "..."]
  },
  "greeting": "经典问候语（符合人物性格）",
  "farewell": "告别语（符合人物性格）",
  "expertise": ["擅长讲解的文物类型1", "..."],
  "famous_works": ["代表作品1", "..."],
  "self_intro": "自我介绍（符合人物性格的第一人称介绍）"
}

【生成规则】
1. id使用姓名拼音缩写（小写），如"王羲之"→"wangxizhi"
2. 只生成中国历史上公认的正面的历史人物
3. personality中的traits不超过6个
4. speaking_style中的vocabulary不超过8个
5. expertise中的文物类型必须是该人物确实擅长的领域
6. famous_works必须是该人物真实创作的作品
7. greeting和farewell要符合人物的说话风格

请直接输出JSON，不要有其他内容。"""

    user_prompt = f"请生成历史人物「{character_name}」的人物画像JSON"
    
    result = call_api(config, system_prompt, user_prompt, 0.7, 1500)
    
    # 优化JSON解析逻辑
    result = result.strip()
    if "```json" in result:
        result = result.split("```json")[1].split("```")[0].strip()
    elif "```" in result:
        result = result.split("```")[1].split("```")[0].strip()
    
    # 尝试解析JSON，如果失败，尝试提取JSON部分
    try:
        persona = json.loads(result)
    except json.JSONDecodeError:
        # 尝试找到JSON的开始和结束位置
        start_idx = result.find('{')
        end_idx = result.rfind('}')
        if start_idx != -1 and end_idx != -1:
            json_str = result[start_idx:end_idx+1]
            try:
                persona = json.loads(json_str)
            except json.JSONDecodeError:
                raise ValueError("生成的内容不是有效的JSON格式")
        else:
            raise ValueError("生成的内容不是有效的JSON格式")
    
    required_fields = ["id", "name", "title", "era", "personality", "speaking_style", "expertise", "greeting", "farewell", "self_intro"]
    for field in required_fields:
        if field not in persona:
            raise ValueError(f"生成的人物画像缺少必要字段: {field}")
    
    return persona


def main():
    if len(sys.argv) < 2:
        print("用法: python3 persona_generator.py <人物名称>")
        sys.exit(1)
    
    character_name = sys.argv[1]
    
    loader = CharacterLoader()
    existing = loader.load_character(character_name)
    
    if existing:
        print(f"✅ 人物「{character_name}」已存在于库中")
        print(json.dumps(existing, ensure_ascii=False, indent=2))
        return
    
    try:
        print(f"🔄 正在为「{character_name}」生成画像...")
        persona = generate_persona(character_name)
        
        if loader.save_persona(persona):
            print(f"✅ 人物「{character_name}」画像生成成功并已保存！")
            print("\n生成的人物画像：")
            print(json.dumps(persona, ensure_ascii=False, indent=2))
        else:
            print("⚠️ 画像生成成功，但保存失败")
            print(json.dumps(persona, ensure_ascii=False, indent=2))
            
    except Exception as e:
        print(f"❌ 生成失败: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
