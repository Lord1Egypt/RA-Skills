#!/usr/bin/env python3
"""
BizyAir 异步分镜图生成完整流程示例

使用方法:
1. 设置环境变量: export BIZYAIR_API_KEY="your_key"
2. 运行: python scripts/storyboard.py
"""

import time
import requests
import os
import sys
import argparse

# API 配置
BASE_URL = "https://api.bizyair.cn/w/v1/webapp/task/openapi"
WEB_APP_ID = 38223

# 模特提示词（当检测到人物相关关键词时自动追加）
MODEL_SUFFIX = (
    ",漏斗身材，大胸展示，moweifei，feifei 妃妃,一位大美女，完美身材，"
    "写实人像写真、中式风格、韩式写真、人像写真，氛围海报，艺术摄影,"
    "a photo-realistic shoot from a front camera angle about a young woman, "
    "a 20-year-old asian woman with light skin and brown hair styled in a single hair bun, "
    "looking directly at the camera with a neutral expression,"
)

# 尺寸映射表
SIZE_MAP = {
    "1:1": (1240, 1240),
    "4:3": (1080, 1440),
    "3:4": (1440, 1080),
    "9:16": (928, 1664),
    "16:9": (1664, 928),
    "1:2": (870, 1740),
    "2:1": (1740, 870),
    "1:3": (720, 2160),
    "3:1": (2160, 720),
    "2:3": (960, 1440),
    "3:2": (1440, 960),
    "2:5": (720, 1800),
    "5:2": (1800, 720),
    "3:5": (960, 1600),
    "5:3": (1600, 960),
    "4:5": (1080, 1350),
    "5:4": (1350, 1080),
}

# 模特触发关键词
MODEL_KEYWORDS_ZH = ["模特", "人物", "人像", "女性", "女士", "女孩", "美女", "穿搭", "展示", "试穿"]
MODEL_KEYWORDS_EN = ["model", "woman", "female", "girl", "portrait", "character", "person"]


def has_model_keyword(text: str) -> bool:
    """检测文本是否包含模特相关关键词"""
    if not text:
        return False

    for kw in MODEL_KEYWORDS_ZH:
        if kw in text:
            return True

    text_lower = text.lower()
    for kw in MODEL_KEYWORDS_EN:
        if kw in text_lower:
            return True

    return False


def process_prompt(prompt: str) -> str:
    """处理 prompt：自动追加模特提示词"""
    if not prompt:
        return ""

    if has_model_keyword(prompt):
        # 避免重复追加
        if "moweifei" not in prompt and "elegant woman" not in prompt:
            return prompt + MODEL_SUFFIX
    return prompt


def get_headers():
    """获取请求头"""
    api_key = os.environ.get("BIZYAIR_API_KEY", "")
    if not api_key:
        raise ValueError("BIZYAIR_API_KEY 环境变量未设置")

    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }


def create_task(prompt: str, width: int, height: int, batch_size: int = 4) -> str:
    """创建异步生成任务"""
    url = f"{BASE_URL}/create"
    headers = get_headers()
    headers["X-Bizyair-Task-Async"] = "enable"

    payload = {
        "web_app_id": WEB_APP_ID,
        "suppress_preview_output": True,
        "input_values": {
            "107:BizyAirSiliconCloudLLMAPI.user_prompt": prompt,
            "81:EmptySD3LatentImage.width": width,
            "81:EmptySD3LatentImage.height": height,
            "81:EmptySD3LatentImage.batch_size": batch_size
        }
    }

    print(f"📤 创建任务: prompt='{prompt[:50]}...', size={width}x{height}, batch={batch_size}")

    response = requests.post(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()

    data = response.json()
    request_id = data.get("requestId") or data.get("request_id")

    if not request_id:
        raise ValueError(f"响应中未找到 requestId: {data}")

    print(f"✅ 任务已创建，ID: {request_id}")
    return request_id


def poll_status(request_id: str, timeout: int = 900) -> bool:
    """轮询任务状态直到完成"""
    url = f"{BASE_URL}/detail"
    headers = get_headers()
    # 移除 Async header
    headers.pop("X-Bizyair-Task-Async", None)

    start_time = time.time()
    last_progress_time = start_time
    poll_count = 0
    progress_interval = 30  # 每30秒输出一次进度

    print("⏳ 开始轮询任务状态（预计 3-10 分钟，请耐心等待）...")

    while True:
        elapsed = time.time() - start_time
        if elapsed > timeout:
            raise TimeoutError(f"任务超时（{timeout}秒 = {timeout/60:.0f}分钟）")

        poll_count += 1
        elapsed_minutes = elapsed / 60

        # 定期输出进度
        if time.time() - last_progress_time >= progress_interval:
            print(f"⏱️ 任务进行中... 已等待 {elapsed_minutes:.1f} 分钟 (轮询 {poll_count})")
            last_progress_time = time.time()

        try:
            response = requests.get(
                url,
                params={"requestId": request_id},
                headers=headers,
                timeout=20
            )
            response.raise_for_status()

            data = response.json()
            task_data = data.get("data", {})
            status = task_data.get("status")

            print(f"🔄 [{poll_count}] 当前状态: {status} ({elapsed_minutes:.1f}分钟)")

            if status == "Success":
                print(f"✅ 任务完成（总耗时 {elapsed_minutes:.1f} 分钟，轮询 {poll_count} 次）")
                return True
            elif status in ["Failed", "Canceled"]:
                error_info = task_data.get("error_info", {})
                error_msg = error_info.get("message", error_info.get("error_type", "未知错误"))
                print(f"❌ 任务{status}: {error_msg}")
                return False

            time.sleep(5)  # 每5秒查询一次

        except requests.exceptions.Timeout:
            print(f"⚠️ [{poll_count}] 查询超时，继续轮询...")
            time.sleep(5)
        except requests.exceptions.RequestException as e:
            print(f"⚠️ [{poll_count}] 网络错误，继续轮询... ({e})")
            time.sleep(5)


def get_results(request_id: str) -> list:
    """获取任务结果"""
    url = f"{BASE_URL}/outputs"
    headers = get_headers()

    response = requests.get(
        url,
        params={"requestId": request_id},
        headers=headers,
        timeout=30
    )
    response.raise_for_status()

    data = response.json()
    outputs = data.get("data", {}).get("outputs", [])

    urls = []
    for out in outputs:
        url = out.get("object_url")
        if url:
            urls.append(url)

    return urls


def print_results(urls: list, prompt: str, width: int, height: int):
    """打印结果表格"""
    print("\n" + "=" * 60)
    print("🎨 分镜场景图生成结果")
    print("=" * 60)
    print(f"📝 Prompt: {prompt[:80]}{'...' if len(prompt) > 80 else ''}")
    print(f"📐 尺寸: {width}×{height}")
    print(f"📊 生成数量: {len(urls)} 张")
    print("\n| 序号 | 图片 URL |")
    print("| --- | --- |")

    for idx, url in enumerate(urls, 1):
        print(f"| {idx} | {url} |")

    print("\n" + "=" * 60)


def main():
    parser = argparse.ArgumentParser(description="BizyAir 分镜图生成工具")
    parser.add_argument("prompt", help="图片生成描述")
    parser.add_argument("--ratio", default="9:16", help="图片比例 (默认: 9:16)")
    parser.add_argument("--width", type=int, help="图片宽度（像素）")
    parser.add_argument("--height", type=int, help="图片高度（像素）")
    parser.add_argument("--batch", type=int, default=4, help="批次数量 (默认: 4)")
    parser.add_argument("--timeout", type=int, default=300, help="轮询超时时间（秒）")

    args = parser.parse_args()

    try:
        # 处理 prompt
        final_prompt = process_prompt(args.prompt)
        if final_prompt != args.prompt:
            print("🤖 检测到模特关键词，已自动追加提示词")

        # 解析尺寸
        if args.width and args.height:
            width, height = args.width, args.height
        elif args.ratio in SIZE_MAP:
            width, height = SIZE_MAP[args.ratio]
        else:
            width, height = SIZE_MAP["9:16"]  # 默认

        # 创建任务
        request_id = create_task(final_prompt, width, height, args.batch)

        # 轮询状态
        poll_status(request_id, args.timeout)

        # 获取结果
        urls = get_results(request_id)

        # 打印结果
        print_results(urls, final_prompt, width, height)

    except Exception as e:
        print(f"\n❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
