#!/usr/bin/env python3
"""
获取本地录像回放列表脚本
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


def get_local_video_list(device_token, start_time, stop_time, uuid, app_key, 
                         app_secret, movecard=5, channel=0, event="*", 
                         endpoint="api.jftechws.com"):
    """获取本地录像回放列表"""
    time_millis = generate_timestamp()
    signature = generate_signature(uuid, app_key, app_secret, time_millis, movecard)
    
    url = f"https://{endpoint}/gwp/v3/rtc/device/opdev/{device_token}"
    headers = {
        "uuid": uuid, "appKey": app_key, "timeMillis": time_millis,
        "signature": signature, "Content-Type": "application/json"
    }
    
    body = {
        "Name": "OPFileQuery",
        "OPFileQuery": {
            "BeginTime": start_time,
            "EndTime": stop_time,
            "Channel": channel,
            "DriverTypeMask": "0x0000FFFF",
            "Event": event,
            "StreamType": "0x00000000",
            "Type": "h264"
        }
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


def format_video_list(result):
    """格式化本地录像列表输出"""
    if result.get('error'):
        return f"❌ 错误：{result['error']}"
    
    if result.get('code') != 2000:
        return f"❌ API 错误码：{result.get('code')}\n   详情：{result.get('msg', 'Unknown error')}"
    
    data = result.get('data', {})
    if data.get('Ret') != 100:
        return f"❌ 设备错误码：{data.get('Ret')}"
    
    videos = data.get('OPFileQuery', [])
    if not videos:
        return "📭 未找到匹配的录像文件"
    
    output = [f"✅ 找到 {len(videos)} 个录像文件", ""]
    
    for i, video in enumerate(videos, 1):
        output.append(f"📹 录像 {i}:")
        output.append(f"   时间：{video.get('BeginTime', 'N/A')} - {video.get('EndTime', 'N/A')}")
        output.append(f"   文件名：{video.get('FileName', 'N/A')}")
        file_length = video.get('FileLength', '0')
        if isinstance(file_length, str) and file_length.startswith('0x'):
            file_length_kb = int(file_length, 16) / 1024
        else:
            file_length_kb = int(file_length) / 1024 if file_length else 0
        output.append(f"   大小：{file_length_kb:.1f} MB")
        output.append("")
    
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description='获取本地录像回放列表')
    parser.add_argument('--start-time', required=True, help='开始时间（YYYY-mm-dd HH:MM:SS）')
    parser.add_argument('--stop-time', required=True, help='结束时间')
    parser.add_argument('--channel', type=int, default=0, help='设备通道号')
    parser.add_argument('--event', default='*', help='录像类型')
    parser.add_argument('--json', action='store_true', help='输出 JSON 格式')
    
    args = parser.parse_args()
    
    try:
        config = get_config_from_env()
    except Exception as e:
        print(f'❌ 配置错误：{e}')
        sys.exit(1)
    
    print("=" * 70)
    print("📋 获取本地录像回放列表")
    print("=" * 70)
    print(f"设备 SN: {config['sn']}")
    print(f"时间范围：{args.start_time} - {args.stop_time}")
    print(f"录像类型：{args.event}")
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
    
    print(">>> 获取本地录像列表...")
    result = get_local_video_list(
        device_token=device_token, start_time=args.start_time, stop_time=args.stop_time,
        uuid=config['uuid'], app_key=config['appkey'], app_secret=config['appsecret'],
        movecard=config['movecard'], channel=args.channel, event=args.event,
        endpoint=config['endpoint']
    )
    
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(format_video_list(result))
    
    sys.exit(0 if result.get('code') == 2000 and result.get('data', {}).get('Ret') == 100 else 1)


if __name__ == '__main__':
    main()
