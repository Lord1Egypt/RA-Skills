#!/usr/bin/env python3
"""
杰峰 Watchdog 监控 — 主脚本

功能：
- capture: 批量抓图 monitors.json 中所有设备
- capture-single: 单设备抓图（用于 baseline 设置）
- crop-regions: 按 monitors.json 中的坐标裁剪图片
- crop-baselines: 按 Widget JSON 输出的坐标裁剪 baseline 图片
"""

import os
import sys
import argparse
import json
import requests
from datetime import datetime
from typing import Dict, Any, List

# 导入加密工具（同目录）
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from crypto import get_time_millis, generate_signature
except ImportError:
    print("错误：找不到 crypto.py 模块", file=sys.stderr)
    print("   请确保 scripts/crypto.py 存在", file=sys.stderr)
    sys.exit(1)

# 导入 PIL（裁剪用）
try:
    from PIL import Image
except ImportError:
    print("错误：缺少 Pillow 库，请执行 pip install Pillow", file=sys.stderr)
    sys.exit(1)

# API 基础地址
JF_ENDPOINT = os.getenv("JF_ENDPOINT", "api-cn.jftechws.com")
JF_BASE_URL = f"https://{JF_ENDPOINT}/gwp/v3"

# Skill 根目录（scripts/ 的上一级）
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ---------------------------------------------------------------------------
# API 工具函数
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# 配置读写
# ---------------------------------------------------------------------------

def load_monitors_config(config_path: str) -> Dict[str, Any]:
    """加载 monitors.json 配置文件"""
    if not os.path.exists(config_path):
        return {"monitors": [], "settings": {"default_channel": 0, "sensitivity": "moderate"}}
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_monitors_config(config_path: str, config: Dict[str, Any]) -> None:
    """保存 monitors.json 配置文件"""
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# 裁剪工具
# ---------------------------------------------------------------------------

def crop_image(source_path: str, x: int, y: int, width: int, height: int,
               output_path: str) -> bool:
    """
    使用 PIL 裁剪图片

    Args:
        source_path: 源图片路径
        x, y: 裁剪左上角坐标
        width, height: 裁剪宽高
        output_path: 输出路径

    Returns:
        True 成功, False 失败
    """
    try:
        img = Image.open(source_path)
        # PIL crop box: (left, upper, right, lower)
        box = (x, y, x + width, y + height)
        cropped = img.crop(box)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        cropped.save(output_path)
        return True
    except Exception as e:
        return False


# ---------------------------------------------------------------------------
# Action: capture — 批量抓图
# ---------------------------------------------------------------------------

def action_capture(config_path: str, uuid: str, app_key: str, app_secret: str,
                   move_card: int, output_dir: str, channel: int,
                   json_output: bool) -> int:
    """
    批量抓图 monitors.json 中所有设备

    Returns: 0=全部成功, 1=有失败
    """
    config = load_monitors_config(config_path)
    monitors = config.get("monitors", [])

    if not monitors:
        if json_output:
            print(json.dumps({"total": 0, "success": 0, "failed": 0,
                              "results": [], "error": "配置中没有监控设备"},
                             ensure_ascii=False))
        else:
            print("配置中没有监控设备，请先添加设备")
        return 1

    device_sns = [m['sn'] for m in monitors]

    # 如果 CLI 未指定通道号，使用配置中的默认值
    if channel is None:
        channel = config.get("settings", {}).get("default_channel", 0)

    if not json_output:
        print(f"正在抓图 {len(monitors)} 个设备...")

    # 批量获取 Token
    try:
        token_map = get_device_tokens(device_sns, uuid, app_key, app_secret, move_card)
    except RuntimeError as e:
        if json_output:
            print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        else:
            print(f"错误：{e}", file=sys.stderr)
        return 1

    os.makedirs(output_dir, exist_ok=True)

    success_count = 0
    fail_count = 0
    results = []

    for monitor in monitors:
        sn = monitor['sn']
        name = monitor.get('name', sn)

        if sn not in token_map:
            fail_count += 1
            if json_output:
                results.append({"sn": sn, "name": name, "success": False,
                                "error": "Token 获取失败"})
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

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{sn}_{timestamp}.png"
            output_path = os.path.join(output_dir, filename)

            if download_image(image_url, output_path):
                success_count += 1
                if json_output:
                    results.append({"sn": sn, "name": name, "success": True,
                                    "file": output_path, "url": image_url})
                else:
                    print(f"  {name} ({sn}): 抓图成功 -> {output_path}")
            else:
                fail_count += 1
                if json_output:
                    results.append({"sn": sn, "name": name, "success": False,
                                    "error": "下载失败"})
                else:
                    print(f"  {name} ({sn}): 下载失败")

        except RuntimeError as e:
            fail_count += 1
            if json_output:
                results.append({"sn": sn, "name": name, "success": False,
                                "error": str(e)})
            else:
                print(f"  {name} ({sn}): {e}")

    if json_output:
        print(json.dumps({
            "total": len(monitors),
            "success": success_count,
            "failed": fail_count,
            "results": results
        }, ensure_ascii=False, indent=2))
    else:
        print(f"抓图完成：成功 {success_count} 台，失败 {fail_count} 台")

    return 0 if fail_count == 0 else 1


# ---------------------------------------------------------------------------
# Action: capture-single — 单设备抓图
# ---------------------------------------------------------------------------

def action_capture_single(device_sn: str, device_name: str, password: str,
                          uuid: str, app_key: str, app_secret: str,
                          move_card: int, output_dir: str, channel: int,
                          json_output: bool) -> int:
    """
    单设备抓图（用于 baseline 设置）

    Returns: 0=成功, 1=失败
    """
    if channel is None:
        channel = 0

    name = device_name or device_sn

    if not json_output:
        print(f"正在抓图 {name} ({device_sn})...")

    # 获取 Token
    try:
        token_map = get_device_tokens([device_sn], uuid, app_key, app_secret, move_card)
    except RuntimeError as e:
        if json_output:
            print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        else:
            print(f"错误：{e}", file=sys.stderr)
        return 1

    if device_sn not in token_map:
        msg = "Token 获取失败"
        if json_output:
            print(json.dumps({"sn": device_sn, "name": name, "success": False,
                              "error": msg}, ensure_ascii=False))
        else:
            print(f"  {name} ({device_sn}): {msg}")
        return 1

    try:
        data = device_capture(
            device_token=token_map[device_sn],
            uuid=uuid, app_key=app_key,
            app_secret=app_secret, move_card=move_card,
            channel=channel
        )
        image_url = data.get("image", "")

        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{device_sn}_{timestamp}.png"
        output_path = os.path.join(output_dir, filename)

        if download_image(image_url, output_path):
            if json_output:
                print(json.dumps({"sn": device_sn, "name": name, "success": True,
                                  "file": output_path, "url": image_url},
                                 ensure_ascii=False, indent=2))
            else:
                print(f"  {name} ({device_sn}): 抓图成功 -> {output_path}")
            return 0
        else:
            msg = "下载失败"
            if json_output:
                print(json.dumps({"sn": device_sn, "name": name, "success": False,
                                  "error": msg}, ensure_ascii=False))
            else:
                print(f"  {name} ({device_sn}): {msg}")
            return 1

    except RuntimeError as e:
        if json_output:
            print(json.dumps({"sn": device_sn, "name": name, "success": False,
                              "error": str(e)}, ensure_ascii=False))
        else:
            print(f"  {name} ({device_sn}): {e}")
        return 1


# ---------------------------------------------------------------------------
# Action: crop-regions — 按 monitors.json 坐标裁剪
# ---------------------------------------------------------------------------

def action_crop_regions(config_path: str, source_image: str, device_sn: str,
                        output_dir: str, json_output: bool) -> int:
    """
    从 monitors.json 中找到指定设备，按其 regions 坐标裁剪图片

    Returns: 0=全部成功, 1=有失败
    """
    config = load_monitors_config(config_path)
    monitors = config.get("monitors", [])

    # 查找目标设备
    target = None
    for m in monitors:
        if m.get('sn') == device_sn:
            target = m
            break

    if target is None:
        msg = f"配置中未找到设备 {device_sn}"
        if json_output:
            print(json.dumps({"error": msg}, ensure_ascii=False))
        else:
            print(f"错误：{msg}", file=sys.stderr)
        return 1

    regions = target.get("regions", [])
    if not regions:
        msg = f"设备 {device_sn} 没有配置裁剪区域"
        if json_output:
            print(json.dumps({"error": msg, "sn": device_sn, "regions": 0},
                             ensure_ascii=False))
        else:
            print(f"提示：{msg}")
        return 1

    if not os.path.exists(source_image):
        msg = f"源图片不存在：{source_image}"
        if json_output:
            print(json.dumps({"error": msg}, ensure_ascii=False))
        else:
            print(f"错误：{msg}", file=sys.stderr)
        return 1

    os.makedirs(output_dir, exist_ok=True)

    success_count = 0
    fail_count = 0
    results = []

    for region in regions:
        region_id = region.get("id", "unknown")
        x = region.get("x", 0)
        y = region.get("y", 0)
        w = region.get("width", 0)
        h = region.get("height", 0)

        filename = f"{device_sn}_{region_id}.png"
        output_path = os.path.join(output_dir, filename)

        if crop_image(source_image, x, y, w, h, output_path):
            success_count += 1
            if json_output:
                results.append({"regionId": region_id, "success": True,
                                "file": output_path,
                                "box": {"x": x, "y": y, "width": w, "height": h}})
            else:
                print(f"  区域 {region_id}: 裁剪成功 -> {output_path}")
        else:
            fail_count += 1
            if json_output:
                results.append({"regionId": region_id, "success": False,
                                "error": "裁剪失败"})
            else:
                print(f"  区域 {region_id}: 裁剪失败")

    if json_output:
        print(json.dumps({
            "sn": device_sn,
            "total": len(regions),
            "success": success_count,
            "failed": fail_count,
            "results": results
        }, ensure_ascii=False, indent=2))
    else:
        print(f"裁剪完成：成功 {success_count} 个区域，失败 {fail_count} 个")

    return 0 if fail_count == 0 else 1


# ---------------------------------------------------------------------------
# Action: crop-baselines — 按 Widget JSON 坐标裁剪 baseline
# ---------------------------------------------------------------------------

def action_crop_baselines(source_image: str, device_sn: str, regions_json: str,
                          output_dir: str, json_output: bool) -> int:
    """
    按 Widget JSON 输出的区域坐标裁剪 baseline 图片

    regions_json: JSON 字符串，格式如
        [{"id": "r1", "x": 0, "y": 0, "width": 100, "height": 100}, ...]

    输出文件名: {sn}_{regionId}_baseline.png

    Returns: 0=全部成功, 1=有失败
    """
    # 解析 regions JSON
    try:
        regions = json.loads(regions_json)
    except json.JSONDecodeError as e:
        msg = f"regions-json 解析失败：{e}"
        if json_output:
            print(json.dumps({"error": msg}, ensure_ascii=False))
        else:
            print(f"错误：{msg}", file=sys.stderr)
        return 1

    if not isinstance(regions, list) or not regions:
        msg = "regions-json 为空或格式不正确"
        if json_output:
            print(json.dumps({"error": msg}, ensure_ascii=False))
        else:
            print(f"错误：{msg}", file=sys.stderr)
        return 1

    if not os.path.exists(source_image):
        msg = f"源图片不存在：{source_image}"
        if json_output:
            print(json.dumps({"error": msg}, ensure_ascii=False))
        else:
            print(f"错误：{msg}", file=sys.stderr)
        return 1

    os.makedirs(output_dir, exist_ok=True)

    success_count = 0
    fail_count = 0
    results = []

    for region in regions:
        region_id = region.get("id", "unknown")
        x = region.get("x", 0)
        y = region.get("y", 0)
        w = region.get("width", 0)
        h = region.get("height", 0)

        filename = f"{device_sn}_{region_id}_baseline.png"
        output_path = os.path.join(output_dir, filename)

        if crop_image(source_image, x, y, w, h, output_path):
            success_count += 1
            if json_output:
                results.append({"regionId": region_id, "success": True,
                                "file": output_path,
                                "box": {"x": x, "y": y, "width": w, "height": h}})
            else:
                print(f"  区域 {region_id}: baseline 裁剪成功 -> {output_path}")
        else:
            fail_count += 1
            if json_output:
                results.append({"regionId": region_id, "success": False,
                                "error": "裁剪失败"})
            else:
                print(f"  区域 {region_id}: baseline 裁剪失败")

    if json_output:
        print(json.dumps({
            "sn": device_sn,
            "total": len(regions),
            "success": success_count,
            "failed": fail_count,
            "results": results
        }, ensure_ascii=False, indent=2))
    else:
        print(f"Baseline 裁剪完成：成功 {success_count} 个区域，失败 {fail_count} 个")

    return 0 if fail_count == 0 else 1


# ---------------------------------------------------------------------------
# CLI 入口
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="杰峰 Watchdog 监控 — 抓图与裁剪工具"
    )

    parser.add_argument("--action", required=True,
                        choices=["capture", "capture-single",
                                 "crop-regions", "crop-baselines"],
                        help="操作类型")
    parser.add_argument("--uuid", default=os.getenv("JF_UUID"),
                        help="开放平台用户 uuid (env: JF_UUID)")
    parser.add_argument("--app-key", default=os.getenv("JF_APP_KEY"),
                        help="应用 appKey (env: JF_APP_KEY)")
    parser.add_argument("--app-secret", default=os.getenv("JF_APP_SECRET"),
                        help="应用密钥 (env: JF_APP_SECRET)")
    parser.add_argument("--move-card", type=int,
                        default=int(os.getenv("JF_MOVE_CARD", "2")),
                        help="移动卡标识 (env: JF_MOVE_CARD, default: 2)")

    # 配置文件
    parser.add_argument("--config",
                        help="monitors.json 路径 (default: config/monitors.json)")

    # capture-single 参数
    parser.add_argument("--device-sn", help="设备序列号")
    parser.add_argument("--device-name", default="", help="设备显示名称")
    parser.add_argument("--password", default="", help="设备密码")

    # crop 参数
    parser.add_argument("--source-image", help="源图片路径 (crop 操作)")
    parser.add_argument("--regions-json",
                        help="区域 JSON 字符串 (crop-baselines)")

    # 通用参数
    parser.add_argument("--output-dir", help="输出目录")
    parser.add_argument("--channel", type=int, default=None,
                        help="通道号 (覆盖配置)")
    parser.add_argument("--json", action="store_true", dest="json_output",
                        help="JSON 格式输出")

    args = parser.parse_args()

    # ---- 验证必需参数（capture / capture-single 需要凭证） ----
    needs_credentials = args.action in ("capture", "capture-single")
    if needs_credentials:
        if not args.uuid:
            print("错误：缺少 --uuid 或 JF_UUID 环境变量", file=sys.stderr)
            return 1
        if not args.app_key:
            print("错误：缺少 --app-key 或 JF_APP_KEY 环境变量", file=sys.stderr)
            return 1
        if not args.app_secret:
            print("错误：缺少 --app-secret 或 JF_APP_SECRET 环境变量",
                  file=sys.stderr)
            return 1

    # ---- 默认配置文件路径 ----
    if not args.config:
        args.config = os.path.join(SKILL_DIR, "config", "monitors.json")

    # ---- 执行对应 action ----
    if args.action == "capture":
        # 默认输出目录: {skill_dir}/captures/{YYYYMMDD}/
        if not args.output_dir:
            today = datetime.now().strftime("%Y%m%d")
            args.output_dir = os.path.join(SKILL_DIR, "captures", today)

        return action_capture(
            config_path=args.config,
            uuid=args.uuid, app_key=args.app_key,
            app_secret=args.app_secret, move_card=args.move_card,
            output_dir=args.output_dir, channel=args.channel,
            json_output=args.json_output
        )

    elif args.action == "capture-single":
        if not args.device_sn:
            print("错误：capture-single 需要 --device-sn 参数", file=sys.stderr)
            return 1

        # 默认输出目录: {skill_dir}/captures/{YYYYMMDD}/
        if not args.output_dir:
            today = datetime.now().strftime("%Y%m%d")
            args.output_dir = os.path.join(SKILL_DIR, "captures", today)

        return action_capture_single(
            device_sn=args.device_sn,
            device_name=args.device_name,
            password=args.password,
            uuid=args.uuid, app_key=args.app_key,
            app_secret=args.app_secret, move_card=args.move_card,
            output_dir=args.output_dir, channel=args.channel,
            json_output=args.json_output
        )

    elif args.action == "crop-regions":
        if not args.source_image:
            print("错误：crop-regions 需要 --source-image 参数", file=sys.stderr)
            return 1
        if not args.device_sn:
            print("错误：crop-regions 需要 --device-sn 参数", file=sys.stderr)
            return 1

        # 默认输出目录: {skill_dir}/baselines/
        if not args.output_dir:
            args.output_dir = os.path.join(SKILL_DIR, "baselines")

        return action_crop_regions(
            config_path=args.config,
            source_image=args.source_image,
            device_sn=args.device_sn,
            output_dir=args.output_dir,
            json_output=args.json_output
        )

    elif args.action == "crop-baselines":
        if not args.source_image:
            print("错误：crop-baselines 需要 --source-image 参数", file=sys.stderr)
            return 1
        if not args.device_sn:
            print("错误：crop-baselines 需要 --device-sn 参数", file=sys.stderr)
            return 1
        if not args.regions_json:
            print("错误：crop-baselines 需要 --regions-json 参数", file=sys.stderr)
            return 1

        # 默认输出目录: {skill_dir}/baselines/
        if not args.output_dir:
            args.output_dir = os.path.join(SKILL_DIR, "baselines")

        return action_crop_baselines(
            source_image=args.source_image,
            device_sn=args.device_sn,
            regions_json=args.regions_json,
            output_dir=args.output_dir,
            json_output=args.json_output
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
