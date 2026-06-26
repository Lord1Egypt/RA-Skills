#!/usr/bin/env python3
"""
图片理解 - 支持多种多模态模型
"""
import os
import json
import base64
import subprocess
import sys

def understand_with_minimax(image_path, prompt):
    """MiniMax VLM"""
    API_KEY = os.environ.get("MINIMAX_API_KEY", "")
    API_HOST = os.environ.get("MINIMAX_API_HOST", "https://api.minimaxi.com")
    
    if not API_KEY:
        return "[错误] 请设置 MINIMAX_API_KEY 环境变量"
    
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")
    
    ext = os.path.splitext(image_path)[1].lower()
    media_type = f"image/{ext[1:]}"
    if media_type == "image/jpg":
        media_type = "image/jpeg"
    
    image_url = f"data:{media_type};base64,{image_data}"
    payload = {"prompt": prompt, "image_url": image_url}
    
    cmd = [
        "curl", "-s", "--max-time", "30",
        f"{API_HOST}/v1/coding_plan/vlm",
        "-H", f"Authorization: Bearer {API_KEY}",
        "-H", "Content-Type: application/json",
        "-d", json.dumps(payload)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=35)
    data = json.loads(result.stdout)
    
    if data.get("base_resp", {}).get("status_code") == 0:
        return data.get("content", "")
    return f"[失败: {data.get('base_resp', {}).get('status_msg', '未知错误')}]"

def understand_with_openai(image_path, prompt):
    """OpenAI GPT-4V"""
    API_KEY = os.environ.get("OPENAI_API_KEY", "")
    
    if not API_KEY:
        return "[错误] 请设置 OPENAI_API_KEY 环境变量"
    
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")
    
    import requests
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_data}"}}
                ]
            }
        ],
        "max_tokens": 1000
    }
    
    resp = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=60)
    data = resp.json()
    
    if "choices" in data and data["choices"]:
        return data["choices"][0]["message"]["content"]
    return f"[失败: {data.get('error', {}).get('message', '未知错误')}]"

def understand_with_anthropic(image_path, prompt):
    """Anthropic Claude Vision"""
    API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
    
    if not API_KEY:
        return "[错误] 请设置 ANTHROPIC_API_KEY 环境变量"
    
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")
    
    import requests
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01"
    }
    
    payload = {
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 1000,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": image_data}}
                ]
            }
        ]
    }
    
    resp = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=payload, timeout=60)
    data = resp.json()
    
    if "content" in data:
        for block in data["content"]:
            if block.get("type") == "text":
                return block["text"]
    return f"[失败: {data.get('error', {}).get('message', '未知错误')}]"

def understand_image(image_path, model="minimax", prompt="直接描述这张图片的业务含义和数据内容，不要罗列元素位置关系"):
    """根据模型调用对应的理解函数"""
    if model == "openai":
        return understand_with_openai(image_path, prompt)
    elif model == "anthropic":
        return understand_with_anthropic(image_path, prompt)
    else:
        return understand_with_minimax(image_path, prompt)

def main():
    if len(sys.argv) < 2:
        print("用法: python understand_image.py <图片路径> [model] [prompt]")
        print("model: minimax (默认), openai, anthropic")
        sys.exit(1)
    
    image_path = sys.argv[1]
    model = sys.argv[2] if len(sys.argv) > 2 else "minimax"
    prompt = sys.argv[3] if len(sys.argv) > 3 else "直接描述这张图片的业务含义和数据内容，不要罗列元素位置关系"
    
    result = understand_image(image_path, model, prompt)
    print(result)

if __name__ == "__main__":
    main()
