#!/usr/bin/env python3
"""
Seedance 2.0 视频生成 - 下载结果脚本
用法:
  python download_video.py <task_id> [--output-dir ./output]
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


def query_task(api_key, base_url, task_id):
    """查询任务状态和结果"""
    url = f"{base_url}/api/v3/contents/generations/tasks/{task_id}"

    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {api_key}"},
        method="GET",
    )

    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def download_file(url, output_path):
    """下载文件"""
    print(f"⬇️  下载中: {url}")
    print(f"   保存至: {output_path}")

    urllib.request.urlretrieve(url, output_path)

    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"✅ 下载完成! 文件大小: {size_mb:.2f} MB")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="下载 Seedance 生成的视频")
    parser.add_argument("task_id", help="任务 ID")
    parser.add_argument("--output-dir", default="./output", help="输出目录 (默认: ./output)")

    args = parser.parse_args()

    api_key, base_url = get_config()

    # 查询任务状态
    print(f"🔍 查询任务: {args.task_id}")
    result = query_task(api_key, base_url, args.task_id)

    status = result.get("status")
    if status != "completed":
        print(f"❌ 任务尚未完成，当前状态: {status}", file=sys.stderr)
        print("   请稍后重试或使用 query_task.py --poll 等待完成")
        sys.exit(1)

    # 创建输出目录
    os.makedirs(args.output_dir, exist_ok=True)

    video_result = result.get("video_result", {})
    downloaded_files = []

    # 下载视频
    video_url = video_result.get("video_url")
    if video_url:
        video_path = os.path.join(args.output_dir, f"{args.task_id}.mp4")
        download_file(video_url, video_path)
        downloaded_files.append(video_path)

    # 下载封面图
    cover_url = video_result.get("cover_image_url")
    if cover_url:
        cover_path = os.path.join(args.output_dir, f"{args.task_id}_cover.jpg")
        download_file(cover_url, cover_path)
        downloaded_files.append(cover_path)

    print()
    print(f"📁 所有文件已保存到: {os.path.abspath(args.output_dir)}")
    for f in downloaded_files:
        print(f"   📄 {f}")


if __name__ == "__main__":
    main()
