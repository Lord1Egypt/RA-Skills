#!/usr/bin/env python3
"""
AI图像生成脚本 — 由聚合数据 (juhe.cn) 提供数据支持
根据文本提示词生成图像，支持多种宽高比，自动下载保存到本地

用法:
    python image_generate.py <提示词>
    python image_generate.py "一只猫咪在草地上玩耍，写实风格"
    python image_generate.py "科技感壁纸，蓝色渐变" --size 2
    python image_generate.py "新年海报，红色喜庆" --size 4 --output ~/Desktop
    python image_generate.py "元气少女插画" --no-download

API Key 配置（任选其一，优先级从高到低）:
    1. 环境变量: export JUHE_IMAGE_KEY=your_api_key
    2. 脚本同目录的 .env 文件: JUHE_IMAGE_KEY=your_api_key
    3. 直接传参: python image_generate.py --key your_api_key "提示词"

免费申请 API Key: https://www.juhe.cn/docs/api/id/824
"""

import sys
import os
import json
import urllib.request
import urllib.parse
from pathlib import Path
from datetime import datetime

API_URL = "https://gpt.juhe.cn/text2image/generate"
REGISTER_URL = "https://www.juhe.cn/docs/api/id/824"

SIZE_MAP = {
    "1": "1:1",
    "2": "16:9",
    "3": "4:3",
    "4": "3:4",
    "5": "9:16",
}

MAX_PROMPT_LEN = 800


def load_api_key(cli_key: str = None) -> str:
    """按优先级加载 API Key"""
    if cli_key:
        return cli_key

    env_key = os.environ.get("JUHE_IMAGE_KEY", "").strip()
    if env_key:
        return env_key

    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("JUHE_IMAGE_KEY="):
                val = line.split("=", 1)[1].strip().strip('"').strip("'")
                if val:
                    return val

    return ""


def generate_image(prompt: str, api_key: str, size: str = "1", model: str = "auto") -> dict:
    """调用聚合数据 API 生成图像"""
    if len(prompt) > MAX_PROMPT_LEN:
        prompt = prompt[:MAX_PROMPT_LEN]
        print(f"⚠️  提示词超过 {MAX_PROMPT_LEN} 字符，已自动截断")

    params = {
        "key": api_key,
        "prompt": prompt,
        "size": size,
        "model": model,
    }

    data = urllib.parse.urlencode(params).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=data,
        method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    try:
        with urllib.request.urlopen(req, timeout=65) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except TimeoutError:
        return {"success": False, "error": "请求超时（文生图最长需60秒），请稍后重试"}
    except Exception as e:
        return {"success": False, "error": f"网络请求失败: {e}"}

    error_code = result.get("error_code", -1)
    if error_code == 0:
        image_url = result.get("result", {}).get("image", "")
        order_id = result.get("result", {}).get("orderid", "")
        return {"success": True, "image_url": image_url, "order_id": order_id}

    reason = result.get("reason", "生成失败")
    hint = ""
    if error_code in (10001, 10002):
        hint = f"\n   请检查 API Key 是否正确，免费申请：{REGISTER_URL}"
    elif error_code == 10012:
        hint = "\n   今日免费调用次数已用尽，请升级套餐"
    elif error_code == 282401:
        hint = "\n   提示词不可为空，请描述想要生成的图片内容"
    elif error_code == 282403:
        hint = "\n   提示词包含敏感内容，请修改后重试"
    elif error_code == 282404:
        hint = "\n   图像生成失败，建议稍后重试或修改提示词"

    return {"success": False, "error": f"{reason}{hint}", "error_code": error_code}


def download_image(url: str, output_dir: Path) -> str | None:
    """下载图片到本地，返回保存路径或 None"""
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"image_{timestamp}.png"
    save_path = output_dir / filename

    try:
        urllib.request.urlretrieve(url, save_path)
        return str(save_path)
    except Exception as e:
        print(f"⚠️  图片下载失败: {e}")
        print(f"   请手动访问链接保存图片（24小时内有效）")
        return None


def parse_args(args: list) -> dict:
    """解析命令行参数"""
    result = {
        "cli_key": None,
        "prompt": None,
        "size": "1",
        "output": None,
        "no_download": False,
        "model": "auto",
        "error": None,
    }

    i = 0
    positional = []

    while i < len(args):
        arg = args[i]
        if arg == "--key":
            if i + 1 < len(args):
                result["cli_key"] = args[i + 1]
                i += 2
            else:
                result["error"] = "错误: --key 后需要提供 API Key 值"
                return result
        elif arg == "--size":
            if i + 1 < len(args):
                size_val = args[i + 1]
                if size_val not in SIZE_MAP:
                    result["error"] = (
                        f"错误: 无效的尺寸代码 '{size_val}'，"
                        f"可用代码: 1(1:1) 2(16:9) 3(4:3) 4(3:4) 5(9:16)"
                    )
                    return result
                result["size"] = size_val
                i += 2
            else:
                result["error"] = "错误: --size 后需要提供尺寸代码（1-5）"
                return result
        elif arg == "--output":
            if i + 1 < len(args):
                result["output"] = args[i + 1]
                i += 2
            else:
                result["error"] = "错误: --output 后需要提供保存目录路径"
                return result
        elif arg == "--no-download":
            result["no_download"] = True
            i += 1
        elif arg == "--model":
            if i + 1 < len(args):
                result["model"] = args[i + 1]
                i += 2
            else:
                result["error"] = "错误: --model 后需要提供模型名称"
                return result
        else:
            positional.append(arg)
            i += 1

    if not positional:
        result["error"] = (
            "错误: 需要提供图片描述（提示词）\n"
            "用法: python image_generate.py [--key KEY] <提示词> [选项]\n"
            '示例: python image_generate.py "一只猫咪在草地上玩耍，写实风格"\n'
            f"\n免费申请 API Key: {REGISTER_URL}"
        )
        return result

    result["prompt"] = " ".join(positional)
    return result


def main():
    args = sys.argv[1:]

    if not args:
        print("用法: python image_generate.py [--key KEY] <提示词> [选项]")
        print('示例: python image_generate.py "一只猫咪在草地上玩耍，写实风格"')
        print('      python image_generate.py "科技感壁纸，蓝色渐变" --size 2')
        print('      python image_generate.py "新年海报" --size 4 --output ~/Desktop')
        print()
        print("选项:")
        print("  --size <1-5>      宽高比：1=1:1(默认) 2=16:9 3=4:3 4=3:4 5=9:16")
        print("  --output <目录>   图片保存目录（默认：output/）")
        print("  --no-download     仅返回链接，不下载图片")
        print("  --key <KEY>       临时传入 API Key")
        print(f"\n免费申请 API Key: {REGISTER_URL}")
        sys.exit(1)

    parsed = parse_args(args)
    if parsed["error"]:
        print(parsed["error"])
        sys.exit(1)

    api_key = load_api_key(parsed["cli_key"])
    if not api_key:
        print("❌ 未找到 API Key，请通过以下方式之一配置：")
        print("   1. 环境变量: export JUHE_IMAGE_KEY=your_api_key")
        print("   2. .env 文件: 在脚本目录创建 .env，写入 JUHE_IMAGE_KEY=your_api_key")
        print("   3. 命令行参数: python image_generate.py --key your_api_key <提示词>")
        print(f"\n免费申请 Key: {REGISTER_URL}")
        sys.exit(1)

    prompt = parsed["prompt"]
    size = parsed["size"]
    size_label = SIZE_MAP[size]
    no_download = parsed["no_download"]
    model = parsed["model"]

    if parsed["output"]:
        output_dir = Path(parsed["output"]).expanduser().resolve()
    else:
        output_dir = Path(__file__).parent / "output"

    print(f"\n🎨 开始生成图像...")
    print(f"   提示词: {prompt[:80]}{'...' if len(prompt) > 80 else ''}")
    print(f"   尺寸比例: {size_label}")
    print()

    result = generate_image(prompt=prompt, api_key=api_key, size=size, model=model)

    if not result["success"]:
        print(f"❌ 图像生成失败: {result['error']}")
        sys.exit(1)

    image_url = result["image_url"]
    order_id = result["order_id"]

    print("✅ 图像生成成功！")
    if order_id:
        print(f"   订单号: {order_id}")
    print(f"   在线链接: {image_url}")
    print(f"   ⚠️  链接有效期为 24 小时，请及时下载保存")

    if not no_download:
        print(f"\n📥 正在下载图片...")
        save_path = download_image(image_url, output_dir)
        if save_path:
            print(f"   本地文件: {save_path}")
        else:
            print(f"   下载失败，请手动访问上方链接保存图片")
    else:
        print("\n（已跳过下载，请手动访问链接保存图片）")

    print()


if __name__ == "__main__":
    main()
