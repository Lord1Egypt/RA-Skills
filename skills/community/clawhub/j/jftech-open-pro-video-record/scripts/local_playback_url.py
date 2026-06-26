#!/usr/bin/env python3
"""
获取本地录像回放或下载地址脚本
"""

import argparse
import hashlib
import json
import os
import sys
import time
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError


def generate_timestamp():
    """生成 20 位时间戳（毫秒）"""
    return str(int(time.time() * 1000)).zfill(20)


def str2byte(s):
    """字符串转字节数组"""
    return list(s.encode('utf-8'))


def change(encrypt_str, move_card):
    """移位算法"""
    encrypt_byte = str2byte(encrypt_str)
    length = len(encrypt_byte)
    for idx in range(length):
        tmp = encrypt_byte[idx] if (idx % move_card) > ((length - idx) % move_card) else encrypt_byte[length - (idx + 1)]
        encrypt_byte[idx], encrypt_byte[length - (idx + 1)] = encrypt_byte[length - (idx + 1)], tmp
    return encrypt_byte


def merge_byte(encrypt_byte, change_byte):
    """合并字节数组"""
    length = len(encrypt_byte)
    temp = [0] * (length * 2)
    for idx in range(length):
        temp[idx] = encrypt_byte[idx]
        temp[length * 2 - 1 - idx] = change_byte[idx]
    return temp


def generate_signature(uuid, app_key, app_secret, time_millis, movecard=5):
    """生成杰峰 API 签名"""
    encrypt_str = uuid + app_key + app_secret + time_millis
    encrypt_byte = str2byte(encrypt_str)
    change_byte = change(encrypt_str, movecard)
    merged_byte = merge_byte(encrypt_byte, change_byte)
    return hashlib.md5(bytes(merged_byte)).hexdigest()


def get_device_token(sn, uuid, app_key, app_secret, movecard=5, endpoint="api.jftechws.com"):
    """通过设备序列号生成 deviceToken"""
    time_millis = generate_timestamp()
    signature = generate_signature(uuid, app_key, app_secret, time_millis, movecard)
    
    url = f"https://{endpoint}/gwp/v3/rtc/device/token"
    headers = {
        "uuid": uuid, "appKey": app_key, "timeMillis": time_millis,
        "signature": signature, "Content-Type": "application/json"
    }
    body = {"sns": [sn], "accessToken": ""}
    
    req = Request(url, data=json.dumps(body).encode('utf-8'), headers=headers, method="POST")
    try:
        with urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except HTTPError as e:
        return {"error": f"HTTP Error {e.code}: {e.reason}", "status": e.code}
    except Exception as e:
        return {"error": str(e)}


def get_local_playback_url(device_token, uuid, app_key, app_secret, movecard=5,
                           channel=0, stream_type=1, protocol="hls-ts",
                           start_time=None, end_time=None, file_name=None,
                           username="admin", password="", download=False,
                           endpoint="api.jftechws.com"):
    """获取本地录像回放或下载地址"""
    time_millis = generate_timestamp()
    signature = generate_signature(uuid, app_key, app_secret, time_millis, movecard)
    
    url = f"https://{endpoint}/gwp/v3/rtc/device/playbackUrl/{device_token}"
    headers = {
        "uuid": uuid, "appKey": app_key, "timeMillis": time_millis,
        "signature": signature, "Content-Type": "application/json"
    }
    
    body = {
        "channel": channel,
        "streamType": stream_type,
        "protocol": protocol,
        "startTime": start_time,
        "endTime": end_time,
        "fileName": file_name,
        "username": username,
        "password": password,
        "download": 1 if download else 0
    }
    
    req = Request(url, data=json.dumps(body).encode('utf-8'), headers=headers, method="POST")
    try:
        with urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except HTTPError as e:
        return {"error": f"HTTP Error {e.code}: {e.reason}", "status": e.code}
    except Exception as e:
        return {"error": str(e)}


def get_config_from_env():
    """从环境变量读取配置"""
    required_vars = ['JF_UUID', 'JF_APPKEY', 'JF_APPSECRET', 'JF_MOVECARD', 'JF_SN']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    if missing_vars:
        raise Exception(f"缺少必需的环境变量：{', '.join(missing_vars)}")
    
    return {
        'uuid': os.environ.get('JF_UUID'),
        'appkey': os.environ.get('JF_APPKEY'),
        'appsecret': os.environ.get('JF_APPSECRET'),
        'movecard': int(os.environ.get('JF_MOVECARD', 5)),
        'sn': os.environ.get('JF_SN'),
        'username': os.environ.get('JF_USERNAME', 'admin'),
        'password': os.environ.get('JF_PASSWORD', ''),
        'endpoint': os.environ.get('JF_ENDPOINT', 'api.jftechws.com')
    }


def main():
    parser = argparse.ArgumentParser(description='获取本地录像回放或下载地址')
    parser.add_argument('--file-name', required=True, help='录像文件名')
    parser.add_argument('--start-time', required=True, help='回放开始时间')
    parser.add_argument('--stop-time', required=True, help='回放结束时间')
    parser.add_argument('--channel', type=int, default=0, help='设备通道号')
    parser.add_argument('--stream-type', type=int, choices=[0, 1], default=1, help='码流类型')
    parser.add_argument('--protocol', default='hls-ts', choices=['flv', 'flv-enhanced', 'hls-ts', 'hls-fmp4', 'mp4', 'rtsp-sdp', 'rtsp-pri'])
    parser.add_argument('--download', action='store_true', help='下载模式')
    
    args = parser.parse_args()
    
    try:
        config = get_config_from_env()
    except Exception as e:
        print(f'❌ 配置错误：{e}')
        sys.exit(1)
    
    print("=" * 70)
    print("🎬 获取本地录像回放地址")
    print("=" * 70)
    print(f"设备 SN: {config['sn']}")
    print(f"文件名：{args.file_name}")
    print(f"时间：{args.start_time} - {args.stop_time}")
    print(f"协议：{args.protocol}")
    print()
    
    print(">>> 获取设备 Token...")
    token_result = get_device_token(config['sn'], config['uuid'], config['appkey'], 
                                    config['appsecret'], config['movecard'], config['endpoint'])
    
    if token_result.get('error') or token_result.get('code') != 2000:
        print(f"❌ 获取设备 Token 失败：{token_result.get('error') or token_result.get('msg')}")
        sys.exit(1)
    
    device_token = token_result['data'][0]['token']
    print(f"✅ 设备 Token 获取成功")
    print()
    
    print(">>> 获取回放地址...")
    result = get_local_playback_url(
        device_token=device_token, uuid=config['uuid'], app_key=config['appkey'],
        app_secret=config['appsecret'], movecard=config['movecard'],
        channel=args.channel, stream_type=args.stream_type, protocol=args.protocol,
        start_time=args.start_time, end_time=args.stop_time, file_name=args.file_name,
        username=config['username'], password=config['password'], download=args.download,
        endpoint=config['endpoint']
    )
    
    if result.get('error'):
        print(f"❌ 获取回放地址失败：{result['error']}")
        sys.exit(1)
    
    if result.get('code') != 2000:
        print(f"❌ API 错误码：{result.get('code')} - {result.get('msg')}")
        sys.exit(1)
    
    data = result.get('data', {})
    if data.get('Ret') != 100:
        print(f"❌ 设备错误码：{data.get('Ret')}")
        sys.exit(1)
    
    play_url = data.get('url')
    if not play_url:
        print("❌ 未找到播放 URL")
        sys.exit(1)
    
    print("✅ 回放地址获取成功！")
    print()
    print("=" * 70)
    print("🔗 播放地址")
    print("=" * 70)
    print(f"{play_url}")
    print()
    print("⚠️ 回放地址有效期 10 小时，同时只支持一路回放")
    print()
    # 仅输出必要信息，避免泄露完整响应数据
    print("=" * 70)
    print("📋 响应摘要")
    print("=" * 70)
    print()
    print(json.dumps({"code": result.get('code'), "msg": result.get('msg')}, indent=2, ensure_ascii=False))
    
    sys.exit(0)


if __name__ == '__main__':
    main()
