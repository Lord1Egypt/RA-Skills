#!/usr/bin/env python3
"""
杰峰云台设备控制技能（开发版）

支持功能：
- 云台方向控制（上/下/左/右/左上/左下/右上/右下）
- 变倍和聚焦控制
- 预置位管理（设置/删除/转到/编辑）
- 巡航计划（添加/删除/开始/停止/清除）
- 特殊预置位（移动追踪守望位 100、自检回归预置位 128）
"""

import os
import sys
import time
import argparse
import requests
from typing import Optional, Dict, Any

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


def ptz_direction(device_token: str, uuid: str, app_key: str,
                  app_secret: str, move_card: int,
                  direction: str, command: str,
                  channel: int = 0, step: int = 5) -> Dict[str, Any]:
    """
    云台方向控制
    
    API: POST /gwp/v3/rtc/device/opdev/{deviceToken}
    Name: OPPTZControl
    """
    url = f"{JF_BASE_URL}/rtc/device/opdev/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)
    
    # 方向映射
    direction_map = {
        "up": "DirectionUp",
        "down": "DirectionDown",
        "left": "DirectionLeft",
        "right": "DirectionRight",
        "leftup": "DirectionLeftUp",
        "leftdown": "DirectionLeftDown",
        "rightup": "DirectionRightUp",
        "rightdown": "DirectionRightDown"
    }
    
    body = {
        "Name": "OPPTZControl",
        "OPPTZControl": {
            "Command": direction_map.get(direction.lower(), direction),
            "Parameter": {
                "Preset": 0 if command == "start" else -1,
                "Channel": channel,
                "Step": step
            }
        }
    }
    
    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()
    
    if result.get("code") != 2000:
        raise RuntimeError(f"云台控制失败：{result.get('msg', '未知错误')}")
    
    if result.get("data", {}).get("Ret") != 100:
        raise RuntimeError(f"设备返回错误：{result.get('data', {}).get('Ret')}")
    
    return result.get("data", {})


def ptz_zoom_focus(device_token: str, uuid: str, app_key: str,
                   app_secret: str, move_card: int,
                   command: str, channel: int = 0,
                   step: int = 5) -> Dict[str, Any]:
    """
    变倍和聚焦控制
    
    API: POST /gwp/v3/rtc/device/opdev/{deviceToken}
    Name: OPPTZControl
    """
    url = f"{JF_BASE_URL}/rtc/device/opdev/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)
    
    # 命令映射
    command_map = {
        "zoom-in": "ZoomTile",
        "zoom-out": "ZoomWide",
        "focus-far": "FocusFar",
        "focus-near": "FocusNear",
        "iris-small": "IrisSmall",
        "iris-large": "IrisLarge"
    }
    
    body = {
        "Name": "OPPTZControl",
        "OPPTZControl": {
            "Command": command_map.get(command.lower(), command),
            "Parameter": {
                "Channel": channel,
                "Step": step
            }
        }
    }
    
    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()
    
    if result.get("code") != 2000:
        raise RuntimeError(f"变倍聚焦控制失败：{result.get('msg', '未知错误')}")
    
    if result.get("data", {}).get("Ret") != 100:
        raise RuntimeError(f"设备返回错误：{result.get('data', {}).get('Ret')}")
    
    return result.get("data", {})


def ptz_preset(device_token: str, uuid: str, app_key: str,
               app_secret: str, move_card: int,
               command: str, preset: int,
               channel: int = 0, preset_name: str = "") -> Dict[str, Any]:
    """
    预置位操作
    
    API: POST /gwp/v3/rtc/device/opdev/{deviceToken}
    Name: OPPTZControl
    """
    url = f"{JF_BASE_URL}/rtc/device/opdev/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)
    
    # 命令映射
    command_map = {
        "set": "SetPreset",
        "clear": "ClearPreset",
        "goto": "GotoPreset",
        "set-name": "SetPresetName"
    }
    
    body = {
        "Name": "OPPTZControl",
        "OPPTZControl": {
            "Command": command_map.get(command.lower(), command),
            "Parameter": {
                "Preset": preset,
                "Channel": channel
            }
        }
    }
    
    if command in ["set", "set-name"] and preset_name:
        body["OPPTZControl"]["Parameter"]["PresetName"] = preset_name
    
    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()
    
    if result.get("code") != 2000:
        raise RuntimeError(f"预置位操作失败：{result.get('msg', '未知错误')}")
    
    if result.get("data", {}).get("Ret") != 100:
        raise RuntimeError(f"设备返回错误：{result.get('data', {}).get('Ret')}")
    
    return result.get("data", {})


def ptz_tour(device_token: str, uuid: str, app_key: str,
             app_secret: str, move_card: int,
             command: str, tour: int = 0,
             preset: int = 0, channel: int = 0,
             step: int = 5) -> Dict[str, Any]:
    """
    巡航计划操作
    
    API: POST /gwp/v3/rtc/device/opdev/{deviceToken}
    Name: OPPTZControl
    """
    url = f"{JF_BASE_URL}/rtc/device/opdev/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)
    
    # 命令映射
    command_map = {
        "add": "AddTour",
        "delete": "DeleteTour",
        "start": "StartTour",
        "stop": "StopTour",
        "clear": "ClearTour"
    }
    
    body = {
        "Name": "OPPTZControl",
        "OPPTZControl": {
            "Command": command_map.get(command.lower(), command),
            "Parameter": {
                "Tour": tour,
                "Channel": channel
            }
        }
    }
    
    if command in ["add", "delete"]:
        body["OPPTZControl"]["Parameter"]["Preset"] = preset
        body["OPPTZControl"]["Parameter"]["Step"] = step
    
    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()
    
    if result.get("code") != 2000:
        raise RuntimeError(f"巡航操作失败：{result.get('msg', '未知错误')}")
    
    if result.get("data", {}).get("Ret") != 100:
        raise RuntimeError(f"设备返回错误：{result.get('data', {}).get('Ret')}")
    
    return result.get("data", {})


def get_preset_list(device_token: str, uuid: str, app_key: str,
                    app_secret: str, move_card: int) -> Dict[str, Any]:
    """
    获取预置位列表
    
    API: POST /gwp/v3/rtc/device/getconfig/{deviceToken}
    Name: Uart.PTZPreset
    """
    url = f"{JF_BASE_URL}/rtc/device/getconfig/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)
    
    body = {"Name": "Uart.PTZPreset"}
    
    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()
    
    if result.get("code") != 2000:
        raise RuntimeError(f"获取预置位列表失败：{result.get('msg', '未知错误')}")
    
    return result.get("data", {})


def get_tour_config(device_token: str, uuid: str, app_key: str,
                    app_secret: str, move_card: int) -> Dict[str, Any]:
    """
    获取巡航配置
    
    API: POST /gwp/v3/rtc/device/getconfig/{deviceToken}
    Name: Uart.PTZTour
    """
    url = f"{JF_BASE_URL}/rtc/device/getconfig/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)
    
    body = {"Name": "Uart.PTZTour"}
    
    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()
    
    if result.get("code") != 2000:
        raise RuntimeError(f"获取巡航配置失败：{result.get('msg', '未知错误')}")
    
    return result.get("data", {})


# ============== 动作处理函数 ==============

def direction_action(args: argparse.Namespace) -> int:
    """执行方向控制操作"""
    try:
        direction_names = {
            "up": "上", "down": "下", "left": "左", "right": "右",
            "leftup": "左上", "leftdown": "左下",
            "rightup": "右上", "rightdown": "右下"
        }
        
        dir_name = direction_names.get(args.direction.lower(), args.direction)
        print(f"正在控制云台向 {dir_name} 转动...")
        
        # 开始转动
        print("  开始转动...")
        ptz_direction(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            direction=args.direction,
            command="start",
            channel=args.channel,
            step=args.step
        )
        
        # 间隔 500ms
        time.sleep(0.5)
        
        # 停止转动
        print("  停止转动...")
        ptz_direction(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            direction=args.direction,
            command="stop",
            channel=args.channel,
            step=args.step
        )
        
        print()
        print("✅ 云台方向控制完成")
        print(f"   方向：{dir_name}")
        print(f"   速度：{args.step}")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def zoom_action(args: argparse.Namespace) -> int:
    """执行变倍操作"""
    try:
        zoom_name = "放大" if args.zoom.lower() == "in" else "缩小"
        print(f"正在{zoom_name}变倍...")
        
        command = "zoom-in" if args.zoom.lower() == "in" else "zoom-out"
        
        ptz_zoom_focus(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            command=command,
            channel=args.channel,
            step=args.step
        )
        
        print()
        print("✅ 变倍控制完成")
        print(f"   操作：{zoom_name}")
        print(f"   速度：{args.step}")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def focus_action(args: argparse.Namespace) -> int:
    """执行聚焦操作"""
    try:
        focus_name = "远处" if args.focus.lower() == "far" else "近处"
        print(f"正在聚焦到{focus_name}...")
        
        command = "focus-far" if args.focus.lower() == "far" else "focus-near"
        
        ptz_zoom_focus(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            command=command,
            channel=args.channel,
            step=args.step
        )
        
        print()
        print("✅ 聚焦控制完成")
        print(f"   聚焦：{focus_name}")
        print(f"   速度：{args.step}")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def set_preset_action(args: argparse.Namespace) -> int:
    """执行设置预置位操作"""
    try:
        preset_name = args.name if args.name else f"预置位{args.preset}"
        print(f"正在设置预置位 {args.preset} ({preset_name})...")
        
        result = ptz_preset(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            command="set",
            preset=args.preset,
            channel=args.channel,
            preset_name=preset_name
        )
        
        print()
        print("✅ 预置位设置成功")
        print(f"   预置位编号：{args.preset}")
        print(f"   预置位名称：{preset_name}")
        print(f"   会话 ID: {result.get('SessionID')}")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def goto_preset_action(args: argparse.Namespace) -> int:
    """执行转到预置位操作"""
    try:
        print(f"正在转到预置位 {args.preset}...")
        
        result = ptz_preset(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            command="goto",
            preset=args.preset,
            channel=args.channel
        )
        
        print()
        print("✅ 已转到预置位")
        print(f"   预置位编号：{args.preset}")
        print(f"   会话 ID: {result.get('SessionID')}")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def clear_preset_action(args: argparse.Namespace) -> int:
    """执行删除预置位操作"""
    try:
        print(f"正在删除预置位 {args.preset}...")
        
        result = ptz_preset(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            command="clear",
            preset=args.preset,
            channel=args.channel
        )
        
        print()
        print("✅ 预置位已删除")
        print(f"   预置位编号：{args.preset}")
        print(f"   会话 ID: {result.get('SessionID')}")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def set_preset_name_action(args: argparse.Namespace) -> int:
    """执行编辑预置位名称操作"""
    try:
        print(f"正在编辑预置位 {args.preset} 的名称...")
        
        result = ptz_preset(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            command="set-name",
            preset=args.preset,
            channel=args.channel,
            preset_name=args.name
        )
        
        print()
        print("✅ 预置位名称已更新")
        print(f"   预置位编号：{args.preset}")
        print(f"   新名称：{args.name}")
        print(f"   会话 ID: {result.get('SessionID')}")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def list_presets_action(args: argparse.Namespace) -> int:
    """执行查询预置位列表操作"""
    try:
        print("正在获取预置位列表...")
        
        result = get_preset_list(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card
        )
        
        preset_list = result.get("Uart.PTZPreset", [])
        
        print()
        print("✅ 获取成功")
        print(f"   预置位数量：{len(preset_list)}")
        
        if preset_list:
            print()
            print("📋 预置位列表:")
            print("-" * 40)
            for preset in preset_list:
                preset_id = preset.get("Id", 0)
                preset_name = preset.get("PresetName", "")
                
                # 特殊预置位标识
                special = ""
                if preset_id == 100:
                    special = " [移动追踪守望位]"
                elif preset_id == 128:
                    special = " [自检回归预置位]"
                
                print(f"   {preset_id}. {preset_name}{special}")
        else:
            print()
            print("⚠️  暂无预置位")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def add_tour_action(args: argparse.Namespace) -> int:
    """执行添加巡航点操作"""
    try:
        print(f"正在添加预置位 {args.preset} 到巡航线路 {args.tour}...")
        
        result = ptz_tour(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            command="add",
            tour=args.tour,
            preset=args.preset,
            channel=args.channel,
            step=args.step
        )
        
        print()
        print("✅ 巡航点已添加")
        print(f"   巡航线路：{args.tour}")
        print(f"   预置位编号：{args.preset}")
        print(f"   转动速度：{args.step}")
        print(f"   会话 ID: {result.get('SessionID')}")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def delete_tour_action(args: argparse.Namespace) -> int:
    """执行删除巡航点操作"""
    try:
        print(f"正在从巡航线路 {args.tour} 删除预置位 {args.preset}...")
        
        result = ptz_tour(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            command="delete",
            tour=args.tour,
            preset=args.preset,
            channel=args.channel
        )
        
        print()
        print("✅ 巡航点已删除")
        print(f"   巡航线路：{args.tour}")
        print(f"   预置位编号：{args.preset}")
        print(f"   会话 ID: {result.get('SessionID')}")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def start_tour_action(args: argparse.Namespace) -> int:
    """执行开始巡航操作"""
    try:
        print(f"正在开始巡航线路 {args.tour}...")
        
        result = ptz_tour(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            command="start",
            tour=args.tour,
            channel=args.channel
        )
        
        print()
        print("✅ 巡航已开始")
        print(f"   巡航线路：{args.tour}")
        print(f"   会话 ID: {result.get('SessionID')}")
        print()
        print("ℹ️  设备将在预设的预置点之间自动循环转动")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def stop_tour_action(args: argparse.Namespace) -> int:
    """执行停止巡航操作"""
    try:
        print(f"正在停止巡航线路 {args.tour}...")
        
        result = ptz_tour(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            command="stop",
            tour=args.tour,
            channel=args.channel
        )
        
        print()
        print("✅ 巡航已停止")
        print(f"   巡航线路：{args.tour}")
        print(f"   会话 ID: {result.get('SessionID')}")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def clear_tour_action(args: argparse.Namespace) -> int:
    """执行清除巡航线路操作"""
    try:
        print(f"正在清除巡航线路 {args.tour}...")
        
        result = ptz_tour(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            command="clear",
            tour=args.tour,
            channel=args.channel
        )
        
        print()
        print("✅ 巡航线路已清除")
        print(f"   巡航线路：{args.tour}")
        print(f"   会话 ID: {result.get('SessionID')}")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def list_tours_action(args: argparse.Namespace) -> int:
    """执行查询巡航配置操作"""
    try:
        print("正在获取巡航配置...")
        
        result = get_tour_config(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card
        )
        
        print()
        print("✅ 获取成功")
        print(f"   会话 ID: {result.get('SessionID')}")
        print()
        print("⚠️  巡航配置响应格式可能因设备而异")
        print("   详细配置请参考设备返回数据")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="杰峰云台设备控制技能")
    
    # 全局参数
    parser.add_argument("--action", required=True,
                        choices=[
                            "direction", "zoom", "focus",
                            "set-preset", "goto-preset", "clear-preset",
                            "set-preset-name", "list-presets",
                            "add-tour", "delete-tour", "start-tour",
                            "stop-tour", "clear-tour", "list-tours"
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
    
    # direction 参数
    parser.add_argument("--direction",
                        help="方向（up/down/left/right/leftup/leftdown/rightup/rightdown）")
    parser.add_argument("--step", type=int, default=5,
                        help="运动速度（1-8，1 最慢）")
    
    # zoom 参数
    parser.add_argument("--zoom", choices=["in", "out"],
                        help="变倍方向（in=放大，out=缩小）")
    
    # focus 参数
    parser.add_argument("--focus", choices=["far", "near"],
                        help="聚焦方向（far=远处，near=近处）")
    
    # preset 参数
    parser.add_argument("--preset", type=int,
                        help="预置位编号（1-255）")
    parser.add_argument("--name",
                        help="预置位名称")
    
    # tour 参数
    parser.add_argument("--tour", type=int, default=0,
                        help="巡航线路编号（默认 0）")
    
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
    if args.action == "direction" and not args.direction:
        print("❌ 错误：direction 需要 --direction 参数", file=sys.stderr)
        return 1
    if args.action == "zoom" and not args.zoom:
        print("❌ 错误：zoom 需要 --zoom 参数", file=sys.stderr)
        return 1
    if args.action == "focus" and not args.focus:
        print("❌ 错误：focus 需要 --focus 参数", file=sys.stderr)
        return 1
    if args.action in ["set-preset", "goto-preset", "clear-preset", "set-preset-name"] and not args.preset:
        print(f"❌ 错误：{args.action} 需要 --preset 参数", file=sys.stderr)
        return 1
    if args.action == "set-preset-name" and not args.name:
        print("❌ 错误：set-preset-name 需要 --name 参数", file=sys.stderr)
        return 1
    if args.action in ["add-tour", "delete-tour"] and not args.preset:
        print(f"❌ 错误：{args.action} 需要 --preset 参数", file=sys.stderr)
        return 1
    
    # 执行对应操作
    if args.action == "direction":
        return direction_action(args)
    elif args.action == "zoom":
        return zoom_action(args)
    elif args.action == "focus":
        return focus_action(args)
    elif args.action == "set-preset":
        return set_preset_action(args)
    elif args.action == "goto-preset":
        return goto_preset_action(args)
    elif args.action == "clear-preset":
        return clear_preset_action(args)
    elif args.action == "set-preset-name":
        return set_preset_name_action(args)
    elif args.action == "list-presets":
        return list_presets_action(args)
    elif args.action == "add-tour":
        return add_tour_action(args)
    elif args.action == "delete-tour":
        return delete_tour_action(args)
    elif args.action == "start-tour":
        return start_tour_action(args)
    elif args.action == "stop-tour":
        return stop_tour_action(args)
    elif args.action == "clear-tour":
        return clear_tour_action(args)
    elif args.action == "list-tours":
        return list_tours_action(args)
    else:
        print(f"❌ 未知操作：{args.action}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
