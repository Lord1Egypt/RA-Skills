#!/usr/bin/env python3
"""
Seedance 2.0 视频生成 - 提交任务脚本
用法:
  python generate_video.py --prompt "视频描述" [选项]
"""

import argparse
import json
import os
import sys
import urllib.request


def get_config():
    """获取 API 配置"""
    api_key = os.environ.get("ARK_API_KEY")
    if not api_key:
        print("错误: 请设置环境变量 ARK_API_KEY", file=sys.stderr)
        sys.exit(1)

    base_url = os.environ.get("ARK_API_URL", "https://ark.cn-beijing.volces.com")
    return api_key, base_url


def build_content(prompt, image_urls, video_urls, audio_urls):
    """构建 content 多模态数组"""
    content = [{"type": "text", "text": prompt}]

    for url in (image_urls or []):
        content.append({
            "type": "image_url",
            "image_url": {"url": url},
            "role": "reference_image"
        })

    for url in (video_urls or []):
        content.append({
            "type": "video_url",
            "video_url": {"url": url},
            "role": "reference_video"
        })

    for url in (audio_urls or []):
        content.append({
            "type": "audio_url",
            "audio_url": {"url": url},
            "role": "reference_audio"
        })

    return content


def submit_task(api_key, base_url, payload):
    """提交视频生成任务"""
    url = f"{base_url}/api/v3/contents/generations/tasks"

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    return result


def main():
    parser = argparse.ArgumentParser(description="Seedance 2.0 视频生成任务提交")
    parser.add_argument("--model", required=True, help="模型名称，如 doubao-seedance-2-0-fast-260128")
    parser.add_argument("--prompt", required=True, help="视频描述提示词")
    parser.add_argument("--ratio", default="16:9", choices=["16:9", "9:16", "1:1"], help="视频比例 (默认: 16:9)")
    parser.add_argument("--duration", type=int, default=10, help="视频时长秒数 5-11 (默认: 10)")
    parser.add_argument("--image-url", action="append", default=[], dest="image_urls", help="参考图片 URL（可多次指定）")
    parser.add_argument("--video-url", action="append", default=[], dest="video_urls", help="参考视频 URL（可多次指定）")
    parser.add_argument("--audio-url", action="append", default=[], dest="audio_urls", help="参考音频 URL（可多次指定）")
    parser.add_argument("--generate-audio", action="store_true", help="同时生成音频")
    parser.add_argument("--watermark", action="store_true", default=True, help="添加水印（默认开启）")
    parser.add_argument("--no-watermark", action="store_false", dest="watermark", help="不添加水印")

    args = parser.parse_args()

    # 参数校验
    if not 5 <= args.duration <= 11:
        print(f"错误: duration 必须在 5-11 之间，当前值: {args.duration}", file=sys.stderr)
        sys.exit(1)

    api_key, base_url = get_config()

    content = build_content(args.prompt, args.image_urls, args.video_urls, args.audio_urls)

    payload = {
        "model": args.model,
        "content": content,
        "generate_audio": args.generate_audio,
        "ratio": args.ratio,
        "duration": args.duration,
        "watermark": args.watermark,
    }

    print(f"🎬 提交 Seedance 视频生成任务...")
    print(f"   模型: {args.model}")
    print(f"   时长: {args.duration}s | 比例: {args.ratio} | 音频: {args.generate_audio} | 水印: {args.watermark}")
    print(f"   参考图: {len(args.image_urls)} 张 | 参考视频: {len(args.video_urls)} 个 | 参考音频: {len(args.audio_urls)} 个")
    print()

    try:
        result = submit_task(api_key, base_url, payload)
        task_id = result.get("id")
        print(f"✅ 任务提交成功！")
        print(f"   Task ID: {task_id}")
        print()
        print(f"查询状态命令:")
        print(f'   python3 "{os.path.abspath(__file__).replace('generate_video.py', 'query_task.py')}" {task_id}')
        return task_id
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        print(f"❌ API 错误 ({e.code}): {error_body}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
