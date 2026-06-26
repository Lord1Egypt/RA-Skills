#!/usr/bin/env python3
"""
杰峰设备直播预览技能（开发版）

支持功能：
- 获取 FLV/HLS/RTMP/RTSP/MP4/WebRTC直播地址
- 支持主码流（高清）和辅码流（标清）
- 自定义 URL 有效期
"""

import os
import sys
import argparse
import requests
from datetime import datetime, timedelta
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


def get_livestream_url(device_token: str, uuid: str, app_key: str,
                       app_secret: str, move_card: int,
                       channel: str = "0", stream: str = "1",
                       protocol: str = "flv",
                       username: str = "admin", password: str = "",
                       expire_time: Optional[int] = None) -> Dict[str, Any]:
    """
    获取设备直播地址
    
    API: POST /gwp/v3/rtc/device/livestream/{deviceToken}
    """
    url = f"{JF_BASE_URL}/rtc/device/livestream/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)
    
    body = {
        "channel": channel,
        "stream": stream,
        "protocol": protocol,
        "username": username,
        "password": password
    }
    
    if expire_time:
        body["expireTime"] = str(expire_time)
    
    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()
    
    if result.get("code") != 2000:
        raise RuntimeError(f"获取直播地址失败：{result.get('msg', '未知错误')}")
    
    data = result.get("data", {})
    ret = data.get("Ret")
    
    if ret not in [100, "100", 200, "200"]:
        ret_msg = data.get("retMsg", "未知错误")
        raise RuntimeError(f"设备返回错误：{ret_msg} (Ret={ret})")
    
    return data


# ============== 动作处理函数 ==============

def get_url_action(args: argparse.Namespace) -> int:
    """执行获取直播地址操作"""
    try:
        # 计算过期时间
        expire_time = None
        if args.expire_hours:
            expire_dt = datetime.now() + timedelta(hours=args.expire_hours)
            expire_time = int(expire_dt.timestamp() * 1000)
        elif args.expire_days:
            expire_dt = datetime.now() + timedelta(days=args.expire_days)
            expire_time = int(expire_dt.timestamp() * 1000)
        elif args.expire_time:
            expire_time = args.expire_time
        
        # 码流说明
        stream_name = "高清（主码流）" if args.stream == "0" else "标清（辅码流）"
        
        print(f"正在获取设备 {args.device_sn} 的直播地址...")
        print(f"   协议：{args.protocol}")
        print(f"   码流：{stream_name}")
        print(f"   通道：{args.channel}")
        if expire_time:
            expire_dt = datetime.fromtimestamp(expire_time / 1000)
            print(f"   有效期：至 {expire_dt.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(f"   有效期：默认 10 小时")
        print()
        
        result = get_livestream_url(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            channel=args.channel,
            stream=args.stream,
            protocol=args.protocol,
            username=args.username,
            password=args.password,
            expire_time=expire_time
        )
        
        live_url = result.get("url", "")
        
        print("✅ 获取成功")
        print()
        print("📺 直播地址:")
        print(f"   {live_url}")
        print()
        
        # 显示使用说明
        print("💡 使用说明:")
        
        protocol = args.protocol.lower()
        if protocol in ["flv", "ws-flv"]:
            print("   - 适用于 Web 端（配合 flv.js）")
            print("   - 示例：<script src=\"https://cdn.bootcdn.net/ajax/libs/flv.js/1.6.2/flv.min.js\"></script>")
        elif protocol in ["hls-ts", "hls-fmp4"]:
            print("   - 适用于 iOS、Safari、微信小程序")
            print("   - 示例：<video src=\"{url}\" controls></video>")
        elif protocol in ["rtmp-flv", "rtmp-enhanced"]:
            print("   - 适用于微信小程序 live-player")
            print("   - mode: live, autoplay: true")
        elif protocol == "webrtc":
            print("   - 适用于 WebRTC 低时延播放（仅 H.264）")
            print("   - 需要 HTTPS 环境")
        elif protocol in ["rtsp-sdp", "rtsp-pri"]:
            print("   - 适用于 VLC、FFmpeg 等播放器")
            print("   - 示例：vlc {url}")
        elif protocol == "mp4":
            print("   - 适用于 Chrome 23+ 浏览器")
            print("   - 示例：<video src=\"{url}\" controls></video>")
        
        print()
        print("⚠️  注意事项:")
        print("   - URL 在有效期内可重复使用")
        print("   - 低功耗设备需在 3 秒内播放")
        print("   - 部分设备同时只支持一路直播")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def test_url_action(args: argparse.Namespace) -> int:
    """执行测试 URL 操作（检查 URL 是否有效）"""
    try:
        print(f"正在测试直播地址...")
        
        # 先获取 URL
        result = get_livestream_url(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            channel=args.channel,
            stream=args.stream,
            protocol=args.protocol,
            username=args.username,
            password=args.password
        )
        
        live_url = result.get("url", "")
        
        if not live_url:
            print("❌ 未获取到直播地址")
            return 1
        
        # 测试 URL 连通性（HEAD 请求）
        print(f"   测试 URL: {live_url[:80]}...")
        
        resp = requests.head(live_url, timeout=10, allow_redirects=True)
        
        if resp.status_code in [200, 301, 302]:
            print()
            print("✅ URL 有效")
            print(f"   状态码：{resp.status_code}")
            print(f"   Content-Type: {resp.headers.get('Content-Type', 'unknown')}")
            return 0
        else:
            print()
            print(f"⚠️  URL 响应异常")
            print(f"   状态码：{resp.status_code}")
            return 1
        
    except requests.exceptions.RequestException as e:
        print(f"❌ URL 测试失败：{e}")
        return 1
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="杰峰设备直播预览技能")
    
    # 全局参数
    parser.add_argument("--action", required=True,
                        choices=["get-url", "test-url"],
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
    parser.add_argument("--username", default=os.getenv("JF_DEVICE_USERNAME", "admin"),
                        help="设备用户名")
    parser.add_argument("--password", default=os.getenv("JF_DEVICE_PASSWORD", ""),
                        help="设备密码")
    
    # get-url 参数
    parser.add_argument("--channel", default="0",
                        help="通道号（默认 0）")
    parser.add_argument("--stream", default="1", choices=["0", "1"],
                        help="码流类型（0=高清主码流，1=标清辅码流）")
    parser.add_argument("--protocol", default="flv",
                        choices=[
                            "flv", "flv-enhanced",
                            "hls-ts", "hls-fmp4",
                            "rtmp-flv", "rtmp-enhanced",
                            "rtsp-sdp", "rtsp-pri",
                            "mp4",
                            "ws-pri", "ws-flv", "ws-flv-enhanced",
                            "webrtc"
                        ],
                        help="播放协议")
    parser.add_argument("--expire-hours", type=int,
                        help="URL 有效期（小时）")
    parser.add_argument("--expire-days", type=int,
                        help="URL 有效期（天）")
    parser.add_argument("--expire-time", type=int,
                        help="URL 过期时间戳（毫秒）")
    
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
    if args.action == "get-url":
        return get_url_action(args)
    elif args.action == "test-url":
        return test_url_action(args)
    else:
        print(f"❌ 未知操作：{args.action}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
