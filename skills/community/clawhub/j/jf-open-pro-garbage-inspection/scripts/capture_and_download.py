#!/usr/bin/env python3
"""
杰峰垃圾溢出巡检 — 抓图 + 下载脚本

功能：
- 从 config/cameras.json 或 CLI 参数获取摄像头列表
- 批量获取 deviceToken
- 对每个设备执行抓图
- 将图片下载到指定本地目录
"""

import os
import sys
import argparse
import requests
import json
from datetime import datetime
from typing import Dict, Any, List

# 导入加密工具
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from crypto import get_time_millis, generate_signature
except ImportError:
    print("错误：找不到 crypto.py 模块")
    print("   请确保 scripts/crypto.py 存在")
    sys.exit(1)

# API 基础地址
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


def get_device_tokens(device_sns: List[str], uuid: str, app_key: str,
                      app_secret: str, move_card: int) -> Dict[str, str]:
    """获取设备 Token 列表，返回 sn -> token 映射"""
    url = f"{JF_BASE_URL}/rtc/device/token"
    headers = get_headers(uuid, app_key, app_secret, move_card)
    body = {"sns": device_sns, "accessToken": ""}
    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()
    if result.get("code") != 2000:
        raise RuntimeError(f"获取设备 Token 失败：{result.get('msg', '未知错误')}")
    token_map = {}
    for item in result.get("data", []):
        sn = item.get("sn")
        token = item.get("token")
        if sn and token:
            token_map[sn] = token
    return token_map


def device_capture(device_token: str, uuid: str, app_key: str,
                   app_secret: str, move_card: int,
                   channel: int = 0, pic_type: int = 0) -> Dict[str, Any]:
    """设备抓图，返回包含 image URL 的 data 字典"""
    url = f"{JF_BASE_URL}/rtc/device/capture/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)
    body = {
        "Name": "OPSNAP",
        "OPSNAP": {"Channel": channel, "PicType": pic_type}
    }
    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()
    if result.get("code") != 2000:
        raise RuntimeError(f"抓图失败：{result.get('msg', '未知错误')}")
    data = result.get("data", {})
    ret = data.get("Ret")
    if ret not in [100, "100", 200, "200"]:
        ret_msg = data.get("retMsg", "未知错误")
        raise RuntimeError(f"设备返回错误：{ret_msg} (Ret={ret})")
    return data


def download_image(image_url: str, output_path: str, max_retries: int = 1) -> bool:
    """下载图片到本地，失败重试一次"""
    for attempt in range(max_retries + 1):
        try:
            resp = requests.get(image_url, timeout=30)
            if resp.status_code == 200:
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, 'wb') as f:
                    f.write(resp.content)
                return True
        except Exception:
            if attempt < max_retries:
                continue
    return False


def load_cameras_config(config_path: str) -> Dict[str, Any]:
    """加载摄像头配置文件"""
    if not os.path.exists(config_path):
        return {"cameras": [], "settings": {"overflow_threshold": "moderate", "default_channel": 0}}
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def inspect_devices(devices: List[Dict[str, str]], uuid: str, app_key: str,
                    app_secret: str, move_card: int, output_dir: str,
                    channel: int = 0, json_output: bool = False) -> int:
    """
    对设备列表执行抓图 + 下载

    devices: [{"sn": "...", "name": "...", "password": "...", "location": "..."}]
    返回: 0=全部成功, 1=有失败
    """
    if not devices:
        if json_output:
            print(json.dumps({"total": 0, "success": 0, "failed": 0, "results": []}, ensure_ascii=False))
        else:
            print("没有需要巡检的设备")
        return 0

    device_sns = [d['sn'] for d in devices]

    if not json_output:
        print(f"正在巡检 {len(devices)} 个摄像头...")

    # 批量获取 Token
    try:
        token_map = get_device_tokens(device_sns, uuid, app_key, app_secret, move_card)
    except RuntimeError as e:
        if json_output:
            print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        else:
            print(f"错误：{e}", file=sys.stderr)
        return 1

    # 准备输出目录
    os.makedirs(output_dir, exist_ok=True)

    success_count = 0
    fail_count = 0
    results = []

    for device in devices:
        sn = device['sn']
        name = device.get('name', sn)
        location = device.get('location', '')

        if sn not in token_map:
            fail_count += 1
            if json_output:
                results.append({"sn": sn, "name": name, "location": location,
                                "success": False, "error": "Token 获取失败"})
            else:
                print(f"  {name} ({sn}): Token 获取失败")
            continue

        try:
            data = device_capture(
                device_token=token_map[sn],
                uuid=uuid, app_key=app_key,
                app_secret=app_secret, move_card=move_card,
                channel=channel
            )
            image_url = data.get("image", "")

            # 生成文件名并下载
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{sn}_{timestamp}.png"
            output_path = os.path.join(output_dir, filename)

            if download_image(image_url, output_path):
                success_count += 1
                if json_output:
                    results.append({"sn": sn, "name": name, "location": location,
                                    "success": True, "file": output_path, "url": image_url})
                else:
                    print(f"  {name} ({sn}): 抓图成功 -> {output_path}")
            else:
                fail_count += 1
                if json_output:
                    results.append({"sn": sn, "name": name, "location": location,
                                    "success": False, "error": "下载失败"})
                else:
                    print(f"  {name} ({sn}): 下载失败")

        except RuntimeError as e:
            fail_count += 1
            if json_output:
                results.append({"sn": sn, "name": name, "location": location,
                                "success": False, "error": str(e)})
            else:
                print(f"  {name} ({sn}): {e}")

    if json_output:
        print(json.dumps({
            "total": len(devices),
            "success": success_count,
            "failed": fail_count,
            "results": results
        }, ensure_ascii=False, indent=2))
    else:
        print(f"巡检完成：成功 {success_count} 台，失败 {fail_count} 台")

    return 0 if fail_count == 0 else 1


def main():
    parser = argparse.ArgumentParser(description="杰峰垃圾溢出巡检 — 抓图下载")

    parser.add_argument("--action", required=True,
                        choices=["inspect-single", "inspect-batch"],
                        help="操作类型")
    parser.add_argument("--uuid", default=os.getenv("JF_UUID"),
                        help="开放平台用户 uuid")
    parser.add_argument("--app-key", default=os.getenv("JF_APP_KEY"),
                        help="应用 appKey")
    parser.add_argument("--app-secret", default=os.getenv("JF_APP_SECRET"),
                        help="应用密钥")
    parser.add_argument("--move-card", type=int,
                        default=int(os.getenv("JF_MOVE_CARD", "2")),
                        help="移动卡标识")

    # inspect-single 参数
    parser.add_argument("--device-sn", help="单设备模式指定设备 SN")
    parser.add_argument("--device-name", default="", help="单设备模式指定设备名称")
    parser.add_argument("--device-location", default="", help="单设备模式指定位置描述")

    # inspect-batch 参数
    parser.add_argument("--config", help="配置文件路径（默认 config/cameras.json）")

    # 通用参数
    parser.add_argument("--output-dir", help="图片下载目录")
    parser.add_argument("--channel", type=int, help="通道号（覆盖配置）")
    parser.add_argument("--json", action="store_true", dest="json_output",
                        help="JSON 格式输出")

    args = parser.parse_args()

    # 验证必需参数
    if not args.uuid:
        print("错误：缺少 --uuid 或 JF_UUID 环境变量", file=sys.stderr)
        return 1
    if not args.app_key:
        print("错误：缺少 --app-key 或 JF_APP_KEY 环境变量", file=sys.stderr)
        return 1
    if not args.app_secret:
        print("错误：缺少 --app-secret 或 JF_APP_SECRET 环境变量", file=sys.stderr)
        return 1

    # 确定输出目录
    if not args.output_dir:
        today = datetime.now().strftime("%Y%m%d")
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        args.output_dir = os.path.join(script_dir, "captures", today)

    # 确定通道号
    channel = args.channel if args.channel is not None else 0

    # 执行对应操作
    if args.action == "inspect-single":
        if not args.device_sn:
            print("错误：inspect-single 需要 --device-sn 参数", file=sys.stderr)
            return 1
        devices = [{
            "sn": args.device_sn,
            "name": args.device_name or args.device_sn,
            "password": "",
            "location": args.device_location
        }]
        return inspect_devices(devices, args.uuid, args.app_key, args.app_secret,
                               args.move_card, args.output_dir, channel, args.json_output)

    elif args.action == "inspect-batch":
        # 确定配置文件路径
        if not args.config:
            script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            args.config = os.path.join(script_dir, "config", "cameras.json")

        config = load_cameras_config(args.config)
        cameras = config.get("cameras", [])

        if not cameras:
            if args.json_output:
                print(json.dumps({"total": 0, "success": 0, "failed": 0,
                                  "results": [], "error": "配置文件中没有摄像头"}, ensure_ascii=False))
            else:
                print("配置文件中没有摄像头，请先添加摄像头")
            return 1

        # 使用配置中的通道号（如 CLI 未指定）
        if args.channel is None:
            channel = config.get("settings", {}).get("default_channel", 0)

        return inspect_devices(cameras, args.uuid, args.app_key, args.app_secret,
                               args.move_card, args.output_dir, channel, args.json_output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
