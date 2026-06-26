#!/usr/bin/env python3
"""
GrsAI Nano Banana Pro 图片生成脚本

API文档: https://grsai.ai/zh/dashboard/documents/nano-banana

使用方式:
    export GRSAAI_API_KEY='your-api-key'
    python skills/grs-image/scripts/grs_image.py "一只可爱的橘猫" -o output.png
"""

import sys
import os
import json
import time
import requests
import argparse
from pathlib import Path


API_KEY = os.environ.get("GRSAAI_API_KEY", "")
BASE_URL = "https://grsai.dakka.com.cn"


def generate_image(prompt, output_path="output.png", ratio="auto", size="1K",
                   model="nano-banana-pro", urls=None):
    """调用 GrsAI Nano Banana Pro API 生成图片"""
    
    if not API_KEY:
        print("错误：请设置环境变量 GRSAAI_API_KEY")
        print("  export GRSAAI_API_KEY='your-api-key'")
        return None
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # 构造请求
    payload = {
        "model": model,
        "prompt": prompt,
        "aspectRatio": ratio,
        "imageSize": size,
    }
    
    if urls:
        payload["urls"] = urls if isinstance(urls, list) else [urls]
    
    print(f"正在生成图片...")
    print(f"Prompt: {prompt}")
    print(f"Ratio: {ratio}")
    print(f"Size: {size}")
    if urls:
        print(f"参考图: {urls}")
    
    try:
        # 发起请求（API返回SSE流，逐行解析）
        response = requests.post(
            f"{BASE_URL}/v1/draw/nano-banana",
            headers=headers,
            json=payload,
            timeout=60,
            stream=True
        )
        
        # SSE格式：每行以"data: "开头，取第一个有效data行
        result = None
        for line in response.iter_lines():
            if line:
                decoded = line.decode('utf-8')
                if decoded.startswith('data: '):
                    result = json.loads(decoded[6:])
                    break
        
        if result is None:
            print(f"请求失败: 响应为空")
            return None
        
        task_id = result.get("id")
        if not task_id:
            print(f"请求失败: 响应中无任务ID")
            return None
        
        print(f"任务ID: {task_id}")
        
        # 轮询获取结果
        result_url = f"{BASE_URL}/v1/draw/result"
        
        for i in range(60):  # 最多等120秒
            time.sleep(2)
            
            result_resp = requests.post(
                result_url,
                headers=headers,
                json={"id": task_id},
                timeout=60
            )
            result_data = result_resp.json()
            
            if result_data.get("code") != 0:
                print(f"\n轮询失败: {result_data.get('msg')}")
                return None
            
            data = result_data.get("data", {})
            progress = data.get("progress", 0)
            status = data.get("status", "")
            
            print(f"\r生成中... {progress}%", end="", flush=True)
            
            if status == "succeeded":
                results = data.get("results", [])
                if results:
                    image_url = results[0].get("url")
                    print(f"\n图片URL: {image_url}")
                    
                    # 下载图片
                    img_resp = requests.get(image_url, timeout=60)
                    with open(output_path, "wb") as f:
                        f.write(img_resp.content)
                    print(f"已保存: {output_path}")
                    return output_path
                else:
                    print(f"\n生成成功但无图片URL")
                    return None
            
            elif status == "failed":
                reason = data.get("failure_reason", "")
                error = data.get("error", "")
                print(f"\n生成失败: {reason} {error}")
                return None
        
        print("\n图片因API生成较慢，稍后再试。")
        return None
        
    except Exception as e:
        print(f"请求失败: {e}")
        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GrsAI Nano Banana Pro 图片生成")
    parser.add_argument("prompt", help="图片描述")
    parser.add_argument("--output", "-o", default="output.png", help="输出文件")
    parser.add_argument("--ratio", "-r", default="auto",
                        help="宽高比: auto/1:1/16:9/9:16/4:3/3:4/3:2/2:3/5:4/4:5/21:9 (默认: auto)")
    parser.add_argument("--size", "-s", default="1K",
                        help="分辨率: 1K/2K/4K (默认: 1K)")
    parser.add_argument("--model", "-m", default="nano-banana-pro",
                        choices=[
                            "nano-banana-pro", "nano-banana-pro-vt", "nano-banana-pro-cl",
                            "nano-banana-pro-vip", "nano-banana-pro-4k-vip",
                            "nano-banana-fast", "nano-banana",
                            "nano-banana-2", "nano-banana-2-cl", "nano-banana-2-4k-cl"
                        ],
                        help="模型选择 (默认: nano-banana-pro)")
    parser.add_argument("--urls", "-u", default=None,
                        help="参考图片URL (图生图用，支持URL或Base64)")
    
    args = parser.parse_args()
    
    # 处理参考图URLs
    urls = None
    if args.urls:
        urls = [u.strip() for u in args.urls.split(',') if u.strip()]
    
    result = generate_image(
        args.prompt,
        args.output,
        args.ratio,
        args.size,
        args.model,
        urls
    )
    
    if result:
        print(f"\n完成: {result}")
    else:
        sys.exit(1)
