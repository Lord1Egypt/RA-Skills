#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
腾讯混元生3D API调用脚本（OpenAI兼容接口）
支持：文生3D、图生3D（仅专业版）

API文档：https://cloud.tencent.com/document/product/1804/126189
"""

import os
import sys
import json
import time
import argparse
from datetime import datetime
from pathlib import Path
from urllib import request, parse
import ssl


# OpenAI兼容接口配置
BASE_URL = "https://api.ai3d.cloud.tencent.com"
SUBMIT_URL = f"{BASE_URL}/v1/ai3d/submit"
QUERY_URL = f"{BASE_URL}/v1/ai3d/query"


def get_api_key():
    """从环境变量获取API Key"""
    api_key = os.environ.get("HUNYUAN_3D_API_KEY")
    
    if not api_key:
        print("错误：未设置环境变量 HUNYUAN_3D_API_KEY")
        print("请设置后再运行:")
        print('  $env:HUNYUAN_3D_API_KEY = "sk-xxxxx"')
        print("")
        print("获取API Key步骤:")
        print("1. 登录 https://console.cloud.tencent.com/hunyuan/start")
        print("2. 进入 API KEY 页面")
        print("3. 创建新的 API Key")
        sys.exit(1)
    
    return api_key


def submit_3d_job(api_key, params):
    """提交3D生成任务"""
    headers = {
        'Authorization': api_key,
        'Content-Type': 'application/json'
    }
    
    payload = json.dumps(params).encode('utf-8')
    
    try:
        req = request.Request(SUBMIT_URL, data=payload, headers=headers, method='POST')
        
        with request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"提交任务失败: {e}")
        return None


def query_3d_job(api_key, job_id):
    """查询3D生成任务状态"""
    headers = {
        'Authorization': api_key,
        'Content-Type': 'application/json'
    }
    
    params = {
        "JobId": job_id
    }
    
    payload = json.dumps(params).encode('utf-8')
    
    try:
        req = request.Request(QUERY_URL, data=payload, headers=headers, method='POST')
        
        with request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"查询任务失败: {e}")
        return None


def download_file(url, output_path):
    """下载文件"""
    try:
        req = request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.0'
        })
        with request.urlopen(req, timeout=60) as response:
            with open(output_path, 'wb') as f:
                f.write(response.read())
        return True
    except Exception as e:
        print(f"下载文件失败: {e}")
        return False


def wait_for_completion(api_key, job_id, timeout=600):
    """等待任务完成"""
    print(f"任务ID: {job_id}")
    print("等待3D模型生成完成...", end="", flush=True)
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        result = query_3d_job(api_key, job_id)
        if not result:
            return None
        
        status = result.get("Status", "")
        
        if status == "DONE":
            print("\n✅ 3D模型生成完成!")
            return result
        elif status == "FAILED":
            print(f"\n❌ 生成失败: {result.get('ErrorMessage', '')}")
            return None
        
        print(".", end="", flush=True)
        time.sleep(5)
    
    print("\n⏱️ 等待超时")
    return None


def main():
    parser = argparse.ArgumentParser(description="腾讯混元生3D (OpenAI兼容接口版)")
    parser.add_argument("--mode", type=str, default="text",
                       choices=["text", "image"],
                       help="生成模式：文生3D/图生3D")
    parser.add_argument("--prompt", type=str, help="文本描述（文生3D）")
    parser.add_argument("--image-url", type=str, help="图片URL（图生3D）")
    parser.add_argument("--model", type=str, default="3.0",
                       choices=["3.0", "3.1"],
                       help="模型版本：3.0(默认), 3.1")
    parser.add_argument("--output", type=str, default="./models", help="输出目录")
    
    args = parser.parse_args()
    
    # 获取API Key
    api_key = get_api_key()
    
    # 构建请求参数
    params = {
        "Model": args.model
    }
    
    # 根据模式设置参数
    if args.mode == "text":
        if not args.prompt:
            print("错误：文生3D模式需要提供 --prompt 参数")
            sys.exit(1)
        
        print(f"🎨 文生3D (专业版)")
        print(f"   描述: {args.prompt}")
        print(f"   模型版本: {args.model}")
        
        params["Prompt"] = args.prompt
        
    elif args.mode == "image":
        if not args.image_url:
            print("错误：图生3D模式需要提供 --image-url 参数")
            sys.exit(1)
        
        print(f"🎨 图生3D (专业版)")
        print(f"   图片: {args.image_url}")
        print(f"   模型版本: {args.model}")
        
        params["ImageUrl"] = args.image_url
    
    # 提交任务
    print("\n提交任务...")
    result = submit_3d_job(api_key, params)
    
    if not result:
        print("❌ 提交任务失败")
        sys.exit(1)
    
    # 检查错误
    if "Error" in result:
        error = result["Error"]
        print(f"❌ API错误: {error.get('Code')} - {error.get('Message')}")
        sys.exit(1)
    
    job_id = result.get("JobId")
    if not job_id:
        print("❌ 未获取到JobId")
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        sys.exit(1)
    
    print(f"✅ 任务提交成功，Job ID: {job_id}")
    
    # 等待完成
    final_result = wait_for_completion(api_key, job_id)
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
    
    # 下载3D模型
    model_url = final_result.get("ResultUrl", "")
    if model_url:
        # 根据URL后缀判断格式
        ext = model_url.split('.')[-1].split('?')[0] if '.' in model_url else "glb"
        model_path = output_dir / f"model.{ext}"
        if download_file(model_url, model_path):
            print(f"✅ 已保存: {model_path}")
    else:
        print("⚠️ 未找到模型下载链接")
        print(f"完整响应: {json.dumps(final_result, indent=2, ensure_ascii=False)}")
    
    print(f"\n📁 输出目录: {output_dir}")


if __name__ == "__main__":
    main()
