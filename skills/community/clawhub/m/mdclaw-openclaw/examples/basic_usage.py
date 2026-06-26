#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MDClaw OpenClaw 基本使用示例
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mdclaw_client import MDClawClient


def example_text_to_speech():
    """示例 1: 文字转语音"""
    print("=" * 60)
    print("示例 1: 文字转语音")
    print("=" * 60)

    client = MDClawClient()
    result = client.text_to_speech("你好，这是语音测试")

    if result.get('success'):
        audio_url = result['result']['audio_url']
        print(f"✅ 语音生成成功: {audio_url}")
    else:
        print(f"❌ 生成失败: {result.get('error')}")


def example_text_to_image():
    """示例 2: 文生图"""
    print("\n" + "=" * 60)
    print("示例 2: 文生图")
    print("=" * 60)

    client = MDClawClient()
    result = client.text_to_image(
        prompt="一只可爱的橘猫在阳光下伸懒腰",
        aspect_ratio="9:16"
    )

    if result.get('success'):
        image_urls = result['result']['image_urls']
        print(f"✅ 图片生成成功，共 {len(image_urls)} 张:")
        for url in image_urls:
            print(f"   {url}")
    else:
        print(f"❌ 生成失败: {result.get('error')}")


def example_image_to_video():
    """示例 3: 图生视频"""
    print("\n" + "=" * 60)
    print("示例 3: 图生视频")
    print("=" * 60)

    client = MDClawClient()

    # 先生成图片
    img_result = client.text_to_image(
        prompt="一只金毛犬在公园草地上",
        aspect_ratio="16:9"
    )

    if not img_result.get('success'):
        print(f"❌ 图片生成失败: {img_result.get('error')}")
        return

    image_url = img_result['result']['image_urls'][0]
    print(f"✅ 图片生成成功: {image_url}")

    # 生成视频
    vid_result = client.image_to_video(
        image=image_url,
        prompt="金毛犬缓缓起身，摇着尾巴",
        duration=6
    )

    if not vid_result.get('success'):
        print(f"❌ 视频生成失败: {vid_result.get('error')}")
        return

    task_id = vid_result['result']['task_id']
    print(f"✅ 视频任务已提交，task_id: {task_id}")
    print("等待视频生成完成...")

    # 等待完成
    final_result = client.wait_for_video(task_id, max_wait=120)
    if final_result.get('success'):
        video_url = final_result['result']['url']
        print(f"✅ 视频生成成功: {video_url}")
    else:
        print(f"❌ 视频生成失败")


def example_upload_image():
    """示例 4: 上传本地图片"""
    print("\n" + "=" * 60)
    print("示例 4: 上传本地图片")
    print("=" * 60)

    # 检查示例图片是否存在
    sample_image = os.path.join(os.path.dirname(__file__), "sample.jpg")

    if not os.path.exists(sample_image):
        print(f"⚠️ 示例图片不存在: {sample_image}")
        print("跳过此示例")
        return

    client = MDClawClient()
    result = client.upload_image(sample_image)

    if result.get('success'):
        image_url = result['result']['url']
        print(f"✅ 图片上传成功: {image_url}")
    else:
        print(f"❌ 上传失败: {result.get('error')}")


def example_agent_register():
    """示例 5: 注册新账号"""
    print("\n" + "=" * 60)
    print("示例 5: 注册新账号")
    print("=" * 60)

    client = MDClawClient()
    result = client.agent_register("test_user", "test_password")

    if result.get('success'):
        api_key = result['result']['api_key']
        print(f"✅ 注册成功，API Key: {api_key[:20]}...")
    else:
        print(f"❌ 注册失败: {result.get('error')}")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("MDClaw OpenClaw 基本使用示例")
    print("=" * 60)

    # 检查 API Key
    if not os.getenv('MDCLAW_API_KEY'):
        print("⚠️ 请设置环境变量 MDCLAW_API_KEY")
        print("   export MDCLAW_API_KEY='你的API Key'")
        return

    examples = [
        ("文字转语音", example_text_to_speech),
        ("文生图", example_text_to_image),
        ("图生视频", example_image_to_video),
        ("上传图片", example_upload_image),
        ("注册账号", example_agent_register),
    ]

    for name, example_func in examples:
        try:
            example_func()
        except Exception as e:
            print(f"\n❌ 示例 '{name}' 执行失败: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 60)
    print("示例运行完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
