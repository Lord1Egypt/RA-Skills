#!/usr/bin/env python3
"""DeepSeek V4 转录稿清洗：去噪、分段、修正识别错误"""
import sys, json, os
from openai import OpenAI

def clean_transcript(raw_text: str) -> str:
    """调用 DeepSeek 清洗转录稿"""
    api_key = os.environ.get("DEEPSEEK_API_KEY", "")
    if not api_key:
        return raw_text  # fallback: 返回原文
    
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    
    prompt = f"""你是一个语音转录文稿的清洗助手。请对以下语音识别结果进行清洗：

1. 修正明显的识别错误（同音错字、断句错误）
2. 恢复合理的标点符号和分段
3. 去除重复的句子和语气词
4. 保留所有实质性内容
5. 输出为清晰的信息结构：核心观点→章节→要点

原始转录稿：
{raw_text}

清洗后的文稿："""
    
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=4000
    )
    return resp.choices[0].message.content

if __name__ == "__main__":
    raw = sys.stdin.read()
    cleaned = clean_transcript(raw)
    print(cleaned)
