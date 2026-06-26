#!/usr/bin/env python3
"""
AI 智搜 + 云存回放完整流程脚本

工作流程：
1. 调用 AI 智搜 API 获取视频列表
2. 选择指定索引的视频
3. 提取开始/结束时间
4. 调用云存回放 API 获取播放地址

用法:
    export JF_UUID="your-uuid"
    export JF_APPKEY="your-appkey"
    export JF_APPSECRET="your-appsecret"
    export JF_MOVECARD=5
    export JF_SN="your-device-sn"
    export JF_USER="admin"
    
    python ai_search_playback.py --search "人" --video-index 0
"""

import argparse
import hashlib
import json
import os
import sys
import time
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError


def generate_jftech_sign(appkey: str, secret: str, timestamp: int) -> str:
    """生成 JF Tech API 签名"""
    sign_str = f"{appkey}{timestamp}{secret}"
    return hashlib.md5(sign_str.encode()).hexdigest()


def search_jftech(sn: str, user: str, query: str, uuid: str, appkey: str, 
                  secret: str, authorization: str = "") -> dict:
    """调用 JF Tech AI 智搜 API"""
    url = "https://api.jftechws.com/aisvr/v3/gateway/api/viewsearch/searchVideo"
    timestamp = int(time.time() * 1000)
    sign = generate_jftech_sign(appkey, secret, timestamp)
    
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


def generate_timestamp(movecard=0):
    """
    生成当前时间戳（毫秒），可选加上 movecard 偏移量
    
    Args:
        movecard: 签名算法偏移量 (0-9)，用于增加签名安全性
    """
    return str(int(time.time() * 1000) + movecard)


def generate_signature(uuid, app_key, app_secret, time_millis):
    """生成杰峰 API 签名"""
    sign_str = uuid + app_key + time_millis + app_secret
    return hashlib.md5(sign_str.encode('utf-8')).hexdigest()


def get_device_token(sn, uuid, app_key, app_secret, movecard=0, endpoint="api.jftechws.com"):
    """通过设备序列号生成 deviceToken"""
    time_millis = generate_timestamp(movecard)
    signature = generate_signature(uuid, app_key, app_secret, time_millis)
    
    url = f"https://{endpoint}/gwp/v3/rtc/device/token"
    
    headers = {
        "uuid": uuid,
        "appKey": app_key,
        "timeMillis": time_millis,
        "signature": signature,
        "Content-Type": "application/json"
    }
    
    body = {"deviceSnList": [sn]}
    
    req = Request(url, data=json.dumps(body).encode('utf-8'), headers=headers, method="POST")
    
    try:
        with urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
    except HTTPError as e:
        return {"error": f"HTTP {e.code}", "message": e.read().decode()}
    except URLError as e:
        return {"error": "Network error", "message": str(e)}


def get_playback_url(sn, user, start_time, stop_time, uuid, app_key, app_secret, movecard=0,
                     endpoint="api.jftechws.com", stream_type="hls"):
    """获取云存回放地址"""
    token_result = get_device_token(sn, uuid, app_key, app_secret, movecard, endpoint)
    
    if token_result.get('error') or token_result.get('code') != 2000:
        return {"error": f"获取 Token 失败：{token_result.get('error') or token_result.get('msg')}"}
    
    if not token_result.get('data') or len(token_result['data']) == 0:
        return {"error": "获取 Token 失败：返回数据为空"}
    
    device_token = token_result['data'][0]['token']
    
    url = f"https://{endpoint}/gwp/v3/rtc/device/getVideoUrl/{device_token}"
    
    time_millis = generate_timestamp(movecard)
    signature = generate_signature(uuid, app_key, app_secret, time_millis)
    
    headers = {
        "uuid": uuid,
        "appKey": app_key,
        "timeMillis": time_millis,
        "signature": signature,
        "Content-Type": "application/json"
    }
    
    body = {
        "user": user,
        "sn": sn,
        "startTime": start_time,
        "stopTime": stop_time,
        "streamType": stream_type
    }
    
    req = Request(url, data=json.dumps(body).encode('utf-8'), headers=headers, method="POST")
    
    try:
        with urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
    except HTTPError as e:
        return {"error": f"HTTP {e.code}", "message": e.read().decode()}
    except URLError as e:
        return {"error": "Network error", "message": str(e)}


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
        'appsecret': os.environ.get('JF_APPSECRET'),
        'movecard': int(os.environ.get('JF_MOVECARD', 5)),
        'sn': os.environ.get('JF_SN'),
        'user': os.environ.get('JF_USER', 'admin'),
        'endpoint': os.environ.get('JF_ENDPOINT', 'api.jftechws.com')
    }


def main():
    parser = argparse.ArgumentParser(
        description='AI 智搜 + 云存回放完整流程',
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
  
  # 搜索"人"并获取第一个视频的回放地址
  python ai_search_playback.py --search "人" --video-index 0
  
  # 搜索"车"并获取第二个视频的回放地址
  python ai_search_playback.py --search "车" --video-index 1
        ''')
    
    parser.add_argument('--search', required=True, help='搜索内容（如"人"、"车"、"狗"）')
    parser.add_argument('--video-index', type=int, default=0, help='选择第几个视频（从 0 开始，默认 0）')
    
    args = parser.parse_args()
    
    # 从环境变量读取配置
    try:
        config = get_config_from_env()
    except Exception as e:
        print(f'❌ 配置错误：{e}')
        sys.exit(1)
    
    print('========================================')
    print('AI 智搜 + 云存回放完整流程')
    print('========================================')
    print(f"设备 SN: {config['sn']}")
    print(f"搜索内容：{args.search}")
    print(f"视频索引：{args.video_index}")
    print()
    
    # 步骤 1: AI 智搜
    print('>>> 步骤 1/3: AI 智搜搜索视频...')
    search_result = search_jftech(
        sn=config['sn'],
        user=config['user'],
        query=args.search,
        uuid=config['uuid'],
        appkey=config['appkey'],
        secret=config['appsecret']
    )
    
    if search_result.get('error'):
        print(f"❌ AI 智搜失败：{search_result['error']}")
        if search_result.get('message'):
            print(f"   详情：{search_result['message']}")
        sys.exit(1)
    
    if search_result.get('code') != 2000:
        print(f"❌ API 错误码：{search_result.get('code')}")
        print(f"   详情：{search_result.get('msg', 'Unknown error')}")
        sys.exit(1)
    
    data = search_result.get('data', {})
    videos = data.get('videos', [])
    
    if not videos:
        print('❌ 未找到匹配的视频')
        sys.exit(1)
    
    print(f"✅ 找到 {len(videos)} 个匹配的视频")
    
    if args.video_index >= len(videos):
        print(f"❌ 视频索引 {args.video_index} 超出范围 (0-{len(videos)-1})")
        sys.exit(1)
    
    video = videos[args.video_index]
    print(f"   选择：片段 {args.video_index + 1}")
    print(f"   时间：{video.get('eventTime', 'N/A')}")
    print(f"   匹配度：{video.get('matchRate', 0):.0%}")
    print()
    
    # 步骤 2: 提取时间
    start_time = video.get('st')
    stop_time = video.get('et')
    
    if not start_time or not stop_time:
        print('❌ 无法提取视频时间信息')
        sys.exit(1)
    
    # 转换时间戳为可读格式
    from datetime import datetime
    start_dt = datetime.fromtimestamp(start_time)
    stop_dt = datetime.fromtimestamp(stop_time)
    
    print('>>> 步骤 2/3: 提取视频时间...')
    print(f"   开始：{start_dt.strftime('%Y-%m-%d %H:%M:%S')} ({start_time})")
    print(f"   结束：{stop_dt.strftime('%Y-%m-%d %H:%M:%S')} ({stop_time})")
    print()
    
    # 步骤 3: 获取回放地址
    print('>>> 步骤 3/3: 获取云存回放地址...')
    playback_result = get_playback_url(
        sn=config['sn'],
        user=config['user'],
        start_time=start_time,
        stop_time=stop_time,
        uuid=config['uuid'],
        app_key=config['appkey'],
        app_secret=config['appsecret'],
        movecard=config['movecard'],
        endpoint=config['endpoint']
    )
    
    if playback_result.get('error'):
        print(f"❌ 获取回放地址失败：{playback_result['error']}")
        sys.exit(1)
    
    if playback_result.get('code') != 2000:
        print(f"❌ API 错误码：{playback_result.get('code')}")
        print(f"   详情：{playback_result.get('msg', 'Unknown error')}")
        sys.exit(1)
    
    playback_data = playback_result.get('data', {})
    playback_url = playback_data.get('url') or playback_data.get('playUrl')
    
    if not playback_url:
        print('❌ 未找到播放 URL')
        print(json.dumps(playback_result, indent=2, ensure_ascii=False))
        sys.exit(1)
    
    print('✅ 回放地址获取成功')
    print()
    print('========================================')
    print('播放信息')
    print('========================================')
    print(f"设备 SN: {config['sn']}")
    print(f"时间范围：{start_dt.strftime('%Y-%m-%d %H:%M:%S')} - {stop_dt.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"播放地址：{playback_url}")
    print()
    print("使用方式:")
    print(f"  - VLC 播放：vlc \"{playback_url}\"")
    print(f"  - 网页播放：在浏览器中打开 URL")
    print(f"  - 下载：curl -o video.mp4 \"{playback_url}\"")
    print('========================================')


if __name__ == "__main__":
    main()
