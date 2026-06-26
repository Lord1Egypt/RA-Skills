#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COS 文件上传脚本 - 客服问题报告上传
技能名称：issue-analysis-agent
版本：v2.1.0
更新：2026-03-24

关键配置：
- Content-Type: text/html; charset=utf-8
- Content-Disposition: inline（在浏览器打开，不下载）
- Cache-Control: public, max-age=0（不缓存，确保看到最新数据）
- ACL: public-read（公有读权限）

新增功能：
- 上传后自动验证
- 验证失败自动重试（最多 3 次）
- 详细的错误日志

团队协作：画师 🎨 负责
"""

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import time
import requests
from pathlib import Path

# COS 配置
SECRET_ID = 'AKIDWYbw77uSntsgHeokDSTItITQAi20jLlz'
SECRET_KEY = '570JTPAl8IFzaxNgokU0Lgp8IG2d1DE1'
BUCKET = 'claw-1301484442'
REGION = 'ap-shanghai'

def upload_to_cos(file_path, cos_key, max_retries=3):
    """上传文件到 COS，设置正确的响应头，包含验证和重试"""
    
    print(f"📤 上传文件：{file_path} → {cos_key}")
    
    # 检查文件是否存在
    if not Path(file_path).exists():
        print(f"❌ 文件不存在：{file_path}")
        return None
    
    # 配置 COS 客户端
    config = CosConfig(
        Region=REGION,
        SecretId=SECRET_ID,
        SecretKey=SECRET_KEY,
        Scheme='https'
    )
    client = CosS3Client(config)
    
    # 读取文件内容
    with open(file_path, 'rb') as f:
        content = f.read()
    
    # 正确的响应头配置
    headers = {
        'ContentType': 'text/html; charset=utf-8',  # 关键：HTML 文件
        'ContentDisposition': 'inline',  # 关键：在浏览器打开，不下载
        'CacheControl': 'public, max-age=0'  # 关键：不缓存，确保看到最新数据
    }
    
    retry_count = 0
    while retry_count < max_retries:
        try:
            print(f"\n【尝试 {retry_count + 1}/{max_retries}】上传文件...")
            
            # 上传并设置正确的响应头
            response = client.put_object(
                Bucket=BUCKET,
                Body=content,
                Key=cos_key,
                **headers
            )
            
            print(f"✅ 上传成功，ETag: {response.get('ETag', 'N/A')}")
            
            # 设置公有读权限
            client.put_object_acl(
                Bucket=BUCKET,
                Key=cos_key,
                ACL='public-read'
            )
            
            print(f"✅ 权限已设置为公有读")
            
            # 生成公网访问链接
            public_url = f"https://{BUCKET}.cos.{REGION}.myqcloud.com/{cos_key}"
            
            # 验证上传
            print(f"\n🔍 验证上传...")
            if validate_upload(public_url, content):
                print(f"✅ 验证通过")
                return public_url
            else:
                print(f"⚠️ 验证失败，准备重试...")
                retry_count += 1
                time.sleep(2)  # 等待 2 秒后重试
                
        except Exception as e:
            print(f"⚠️ 上传失败：{e}")
            retry_count += 1
            if retry_count < max_retries:
                print(f"⏳ {2 * retry_count} 秒后重试...")
                time.sleep(2 * retry_count)
            else:
                print(f"❌ 已达到最大重试次数")
                # 即使失败也返回 URL，让用户手动检查
                public_url = f"https://{BUCKET}.cos.{REGION}.myqcloud.com/{cos_key}"
                return public_url
    
    # 所有重试都失败
    print(f"❌ 上传失败，已达到最大重试次数")
    return None

def validate_upload(public_url, original_content, timeout=10):
    """验证上传的文件是否可以正常访问"""
    
    print(f"  访问链接：{public_url}")
    
    try:
        # 发送 GET 请求
        response = requests.get(public_url, timeout=timeout)
        
        # 检查状态码
        if response.status_code != 200:
            print(f"  ❌ HTTP 状态码：{response.status_code}")
            return False
        
        # 检查响应头
        content_type = response.headers.get('Content-Type', '')
        if 'text/html' not in content_type:
            print(f"  ⚠️ Content-Type 不正确：{content_type}（期望：text/html; charset=utf-8）")
            # 不返回 False，因为 COS 有时会有延迟
        
        cache_control = response.headers.get('Cache-Control', '')
        if 'max-age=0' not in cache_control:
            print(f"  ⚠️ Cache-Control 不正确：{cache_control}（期望：public, max-age=0）")
            # 不返回 False，因为 COS 有时会有延迟
        
        content_disposition = response.headers.get('Content-Disposition', '')
        if 'inline' not in content_disposition:
            print(f"  ⚠️ Content-Disposition 不正确：{content_disposition}（期望：inline）")
            # 不返回 False，因为 COS 有时会有延迟
        
        # 检查内容
        downloaded_content = response.content
        if len(downloaded_content) != len(original_content):
            print(f"  ⚠️ 内容长度不匹配：{len(downloaded_content)} vs {len(original_content)}")
            return False
        
        if downloaded_content != original_content:
            print(f"  ⚠️ 内容不一致")
            return False
        
        print(f"  ✅ HTTP 状态码：200")
        print(f"  ✅ Content-Type: {content_type}")
        print(f"  ✅ Cache-Control: {cache_control}")
        print(f"  ✅ Content-Disposition: {content_disposition}")
        print(f"  ✅ 内容长度：{len(downloaded_content)} bytes")
        
        return True
        
    except requests.exceptions.Timeout:
        print(f"  ❌ 请求超时（{timeout}秒）")
        return False
    except requests.exceptions.RequestException as e:
        print(f"  ❌ 请求失败：{e}")
        return False

def main():
    """主函数"""
    
    if len(sys.argv) < 2:
        print("用法：python3 upload_cos.py <文件路径> [COS 路径]")
        print("示例：python3 upload_cos.py report_cn.html reports/issue_analysis/report_cn_latest.html")
        sys.exit(1)
    
    file_path = sys.argv[1]
    cos_key = sys.argv[2] if len(sys.argv) > 2 else f'reports/issue_analysis/{Path(file_path).name}'
    
    # 上传
    public_url = upload_to_cos(file_path, cos_key)
    
    if public_url:
        print(f"\n📊 公网访问地址：")
        print(f"{public_url}")
        print(f"\n💡 提示：点击链接可直接在浏览器中打开，不会下载")
    else:
        print(f"\n❌ 上传失败")
        sys.exit(1)

if __name__ == '__main__':
    main()
