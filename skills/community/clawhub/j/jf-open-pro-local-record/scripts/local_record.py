#!/usr/bin/env python3
"""
杰峰设备本地录像技能（开发版）

支持功能：
- 录像日历查询
- 录像回放列表
- 录像回放地址
- 录像下载
- 本地报警图片
- 主辅码流切换
"""

import os
import sys
import argparse
import requests
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List

# 导入加密工具（复用）
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from crypto import get_time_millis, generate_signature
except ImportError:
    print("❌ 错误：找不到 crypto.py 模块")
    print("   请确保 scripts/crypto.py 存在")
    sys.exit(1)

# API 基础地址（可通过环境变量切换）
JF_ENDPOINT = os.getenv("JF_ENDPOINT", "api-cn.jftechws.com")
JF_BASE_URL = f"https://{JF_ENDPOINT}/gwp/v3"


def get_headers(uuid: str, app_key: str, app_secret: str, move_card: int) -> Dict[str, str]:
    """生成请求头（包含签名和时间戳）"""
    time_millis = get_time_millis()
    signature = generate_signature(uuid, app_key, app_secret, time_millis, move_card)
    
    return {
        "Content-Type": "application/json; charset=UTF-8",
        "uuid": uuid,
        "appKey": app_key,
        "timeMillis": time_millis,
        "signature": signature,
        "X-Request-Id": os.urandom(16).hex()
    }


def get_playback_calendar(device_token: str, uuid: str, app_key: str,
                          app_secret: str, move_card: int,
                          year: int, month: int, channel: int = 0,
                          event: str = "*", file_type: str = "h264") -> Dict[str, Any]:
    """
    获取录像回放日历
    
    API: POST /gwp/v3/rtc/device/cardPlaybackCalendar/{deviceToken}
    """
    url = f"{JF_BASE_URL}/rtc/device/cardPlaybackCalendar/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)
    
    body = {
        "Name": "OPSCalendar",
        "OPSCalendar": {
            "Event": event,
            "FileType": file_type,
            "Year": year,
            "Month": month,
            "Channel": channel
        }
    }
    
    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()
    
    if result.get("code") != 2000:
        raise RuntimeError(f"获取日历失败：{result.get('msg', '未知错误')}")
    
    return result.get("data", {})


def get_record_list(device_token: str, uuid: str, app_key: str,
                    app_secret: str, move_card: int,
                    start_time: str, end_time: str,
                    channel: int = 0, event: str = "*",
                    stream_type: str = "0x00000000",
                    file_type: str = "h264") -> Dict[str, Any]:
    """
    获取录像回放列表
    
    API: POST /gwp/v3/rtc/device/opdev/{deviceToken}
    """
    url = f"{JF_BASE_URL}/rtc/device/opdev/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)
    
    body = {
        "Name": "OPFileQuery",
        "OPFileQuery": {
            "BeginTime": start_time,
            "EndTime": end_time,
            "Channel": channel,
            "DriverTypeMask": "0x0000FFFF",
            "Event": event,
            "StreamType": stream_type,
            "Type": file_type
        }
    }
    
    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()
    
    if result.get("code") != 2000:
        raise RuntimeError(f"获取录像列表失败：{result.get('msg', '未知错误')}")
    
    return result.get("data", {})


def get_playback_url(device_token: str, uuid: str, app_key: str,
                     app_secret: str, move_card: int,
                     channel: int, stream_type: int, protocol: str,
                     start_time: str, end_time: str,
                     file_name: str, username: str, password: str,
                     download: int = 0, play_prioritize: int = 0) -> Dict[str, Any]:
    """
    获取录像回放/下载地址
    
    API: POST /gwp/v3/rtc/device/playbackUrl/{deviceToken}
    """
    url = f"{JF_BASE_URL}/rtc/device/playbackUrl/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)
    
    body = {
        "channel": channel,
        "streamType": stream_type,
        "protocol": protocol,
        "startTime": start_time,
        "endTime": end_time,
        "fileName": file_name,
        "username": username,
        "password": password,
        "download": download,
        "playPrioritize": play_prioritize
    }
    
    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()
    
    if result.get("code") != 2000:
        raise RuntimeError(f"获取回放地址失败：{result.get('msg', '未知错误')}")
    
    data = result.get("data", {})
    if data.get("Ret") not in [100, "100", 200, "200"]:
        raise RuntimeError(f"设备返回错误：{data.get('retMsg', '未知错误')}")
    
    return data


def get_local_alarm_pic(device_token: str, uuid: str, app_key: str,
                        app_secret: str, move_card: int,
                        start_time: str, end_time: str,
                        file_name: str) -> Dict[str, Any]:
    """
    获取本地报警图片
    
    API: POST /gwp/v3/rtc/device/getDeviceLocalPic/{deviceToken}
    """
    url = f"{JF_BASE_URL}/rtc/device/getDeviceLocalPic/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)
    
    body = {
        "startTime": start_time,
        "endTime": end_time,
        "fileName": file_name
    }
    
    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()
    
    if result.get("code") != 2000:
        raise RuntimeError(f"获取报警图片失败：{result.get('msg', '未知错误')}")
    
    data = result.get("data", {})
    if data.get("Ret") not in [100, "100", 200, "200"]:
        raise RuntimeError(f"设备返回错误：{data.get('retMsg', '未知错误')}")
    
    return data


def switch_stream(device_token: str, uuid: str, app_key: str,
                  app_secret: str, move_card: int,
                  stream: int) -> Dict[str, Any]:
    """
    切换主辅码流
    
    API: POST /gwp/v3/rtc/device/cardVideoSwitchStream/{deviceToken}
    """
    url = f"{JF_BASE_URL}/rtc/device/cardVideoSwitchStream/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)
    
    body = {
        "stream": stream
    }
    
    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()
    
    if result.get("code") != 2000:
        raise RuntimeError(f"切换码流失败：{result.get('msg', '未知错误')}")
    
    if result.get("data", {}).get("Ret") != 100:
        raise RuntimeError(f"设备返回错误：{result.get('data', {}).get('RetMsg', '未知错误')}")
    
    return result.get("data", {})


# ============== 动作处理函数 ==============

def get_calendar_action(args: argparse.Namespace) -> int:
    """执行获取录像日历操作"""
    try:
        print(f"正在获取设备 {args.device_sn} 的录像日历（{args.year}年{args.month}月）...")
        
        result = get_playback_calendar(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            year=args.year,
            month=args.month,
            channel=args.channel,
            event=args.event,
            file_type=args.file_type
        )
        
        calendar_list = result.get("CalendarList", [])
        
        print()
        print(f"✅ 获取成功")
        print(f"   月份：{args.year}年{args.month}月")
        print(f"   录像天数：{sum(1 for c in calendar_list if c.get('is_exist') == 1)}")
        print()
        
        if calendar_list:
            print("📅 录像日历:")
            print("-" * 40)
            for item in calendar_list:
                date = item.get("date", "")
                is_exist = item.get("is_exist", 0)
                status = "📹" if is_exist == 1 else "  "
                print(f"   {date} {status}")
        else:
            print("⚠️  该月份无录像记录")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def get_record_list_action(args: argparse.Namespace) -> int:
    """执行获取录像列表操作"""
    try:
        print(f"正在获取设备 {args.device_sn} 的录像列表...")
        print(f"   时间范围：{args.start} 至 {args.end}")
        
        result = get_record_list(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            start_time=args.start,
            end_time=args.end,
            channel=args.channel,
            event=args.event,
            stream_type=args.stream_type,
            file_type=args.file_type
        )
        
        record_list = result.get("OPFileQuery", [])
        
        print()
        print(f"✅ 获取成功")
        print(f"   录像数量：{len(record_list)}")
        
        if record_list:
            print()
            print("📋 录像列表:")
            print("-" * 70)
            for i, rec in enumerate(record_list[:10], 1):  # 只显示前 10 条
                begin = rec.get("BeginTime", "")
                end = rec.get("EndTime", "")
                file_name = rec.get("FileName", "")
                file_length = rec.get("FileLength", "0")
                
                # 解析文件名中的类型
                file_type = "未知"
                if "[R]" in file_name:
                    file_type = "常规"
                elif "[M]" in file_name:
                    file_type = "动检"
                elif "[A]" in file_name:
                    file_type = "报警"
                elif "[H]" in file_name:
                    file_type = "手动"
                
                size_mb = int(file_length, 16) / 1024 if isinstance(file_length, str) else file_length / 1024
                
                print(f"{i}. {begin} - {end}")
                print(f"   类型：{file_type}  大小：{size_mb:.1f} MB")
                print(f"   文件：{file_name[:60]}...")
                print()
            
            if len(record_list) > 10:
                print(f"   ... 还有 {len(record_list) - 10} 条录像")
        else:
            print()
            print("⚠️  该时间段无录像记录")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def get_playback_url_action(args: argparse.Namespace) -> int:
    """执行获取回放地址操作"""
    try:
        print(f"正在获取录像回放地址...")
        print(f"   文件：{args.file_name[:50]}...")
        print(f"   协议：{args.protocol}")
        print(f"   时间：{args.start} 至 {args.end}")
        
        result = get_playback_url(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            channel=args.channel,
            stream_type=args.stream_type,
            protocol=args.protocol,
            start_time=args.start,
            end_time=args.end,
            file_name=args.file_name,
            username=args.username,
            password=args.password,
            download=0,
            play_prioritize=args.priority
        )
        
        url = result.get("url", "")
        
        print()
        print("✅ 获取成功")
        print()
        print("📺 回放地址:")
        print(f"   {url}")
        print()
        print("⚠️  注意:")
        print("   - URL 有效期 10 小时")
        print("   - 同时只支持一路回放")
        print("   - 本地录像回放按流量计费")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def download_record_action(args: argparse.Namespace) -> int:
    """执行获取下载地址操作"""
    try:
        print(f"正在获取录像下载地址...")
        print(f"   文件：{args.file_name[:50]}...")
        print(f"   时间：{args.start} 至 {args.end}")
        
        result = get_playback_url(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            channel=args.channel,
            stream_type=args.stream_type,
            protocol="mp4",
            start_time=args.start,
            end_time=args.end,
            file_name=args.file_name,
            username=args.username,
            password=args.password,
            download=1,
            play_prioritize=9
        )
        
        url = result.get("url", "")
        
        print()
        print("✅ 获取成功")
        print()
        print("⬇️ 下载地址:")
        print(f"   {url}")
        print()
        print("⚠️  注意:")
        print("   - URL 有效期 10 小时")
        print("   - 同时只支持一路下载")
        print("   - 本地录像下载按流量计费")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def get_alarm_pic_action(args: argparse.Namespace) -> int:
    """执行获取报警图片操作"""
    try:
        print(f"正在获取本地报警图片...")
        print(f"   文件：{args.file_name[:50]}...")
        
        result = get_local_alarm_pic(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            start_time=args.start,
            end_time=args.end,
            file_name=args.file_name
        )
        
        image_url = result.get("image", "")
        
        print()
        print("✅ 获取成功")
        print()
        print("🖼️  图片地址:")
        print(f"   {image_url}")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def switch_stream_action(args: argparse.Namespace) -> int:
    """执行切换码流操作"""
    try:
        stream_name = "高清（主码流）" if args.stream == 0 else "标清（辅码流）"
        print(f"正在切换设备 {args.device_sn} 的录像码流为 {stream_name}...")
        
        result = switch_stream(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            stream=args.stream
        )
        
        print()
        print("✅ 切换成功")
        print(f"   当前码流：{stream_name}")
        print(f"   会话 ID: {result.get('SessionID')}")
        print()
        print("⚠️  注意：切换后新录制的视频将使用新码流")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="杰峰设备本地录像技能")
    
    # 全局参数
    parser.add_argument("--action", required=True,
                        choices=[
                            "get-calendar", "get-record-list", "get-playback-url",
                            "download-record", "get-alarm-pic", "switch-stream"
                        ],
                        help="操作类型")
    parser.add_argument("--uuid", default=os.getenv("JF_UUID"),
                        help="开放平台用户 uuid")
    parser.add_argument("--app-key", default=os.getenv("JF_APP_KEY"),
                        help="应用 appKey")
    parser.add_argument("--app-secret", default=os.getenv("JF_APP_SECRET"),
                        help="应用密钥")
    parser.add_argument("--move-card", type=int, default=os.getenv("JF_MOVE_CARD", "2"),
                        help="移动卡标识")
    parser.add_argument("--device-sn", default=os.getenv("JF_DEVICE_SN"),
                        help="设备序列号")
    parser.add_argument("--device-token", default=os.getenv("JF_DEVICE_TOKEN"),
                        help="设备接口访问令牌")
    parser.add_argument("--channel", type=int, default=0,
                        help="通道号（默认 0）")
    parser.add_argument("--username", default=os.getenv("JF_DEVICE_USERNAME", "admin"),
                        help="设备用户名")
    parser.add_argument("--password", default=os.getenv("JF_DEVICE_PASSWORD"),
                        help="设备密码")
    
    # get-calendar 参数
    parser.add_argument("--year", type=int, default=datetime.now().year,
                        help="年份")
    parser.add_argument("--month", type=int, default=datetime.now().month,
                        help="月份")
    parser.add_argument("--event", default="*",
                        help="录像类型（*=全部，A=外部报警，M=动检，H=手动等）")
    parser.add_argument("--file-type", default="h264",
                        help="文件类型（h264=视频，jpg=图片）")
    
    # get-record-list 参数
    parser.add_argument("--start", default=(datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
                        help="开始时间（yyyy-MM-dd HH:mm:ss）")
    parser.add_argument("--end", default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        help="结束时间（yyyy-MM-dd HH:mm:ss）")
    parser.add_argument("--stream-type", default="0x00000000",
                        help="码流类型（0x00000000=主码流，0x00000001=辅码流）")
    
    # get-playback-url / download-record 参数
    parser.add_argument("--file-name",
                        help="录像文件名（从回放列表获取）")
    parser.add_argument("--protocol", default="flv",
                        help="播放协议（flv/hls-ts/hls-fmp4/mp4/rtsp-sdp）")
    parser.add_argument("--stream-type", dest="playback_stream", type=int, default=1,
                        help="码流类型（0=高清，1=标清）")
    parser.add_argument("--priority", type=int, default=0,
                        help="回放优先级（0-2=普通，8=优先，9=持续）")
    
    # switch-stream 参数
    parser.add_argument("--stream", type=int, default=1, choices=[0, 1],
                        help="码流类型（0=高清主码流，1=标清辅码流）")
    
    args = parser.parse_args()
    
    # 验证必需参数
    if not args.uuid:
        print("❌ 错误：缺少 --uuid 或 JF_UUID 环境变量", file=sys.stderr)
        return 1
    if not args.app_key:
        print("❌ 错误：缺少 --app-key 或 JF_APP_KEY 环境变量", file=sys.stderr)
        return 1
    if not args.app_secret:
        print("❌ 错误：缺少 --app-secret 或 JF_APP_SECRET 环境变量", file=sys.stderr)
        return 1
    if not args.device_token:
        print("❌ 错误：缺少 --device-token 或 JF_DEVICE_TOKEN 环境变量", file=sys.stderr)
        return 1
    if not args.password:
        print("❌ 错误：缺少 --password 或 JF_DEVICE_PASSWORD 环境变量", file=sys.stderr)
        return 1
    
    # 特定操作验证
    if args.action in ["get-playback-url", "download-record", "get-alarm-pic"]:
        if not args.file_name:
            print(f"❌ 错误：{args.action} 需要 --file-name 参数", file=sys.stderr)
            return 1
    
    # 执行对应操作
    if args.action == "get-calendar":
        return get_calendar_action(args)
    elif args.action == "get-record-list":
        return get_record_list_action(args)
    elif args.action == "get-playback-url":
        return get_playback_url_action(args)
    elif args.action == "download-record":
        return download_record_action(args)
    elif args.action == "get-alarm-pic":
        return get_alarm_pic_action(args)
    elif args.action == "switch-stream":
        return switch_stream_action(args)
    else:
        print(f"❌ 未知操作：{args.action}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
