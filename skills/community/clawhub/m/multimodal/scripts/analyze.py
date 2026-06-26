#!/usr/bin/env python3
"""
GLM-4.6V Multimodal Analysis Script

Usage:
    python analyze.py --type image --input <url> --prompt "描述这张图片"
    python analyze.py --type video --input <url> --prompt "视频讲了什么"
    python analyze.py --type file --input <url> --prompt "总结这个文档"
"""

import argparse
import json
import os
import sys
import base64
import mimetypes
from pathlib import Path

try:
    import requests
except ImportError:
    print("需要安装requests: pip install requests")
    sys.exit(1)

API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
MODEL = "glm-4.6v"
MAX_TOKENS = 4096


def get_api_key():
    """获取API密钥"""
    api_key = os.environ.get("ZHIPU_API_KEY")
    if not api_key:
        print("错误: 未设置 ZHIPU_API_KEY 环境变量")
        print("请运行: export ZHIPU_API_KEY='your-api-key'")
        sys.exit(1)
    return api_key


def is_local_file(path):
    """检查是否为本地文件"""
    return os.path.exists(path) and not path.startswith(("http://", "https://"))


def get_mime_type(path):
    """获取文件MIME类型"""
    mime_type, _ = mimetypes.guess_type(path)
    return mime_type or "application/octet-stream"


def file_to_data_url(path):
    """将本地文件转换为data URL"""
    mime_type = get_mime_type(path)
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime_type};base64,{data}"


def build_content(input_type, input_value, prompt):
    """构建消息内容"""
    content = []
    
    # 添加媒体内容
    if input_type == "image":
        if is_local_file(input_value):
            url = file_to_data_url(input_value)
        else:
            url = input_value
        content.append({
            "type": "image_url",
            "image_url": {"url": url}
        })
    elif input_type == "video":
        if is_local_file(input_value):
            print("警告: 视频文件建议使用公网URL，本地文件可能过大")
            url = file_to_data_url(input_value)
        else:
            url = input_value
        content.append({
            "type": "video_url",
            "video_url": {"url": url}
        })
    elif input_type == "file":
        if is_local_file(input_value):
            url = file_to_data_url(input_value)
        else:
            url = input_value
        content.append({
            "type": "file_url",
            "file_url": {"url": url}
        })
    
    # 添加文本提示
    content.append({
        "type": "text",
        "text": prompt
    })
    
    return content


def analyze(input_type, input_value, prompt, thinking=False, stream=False):
    """调用GLM-4.6V进行分析"""
    api_key = get_api_key()
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    messages = [{
        "role": "user",
        "content": build_content(input_type, input_value, prompt)
    }]
    
    payload = {
        "model": MODEL,
        "messages": messages,
        "max_tokens": MAX_TOKENS
    }
    
    if thinking:
        payload["thinking"] = {"type": "enabled"}
    
    if stream:
        payload["stream"] = True
        return stream_response(headers, payload)
    else:
        return sync_response(headers, payload)


def sync_response(headers, payload):
    """同步请求"""
    response = requests.post(API_URL, headers=headers, json=payload, timeout=120)
    
    if response.status_code != 200:
        print(f"API错误: {response.status_code}")
        print(response.text)
        sys.exit(1)
    
    result = response.json()
    
    if "choices" in result and len(result["choices"]) > 0:
        return result["choices"][0]["message"]["content"]
    else:
        return json.dumps(result, ensure_ascii=False, indent=2)


def stream_response(headers, payload):
    """流式请求"""
    response = requests.post(API_URL, headers=headers, json=payload, stream=True, timeout=120)
    
    if response.status_code != 200:
        print(f"API错误: {response.status_code}")
        print(response.text)
        sys.exit(1)
    
    full_content = ""
    for line in response.iter_lines():
        if line:
            line = line.decode("utf-8")
            if line.startswith("data: "):
                data = line[6:]
                if data == "[DONE]":
                    break
                try:
                    chunk = json.loads(data)
                    if "choices" in chunk and len(chunk["choices"]) > 0:
                        delta = chunk["choices"][0].get("delta", {})
                        content = delta.get("content", "")
                        if content:
                            print(content, end="", flush=True)
                            full_content += content
                except json.JSONDecodeError:
                    continue
    
    print()  # 换行
    return full_content


def main():
    parser = argparse.ArgumentParser(
        description="GLM-4.6V 多模态分析工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --type image --input photo.jpg --prompt "描述这张图片"
  %(prog)s --type video --input https://example.com/video.mp4 --prompt "视频讲了什么"
  %(prog)s --type file --input document.pdf --prompt "总结这个文档" --thinking
        """
    )
    
    parser.add_argument("--type", "-t", required=True, 
                        choices=["image", "video", "file"],
                        help="输入类型: image, video, file")
    parser.add_argument("--input", "-i", required=True,
                        help="输入文件路径或URL")
    parser.add_argument("--prompt", "-p", required=True,
                        help="分析提示词")
    parser.add_argument("--thinking", action="store_true",
                        help="启用深度思考模式")
    parser.add_argument("--stream", "-s", action="store_true",
                        help="流式输出")
    
    args = parser.parse_args()
    
    # 验证输入
    if args.type == "video" and is_local_file(args.input):
        file_size = os.path.getsize(args.input)
        if file_size > 50 * 1024 * 1024:  # 50MB
            print("警告: 视频文件过大，建议使用公网URL")
    
    result = analyze(
        input_type=args.type,
        input_value=args.input,
        prompt=args.prompt,
        thinking=args.thinking,
        stream=args.stream
    )
    
    if not args.stream:
        print(result)


if __name__ == "__main__":
    main()
