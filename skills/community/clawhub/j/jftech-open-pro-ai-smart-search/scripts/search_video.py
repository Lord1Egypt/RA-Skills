#!/usr/bin/env python3
"""
AI 智搜脚本 - 搜索云存报警视频

仅支持环境变量配置凭据，避免命令行泄露风险。

支持平台：JF Tech（杰峰）
用法:
    export JF_UUID="your-uuid"
    export JF_APPKEY="your-appkey"
    export JF_APPSECRET="your-appsecret"
    export JF_MOVECARD=5
    export JF_SN="your-device-sn"
    export JF_USER="admin"
    
    python search_video.py --search "人"
    python search_video.py --search "车"
    python search_video.py --search "戴帽子的人"
"""

import argparse
import hashlib
import json
import os
import time
import sys
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError


def generate_jftech_sign(appkey: str, secret: str, timestamp: int, movecard: int = 0) -> str:
    """
    生成 JF Tech API 签名
    
    Args:
        appkey: 应用 appKey
        secret: 应用密钥
        timestamp: 时间戳（毫秒）
        movecard: 签名算法偏移量 (0-9)，用于增加签名安全性
    """
    # 时间戳加上 movecard 偏移量
    adjusted_timestamp = timestamp + movecard
    sign_str = f"{appkey}{adjusted_timestamp}{secret}"
    return hashlib.md5(sign_str.encode()).hexdigest()


def search_jftech(sn: str, user: str, query: str, uuid: str, appkey: str, 
                  secret: str, authorization: str, movecard: int = 0) -> dict:
    """
    调用 JF Tech AI 智搜 API
    
    Args:
        sn: 设备序列号
        user: 用户 ID
        query: 搜索内容（语义描述）
        uuid: 开放平台用户 uuid
        appkey: 应用 appKey
        secret: 应用密钥
        authorization: 用户 token
        movecard: 签名算法偏移量 (0-9)
    
    Returns:
        API 响应字典
    """
    url = "https://api.jftechws.com/aisvr/v3/gateway/api/viewsearch/searchVideo"
    timestamp = int(time.time() * 1000)
    sign = generate_jftech_sign(appkey, secret, timestamp, movecard)
    
    headers = {
        "Content-Type": "application/json",
        "uuid": uuid,
        "appkey": appkey,
        "sign": sign,
        "timestamp": str(timestamp),
        "authorization": authorization
    }
    
    body = {
        "sn": sn,
        "user": user,
        "searchContent": query
    }
    
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    
    try:
        with urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode())
            return result
    except HTTPError as e:
        return {"error": f"HTTP {e.code}", "message": e.read().decode()}
    except URLError as e:
        return {"error": "Network error", "message": str(e)}


def format_results(results: dict) -> str:
    """格式化搜索结果输出"""
    if "error" in results:
        return f"❌ 错误：{results.get('error', 'Unknown')}\n{results.get('message', '')}"
    
    if results.get("code") != 2000:
        return f"❌ API 错误码：{results.get('code')}\n{results.get('msg', '')}"
    
    data = results.get("data", {})
    videos = data.get("videos", [])
    
    if not videos:
        return "📭 未找到匹配的视频"
    
    output = []
    output.append(f"✅ 找到 {len(videos)} 个匹配的视频片段\n")
    
    for i, video in enumerate(videos, 1):
        output.append(f"📹 片段 {i}:")
        output.append(f"   时间：{video.get('eventTime', 'N/A')}")
        output.append(f"   匹配度：{video.get('matchRate', 0):.0%}")
        output.append(f"   标签：{', '.join(video.get('queryTags', []))}")
        output.append(f"   大小：{video.get('vidsz', 0) / 1024:.1f} KB")
        if video.get('picfg') == 1:
            output.append(f"   缩略图：有")
        output.append("")
    
    return "\n".join(output)


def get_config_from_env():
    """从环境变量读取配置"""
    required_vars = ['JF_UUID', 'JF_APPKEY', 'JF_APPSECRET', 'JF_MOVECARD', 'JF_SN']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        raise Exception(f"缺少必需的环境变量：{', '.join(missing_vars)}\n"
                       f"请设置：export JF_UUID='...' JF_APPKEY='...' JF_APPSECRET='...' JF_MOVECARD=5 JF_SN='...'")
    
    return {
        'uuid': os.environ.get('JF_UUID'),
        'appkey': os.environ.get('JF_APPKEY'),
        'secret': os.environ.get('JF_APPSECRET'),
        'movecard': int(os.environ.get('JF_MOVECARD', 5)),
        'sn': os.environ.get('JF_SN'),
        'user': os.environ.get('JF_USER', 'admin'),
        'endpoint': os.environ.get('JF_ENDPOINT', 'api.jftechws.com')
    }


def main():
    parser = argparse.ArgumentParser(
        description="AI 智搜 - 搜索云存报警视频",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
环境变量:
  JF_UUID       开放平台用户唯一标识 (必需)
  JF_APPKEY     开放平台应用 Key (必需)
  JF_APPSECRET  开放平台应用密钥 (必需)
  JF_MOVECARD   签名算法偏移量，通常设为 5 (必需)
  JF_SN         设备序列号 (必需)
  JF_USER       用户 ID，默认 admin (可选)
  JF_ENDPOINT   API 端点，默认 api.jftechws.com (可选)

示例:
  # 设置环境变量
  export JF_UUID="your-uuid"
  export JF_APPKEY="your-appkey"
  export JF_APPSECRET="your-appsecret"
  export JF_MOVECARD=5
  export JF_SN="your-device-sn"
  export JF_USER="admin"
  
  # 搜索"人"相关的视频
  python search_video.py --search "人"
  
  # 搜索"车"相关的视频
  python search_video.py --search "车"
  
  # 搜索"戴帽子的人"
  python search_video.py --search "戴帽子的人"
        ''')
    
    parser.add_argument("--search", dest="query", required=True, help="搜索内容（语义描述）")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    
    args = parser.parse_args()
    
    try:
        config = get_config_from_env()
    except Exception as e:
        print(f'❌ 配置错误：{e}')
        sys.exit(1)
    
    result = search_jftech(
        sn=config['sn'],
        user=config['user'],
        query=args.query,
        uuid=config['uuid'],
        appkey=config['appkey'],
        secret=config['secret'],
        authorization='',  # 如需 authorization 可从环境变量添加
        movecard=config['movecard']
    )
    
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(format_results(result))


if __name__ == "__main__":
    main()
