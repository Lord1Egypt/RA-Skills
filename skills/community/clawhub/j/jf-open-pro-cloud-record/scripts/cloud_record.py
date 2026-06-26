#!/usr/bin/env python3
"""
杰峰设备云存储技能（开发版）

支持功能：
- 云存视频列表查询
- 云存视频回放/下载地址获取
- 云存报警消息列表查询
"""

import os
import sys
import argparse
import requests
import json
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


def get_video_list(device_token: str, uuid: str, app_key: str,
                   app_secret: str, move_card: int,
                   sn: str, start_time: str, stop_time: str,
                   channel: int = 0, page_start: int = 1,
                   page_size: int = 200, events: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    获取云存视频列表
    
    API: POST /gwp/v3/rtc/device/getVideoList/{deviceToken}
    """
    url = f"{JF_BASE_URL}/rtc/device/getVideoList/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)
    
    body = {
        "startTime": start_time,
        "stopTime": stop_time,
        "sn": sn,
        "channel": channel,
        "pageStart": page_start,
        "pageSize": page_size
    }
    
    if events:
        body["events"] = events
    
    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()
    
    if result.get("code") != 2000:
        raise RuntimeError(f"获取云存视频列表失败：{result.get('msg', '未知错误')}")
    
    return result.get("data", {})


def get_video_url(device_token: str, uuid: str, app_key: str,
                  app_secret: str, move_card: int,
                  channel: int = 0, file_format: str = "m3u8",
                  video_id: Optional[str] = None,
                  start_time: Optional[str] = None,
                  stop_time: Optional[str] = None,
                  multi_video: bool = False) -> Dict[str, Any]:
    """
    获取云存视频回放/下载地址
    
    API: POST /gwp/v3/rtc/device/getVideoUrl/{deviceToken}
    """
    url = f"{JF_BASE_URL}/rtc/device/getVideoUrl/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)
    
    body = {
        "channel": channel,
        "fileFormat": file_format
    }
    
    if video_id:
        body["videoId"] = video_id
    
    if start_time and stop_time:
        body["startTime"] = start_time
        body["stopTime"] = stop_time
    
    if multi_video:
        body["multiVideo"] = "1"
    
    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()
    
    if result.get("code") != 2000:
        raise RuntimeError(f"获取视频地址失败：{result.get('msg', '未知错误')}")
    
    return result.get("data", {})


def get_alarm_list(device_token: str, uuid: str, app_key: str,
                   app_secret: str, move_card: int,
                   start_time: str, end_time: str,
                   page_num: int = 1, page_size: int = 10,
                   alarm_event: Optional[str] = None) -> Dict[str, Any]:
    """
    获取云存报警消息列表
    
    API: POST /gwp/v3/rtc/device/getDeviceAlarmList/{deviceToken}
    """
    url = f"{JF_BASE_URL}/rtc/device/getDeviceAlarmList/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)
    
    body = {
        "startTime": start_time,
        "endTime": end_time,
        "pageNum": page_num,
        "pageSize": page_size
    }
    
    if alarm_event:
        body["alarmEvent"] = alarm_event
    
    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()
    
    if result.get("code") != 2000:
        raise RuntimeError(f"获取报警消息列表失败：{result.get('msg', '未知错误')}")
    
    return result.get("data", {})


# ============== 动作处理函数 ==============

def get_video_list_action(args: argparse.Namespace) -> int:
    """执行获取云存视频列表操作"""
    try:
        print(f"正在查询云存视频列表...")
        print(f"   时间范围：{args.start} 至 {args.stop}")
        print(f"   设备：{args.sn}")
        if args.event:
            print(f"   报警类型：{args.event}")
        print()
        
        events = [args.event] if args.event else None
        
        result = get_video_list(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            sn=args.sn,
            start_time=args.start,
            stop_time=args.stop,
            channel=args.channel,
            page_start=args.page_start,
            page_size=args.page_size,
            events=events
        )
        
        video_array = result.get("VideoArray", [])
        total = result.get("total", len(video_array))
        is_finished = result.get("isFinished", True)
        
        print(f"✅ 查询成功")
        print(f"   视频数量：{len(video_array)}")
        print(f"   总记录数：{total}")
        print(f"   是否完成：{'是' if is_finished else '否'}")
        print()
        
        if video_array:
            print("📋 视频列表:")
            print("=" * 80)
            for i, video in enumerate(video_array[:10], 1):
                start = video.get("StartTime", "")
                stop = video.get("StopTime", "")
                index_file = video.get("IndexFile", "")
                video_size = video.get("VideoSize", 0)
                pic_flag = video.get("PicFlag", 0)
                events = video.get("events", [])
                video_id = video.get("videoId", "")
                
                size_mb = video_size / 1024 / 1024
                pic_text = "🖼️" if pic_flag == 1 else ""
                event_text = ", ".join(events) if events else "常规录像"
                
                print(f"{i}. {start} - {stop}")
                print(f"   文件：{index_file}")
                print(f"   大小：{size_mb:.2f} MB {pic_text}")
                print(f"   类型：{event_text}")
                if video_id:
                    print(f"   视频 ID: {video_id}")
                print()
            
            if len(video_array) > 10:
                print(f"   ... 还有 {len(video_array) - 10} 条视频")
        else:
            print("⚠️  该时间段无云存视频")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def get_video_url_action(args: argparse.Namespace) -> int:
    """执行获取云存视频地址操作"""
    try:
        format_name = "在线播放" if args.format.lower() == "m3u8" else "下载"
        print(f"正在获取云存视频{format_name}地址...")
        
        if args.video_id:
            print(f"   视频 ID: {args.video_id}")
        else:
            print(f"   时间范围：{args.start} 至 {args.stop}")
        
        print(f"   格式：{args.format}")
        print()
        
        result = get_video_url(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            channel=args.channel,
            file_format=args.format,
            video_id=args.video_id,
            start_time=args.start,
            stop_time=args.stop,
            multi_video=args.multi_video
        )
        
        url = result.get("url", "")
        
        print(f"✅ 获取成功")
        print()
        print("📺 视频地址:")
        print(f"   {url}")
        print()
        print("⚠️  注意:")
        print("   - URL 有效期 24 小时")
        if args.format.lower() == "mp4":
            print("   - MP4 下载按文件大小消耗流量计费")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def get_alarm_list_action(args: argparse.Namespace) -> int:
    """执行获取云存报警消息操作"""
    try:
        print(f"正在查询云存报警消息...")
        print(f"   时间范围：{args.start} 至 {args.end}")
        if args.event:
            print(f"   报警类型：{args.event}")
        print()
        
        result = get_alarm_list(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            start_time=args.start,
            end_time=args.end,
            page_num=args.page_num,
            page_size=args.page_size,
            alarm_event=args.event
        )
        
        alarm_total = result.get("AlarmTotal", 0)
        alarm_array = result.get("AlarmArray", [])
        
        print(f"✅ 查询成功")
        print(f"   报警总数：{alarm_total}")
        print(f"   返回数量：{len(alarm_array)}")
        print()
        
        if alarm_array:
            print("📋 报警消息列表:")
            print("=" * 70)
            for i, alarm in enumerate(alarm_array[:10], 1):
                alarm_time = alarm.get("AlarmTime", "")
                alarm_event = alarm.get("AlarmEvent", "")
                alarm_id = alarm.get("AlarmId", "")
                channel = alarm.get("Channel", "")
                pic_info = alarm.get("PicInfo", {})
                video_info = alarm.get("VideoInfo", {})
                
                print(f"{i}. [{alarm_time}] {alarm_event}")
                print(f"   报警 ID: {alarm_id}")
                print(f"   通道：{channel}")
                if pic_info:
                    print(f"   图片：{pic_info.get('ObjName', '')}")
                if video_info:
                    print(f"   视频：{video_info.get('VideoLength', 0)}秒")
                print()
            
            if len(alarm_array) > 10:
                print(f"   ... 还有 {len(alarm_array) - 10} 条报警")
        else:
            print("⚠️  该时间段无报警消息")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="杰峰设备云存储技能")
    
    # 全局参数
    parser.add_argument("--action", required=True,
                        choices=["get-video-list", "get-video-url", "get-alarm-list"],
                        help="操作类型")
    parser.add_argument("--uuid", default=os.getenv("JF_UUID"),
                        help="开放平台用户 uuid")
    parser.add_argument("--app-key", default=os.getenv("JF_APP_KEY"),
                        help="应用 appKey")
    parser.add_argument("--app-secret", default=os.getenv("JF_APP_SECRET"),
                        help="应用密钥")
    parser.add_argument("--move-card", type=int, default=os.getenv("JF_MOVE_CARD", "2"),
                        help="移动卡标识")
    parser.add_argument("--device-token", default=os.getenv("JF_DEVICE_TOKEN"),
                        help="设备接口访问令牌")
    parser.add_argument("--sn", default=os.getenv("JF_DEVICE_SN"),
                        help="设备序列号")
    parser.add_argument("--channel", type=int, default=0,
                        help="通道号（默认 0）")
    
    # get-video-list 参数
    parser.add_argument("--start",
                        help="开始时间（yyyy-MM-dd HH:mm:ss）")
    parser.add_argument("--stop",
                        help="结束时间（yyyy-MM-dd HH:mm:ss）")
    parser.add_argument("--page-start", type=int, default=1,
                        help="起始页（默认 1）")
    parser.add_argument("--page-size", type=int, default=200,
                        help="每页数量（默认 200，最大 200）")
    parser.add_argument("--event",
                        help="报警类型（如 HumanDetect）")
    
    # get-video-url 参数
    parser.add_argument("--video-id",
                        help="视频 ID（精准查询）")
    parser.add_argument("--format", default="m3u8", choices=["m3u8", "MP4"],
                        help="视频格式（m3u8=在线播放，MP4=下载）")
    parser.add_argument("--multi-video", action="store_true",
                        help="多目设备标识")
    
    # get-alarm-list 参数
    parser.add_argument("--end",
                        help="结束时间（yyyy-MM-dd HH:mm:ss）")
    parser.add_argument("--page-num", type=int, default=1,
                        help="页数（默认 1）")
    parser.add_argument("--page-size", type=int, default=10,
                        help="每页数量（默认 10，最大 100）")
    
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
    
    # 特定操作验证
    if args.action == "get-video-list":
        if not args.start or not args.stop:
            print("❌ 错误：get-video-list 需要 --start 和 --stop 参数", file=sys.stderr)
            return 1
        if not args.sn:
            print("❌ 错误：get-video-list 需要 --sn 参数", file=sys.stderr)
            return 1
    
    if args.action == "get-video-url":
        if not args.video_id and not (args.start and args.stop):
            print("❌ 错误：get-video-url 需要 --video-id 或 --start/--stop 参数", file=sys.stderr)
            return 1
    
    if args.action == "get-alarm-list":
        if not args.start or not args.end:
            print("❌ 错误：get-alarm-list 需要 --start 和 --end 参数", file=sys.stderr)
            return 1
    
    # 执行对应操作
    if args.action == "get-video-list":
        return get_video_list_action(args)
    elif args.action == "get-video-url":
        return get_video_url_action(args)
    elif args.action == "get-alarm-list":
        return get_alarm_list_action(args)
    else:
        print(f"❌ 未知操作：{args.action}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
