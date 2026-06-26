#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests>=2.28.0",
# ]
# ///
"""
grsai nano-banana 图片生成脚本

使用 grsai 平台的 nano-banana 系列模型生成图片。
支持文生图、图生图，异步轮询模式。

Usage:
    uv run generate.py --prompt "描述" --api-key "sk-xxx" [选项]

示例:
    # 文生图 - 头像
    uv run generate.py --prompt "可爱柴犬头像" --model "nano-banana-pro" --aspect-ratio "1:1" --api-key "sk-xxx"
    
    # 图生图
    uv run generate.py --prompt "油画风格" --input-image "https://example.com/photo.png" --api-key "sk-xxx"
"""

import argparse
import base64
import io
import re
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: requests 库未安装", file=sys.stderr)
    print("Run: uv run pip install requests", file=sys.stderr)
    sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser(
        description="grsai nano-banana 图片生成",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 文生图 - 头像
  uv run generate.py --prompt "可爱柴犬头像" --model "nano-banana-pro" --aspect-ratio "1:1" --api-key "sk-xxx"
  
  # 图生图
  uv run generate.py --prompt "油画风格" --input-image "https://example.com/photo.png" --api-key "sk-xxx"
  
  # 自定义输出
  uv run generate.py --prompt "风景" --filename "my-image.png" --output-dir "/path/to/dir" --api-key "sk-xxx"
        """
    )
    
    # 必填参数
    parser.add_argument("--prompt", "-p", required=True, help="提示词，描述想要生成的内容")
    parser.add_argument("--api-key", "-k", required=True, help="grsai API Key")
    
    # 选填参数
    parser.add_argument("--filename", "-f", default=None, help="输出文件名（默认自动生成：yyyymmdd_模型_描述.png）")
    parser.add_argument("--output-dir", default="./generated", help="输出目录（默认：./generated，相对于当前目录）")
    parser.add_argument("--input-image", "-i", action="append", dest="input_images", metavar="URL",
                        help="参考图 URL（图生图时使用，可多个）")
    parser.add_argument("--resolution", "-r", choices=["1K", "2K", "4K"], default="1K",
                        help="输出分辨率：1K（默认）、2K、4K")
    parser.add_argument("--aspect-ratio", "-a", default="auto",
                        help="宽高比：auto（默认）、1:1、16:9、9:16、4:3、3:4、3:2、2:3、5:4、4:5、21:9")
    parser.add_argument("--model", "-m", default="nano-banana-pro",
                        help="模型：nano-banana-pro（默认）、nano-banana-fast、nano-banana-2 等")
    
    # 轮询参数
    parser.add_argument("--initial-wait", type=int, default=300,
                        help="首次轮询前等待时间（秒），默认 300 = 5 分钟")
    parser.add_argument("--poll-interval", type=int, default=60,
                        help="轮询间隔（秒），默认 60 = 1 分钟")
    parser.add_argument("--max-retries", type=int, default=3,
                        help="最大轮询次数，默认 3 次")
    
    # API 参数
    parser.add_argument("--base-url", default="https://grsai.dakka.com.cn",
                        help="grsai API 基础 URL（默认：https://grsai.dakka.com.cn）")
    
    return parser.parse_args()


def generate_filename(args):
    """生成输出文件名"""
    if args.filename:
        return args.filename
    
    import datetime
    import os
    
    date_str = datetime.datetime.now().strftime("%Y%m%d")
    
    # 简化模型名
    model_short = args.model
    if "pro-4k-vip" in args.model:
        model_short = "pro-4k-vip"
    elif "pro-vip" in args.model:
        model_short = "pro-vip"
    elif "pro-vt" in args.model:
        model_short = "pro-vt"
    elif "pro-cl" in args.model:
        model_short = "pro-cl"
    elif "pro" in args.model:
        model_short = "pro"
    elif "fast" in args.model:
        model_short = "fast"
    elif "nano-banana-2" in args.model:
        model_short = "banana-2"
    
    # 清理提示词（保留中文、英文、数字，其他替换为下划线）
    prompt_clean = re.sub(r'[^\w\u4e00-\u9fff]', '_', args.prompt)[:20].strip('_')
    
    return f"{date_str}_{model_short}_{prompt_clean}.png"


def submit_task(args):
    """提交生图任务"""
    url = f"{args.base_url}/v1/draw/nano-banana"
    
    payload = {
        "model": args.model,
        "prompt": args.prompt,
        "imageSize": args.resolution,
        "aspectRatio": args.aspect_ratio,
        "webHook": "-1",  # 立即返回 task_id
        "shutProgress": False
    }
    
    # 添加参考图
    if args.input_images:
        payload["urls"] = args.input_images
    
    headers = {
        "Authorization": f"Bearer {args.api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        if result.get("code") != 0:
            print(f"❌ 提交失败：{result.get('msg', 'Unknown error')}", file=sys.stderr)
            sys.exit(1)
        
        task_id = result.get("data", {}).get("id")
        if not task_id:
            print(f"❌ 未返回 task_id", file=sys.stderr)
            print(f"响应：{result}", file=sys.stderr)
            sys.exit(1)
        
        return task_id
        
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络错误：{e}", file=sys.stderr)
        if hasattr(e, 'response') and e.response is not None:
            print(f"响应：{e.response.text}", file=sys.stderr)
        sys.exit(1)


def poll_result(args, task_id):
    """轮询生图结果"""
    url = f"{args.base_url}/v1/draw/result"
    headers = {
        "Authorization": f"Bearer {args.api_key}",
        "Content-Type": "application/json"
    }
    
    for attempt in range(1, args.max_retries + 1):
        print(f"🔄 第 {attempt}/{args.max_retries} 次轮询...")
        
        try:
            response = requests.post(url, json={"id": task_id}, headers=headers, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            if result.get("code") != 0:
                print(f"⚠️  查询失败：{result.get('msg', 'Unknown error')}")
                if attempt < args.max_retries:
                    time.sleep(args.poll_interval)
                    continue
                return None
            
            data = result.get("data", {})
            status = data.get("status")
            results = data.get("results", [])
            image_url = results[0].get("url") if results else None
            
            if status == "succeeded" and image_url:
                print(f"✅ 生成成功！")
                return image_url
            elif status == "failed" or status == "error":
                error_msg = data.get("error") or data.get("failure_reason", "Unknown error")
                print(f"❌ 任务失败：{error_msg}", file=sys.stderr)
                sys.exit(1)
            else:
                print(f"⏳ 状态：{status} 或 {data.get('progress', '?')}%")
                if attempt < args.max_retries:
                    print(f"   等待 {args.poll_interval}秒后重试...")
                    time.sleep(args.poll_interval)
                    
        except requests.exceptions.RequestException as e:
            print(f"⚠️  轮询错误：{e}")
            if attempt < args.max_retries:
                time.sleep(args.poll_interval)
        except Exception as e:
            print(f"⚠️  处理错误：{e}")
            if attempt < args.max_retries:
                time.sleep(args.poll_interval)
    
    print(f"❌ 超过最大轮询次数，任务未完成", file=sys.stderr)
    return None


def download_image(image_url, output_path):
    """下载图片"""
    try:
        response = requests.get(image_url, timeout=120)
        response.raise_for_status()
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        return True
        
    except Exception as e:
        print(f"❌ 下载失败：{e}", file=sys.stderr)
        return False


def main():
    args = parse_args()
    
    # 生成输出路径
    filename = generate_filename(args)
    output_path = Path(args.output_dir) / filename
    
    print("=" * 60)
    print("🎨 grsai nano-banana 图片生成")
    print("=" * 60)
    print(f"模型：{args.model}")
    print(f"提示词：{args.prompt}")
    print(f"分辨率：{args.resolution}")
    print(f"比例：{args.aspect_ratio}")
    if args.input_images:
        print(f"参考图：{len(args.input_images)} 张")
    print(f"输出：{output_path}")
    print("=" * 60)
    
    # 步骤 1: 提交任务
    print("📤 提交任务...")
    task_id = submit_task(args)
    print(f"✅ 任务 ID: {task_id}")
    
    # 步骤 2: 等待并轮询
    print(f"⏳ 等待 {args.initial_wait}秒（约{args.initial_wait//60}分钟）后开始轮询...")
    print("   （grsai 生图需要时间，请耐心等待）")
    time.sleep(args.initial_wait)
    
    print("🔍 开始轮询结果...")
    image_url = poll_result(args, task_id)
    
    if not image_url:
        sys.exit(1)
    
    # 步骤 3: 下载图片
    print(f"📥 下载图片：{image_url}")
    if download_image(image_url, output_path):
        print("=" * 60)
        print(f"✅ 完成！图片已保存：{output_path}")
        print(f"MEDIA: {output_path}")
        print("=" * 60)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
