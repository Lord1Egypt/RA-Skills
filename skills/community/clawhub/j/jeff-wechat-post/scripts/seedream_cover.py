#!/usr/bin/env python3
"""
微信朋友圈营销图生成 - Seedream 5.0 API
用法: python3 seedream_cover.py --title "产品标题" --output /path/to/output.png [--style minimal] [--palette "深蓝金"]
"""

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request


# 从凭据文件读取 API Key（安全存储）
CREDENTIALS_FILE = "/root/.openclaw/credentials/seedream.json"

def _load_credentials() -> dict:
    """加载凭据文件。"""
    try:
        with open(CREDENTIALS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ 凭据文件未找到: {CREDENTIALS_FILE}")
        print("   请创建该文件并填入 seedream API 配置")
        sys.exit(2)
    except json.JSONDecodeError:
        print(f"❌ 凭据文件 JSON 格式错误: {CREDENTIALS_FILE}")
        sys.exit(2)


_CREDENTIALS = _load_credentials()


API_URL = _CREDENTIALS.get("endpoint", "https://ark.cn-beijing.volces.com/api/v3/images/generations")
API_KEY = _CREDENTIALS.get("api_key", "")
MODEL = _CREDENTIALS.get("model", "doubao-seedream-5-0-260128")

if not API_KEY:
    print("❌ seedream.json 中缺少 api_key")
    sys.exit(2)


# 尺寸映射（必须 >= 3686400 pixels，火山引擎最低要求）
SIZE_MAP = {
    "9:16": "1920x2560",   # 4,915,200 pixels
    "3:4":  "1920x2560",   # ~2,185,600 pixels
    "1:1":  "1920x1920",   # 3,686,400 pixels (exact minimum)
}


def buildPrompt(
    title: str,
    style: str,
    palette: str,
    selling_points: str = "",
    discounted_price: str = "",
    original_price: str = "",
    has_qr: bool = False,
) -> str:
    """构造 WeChat 朋友圈图 prompt

    默认生图模式：背景图 + 矢量装饰 + 暖色调
    ⚠️ 关键规则：
    - 没有用户提供二维码时，图片中禁止出现任何二维码占位或扫码CTA
    - 价格展示：优惠价大字，原价灰色划线（如果有原价）
    """
    # 暖色基调默认配色词
    warm_palette = {
        "minimal": "暖橙米色系，柔和渐变背景，温馨商业风格",
        "notion": "暖米色主调，淡雅矢量装饰，清新温暖",
        "warm": "暖橙珊瑚色调，温暖柔和，亲切感强",
        "blueprint": "暖灰蓝调，专业温和，结构清晰",
    }
    warm_bg = "温暖渐变背景，柔和暖色调，几何矢量装饰图形，简约线条装饰，圆角设计"
    style_desc = warm_palette.get(style, warm_palette["minimal"])

    # 价格区
    price_desc = ""
    if discounted_price:
        if original_price:
            price_desc = f"，原价{original_price}居中，数字中间水平贯穿直线，优惠价{discounted_price}突出金色，旁边有「限时优惠」圆角Badge标签（深色底白字）"
        else:
            price_desc = f"，价格{discounted_price}突出"

    # QR区（仅当用户提供二维码时）
    qr_desc = "，底部右侧有二维码区域" if has_qr else "，无二维码区域"

    points_desc = f"，卖点：{selling_points}" if selling_points else ""

    # 只生成有数据的模块，禁止臆造任何未提供的信息
    layout_parts = []
    if selling_points:
        layout_parts.append("【卖点区域】：独立居中Container，Container宽度适中，内容文字左对齐，排版整齐。")
    if discounted_price:
        if original_price:
            layout_parts.append("【价格区域】：独立居中Container，优惠价突出金色，原价数字中间水平贯穿直线（非上下线），「限时优惠」Badge标签，文字左对齐。")
        else:
            layout_parts.append("【价格区域】：独立居中Container，优惠价突出金色，文字左对齐。")

    layout_rule = ("重要排版规则：" + "".join(layout_parts) + "整体居中布局，各区域分明，不堆砌。") if layout_parts else ""

    return (
        f"WeChat朋友圈营销海报，{title}{points_desc}{price_desc}，"
        f"{warm_bg}，{style_desc}，{palette}，"
        f"竖版9:16构图，高质感，商业海报风格，精致细节{qr_desc}。"
        f"{layout_rule}"
    )


def generateImage(
    title: str,
    output_path: str,
    style: str = "minimal",
    palette: str = "深蓝配金",
    aspect: str = "9:16",
    selling_points: str = "",
    discounted_price: str = "",
    original_price: str = "",
    has_qr: bool = False,
) -> bool:
    """调用 Seedream 5.0 API"""

    size = SIZE_MAP.get(aspect, "1920x2560")
    prompt = buildPrompt(title, style, palette, selling_points, discounted_price, original_price, has_qr)

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "sequential_image_generation": "disabled",
        "response_format": "url",
        "size": size,
        "stream": False,
        "watermark": False,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    print(f"🎨 正在生成朋友圈营销图...")
    print(f"   尺寸: {aspect} ({size})")
    print(f"   风格: {style} | 配色: {palette}")
    extra = f" (原价{original_price}中间直线划线+限时优惠Badge)" if original_price else ""; print(f"   价格: {discounted_price}{extra}")
    print(f"   二维码: {'有' if has_qr else '无（禁止臆造）'}")
    print(f"   Prompt: {prompt[:80]}...")

    req = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"❌ API HTTP 错误 {e.code}: {e.read().decode()[:300]}")
        return False
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return False

    if "data" not in result or not result["data"]:
        print(f"❌ 返回无 data: {result}")
        return False

    image_url = result["data"][0].get("url")
    if not image_url:
        print(f"❌ 未获取到图片 URL")
        return False

    print(f"✅ 生成成功，正在下载...")
    try:
        urllib.request.urlretrieve(image_url, output_path)
        size_kb = os.path.getsize(output_path) / 1024
        print(f"✅ 下载完成: {output_path} ({size_kb:.1f} KB)")
        return True
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="微信朋友圈营销图 - Seedream 5.0")
    parser.add_argument("--title", required=True, help="产品/服务标题")
    parser.add_argument("--output", required=True, help="输出图片路径（.png）")
    parser.add_argument(
        "--style",
        default="minimal",
        choices=["minimal", "notion", "warm", "blueprint"],
        help="图片风格",
    )
    parser.add_argument(
        "--palette",
        default="深蓝配金",
        help="配色方案",
    )
    parser.add_argument(
        "--aspect",
        default="9:16",
        choices=["9:16", "3:4", "1:1"],
        help="图片比例",
    )
    parser.add_argument(
        "--points",
        default="",
        help="核心卖点（用 | 分隔，如：艾宾浩斯记忆法|场景记忆|1v1真人带背）",
    )
    parser.add_argument(
        "--price",
        default="",
        help="优惠价（如：39.9）",
    )
    parser.add_argument(
        "--original-price",
        default="",
        help="原价（显示划线，如：399）",
    )
    parser.add_argument(
        "--qr",
        action="store_true",
        help="如已提供二维码，添加此参数",
    )
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)

    success = generateImage(
        args.title,
        args.output,
        style=args.style,
        palette=args.palette,
        aspect=args.aspect,
        selling_points=args.points,
        discounted_price=args.price,
        original_price=args.original_price,
        has_qr=args.qr,
    )

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
