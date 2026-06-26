#!/usr/bin/env python3
"""
杰峰设备批量抓图技能（开发版）

支持功能：
- 单设备抓图
- 批量设备抓图
- 自动 Token 管理
- 图片下载本地
"""

import os
import sys
import argparse
import requests
import json
from datetime import datetime
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


def get_device_tokens(device_sns: List[str], uuid: str, app_key: str,
                      app_secret: str, move_card: int,
                      access_token: str = "") -> Dict[str, str]:
    """
    获取设备 Token 列表
    
    API: POST /gwp/v3/rtc/device/token
    """
    url = f"{JF_BASE_URL}/rtc/device/token"
    headers = get_headers(uuid, app_key, app_secret, move_card)
    
    body = {
        "sns": device_sns,
        "accessToken": access_token
    }
    
    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()
    
    if result.get("code") != 2000:
        raise RuntimeError(f"获取设备 Token 失败：{result.get('msg', '未知错误')}")
    
    # 返回 sn -> token 映射
    data = result.get("data", [])
    token_map = {}
    for item in data:
        sn = item.get("sn")
        token = item.get("token")
        if sn and token:
            token_map[sn] = token
    
    return token_map


def device_capture(device_token: str, uuid: str, app_key: str,
                   app_secret: str, move_card: int,
                   channel: int = 0, pic_type: int = 0) -> Dict[str, Any]:
    """
    设备抓图
    
    API: POST /gwp/v3/rtc/device/capture/{deviceToken}
    Name: OPSNAP
    """
    url = f"{JF_BASE_URL}/rtc/device/capture/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)
    
    body = {
        "Name": "OPSNAP",
        "OPSNAP": {
            "Channel": channel,
            "PicType": pic_type
        }
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


def download_image(image_url: str, output_path: str) -> bool:
    """
    下载图片到本地
    
    Args:
        image_url: 图片 URL
        output_path: 保存路径
        
    Returns:
        是否成功
    """
    try:
        resp = requests.get(image_url, timeout=30)
        if resp.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(resp.content)
            return True
        return False
    except Exception:
        return False


def load_devices_file(file_path: str) -> List[Dict[str, str]]:
    """
    加载设备列表文件
    
    格式：设备序列号，设备名称（可选）
    """
    devices = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            parts = line.split('，')
            if len(parts) >= 1:
                device = {
                    'sn': parts[0].strip(),
                    'name': parts[1].strip() if len(parts) > 1 else parts[0].strip()
                }
                devices.append(device)
    
    return devices


# ============== 动作处理函数 ==============

def capture_action(args: argparse.Namespace) -> int:
    """执行单设备抓图操作"""
    try:
        pic_type_name = "实时图" if args.pic_type == 0 else "缩略图"
        
        if not args.json_output:
            print(f"正在抓取设备 {args.device_sn} 的图片...")
            print(f"   通道：{args.channel}")
            print(f"   类型：{pic_type_name}")
        
        result = device_capture(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            channel=args.channel,
            pic_type=args.pic_type
        )
        
        image_url = result.get("image", "")
        
        # JSON 格式输出
        if args.json_output:
            print(json.dumps({"url": image_url}, ensure_ascii=False))
        else:
            print()
            print("✅ 抓图成功")
            print()
            print("🖼️  图片地址 (完整 URL):")
            print(f"   {image_url}")
            print()
            
            # 下载图片
            if args.download:
                output_dir = args.output_dir or "."
                os.makedirs(output_dir, exist_ok=True)
                
                # 生成文件名
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{args.device_sn}_ch{args.channel}_{timestamp}.png"
                output_path = os.path.join(output_dir, filename)
                
                print(f"正在下载图片到：{output_path}")
                
                if download_image(image_url, output_path):
                    print(f"✅ 下载成功：{output_path}")
                else:
                    print(f"❌ 下载失败")
                    return 1
            
            print()
            print("⚠️  注意：图片 URL 有效期 24 小时，请及时下载保存")
        
        return 0
        
    except RuntimeError as e:
        if args.json_output:
            print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        else:
            print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def capture_auto_action(args: argparse.Namespace) -> int:
    """执行自动获取 Token 并抓图操作"""
    try:
        if not args.json_output:
            print(f"正在获取设备 {args.device_sn} 的 Token...")
        
        # 获取设备 Token
        token_map = get_device_tokens(
            device_sns=[args.device_sn],
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card
        )
        
        if args.device_sn not in token_map:
            if args.json_output:
                print(json.dumps({"error": "获取设备 Token 失败"}, ensure_ascii=False), file=sys.stderr)
            else:
                print(f"❌ 获取设备 Token 失败")
            return 1
        
        device_token = token_map[args.device_sn]
        
        if not args.json_output:
            print(f"   ✅ Token 获取成功")
            print()
            pic_type_name = "实时图" if args.pic_type == 0 else "缩略图"
            print(f"正在抓取设备 {args.device_sn} 的图片...")
            print(f"   通道：{args.channel}")
            print(f"   类型：{pic_type_name}")
        
        result = device_capture(
            device_token=device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            channel=args.channel,
            pic_type=args.pic_type
        )
        
        image_url = result.get("image", "")
        
        # JSON 格式输出
        if args.json_output:
            print(json.dumps({"url": image_url}, ensure_ascii=False))
        else:
            print()
            print("✅ 抓图成功")
            print()
            print("🖼️  图片地址 (完整 URL):")
            print(f"   {image_url}")
            print()
            
            # 下载图片
            if args.download:
                output_dir = args.output_dir or "."
                os.makedirs(output_dir, exist_ok=True)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{args.device_sn}_ch{args.channel}_{timestamp}.png"
                output_path = os.path.join(output_dir, filename)
                
                print(f"正在下载图片到：{output_path}")
                
                if download_image(image_url, output_path):
                    print(f"✅ 下载成功：{output_path}")
                else:
                    print(f"❌ 下载失败")
                    return 1
            
            print()
            print("⚠️  注意：图片 URL 有效期 24 小时，请及时下载保存")
        
        return 0
        
    except RuntimeError as e:
        if args.json_output:
            print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        else:
            print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def batch_capture_action(args: argparse.Namespace) -> int:
    """执行批量抓图操作"""
    try:
        # 加载设备列表
        if not args.json_output:
            print(f"正在加载设备列表：{args.devices_file}")
        devices = load_devices_file(args.devices_file)
        
        if not devices:
            if args.json_output:
                print(json.dumps({"error": "设备列表为空"}, ensure_ascii=False), file=sys.stderr)
            else:
                print(f"❌ 设备列表为空")
            return 1
        
        if not args.json_output:
            print(f"   设备数量：{len(devices)}")
            print()
        
        # 获取所有设备 Token
        device_sns = [d['sn'] for d in devices]
        if not args.json_output:
            print(f"正在获取设备 Token...")
        
        token_map = get_device_tokens(
            device_sns=device_sns,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card
        )
        
        if not args.json_output:
            print(f"   ✅ 成功获取 {len(token_map)} 个设备 Token")
            print()
        
        # 准备下载目录
        output_dir = args.output_dir or "."
        if args.download and not args.json_output:
            os.makedirs(output_dir, exist_ok=True)
            print(f"图片将下载到：{output_dir}")
            print()
        
        # 批量抓图
        success_count = 0
        fail_count = 0
        results = []  # 存储 JSON 结果
        
        if not args.json_output:
            print("开始批量抓图...")
            print("-" * 60)
        
        for device in devices:
            sn = device['sn']
            name = device['name']
            
            if sn not in token_map:
                if args.json_output:
                    results.append({"device": sn, "success": False, "error": "Token 获取失败"})
                else:
                    print(f"❌ {name} ({sn}): Token 获取失败")
                fail_count += 1
                continue
            
            device_token = token_map[sn]
            
            try:
                result = device_capture(
                    device_token=device_token,
                    uuid=args.uuid,
                    app_key=args.app_key,
                    app_secret=args.app_secret,
                    move_card=args.move_card,
                    channel=args.channel,
                    pic_type=args.pic_type
                )
                
                image_url = result.get("image", "")
                
                if args.download:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"{sn}_ch{args.channel}_{timestamp}.png"
                    output_path = os.path.join(output_dir, filename)
                    
                    if download_image(image_url, output_path):
                        if args.json_output:
                            results.append({"device": sn, "success": True, "url": image_url, "file": filename})
                        else:
                            print(f"✅ {name} ({sn}): 抓图成功 - {filename}")
                        success_count += 1
                    else:
                        if args.json_output:
                            results.append({"device": sn, "success": False, "error": "下载失败"})
                        else:
                            print(f"❌ {name} ({sn}): 下载失败")
                        fail_count += 1
                else:
                    if args.json_output:
                        results.append({"device": sn, "success": True, "url": image_url})
                    else:
                        print(f"✅ {name} ({sn}): 抓图成功")
                        print(f"   URL: {image_url}")
                    success_count += 1
                    
            except RuntimeError as e:
                if args.json_output:
                    results.append({"device": sn, "success": False, "error": str(e)})
                else:
                    print(f"❌ {name} ({sn}): {e}")
                fail_count += 1
        
        # JSON 格式输出
        if args.json_output:
            output = {
                "total": len(devices),
                "success": success_count,
                "failed": fail_count,
                "results": results
            }
            print(json.dumps(output, ensure_ascii=False, indent=2))
        else:
            print()
            print("=" * 60)
            print(f"批量抓图完成")
            print(f"   成功：{success_count} 个")
            print(f"   失败：{fail_count} 个")
        
        return 0 if fail_count == 0 else 1
        
    except RuntimeError as e:
        if args.json_output:
            print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        else:
            print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="杰峰设备批量抓图技能")
    
    # 全局参数
    parser.add_argument("--action", required=True,
                        choices=["capture", "capture-auto", "batch-capture"],
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
    parser.add_argument("--username", default=os.getenv("JF_DEVICE_USERNAME", "admin"),
                        help="设备用户名")
    parser.add_argument("--password", default=os.getenv("JF_DEVICE_PASSWORD", ""),
                        help="设备密码")
    
    # capture / capture-auto 参数
    parser.add_argument("--device-sn",
                        help="设备序列号")
    parser.add_argument("--channel", type=int, default=0,
                        help="通道号（默认 0）")
    parser.add_argument("--pic-type", type=int, default=0, choices=[0, 1],
                        help="图片类型（0=实时图，1=缩略图）")
    
    # batch-capture 参数
    parser.add_argument("--devices-file",
                        help="设备列表文件路径")
    
    # 下载参数
    parser.add_argument("--download", action="store_true",
                        help="下载图片到本地")
    parser.add_argument("--output-dir",
                        help="输出目录（默认当前目录）")
    
    # 输出格式参数
    parser.add_argument("--json", action="store_true", dest="json_output",
                        help="以 JSON 格式输出结果 ({\"url\":\"图片地址\"})")
    
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
    
    # 特定操作验证
    if args.action in ["capture", "capture-auto"] and not args.device_sn:
        print(f"❌ 错误：{args.action} 需要 --device-sn 参数", file=sys.stderr)
        return 1
    if args.action == "capture" and not args.device_token:
        print("❌ 错误：capture 需要 --device-token 参数", file=sys.stderr)
        return 1
    if args.action == "capture-auto" and not args.password:
        print("❌ 错误：capture-auto 需要 --password 参数", file=sys.stderr)
        return 1
    if args.action == "batch-capture" and not args.devices_file:
        print("❌ 错误：batch-capture 需要 --devices-file 参数", file=sys.stderr)
        return 1
    
    # 执行对应操作
    if args.action == "capture":
        return capture_action(args)
    elif args.action == "capture-auto":
        return capture_auto_action(args)
    elif args.action == "batch-capture":
        return batch_capture_action(args)
    else:
        print(f"❌ 未知操作：{args.action}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
