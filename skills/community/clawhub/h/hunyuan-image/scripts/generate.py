#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
腾讯混元生图API调用脚本
"""

import os
import sys
import json
import time
import argparse
from datetime import datetime
from pathlib import Path

# 添加腾讯云SDK
try:
    from tencentcloud.common import credential
    from tencentcloud.common.profile.client_profile import ClientProfile
    from tencentcloud.common.profile.http_profile import HttpProfile
    from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
    from tencentcloud.hunyuan.v20230901 import hunyuan_client, models
except ImportError:
    print("错误：未安装 tencentcloud-sdk-python")
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


def submit_job(client, prompt, **kwargs):
    """提交生图任务"""
    req = models.SubmitHunyuanImageJobRequest()
    
    # 必填参数
    req.Prompt = prompt
    
    # 可选参数
    if kwargs.get("negative_prompt"):
        req.NegativePrompt = kwargs["negative_prompt"]
    if kwargs.get("style"):
        req.Style = str(kwargs["style"])
    if kwargs.get("resolution"):
        req.Resolution = kwargs["resolution"]
    if kwargs.get("num"):
        req.Num = kwargs["num"]
    if kwargs.get("clarity"):
        req.Clarity = kwargs["clarity"]
    if kwargs.get("revise") is not None:
        req.Revise = kwargs["revise"]
    if kwargs.get("seed"):
        req.Seed = kwargs["seed"]
    
    # 水印设置（默认不添加）
    req.LogoAdd = kwargs.get("logo_add", 0)
    
    try:
        resp = client.SubmitHunyuanImageJob(req)
        return json.loads(resp.to_json_string())
    except TencentCloudSDKException as err:
        print(f"提交任务失败: {err}")
        return None


def query_job(client, job_id):
    """查询任务状态"""
    req = models.QueryHunyuanImageJobRequest()
    req.JobId = job_id
    
    try:
        resp = client.QueryHunyuanImageJob(req)
        return json.loads(resp.to_json_string())
    except TencentCloudSDKException as err:
        print(f"查询任务失败: {err}")
        return None


def download_image(url, output_path):
    """下载图片"""
    import urllib.request
    
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.0'
        })
        with urllib.request.urlopen(req, timeout=30) as response:
            with open(output_path, 'wb') as f:
                f.write(response.read())
        return True
    except Exception as e:
        print(f"下载图片失败: {e}")
        return False


def wait_for_completion(client, job_id, timeout=300):
    """等待任务完成"""
    print(f"任务ID: {job_id}")
    print("等待生成完成...", end="", flush=True)
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        result = query_job(client, job_id)
        if not result:
            return None
        
        status = result.get("JobStatusCode", "")
        
        if status == "4":  # 完成
            print("\n✅ 生成完成!")
            return result
        elif status == "5":  # 失败
            print(f"\n❌ 生成失败: {result.get('JobStatusMsg', '')}")
            return None
        
        print(".", end="", flush=True)
        time.sleep(2)
    
    print("\n⏱️ 等待超时")
    return None


def main():
    parser = argparse.ArgumentParser(description="腾讯混元生图")
    parser.add_argument("prompt", help="文本描述")
    parser.add_argument("--style", type=str, help="风格编号")
    parser.add_argument("--resolution", type=str, default="1024:1024", help="分辨率")
    parser.add_argument("--num", type=int, default=1, help="生成数量(1-4)")
    parser.add_argument("--negative", type=str, help="反向提示词")
    parser.add_argument("--clarity", type=str, choices=["x2", "x4"], help="超分选项")
    parser.add_argument("--seed", type=int, help="随机种子")
    parser.add_argument("--no-revise", action="store_true", help="关闭prompt扩写")
    parser.add_argument("--logo", action="store_true", help="添加水印（API级别，默认不添加）")
    parser.add_argument("--output", type=str, default="./images", help="输出目录")
    
    args = parser.parse_args()
    
    # 获取密钥
    secret_id, secret_key = get_env_credentials()
    
    # 创建客户端
    cred = credential.Credential(secret_id, secret_key)
    http_profile = HttpProfile(endpoint="hunyuan.tencentcloudapi.com")
    client_profile = ClientProfile(httpProfile=http_profile)
    client = hunyuan_client.HunyuanClient(cred, "ap-guangzhou", client_profile)
    
    print(f"🎨 生成图片: {args.prompt}")
    
    # 提交任务
    result = submit_job(
        client,
        args.prompt,
        negative_prompt=args.negative,
        style=args.style,
        resolution=args.resolution,
        num=args.num,
        clarity=args.clarity,
        revise=0 if args.no_revise else 1,
        seed=args.seed,
        logo_add=1 if args.logo else 0
    )
    
    if not result:
        sys.exit(1)
    
    job_id = result.get("JobId")
    
    # 等待完成
    final_result = wait_for_completion(client, job_id)
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
    
    # 下载图片
    image_results = final_result.get("ResultDetails", [])
    downloaded = 0
    
    for i, img_info in enumerate(image_results):
        url = img_info.get("Url")
        if url:
            img_path = output_dir / f"image_{i}.png"
            if download_image(url, img_path):
                print(f"✅ 已保存: {img_path}")
                downloaded += 1
    
    # 显示扩写后的prompt
    if final_result.get("RevisedPrompt"):
        print(f"\n📝 扩写后的描述:")
        print(f"   {final_result['RevisedPrompt']}")
    
    print(f"\n📁 输出目录: {output_dir}")
    print(f"📊 成功下载: {downloaded}/{len(image_results)} 张图片")


if __name__ == "__main__":
    main()
