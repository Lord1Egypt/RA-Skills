#!/usr/bin/env python3
"""
获取云存视频列表脚本

支持场景：
1. 条件查询（时间范围）- 根据起始时间和结束时间查询视频列表
2. 组合条件查询（分页 + 报警类型）- 精准查询特定报警类型的视频

官方文档：
https://docs.jftech.com/docs?menusId=54582398fd8d4248962354e92ac2e47a&siderId=66142b2ca13c418d84085772a627d650

API 端点：
POST https://api.jftechws.com/gwp/v3/rtc/device/getVideoList/{deviceToken}

用法:
    export JF_UUID="your-uuid"
    export JF_APPKEY="your-appkey"
    export JF_APPSECRET="your-appsecret"
    export JF_MOVECARD=5
    export JF_SN="your-device-sn"
    
    # 按时间范围查询
    python cloud_video_list.py --start-time "2026-04-07 10:00:00" --stop-time "2026-04-07 18:00:00"
    
    # 带报警类型过滤
    python cloud_video_list.py --start-time "2026-04-07 10:00:00" --stop-time "2026-04-07 18:00:00" --events "HumanDetect"
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
    """字符串转字节数组（UTF-8 编码）"""
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
    """生成杰峰 API 签名（复杂加密算法）"""
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
        "uuid": uuid,
        "appKey": app_key,
        "timeMillis": time_millis,
        "signature": signature,
        "Content-Type": "application/json"
    }
    
    # 使用 sns 参数（杰峰 API 要求）
    body = {"sns": [sn], "accessToken": ""}
    
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


def get_cloud_video_list(device_token, sn, start_time, stop_time, uuid, app_key, 
                         app_secret, movecard=5, channel=0, page_start=1, 
                         page_size=200, events=None, endpoint="api.jftechws.com"):
    """获取云存视频列表"""
    time_millis = generate_timestamp()
    signature = generate_signature(uuid, app_key, app_secret, time_millis, movecard)
    
    url = f"https://{endpoint}/gwp/v3/rtc/device/getVideoList/{device_token}"
    
    headers = {
        "uuid": uuid,
        "appKey": app_key,
        "timeMillis": time_millis,
        "signature": signature,
        "Content-Type": "application/json"
    }
    
    body = {
        "startTime": start_time,
        "stopTime": stop_time,
        "sn": sn,
        "channel": channel,
        "pageStart": page_start,
        "pageSize": page_size
    }
    
    if events:
        body["events"] = events if isinstance(events, list) else [events]
    
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
        'endpoint': os.environ.get('JF_ENDPOINT', 'api.jftechws.com')
    }


def format_video_list(result):
    """格式化视频列表输出"""
    if result.get('error'):
        return f"❌ 错误：{result['error']}"
    
    if result.get('code') != 2000:
        return f"❌ API 错误码：{result.get('code')}\n   详情：{result.get('msg', 'Unknown error')}"
    
    data = result.get('data', {})
    videos = data.get('VideoArray', [])
    
    if not videos:
        return "📭 未找到匹配的视频"
    
    output = []
    output.append(f"✅ 找到 {len(videos)} 个视频片段")
    output.append(f"   总记录数：{data.get('total', 'N/A')}")
    output.append(f"   页码：{data.get('pageNum', 'N/A')}")
    output.append(f"   是否页尾：{data.get('isFinished', 'N/A')}")
    output.append("")
    
    for i, video in enumerate(videos, 1):
        output.append(f"📹 视频 {i}:")
        output.append(f"   时间：{video.get('StartTime', 'N/A')} - {video.get('StopTime', 'N/A')}")
        output.append(f"   文件名：{video.get('IndexFile', 'N/A')}")
        output.append(f"   大小：{video.get('VideoSize', 0) / 1024:.1f} KB")
        output.append(f"   缩略图：{'有' if video.get('PicFlag') == 1 else '无'}")
        if video.get('events'):
            output.append(f"   报警类型：{', '.join(video.get('events', []))}")
        if video.get('videoId'):
            output.append(f"   视频 ID: {video.get('videoId')}")
        output.append("")
    
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description='获取云存视频列表',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
环境变量:
  JF_UUID       开放平台用户唯一标识 (必需)
  JF_APPKEY     开放平台应用 Key (必需)
  JF_APPSECRET  开放平台应用密钥 (必需)
  JF_MOVECARD   签名算法偏移量，通常设为 5 (必需)
  JF_SN         设备序列号 (必需)
  JF_ENDPOINT   API 端点，默认 api.jftechws.com (可选)

报警类型示例:
  HumanDetect           - 人形检测
  MotionDetect          - 移动侦测
  appEventHumanDetectAlarm - 人形报警

示例:
  # 按时间范围查询
  python cloud_video_list.py --start-time "2026-04-07 10:00:00" --stop-time "2026-04-07 18:00:00"
  
  # 带报警类型过滤
  python cloud_video_list.py --start-time "2026-04-07 10:00:00" --stop-time "2026-04-07 18:00:00" --events "HumanDetect"
  
  # 分页查询
  python cloud_video_list.py --start-time "2026-04-07 10:00:00" --stop-time "2026-04-07 18:00:00" --page-start 1 --page-size 50
        '''
    )
    
    parser.add_argument('--start-time', required=True, help='录像查询开始时间（YYYY-mm-dd HH:MM:SS）')
    parser.add_argument('--stop-time', required=True, help='录像查询结束时间（YYYY-mm-dd HH:MM:SS）')
    parser.add_argument('--channel', type=int, default=0, help='设备通道号（默认 0）')
    parser.add_argument('--page-start', type=int, default=1, help='起始页（从 1 开始，默认 1）')
    parser.add_argument('--page-size', type=int, default=200, help='分页大小（1-200，默认 200）')
    parser.add_argument('--events', nargs='+', help='报警类型列表（可选，用于过滤）')
    parser.add_argument('--json', action='store_true', help='输出 JSON 格式')
    
    args = parser.parse_args()
    
    try:
        config = get_config_from_env()
    except Exception as e:
        print(f'❌ 配置错误：{e}')
        sys.exit(1)
    
    print("=" * 70)
    print("📋 获取云存视频列表")
    print("=" * 70)
    print()
    print(f"设备 SN: {config['sn']}")
    print(f"时间范围：{args.start_time} - {args.stop_time}")
    if args.events:
        print(f"报警类型：{', '.join(args.events)}")
    print()
    
    print(">>> 获取设备 Token...")
    token_result = get_device_token(
        config['sn'], config['uuid'], config['appkey'], 
        config['appsecret'], config['movecard'], config['endpoint']
    )
    
    if token_result.get('error') or token_result.get('code') != 2000:
        print(f"❌ 获取设备 Token 失败：{token_result.get('error') or token_result.get('msg')}")
        sys.exit(1)
    
    device_token = token_result['data'][0]['token']
    print(f"✅ 设备 Token 获取成功")
    print()
    
    print(">>> 获取云存视频列表...")
    result = get_cloud_video_list(
        device_token=device_token,
        sn=config['sn'],
        start_time=args.start_time,
        stop_time=args.stop_time,
        uuid=config['uuid'],
        app_key=config['appkey'],
        app_secret=config['appsecret'],
        movecard=config['movecard'],
        channel=args.channel,
        page_start=args.page_start,
        page_size=args.page_size,
        events=args.events,
        endpoint=config['endpoint']
    )
    
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(format_video_list(result))
    
    sys.exit(0 if result.get('code') == 2000 else 1)


if __name__ == '__main__':
    main()
