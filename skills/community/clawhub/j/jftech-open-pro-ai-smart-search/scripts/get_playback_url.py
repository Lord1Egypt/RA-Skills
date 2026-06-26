#!/usr/bin/env python3
"""
云存报警视频回放地址获取脚本

工作流程：
1. 先通过 AI 智搜获取云存报警信息视频列表
2. 提取录像开始时间（st 对应 startTime）和录像结束时间（et 对应 stopTime）
3. 通过设备序列号生成 deviceToken
4. 通过获取云存报警视频回放或下载地址接口，获取播放链接

官方文档：
https://docs.jftech.com/docs?menusId=54582398fd8d4248962354e92ac2e47a&siderId=2e08468f46564602d01ae8a244661672

API 端点：
1. 获取设备 Token: POST https://api.jftechws.com/gwp/v3/rtc/device/token
2. 云存回放：POST https://api.jftechws.com/gwp/v3/rtc/device/getVideoUrl/{deviceToken}

用法：
    # 设置环境变量（必需）
    export JF_UUID="your-uuid"
    export JF_APPKEY="your-appkey"
    export JF_APPSECRET="your-appsecret"
    export JF_MOVECARD=5              # 签名算法偏移量 (0-9)
    export JF_SN="your-device-sn"
    export JF_USER="admin"            # 可选，默认 admin
    export JF_ENDPOINT="api.jftechws.com"  # 可选
    
    # 完整流程：AI 智搜 + 播放地址
    python get_playback_url.py --search "人" --video-index 0
    
    # 直接获取指定时间的播放地址
    python get_playback_url.py --start-time "2026-03-28 15:23:26" --stop-time "2026-03-28 15:23:36"
"""

import argparse
import hashlib
import json
import os
import time
import sys
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError


def generate_timestamp(movecard=0):
    """
    生成当前时间戳（毫秒），可选加上 movecard 偏移量
    
    Args:
        movecard: 签名算法偏移量 (0-9)，用于增加签名安全性
    """
    return str(int(time.time() * 1000) + movecard)


def generate_signature(uuid, app_key, app_secret, time_millis):
    """
    生成杰峰 API 签名
    
    签名算法：MD5(uuid + appKey + timeMillis + secret)
    
    Args:
        uuid: 开放平台用户 uuid
        app_key: 应用 appKey
        app_secret: 应用密钥
        time_millis: 时间戳（毫秒），已包含 movecard 偏移
    """
    sign_str = uuid + app_key + time_millis + app_secret
    return hashlib.md5(sign_str.encode('utf-8')).hexdigest()


def get_device_token(sn, uuid, app_key, app_secret, movecard=0, endpoint="api.jftechws.com"):
    """
    通过设备序列号生成 deviceToken
    
    API: POST https://api.jftechws.com/gwp/v3/rtc/device/token
    
    Args:
        sn: 设备序列号
        uuid: 开放平台用户 uuid
        app_key: 应用 appKey
        app_secret: 应用密钥
        movecard: 签名算法偏移量 (0-9)
        endpoint: API 端点
    
    Returns:
        dict: API 响应，包含 deviceToken
    """
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
        return {"error": f"HTTP Error {e.code}: {e.reason}", "status": e.code}
    except URLError as e:
        return {"error": f"URL Error: {e.reason}"}
    except Exception as e:
        return {"error": str(e)}


def get_cloud_playback_url(device_token, sn, user, start_time, stop_time, 
                           uuid, app_key, app_secret, movecard=0,
                           channel=0, stream_type=1, endpoint="api.jftechws.com"):
    """
    获取云存报警视频回放或下载地址
    
    根据录像开始时间（st 对应 startTime）和录像结束时间（et 对应 stopTime）
    获取对应云存报警视频播放链接
    
    API: POST https://api.jftechws.com/gwp/v3/rtc/device/getVideoUrl/{deviceToken}
    
    官方文档：
    https://docs.jftech.com/docs?menusId=54582398fd8d4248962354e92ac2e47a&siderId=2e08468f46564602d01ae8a244661672
    
    Args:
        device_token: 设备 Token（从 get_device_token 获取）
        sn: 设备序列号
        user: 用户 ID
        start_time: 录像开始时间（格式：YYYY-MM-DD HH:MM:SS，对应 AI 智搜的 st 字段）
        stop_time: 录像结束时间（格式：YYYY-MM-DD HH:MM:SS，对应 AI 智搜的 et 字段）
        uuid: 开放平台用户 uuid
        app_key: 应用 appKey
        app_secret: 应用密钥
        movecard: 签名算法偏移量 (0-9)
        channel: 通道号（默认 0）
        stream_type: 码流类型（1=辅码流，2=主码流，默认 1）
        endpoint: API 端点
    
    Returns:
        dict: API 响应，包含播放地址
    """
    time_millis = generate_timestamp(movecard)
    signature = generate_signature(uuid, app_key, app_secret, time_millis)
    
    # 云存回放 API 端点
    url = f"https://{endpoint}/gwp/v3/rtc/device/getVideoUrl/{device_token}"
    
    headers = {
        "uuid": uuid,
        "appKey": app_key,
        "timeMillis": time_millis,
        "signature": signature,
        "Content-Type": "application/json"
    }
    
    # 请求体：startTime 对应 st，stopTime 对应 et
    body = {
        "sn": sn,
        "user": user,
        "startTime": start_time,
        "stopTime": stop_time,
        "channel": channel,
        "streamType": stream_type
    }
    
    req = Request(url, data=json.dumps(body).encode('utf-8'), headers=headers, method="POST")
    
    try:
        with urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
    except HTTPError as e:
        return {"error": f"HTTP Error {e.code}: {e.reason}", "status": e.code}
    except URLError as e:
        return {"error": f"URL Error: {e.reason}"}
    except Exception as e:
        return {"error": str(e)}


def ai_search(sn, user, search_content, uuid, app_key, app_secret, movecard=0, endpoint="api.jftechws.com"):
    """
    AI 智搜 - 搜索云存报警视频
    
    API: POST https://api.jftechws.com/aisvr/v3/gateway/api/viewsearch/searchVideo
    
    Args:
        sn: 设备序列号
        user: 用户 ID
        search_content: 搜索内容
        uuid: 开放平台用户 uuid
        app_key: 应用 appKey
        app_secret: 应用密钥
        movecard: 签名算法偏移量 (0-9)
        endpoint: API 端点
    
    Returns:
        dict: API 响应
    """
    time_millis = generate_timestamp(movecard)
    signature = generate_signature(uuid, app_key, app_secret, time_millis)
    
    url = f"https://{endpoint}/aisvr/v3/gateway/api/viewsearch/searchVideo"
    
    headers = {
        "uuid": uuid,
        "appKey": app_key,
        "timeMillis": time_millis,
        "signature": signature,
        "Content-Type": "application/json"
    }
    
    body = {
        "sn": sn,
        "user": user,
        "searchContent": search_content
    }
    
    req = Request(url, data=json.dumps(body).encode('utf-8'), headers=headers, method="POST")
    
    try:
        with urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
    except HTTPError as e:
        return {"error": f"HTTP Error {e.code}: {e.reason}"}
    except URLError as e:
        return {"error": f"URL Error: {e.reason}"}
    except Exception as e:
        return {"error": str(e)}


def ai_search_and_playback(sn, user, search_content, uuid, app_key, app_secret, movecard=0,
                           video_index=0, endpoint="api.jftechws.com"):
    """
    完整流程：AI 智搜 + 云存报警视频回放地址获取
    
    1. 通过搜索视频获取云存报警信息视频列表
    2. 提取录像开始时间（st 对应 startTime）和录像结束时间（et 对应 stopTime）
    3. 通过设备序列号生成 deviceToken
    4. 通过获取云存报警视频回放或下载地址接口，获取播放链接
    
    Args:
        sn: 设备序列号
        user: 用户 ID
        search_content: 搜索内容
        uuid: 开放平台用户 uuid
        app_key: 应用 appKey
        app_secret: 应用密钥
        movecard: 签名算法偏移量 (0-9)
        video_index: 选择第几个视频（从 0 开始）
        endpoint: API 端点
    
    Returns:
        dict: 包含搜索结果和播放地址
    """
    print("=" * 70)
    print("🎬 AI 智搜 + 云存报警视频回放地址获取")
    print("=" * 70)
    print()
    print(f"设备 SN: {sn}")
    print(f"用户：{user}")
    print(f"搜索内容：{search_content}")
    print(f"选择视频索引：{video_index}")
    print()
    
    # 步骤 1: AI 智搜 - 获取云存报警信息视频列表
    print(">>> 步骤 1: 搜索视频获取云存报警信息视频列表...")
    search_result = ai_search(sn, user, search_content, uuid, app_key, app_secret, movecard, endpoint)
    
    if search_result.get('error'):
        print(f"❌ AI 智搜失败：{search_result['error']}")
        return {"error": search_result['error']}
    
    if search_result.get('code') != 2000:
        print(f"❌ AI 智搜失败：{search_result.get('msg', 'Unknown error')}")
        return {"error": search_result.get('msg', 'Unknown error')}
    
    videos = search_result.get('data', [])
    if not videos:
        print("❌ 未找到匹配的视频")
        return {"error": "No videos found"}
    
    print(f"✅ AI 智搜成功，找到 {len(videos)} 条视频")
    print()
    
    # 选择指定索引的视频
    if video_index >= len(videos):
        print(f"❌ 视频索引 {video_index} 超出范围（0-{len(videos)-1}）")
        return {"error": f"Video index {video_index} out of range"}
    
    video = videos[video_index]
    print(f"📹 选择第 {video_index + 1} 个视频：")
    print(f"   录像开始时间（st）：{video['st']}")
    print(f"   录像结束时间（et）：{video['et']}")
    print(f"   匹配度：{video['matchRate']:.1%}")
    print(f"   文件名：{video['indx']}")
    print()
    
    # 步骤 2: 通过设备序列号生成 deviceToken
    print(">>> 步骤 2: 通过设备序列号生成 deviceToken...")
    token_result = get_device_token(sn, uuid, app_key, app_secret, movecard, endpoint)
    
    if token_result.get('error'):
        print(f"❌ 获取 deviceToken 失败：{token_result['error']}")
        return {"error": token_result['error'], "search_result": search_result}
    
    if token_result.get('code') != 2000:
        print(f"❌ 获取 deviceToken 失败：{token_result.get('msg', 'Unknown error')}")
        return {"error": token_result.get('msg', 'Unknown error'), "search_result": search_result}
    
    device_token = token_result['data'][0]['deviceToken']
    print(f"✅ deviceToken 获取成功：{device_token[:30]}...")
    print()
    
    # 步骤 3: 获取云存报警视频回放地址
    print(">>> 步骤 3: 获取云存报警视频回放地址...")
    print(f"   API 端点：POST /gwp/v3/rtc/device/getVideoUrl/{device_token[:30]}...")
    print(f"   startTime: {video['st']} (对应 st)")
    print(f"   stopTime: {video['et']} (对应 et)")
    print()
    
    playback_result = get_cloud_playback_url(
        device_token=device_token,
        sn=sn,
        user=user,
        start_time=video['st'],  # st 对应 startTime
        stop_time=video['et'],    # et 对应 stopTime
        uuid=uuid,
        app_key=app_key,
        app_secret=app_secret,
        endpoint=endpoint
    )
    
    if playback_result.get('error'):
        print(f"❌ 获取播放地址失败：{playback_result['error']}")
        return {"error": playback_result['error'], "search_result": search_result}
    
    if playback_result.get('code') != 2000:
        print(f"❌ 获取播放地址失败：{playback_result.get('msg', 'Unknown error')}")
        return {"error": playback_result.get('msg', 'Unknown error'), "search_result": search_result}
    
    # 成功获取播放地址
    play_url = playback_result['data'].get('url')
    print("✅ 云存报警视频播放地址获取成功！")
    print()
    print("=" * 70)
    print("🎬 播放地址")
    print("=" * 70)
    print()
    print(f"📹 视频信息：")
    print(f"   时间：{video['st']} - {video['et']}")
    print(f"   时长：10 秒")
    print(f"   匹配度：{video['matchRate']:.1%}")
    print(f"   文件名：{video['indx']}")
    print()
    print(f"🔗 播放地址：")
    print(f"   {play_url}")
    print()
    print("=" * 70)
    print("🎯 播放方式：")
    print("=" * 70)
    print()
    print("1. VLC 播放器：")
    print(f'   vlc "{play_url}"')
    print()
    print("2. 网页播放（HLS.js）：")
    print(f'   <video src="{play_url}" controls></video>')
    print()
    print("3. FFmpeg 下载：")
    print(f'   ffmpeg -i "{play_url}" -c copy video.mp4')
    print()
    
    return {
        "success": True,
        "search_result": search_result,
        "playback_result": playback_result,
        "video_info": video,
        "play_url": play_url
    }


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
        description='AI 智搜 + 云存报警视频回放地址获取',
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

使用流程：
1. 通过搜索视频获取云存报警信息视频列表
2. 提取录像开始时间（st 对应 startTime）和录像结束时间（et 对应 stopTime）
3. 通过设备序列号生成 deviceToken
4. 通过获取云存报警视频回放或下载地址接口，获取播放链接

官方文档：
https://docs.jftech.com/docs?menusId=54582398fd8d4248962354e92ac2e47a&siderId=2e08468f46564602d01ae8a244661672

示例:
  # 设置环境变量
  export JF_UUID="your-uuid"
  export JF_APPKEY="your-appkey"
  export JF_APPSECRET="your-appsecret"
  export JF_MOVECARD=5
  export JF_SN="your-device-sn"
  export JF_USER="admin"
  
  # 完整流程：AI 智搜 + 播放地址
  python get_playback_url.py --search "人" --video-index 0
  
  # 直接获取指定时间的播放地址
  python get_playback_url.py --start-time "2026-04-07 12:00:00" --stop-time "2026-04-07 12:45:00"
        '''
    )
    
    parser.add_argument('--search', help='搜索内容（如"人"、"车"、"狗"）')
    parser.add_argument('--video-index', type=int, default=0, help='选择第几个视频（从 0 开始，默认 0）')
    parser.add_argument('--start-time', help='录像开始时间（格式：YYYY-MM-DD HH:MM:SS）')
    parser.add_argument('--stop-time', help='录像结束时间（格式：YYYY-MM-DD HH:MM:SS）')
    
    args = parser.parse_args()
    
    # 从环境变量读取配置
    try:
        config = get_config_from_env()
    except Exception as e:
        print(f'❌ 配置错误：{e}')
        sys.exit(1)
    
    # 如果有 search 参数，执行完整流程
    if args.search:
        result = ai_search_and_playback(
            sn=config['sn'],
            user=config['user'],
            search_content=args.search,
            uuid=config['uuid'],
            app_key=config['appkey'],
            app_secret=config['appsecret'],
            movecard=config['movecard'],
            video_index=args.video_index,
            endpoint=config['endpoint']
        )
    # 如果有 start_time 和 stop_time 参数，直接获取播放地址
    elif args.start_time and args.stop_time:
        print(">>> 通过设备序列号生成 deviceToken...")
        token_result = get_device_token(config['sn'], config['uuid'], config['appkey'], config['appsecret'], config['movecard'], config['endpoint'])
        
        if token_result.get('error') or token_result.get('code') != 2000:
            print(f"❌ 获取 deviceToken 失败：{token_result.get('error') or token_result.get('msg')}")
            sys.exit(1)
        
        device_token = token_result['data'][0]['deviceToken']
        print(f"✅ deviceToken 获取成功")
        
        print(">>> 获取云存报警视频回放地址...")
        playback_result = get_cloud_playback_url(
            device_token=device_token,
            sn=config['sn'],
            user=config['user'],
            start_time=args.start_time,
            stop_time=args.stop_time,
            uuid=config['uuid'],
            app_key=config['appkey'],
            app_secret=config['appsecret'],
            movecard=config['movecard'],
            endpoint=config['endpoint']
        )
        
        if playback_result.get('error') or playback_result.get('code') != 2000:
            print(f"❌ 获取播放地址失败：{playback_result.get('error') or playback_result.get('msg')}")
            sys.exit(1)
        
        play_url = playback_result['data'].get('url')
        print(f"✅ 播放地址：{play_url}")
        result = {"success": True, "play_url": play_url}
    else:
        parser.print_help()
        sys.exit(1)
    
    # 输出 JSON 结果
    print()
    print("=" * 70)
    print("📋 JSON 结果")
    print("=" * 70)
    print()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    sys.exit(0 if result.get('success') else 1)


if __name__ == '__main__':
    main()
