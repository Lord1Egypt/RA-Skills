#!/usr/bin/env python3
"""
杰峰设备智能报警技能（开发版）

支持功能：
- 设备状态检查
- 设备登录
- 设备能力集查询
- 智能报警开关设置
- 手机上报开关设置
- 报警时间段配置
- 报警消息列表查询
- 报警图片获取
"""

import os
import sys
import argparse
import requests
import json
from typing import Optional, Dict, Any, List
from datetime import datetime

from crypto import get_time_millis, generate_signature

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


def get_device_status(device_sn: str, uuid: str, app_key: str, 
                      app_secret: str, move_card: int) -> Dict[str, Any]:
    """
    获取设备状态
    
    Returns:
        设备状态数据
    """
    url = f"{JF_BASE_URL}/rtc/device/status"
    headers = get_headers(uuid, app_key, app_secret, move_card)
    headers["DeviceSn"] = device_sn
    
    response = requests.get(url, headers=headers, timeout=30)
    result = response.json()
    
    if result.get("code") != 2000:
        raise RuntimeError(f"获取设备状态失败：{result.get('msg', '未知错误')}")
    
    return result.get("data", {})


def get_device_token(sns: List[str], uuid: str, app_key: str,
                     app_secret: str, move_card: int,
                     access_token: str = "") -> Dict[str, str]:
    """
    获取设备接口访问令牌（deviceToken）
    
    参考文档：/xm-workspace/xm-webs/openapi/smart-alarm/获取设备接口访问令牌.md
    
    Args:
        sns: 设备序列号列表
        uuid: 开放平台用户 uuid
        app_key: 应用 appKey
        app_secret: 应用密钥
        move_card: 移动卡标识
        access_token: 杰峰 AMS 用户系统登录返回的 accessToken（可选）
        
    Returns:
        设备序列号到 deviceToken 的映射字典
    """
    url = f"{JF_BASE_URL}/rtc/device/token"
    headers = get_headers(uuid, app_key, app_secret, move_card)
    
    body = {
        "sns": sns,
        "accessToken": access_token
    }
    
    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()
    
    if result.get("code") != 2000:
        raise RuntimeError(f"获取 deviceToken 失败：{result.get('msg', '未知错误')}")
    
    # 返回 sn -> token 映射
    data = result.get("data", [])
    token_map = {}
    for item in data:
        sn = item.get("sn")
        token = item.get("token")
        if sn and token:
            token_map[sn] = token
    
    return token_map


def get_device_ability(device_token: str, uuid: str, app_key: str,
                       app_secret: str, move_card: int) -> Dict[str, Any]:
    """
    获取设备能力集
    
    Returns:
        能力集数据
    """
    url = f"{JF_BASE_URL}/rtc/device/getability/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)
    
    response = requests.post(url, headers=headers, timeout=30)
    result = response.json()
    
    if result.get("code") != 2000:
        raise RuntimeError(f"获取能力集失败：{result.get('msg', '未知错误')}")
    
    return result.get("data", {})


def check_alarm_ability(ability_data: Dict[str, Any]) -> bool:
    """
    检查设备是否支持智能报警
    
    判断条件：
    - AlarmFunction.MotionDetect 为 true，或
    - AlarmFunction.HumanDetection 为 true
    """
    alarm_func = ability_data.get("AlarmFunction", {})
    
    motion_detect = alarm_func.get("MotionDetect", False)
    human_detection = alarm_func.get("HumanDetection", False)
    
    return bool(motion_detect) or bool(human_detection)


def get_motion_detect_config(device_token: str, uuid: str, app_key: str, 
                              app_secret: str, move_card: int, channel: int = 0) -> Dict[str, Any]:
    """获取移动侦测配置"""
    url = f"{JF_BASE_URL}/rtc/device/getconfig/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)
    
    body = {"Name": "Detect.MotionDetect"}
    if channel is not None:
        body["Channel"] = str(channel)
    
    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()
    
    if result.get("code") != 2000:
        raise RuntimeError(f"获取配置失败：{result.get('msg', '未知错误')}")
    
    return result.get("data", {})


def set_motion_detect_config(device_token: str, uuid: str, app_key: str,
                              app_secret: str, move_card: int, 
                              config: Dict[str, Any]) -> Dict[str, Any]:
    """设置移动侦测配置"""
    url = f"{JF_BASE_URL}/rtc/device/setconfig/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)
    
    body = {
        "Name": "Detect.MotionDetect",
        "Detect.MotionDetect": config
    }
    
    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()
    
    if result.get("code") != 2000:
        raise RuntimeError(f"设置配置失败：{result.get('msg', '未知错误')}")
    
    if result.get("data", {}).get("Ret") != 100:
        raise RuntimeError(f"设备返回错误：{result.get('data', {}).get('Ret')}")
    
    return result.get("data", {})


def set_alarm_switch(device_token: str, uuid: str, app_key: str,
                     app_secret: str, move_card: int, enable: bool,
                     channel: int = 0) -> Dict[str, Any]:
    """设置报警开关"""
    config_data = get_motion_detect_config(device_token, uuid, app_key, 
                                            app_secret, move_card, channel)
    
    motion_detect = config_data.get("Detect.MotionDetect", [])
    if not motion_detect:
        motion_detect = [{
            "Enable": enable,
            "Level": 3,
            "Region": ["0xFFFFFFFF"] * 32,
            "EventHandler": get_default_event_handler()
        }]
    else:
        motion_detect[0]["Enable"] = enable
    
    return set_motion_detect_config(device_token, uuid, app_key, 
                                     app_secret, move_card, motion_detect)


def set_message_notify(device_token: str, uuid: str, app_key: str,
                       app_secret: str, move_card: int, enable: bool,
                       channel: int = 0) -> Dict[str, Any]:
    """设置手机上报开关（MessageEnable）"""
    config_data = get_motion_detect_config(device_token, uuid, app_key, 
                                            app_secret, move_card, channel)
    
    motion_detect = config_data.get("Detect.MotionDetect", [])
    if not motion_detect:
        motion_detect = [{
            "Enable": True,
            "Level": 3,
            "Region": ["0xFFFFFFFF"] * 32,
            "EventHandler": get_default_event_handler()
        }]
        motion_detect[0]["EventHandler"]["MessageEnable"] = enable
    else:
        if "EventHandler" not in motion_detect[0]:
            motion_detect[0]["EventHandler"] = get_default_event_handler()
        motion_detect[0]["EventHandler"]["MessageEnable"] = enable
    
    return set_motion_detect_config(device_token, uuid, app_key, 
                                     app_secret, move_card, motion_detect)


def get_default_event_handler() -> Dict[str, Any]:
    """获取默认的事件联动配置"""
    return {
        "AlarmInfo": "",
        "AlarmOutEnable": False,
        "AlarmOutLatch": 10,
        "AlarmOutMask": "0x00000000",
        "BeepEnable": False,
        "Dejitter": 0,
        "EventLatch": 2,
        "FTPEnable": False,
        "LogEnable": False,
        "MailEnable": False,
        "MatrixEnable": False,
        "MatrixMask": "0x00000000",
        "MessageEnable": True,
        "MsgtoNetEnable": False,
        "PtzEnable": True,
        "PtzLink": [["None", 0]] * 64,
        "RecordEnable": True,
        "RecordLatch": 30,
        "RecordMask": "0x00000001",
        "SnapEnable": True,
        "SnapShotMask": "0x00000001",
        "TimeSection": get_all_day_time_section(),
        "TipEnable": False,
        "TourEnable": False,
        "TourMask": "0x00000000",
        "VoiceEnable": False,
        "VoiceType": 520
    }


def get_all_day_time_section() -> List[List[str]]:
    """获取全天 24 小时时间段配置（周日到周六）"""
    day_section = ["1 00:00:00-24:00:00"] + ["0 00:00:00-00:00:00"] * 5
    return [day_section.copy() for _ in range(7)]


def generate_time_section(days: List[int], start_time: str, end_time: str) -> List[List[str]]:
    """生成自定义时间段配置"""
    time_section = []
    
    for day in range(7):
        if day in days:
            day_section = [f"1 {start_time}-{end_time}"] + ["0 00:00:00-00:00:00"] * 5
        else:
            day_section = ["0 00:00:00-00:00:00"] * 6
        time_section.append(day_section)
    
    return time_section


def get_alarm_list(device_token: str, uuid: str, app_key: str,
                   app_secret: str, move_card: int,
                   start_time: str, end_time: str,
                   page_num: int = 1, page_size: int = 10,
                   alarm_event: Optional[str] = None) -> Dict[str, Any]:
    """获取报警消息列表"""
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
        raise RuntimeError(f"获取报警列表失败：{result.get('msg', '未知错误')}")
    
    return result.get("data", {})


def get_alarm_pictures(device_token: str, uuid: str, app_key: str,
                       app_secret: str, move_card: int,
                       alarm_ids: Optional[List[str]] = None,
                       channel: int = 0,
                       start_time: Optional[str] = None,
                       end_time: Optional[str] = None,
                       page_start: int = 1, page_size: int = 200,
                       events: Optional[List[str]] = None) -> Dict[str, Any]:
    """获取报警图片"""
    url = f"{JF_BASE_URL}/rtc/device/getPicUrl/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)
    
    body = {
        "channel": channel,
        "pageStart": page_start,
        "pageSize": page_size
    }
    
    if alarm_ids:
        body["alarmIds"] = alarm_ids
    
    if start_time:
        body["startTime"] = start_time
    
    if end_time:
        body["endTime"] = end_time
    
    if events:
        body["events"] = events
    
    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()
    
    if result.get("code") != 2000:
        raise RuntimeError(f"获取报警图片失败：{result.get('msg', '未知错误')}")
    
    return result


# ============== 动作处理函数 ==============

def get_ability_action(args: argparse.Namespace) -> int:
    """执行获取设备能力集操作"""
    try:
        print(f"正在查询设备 {args.device_sn} 的能力集...")
        
        ability = get_device_ability(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card
        )
        
        alarm_func = ability.get("AlarmFunction", {})
        motion_detect = alarm_func.get("MotionDetect", False)
        human_detection = alarm_func.get("HumanDetection", False)
        
        print(f"✅ 获取能力集成功")
        print(f"   移动侦测 (MotionDetect): {motion_detect}")
        print(f"   人体检测 (HumanDetection): {human_detection}")
        
        if motion_detect or human_detection:
            print(f"   ✅ 设备支持智能报警功能")
        else:
            print(f"   ⚠️  设备不支持智能报警功能")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def get_config_action(args: argparse.Namespace) -> int:
    """执行获取配置操作"""
    try:
        print(f"正在获取设备 {args.device_sn} 的移动侦测配置...")
        
        config = get_motion_detect_config(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            channel=args.channel
        )
        
        motion_detect = config.get("Detect.MotionDetect", [])
        if motion_detect:
            md = motion_detect[0]
            event_handler = md.get("EventHandler", {})
            
            print(f"✅ 获取配置成功")
            print(f"   报警开关：{'开启' if md.get('Enable') else '关闭'}")
            print(f"   灵敏度：{md.get('Level', 3)}")
            print(f"   手机上报：{'开启' if event_handler.get('MessageEnable') else '关闭'}")
            print(f"   会话 ID: {config.get('SessionID')}")
            
            # 显示时间段摘要
            time_section = event_handler.get("TimeSection", [])
            if time_section:
                print(f"   时间段配置：已设置 ({len(time_section)} 天)")
        else:
            print("⚠️  未找到移动侦测配置")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def set_switch_action(args: argparse.Namespace) -> int:
    """执行设置开关操作"""
    try:
        enable = args.enable.lower() == 'true'
        print(f"正在{'开启' if enable else '关闭'}设备 {args.device_sn} 的报警...")
        
        result = set_alarm_switch(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            enable=enable,
            channel=args.channel
        )
        
        print(f"✅ 设置成功")
        print(f"   报警开关：{'开启' if enable else '关闭'}")
        print(f"   会话 ID: {result.get('SessionID')}")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def set_message_notify_action(args: argparse.Namespace) -> int:
    """执行设置手机上报开关操作"""
    try:
        enable = args.enable.lower() == 'true'
        print(f"正在{'开启' if enable else '关闭'}设备 {args.device_sn} 的手机上报...")
        
        result = set_message_notify(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            enable=enable,
            channel=args.channel
        )
        
        print(f"✅ 设置成功")
        print(f"   手机上报：{'开启' if enable else '关闭'}")
        print(f"   会话 ID: {result.get('SessionID')}")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def set_time_section_action(args: argparse.Namespace) -> int:
    """执行设置时间段操作"""
    try:
        config = get_motion_detect_config(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            channel=args.channel
        )
        
        motion_detect = config.get("Detect.MotionDetect", [])
        if not motion_detect:
            motion_detect = [{
                "Enable": True,
                "Level": 3,
                "Region": ["0xFFFFFFFF"] * 32,
                "EventHandler": get_default_event_handler()
            }]
        
        if "EventHandler" not in motion_detect[0]:
            motion_detect[0]["EventHandler"] = get_default_event_handler()
        
        if args.schedule == 'all-day':
            time_section = get_all_day_time_section()
            print("设置全天 24 小时报警...")
        else:
            days = [int(d) for d in args.days.split(',')]
            time_section = generate_time_section(days, args.start, args.end)
            day_names = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
            day_str = ','.join([day_names[d] for d in days])
            print(f"设置自定义时间段：{day_str} {args.start}-{args.end}")
        
        motion_detect[0]["EventHandler"]["TimeSection"] = time_section
        
        result = set_motion_detect_config(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            config=motion_detect
        )
        
        print(f"✅ 设置成功")
        print(f"   会话 ID: {result.get('SessionID')}")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def get_alarm_list_action(args: argparse.Namespace) -> int:
    """执行获取报警列表操作"""
    try:
        print(f"正在查询报警消息 ({args.start} ~ {args.end})...")
        
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
        
        for alarm in alarm_array:
            print(f"\n   - 报警 ID: {alarm.get('AlarmId')}")
            print(f"     事件：{alarm.get('AlarmEvent')}")
            print(f"     时间：{alarm.get('AlarmTime')}")
            print(f"     通道：{alarm.get('Channel')}")
            if alarm.get('PicInfo'):
                print(f"     图片：{alarm['PicInfo'].get('ObjName')}")
            if alarm.get('VideoInfo'):
                print(f"     视频：{alarm['VideoInfo'].get('VideoLength')}秒")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def get_alarm_pic_action(args: argparse.Namespace) -> int:
    """执行获取报警图片操作"""
    try:
        if args.alarm_ids:
            alarm_ids = args.alarm_ids.split(',')
            print(f"正在获取指定报警的图片 ({len(alarm_ids)} 个)...")
        elif args.start and args.end:
            print(f"正在获取时间段的报警图片 ({args.start} ~ {args.end})...")
        else:
            print("正在获取报警图片...")
        
        result = get_alarm_pictures(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            alarm_ids=args.alarm_ids.split(',') if args.alarm_ids else None,
            channel=args.channel,
            start_time=args.start,
            end_time=args.end,
            page_start=args.page_start,
            page_size=args.page_size,
            events=args.events.split(',') if args.events else None
        )
        
        data = result.get("data", [])
        is_finished = result.get("isFinished", True)
        total = result.get("total", len(data))
        
        print(f"✅ 获取成功")
        print(f"   图片数量：{len(data)}")
        print(f"   总记录数：{total}")
        print(f"   是否完成：{'是' if is_finished else '否'}")
        
        for pic in data:
            print(f"\n   - 报警 ID: {pic.get('id')}")
            print(f"     图片 URL: {pic.get('url')}")
            if pic.get('AlarmEvent'):
                print(f"     事件：{pic.get('AlarmEvent')}")
            if pic.get('AlarmTime'):
                print(f"     时间：{pic.get('AlarmTime')}")
            if pic.get('Channel'):
                print(f"     通道：{pic.get('Channel')}")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="杰峰设备智能报警技能")
    
    # 全局参数
    parser.add_argument("--action", required=True, 
                        choices=["get-ability", "get-config", "set-switch", 
                                 "set-message-notify", "set-time-section",
                                 "get-alarm-list", "get-alarm-pic"],
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
    parser.add_argument("--device-username", default=os.getenv("JF_DEVICE_USERNAME", "admin"),
                        help="设备用户名")
    parser.add_argument("--device-password", default=os.getenv("JF_DEVICE_PASSWORD"),
                        help="设备密码")
    parser.add_argument("--channel", type=int, default=0,
                        help="通道号（默认 0）")
    
    # set-switch / set-message-notify 参数
    parser.add_argument("--enable", default="true",
                        help="是否开启（true/false）")
    
    # set-time-section 参数
    parser.add_argument("--schedule", choices=["all-day", "custom"], default="all-day",
                        help="时间段类型")
    parser.add_argument("--days", default="0,1,2,3,4,5,6",
                        help="星期列表（0=周日，1=周一，...，6=周六）")
    parser.add_argument("--start", default="00:00:00",
                        help="开始时间（HH:MM:SS）")
    parser.add_argument("--end", default="24:00:00",
                        help="结束时间（HH:MM:SS）")
    
    # get-alarm-list / get-alarm-pic 参数
    parser.add_argument("--start-time", dest="start",
                        help="开始时间（yyyy-MM-dd HH:mm:ss）")
    parser.add_argument("--end-time", dest="end",
                        help="结束时间（yyyy-MM-dd HH:mm:ss）")
    parser.add_argument("--page-num", type=int, default=1,
                        help="页数")
    parser.add_argument("--page-size", type=int, default=10,
                        help="每页数量")
    parser.add_argument("--event",
                        help="报警类型")
    parser.add_argument("--alarm-ids",
                        help="报警 ID 列表（逗号分隔）")
    parser.add_argument("--page-start", type=int, default=1,
                        help="起始页")
    parser.add_argument("--events",
                        help="报警类型列表（逗号分隔）")
    
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
    
    # 执行对应操作
    if args.action == "get-ability":
        return get_ability_action(args)
    elif args.action == "get-config":
        return get_config_action(args)
    elif args.action == "set-switch":
        return set_switch_action(args)
    elif args.action == "set-message-notify":
        return set_message_notify_action(args)
    elif args.action == "set-time-section":
        return set_time_section_action(args)
    elif args.action == "get-alarm-list":
        if not args.start or not args.end:
            print("❌ 错误：get-alarm-list 需要 --start-time 和 --end-time 参数", file=sys.stderr)
            return 1
        return get_alarm_list_action(args)
    elif args.action == "get-alarm-pic":
        return get_alarm_pic_action(args)
    else:
        print(f"❌ 未知操作：{args.action}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
