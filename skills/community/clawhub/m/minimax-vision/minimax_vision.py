#!/usr/bin/env python3
"""
MiniMax Vision - 图片理解工具
用法: python3 minimax_vision.py "图片路径" "问题"
"""
import json
import os
import sys

def call_mcp(image_path, prompt="描述这张图片的内容"):
    """调用 mcporter MCP 进行图片识别"""
    import subprocess
    
    # 构建命令
    cmd = [
        "mcporter", "call", "minimax.understand_image", "--args",
        json.dumps({
            "prompt": prompt,
            "image_source": image_path
        })
    ]
    
    # 设置环境变量
    env = os.environ.copy()
    env["PATH"] = "/Users/js/.local/bin:" + env.get("PATH", "")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
            env=env
        )
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 minimax_vision.py <图片路径> [问题]")
        sys.exit(1)
    
    image_path = sys.argv[1]
    prompt = sys.argv[2] if len(sys.argv) > 2 else "描述这张图片的内容"
    
    print(f"识别图片: {image_path}")
    print(f"问题: {prompt}")
    print("-" * 30)
    
    result = call_mcp(image_path, prompt)
    print(result)
