#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
腾讯混元视频生成API调用脚本
支持：文生视频、图生视频、视频风格化

API文档：https://cloud.tencent.com/document/product/1616/107795
"""

import os
import sys
import json
import time
import base64
import argparse
from datetime import datetime
from pathlib import Path

# 添加腾讯云SDK
try:
    from tencentcloud.common import credential
    from tencentcloud.common.profile.client_profile import ClientProfile
    from tencentcloud.common.profile.http_profile import HttpProfile
    from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
    from tencentcloud.vclm.v20240523 import vclm_client, models
except ImportError as e:
    print(f"错误：{e}")
    print("请运行: pip install tencentcloud-sdk-python")
    sys.exit(1)


def get_env_credentials():
    """从环境变量获取密钥"""
    secret_id = os.environ.get("TENCENT_SECRET_ID")
    secret_key = os.environ.get("TENCENT_SECRET_KEY")
    
    if not secret_id or not secret_key:
        print("错误：未设置环境变量 TENCENT_SECRET_ID 和 TENCENT_SECRET_KEY")
        print("请设置后再运行:")
        print('  $env:TENCENT_SECRET_ID = "your-secret-id"')
        print('  $env:TENCENT_SECRET_KEY = "your-secret-key"')
        sys.exit(1)
    
    return secret_id, secret_key


def create_client(secret_id, secret_key):
    """创建VCLM客户端"""
    cred = credential.Credential(secret_id, secret_key)
    http_profile = HttpProfile(endpoint="vclm.tencentcloudapi.com")
    client_profile = ClientProfile(httpProfile=http_profile)
    return vclm_client.VclmClient(cred, "ap-guangzhou", client_profile)


# ==================== 1. 文生视频 ====================

def submit_text_to_video(client, prompt, **kwargs):
    """混元文生视频"""
    req = models.SubmitHunyuanToVideoJobRequest()
    req.Prompt = prompt
    
    if kwargs.get("resolution"):
        req.Resolution = kwargs["resolution"]
    
    resp = client.SubmitHunyuanToVideoJob(req)
    return json.loads(resp.to_json_string())


# ==================== 2. 图生视频 ====================

def submit_image_to_video(client, image_input, **kwargs):
    """混元图生视频
    
    Args:
        image_input: 图片URL或本地图片路径
    """
    req = models.SubmitImageToVideoGeneralJobRequest()
    
    # Image是对象类型，支持URL或Base64
    image = models.Image()
    
    if image_input.startswith('http://') or image_input.startswith('https://'):
        # URL方式
        image.Url = image_input
    elif os.path.exists(image_input):
        # 本地文件，转为base64
        with open(image_input, 'rb') as f:
            image_base64 = base64.b64encode(f.read()).decode('utf-8')
        image.Base64 = image_base64
    else:
        raise ValueError(f"图片路径无效: {image_input}")
    
    req.Image = image
    
    if kwargs.get("prompt"):
        req.Prompt = kwargs["prompt"]
    
    resp = client.SubmitImageToVideoGeneralJob(req)
    return json.loads(resp.to_json_string())


# ==================== 3. 视频风格化 ====================

def submit_video_stylization(client, video_url, style_id, style_strength="medium"):
    """视频风格化"""
    req = models.SubmitVideoStylizationJobRequest()
    req.VideoUrl = video_url
    req.StyleId = style_id
    req.StyleStrength = style_strength
    
    resp = client.SubmitVideoStylizationJob(req)
    return json.loads(resp.to_json_string())


# ==================== 查询任务状态 ====================

def query_job(client, job_id, job_type):
    """查询任务状态"""
    try:
        if job_type == "hunyuan_to_video":
            req = models.DescribeHunyuanToVideoJobRequest()
            req.JobId = job_id
            resp = client.DescribeHunyuanToVideoJob(req)
        elif job_type == "image_to_video":
            req = models.DescribeImageToVideoGeneralJobRequest()
            req.JobId = job_id
            resp = client.DescribeImageToVideoGeneralJob(req)
        elif job_type == "stylization":
            req = models.DescribeVideoStylizationJobRequest()
            req.JobId = job_id
            resp = client.DescribeVideoStylizationJob(req)
        else:
            return None
        
        return json.loads(resp.to_json_string())
    except Exception as e:
        print(f"查询失败: {e}")
        return None


# ==================== 下载文件 ====================

def download_file(url, output_path):
    """下载文件"""
    import urllib.request
    
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.0'
        })
        with urllib.request.urlopen(req, timeout=120) as response:
            with open(output_path, 'wb') as f:
                f.write(response.read())
        return True
    except Exception as e:
        print(f"下载失败: {e}")
        return False


def wait_for_completion(client, job_id, job_type, timeout=600):
    """等待任务完成"""
    print(f"任务ID: {job_id}")
    print("等待生成完成...", end="", flush=True)
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        result = query_job(client, job_id, job_type)
        if not result:
            return None
        
        # 不同接口状态字段不同
        status = result.get("Status") or result.get("JobStatusCode", "")
        
        # 成功状态：文生/图生视频用 "JobSuccess"，风格化用 "4" 或 "5"+ResultDetails
        if status in ["JobSuccess", "SUCCESS", "DONE", "4"]:
            print("\n✅ 生成完成!")
            return result
        elif status in ["JobFailed", "FAILED", "5"]:
            # 风格化接口：StatusCode 5 可能是成功，需要检查 ResultDetails
            if status == "5" and result.get("ResultDetails") == ["Success"]:
                print("\n✅ 生成完成!")
                return result
            print(f"\n❌ 生成失败")
            return None
        
        print(".", end="", flush=True)
        time.sleep(5)
    
    print("\n⏱️ 等待超时")
    return None


# ==================== 主函数 ====================

def main():
    parser = argparse.ArgumentParser(description="腾讯混元视频生成")
    
    # 子命令
    subparsers = parser.add_subparsers(dest="command", help="功能选择")
    
    # 1. 文生视频
    p1 = subparsers.add_parser("text2video", help="文生视频")
    p1.add_argument("prompt", help="文本描述")
    p1.add_argument("--resolution", default="720p", help="分辨率 (720p, 1080p)")
    
    # 2. 图生视频
    p2 = subparsers.add_parser("image2video", help="图生视频")
    p2.add_argument("image", help="图片URL或本地路径")
    p2.add_argument("--prompt", help="辅助描述")
    
    # 3. 视频风格化
    p3 = subparsers.add_parser("stylization", help="视频风格化")
    p3.add_argument("video_url", help="视频URL")
    p3.add_argument("--style", default="2d_anime", 
                   choices=["2d_anime", "3d_cartoon", "3d_china", "pixel_art"],
                   help="风格")
    
    # 通用参数
    parser.add_argument("--output", default="./videos", help="输出目录")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # 获取密钥和创建客户端
    secret_id, secret_key = get_env_credentials()
    client = create_client(secret_id, secret_key)
    
    # 根据命令执行
    print(f"🎬 {args.command}")
    
    if args.command == "text2video":
        print(f"   描述: {args.prompt}")
        result = submit_text_to_video(client, args.prompt, resolution=args.resolution)
        job_type = "hunyuan_to_video"
        
    elif args.command == "image2video":
        print(f"   图片: {args.image}")
        result = submit_image_to_video(client, args.image, prompt=args.prompt)
        job_type = "image_to_video"
        
    elif args.command == "stylization":
        print(f"   视频: {args.video_url}")
        print(f"   风格: {args.style}")
        result = submit_video_stylization(client, args.video_url, args.style)
        job_type = "stylization"
    
    if not result:
        print("❌ 提交任务失败")
        sys.exit(1)
    
    job_id = result.get("JobId")
    print(f"✅ 任务提交成功，Job ID: {job_id}")
    
    # 等待完成
    final_result = wait_for_completion(client, job_id, job_type)
    if not final_result:
        sys.exit(1)
    
    # 创建输出目录
    today = datetime.now().strftime("%Y%m%d")
    output_dir = Path(args.output) / today / job_id
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 保存任务信息
    info_path = output_dir / "info.json"
    with open(info_path, "w", encoding="utf-8") as f:
        json.dump(final_result, f, ensure_ascii=False, indent=2)
    
    # 下载视频
    video_url = final_result.get("ResultVideoUrl", "")
    if video_url:
        video_path = output_dir / f"{args.command}_result.mp4"
        if download_file(video_url, video_path):
            print(f"✅ 已保存: {video_path}")
    
    print(f"\n📁 输出目录: {output_dir}")


if __name__ == "__main__":
    main()
