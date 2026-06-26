#!/usr/bin/env python3
"""
杰峰设备 OSD 水印设置技能（开发版）

支持功能：
- 获取/设置单行 OSD 配置
- 获取/设置多行 OSD 配置
- 通道标题设置
- 时间标题设置
- 隐私区域设置
"""

import os
import sys
import argparse
import requests
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


def get_osd_config(device_token: str, uuid: str, app_key: str,
                   app_secret: str, move_card: int,
                   config_type: str = "single",
                   channel: int = 0) -> Dict[str, Any]:
    """
    获取 OSD 配置
    
    API: POST /gwp/v3/rtc/device/getconfig/{deviceToken}
    """
    url = f"{JF_BASE_URL}/rtc/device/getconfig/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)
    
    name_map = {
        "single": "AVEnc.VideoWidget",
        "multi": "AVEnc.VideoOSD"
    }
    
    body = {
        "Name": name_map.get(config_type, "AVEnc.VideoWidget")
    }
    
    if channel is not None:
        body["Channel"] = str(channel)
    
    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()
    
    if result.get("code") != 2000:
        raise RuntimeError(f"获取 OSD 配置失败：{result.get('msg', '未知错误')}")
    
    return result.get("data", {})


def set_osd_config(device_token: str, uuid: str, app_key: str,
                   app_secret: str, move_card: int,
                   config: Dict[str, Any],
                   config_type: str = "single",
                   channel: int = 0) -> Dict[str, Any]:
    """
    设置 OSD 配置
    
    API: POST /gwp/v3/rtc/device/setconfig/{deviceToken}
    """
    url = f"{JF_BASE_URL}/rtc/device/setconfig/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)
    
    name_map = {
        "single": "AVEnc.VideoWidget",
        "multi": "AVEnc.VideoOSD"
    }
    
    body = {
        "Name": name_map.get(config_type, "AVEnc.VideoWidget")
    }
    
    if config_type == "single":
        body["AVEnc.VideoWidget"] = config
    else:
        body["AVEnc.VideoOSD"] = config
    
    if channel is not None:
        body["Channel"] = str(channel)
    
    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()
    
    if result.get("code") != 2000:
        raise RuntimeError(f"设置 OSD 配置失败：{result.get('msg', '未知错误')}")
    
    return result.get("data", {})


def pixel_to_osd_coord(pixel: int, total_pixels: int = 1920) -> int:
    """像素坐标转换为 OSD 坐标（0-8192 范围）"""
    return int((pixel / total_pixels) * 8192)


def rgba_to_hex(r: int, g: int, b: int, a: int = 255) -> str:
    """RGBA 转换为十六进制颜色字符串"""
    return f"0x{r:02X}{g:02X}{b:02X}{a:02X}"


# ============== 动作处理函数 ==============

def get_single_action(args: argparse.Namespace) -> int:
    """执行获取单行 OSD 配置操作"""
    try:
        print(f"正在获取设备 {args.device_sn} 的单行 OSD 配置...")
        
        result = get_osd_config(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            config_type="single",
            channel=args.channel
        )
        
        print()
        print("✅ 获取成功")
        print()
        print("📋 OSD 配置详情:")
        print("-" * 60)
        
        # 打印配置详情
        print_config_details(result, "single")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def get_multi_action(args: argparse.Namespace) -> int:
    """执行获取多行 OSD 配置操作"""
    try:
        print(f"正在获取设备 {args.device_sn} 的多行 OSD 配置...")
        
        result = get_osd_config(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            config_type="multi",
            channel=args.channel
        )
        
        print()
        print("✅ 获取成功")
        print()
        print("📋 OSD 配置详情:")
        print("-" * 60)
        
        # 打印配置详情
        print_config_details(result, "multi")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def print_config_details(result: Dict[str, Any], config_type: str):
    """打印配置详情"""
    if config_type == "single":
        widget = result.get("AVEnc.VideoWidget", [])
        if widget:
            w = widget[0]
            
            # 通道标题
            channel_title = w.get("ChannelTitle", {})
            print(f"通道标题：{channel_title.get('Name', '-')}")
            
            # 通道标题属性
            title_attr = w.get("ChannelTitleAttribute", {})
            if title_attr:
                encode = "✅" if title_attr.get("EncodeBlend") else "❌"
                preview = "✅" if title_attr.get("PreviewBlend") else "❌"
                pos = title_attr.get("RelativePos", [])
                print(f"  编码叠加：{encode}  预览叠加：{preview}")
                if pos:
                    print(f"  位置：[{pos[0]}, {pos[1]}]")
            
            # 时间标题属性
            time_attr = w.get("TimeTitleAttribute", {})
            if time_attr:
                encode = "✅" if time_attr.get("EncodeBlend") else "❌"
                preview = "✅" if time_attr.get("PreviewBlend") else "❌"
                pos = time_attr.get("RelativePos", [])
                print(f"时间标题：编码叠加：{encode}  预览叠加：{preview}")
                if pos:
                    print(f"  位置：[{pos[0]}, {pos[1]}]")
            
            # 隐私区域
            covers = w.get("Covers", [])
            covers_num = w.get("CoversNum", 0)
            print(f"隐私区域：{covers_num} 个")
            for i, cover in enumerate(covers[:3], 1):
                pos = cover.get("RelativePos", [])
                if pos:
                    print(f"  区域{i}: [{pos[0]}, {pos[1]}]")
    else:
        # 多行配置
        print("多行 OSD 配置（详细配置请参考返回数据）")
        print(result)


def set_channel_title_action(args: argparse.Namespace) -> int:
    """执行设置通道标题操作"""
    try:
        enable = args.enable and not args.disable
        
        print(f"正在{'启用' if enable else '禁用'}通道标题...")
        print(f"   标题：{args.title}")
        
        # 先获取当前配置
        result = get_osd_config(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            config_type="single",
            channel=args.channel
        )
        
        widget = result.get("AVEnc.VideoWidget", [])
        if not widget:
            widget = [{}]
        
        # 更新通道标题
        if "ChannelTitle" not in widget[0]:
            widget[0]["ChannelTitle"] = {}
        
        widget[0]["ChannelTitle"]["Name"] = args.title
        widget[0]["ChannelTitle"]["SerialNo"] = args.device_sn
        
        # 更新属性
        if "ChannelTitleAttribute" not in widget[0]:
            widget[0]["ChannelTitleAttribute"] = {
                "BackColor": "0x00000000",
                "FrontColor": "0xFFFFFFFF",
                "EncodeBlend": enable,
                "PreviewBlend": enable,
                "RelativePos": [100, 50, 0, 0]
            }
        else:
            widget[0]["ChannelTitleAttribute"]["EncodeBlend"] = enable
            widget[0]["ChannelTitleAttribute"]["PreviewBlend"] = enable
        
        # 设置配置
        set_result = set_osd_config(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            config=widget,
            config_type="single",
            channel=args.channel
        )
        
        print()
        print("✅ 通道标题设置成功")
        print(f"   状态：{'启用' if enable else '禁用'}")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="杰峰设备 OSD 水印设置技能")
    
    # 全局参数
    parser.add_argument("--action", required=True,
                        choices=["get-single", "get-multi", "set-channel-title"],
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
    
    # set-channel-title 参数
    parser.add_argument("--title",
                        help="通道标题文本")
    parser.add_argument("--enable", action="store_true",
                        help="启用通道标题")
    parser.add_argument("--disable", action="store_true",
                        help="禁用通道标题")
    
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
    if args.action == "get-single":
        return get_single_action(args)
    elif args.action == "get-multi":
        return get_multi_action(args)
    elif args.action == "set-channel-title":
        return set_channel_title_action(args)
    else:
        print(f"❌ 未知操作：{args.action}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
