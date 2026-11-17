#!/usr/bin/env python3
"""检查营销版面审核脚本的本地依赖和百度 OCR 配置。"""

import argparse
import os
import shutil
import socket
import sys
import tempfile
from pathlib import Path


def reexec_with_skill_venv():
    local_python = Path(__file__).resolve().parent.parent / ".venv" / "bin" / "python"
    if os.environ.get("MARKETING_REVIEW_DEBUG_REEXEC") == "1":
        print(f"reexec debug: current={sys.executable}", file=sys.stderr)
        print(f"reexec debug: local={local_python}", file=sys.stderr)
        print(f"reexec debug: exists={local_python.exists()}", file=sys.stderr)
        print(f"reexec debug: flag={os.environ.get('MARKETING_REVIEW_VENV_REEXEC')}", file=sys.stderr)
    if os.environ.get("MARKETING_REVIEW_VENV_REEXEC") == "1" or not local_python.exists():
        return
    if Path(sys.executable) == local_python:
        return
    env = os.environ.copy()
    env["MARKETING_REVIEW_VENV_REEXEC"] = "1"
    env.pop("__PYVENV_LAUNCHER__", None)
    os.execve(str(local_python), [str(local_python), str(Path(__file__).resolve()), *sys.argv[1:]], env)


reexec_with_skill_venv()


FONT_CANDIDATES = [
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/Library/Fonts/Arial Unicode.ttf",
]


def check_import(module_name):
    try:
        __import__(module_name)
        return True, ""
    except Exception as exc:
        return False, str(exc)


def load_cjk_font(size):
    from PIL import ImageFont

    for font_path in FONT_CANDIDATES:
        if Path(font_path).exists():
            try:
                return ImageFont.truetype(font_path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def env_status():
    has_token = bool(os.environ.get("BAIDU_ACCESS_TOKEN", "").strip())
    has_key_pair = bool(os.environ.get("BAIDU_API_KEY", "").strip() and os.environ.get("BAIDU_SECRET_KEY", "").strip())
    return has_token, has_key_pair


def classify_error(exc):
    message = str(exc)
    if "Could not resolve host" in message or "nodename nor servname" in message:
        return "网络/DNS 解析失败，不是 key 缺失。请检查代理、DNS 或 OpenClaw gateway 的网络环境。"
    if "invalid_client" in message or "access_denied" in message or "error_code" in message:
        return "百度 OCR 返回接口错误，请检查 API Key/Secret Key、服务是否开通和额度。"
    return "请根据上面的原始错误继续排查。"


def main():
    parser = argparse.ArgumentParser(description="检查自动审核脚本依赖和百度 OCR 配置")
    parser.add_argument("--deps-only", action="store_true", help="只检查 Python 依赖，不要求 OCR key")
    parser.add_argument("--live", action="store_true", help="实际调用一次百度 OCR，验证 key 和网络")
    args = parser.parse_args()

    checks = [
        ("Pillow", "PIL"),
        ("OpenCV", "cv2"),
        ("NumPy", "numpy"),
    ]
    ok = True
    print(f"Python: {sys.executable}")
    print(f"工作目录: {Path.cwd()}")
    if os.environ.get("OPENCLAW_SHELL"):
        print(f"OpenClaw运行标记: {os.environ.get('OPENCLAW_SHELL')}")
    print(f"curl: {shutil.which('curl') or '未找到'}")
    try:
        print(f"aip.baidubce.com DNS: {socket.gethostbyname('aip.baidubce.com')}")
    except Exception as exc:
        print(f"aip.baidubce.com DNS: 失败 ({exc})")
    print("")
    print("依赖检查:")
    for label, module_name in checks:
        passed, error = check_import(module_name)
        print(f"- {label}: {'OK' if passed else '缺失'}")
        if not passed:
            print(f"  {error}")
            ok = False

    has_token, has_key_pair = env_status()
    print("\n百度 OCR 配置:")
    print(f"- BAIDU_ACCESS_TOKEN: {'已配置' if has_token else '未配置'}")
    print(f"- BAIDU_API_KEY + BAIDU_SECRET_KEY: {'已配置' if has_key_pair else '未配置'}")
    if not args.deps_only and not (has_token or has_key_pair):
        ok = False
        print("  请配置 BAIDU_API_KEY/BAIDU_SECRET_KEY，或直接配置 BAIDU_ACCESS_TOKEN。")

    if args.live and ok:
        from PIL import Image, ImageDraw

        script_dir = Path(__file__).resolve().parent
        if str(script_dir) not in sys.path:
            sys.path.insert(0, str(script_dir))
        from ocr_localize import ocr_with_baiduocr

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp_path = Path(tmp.name)
        try:
            image = Image.new("RGB", (760, 220), "white")
            draw = ImageDraw.Draw(image)
            font = load_cjk_font(58)
            draw.text((36, 70), "品类领导者 100%优质乳蛋白", fill=(0, 0, 0), font=font)
            image.save(tmp_path)
            regions, source = ocr_with_baiduocr(str(tmp_path))
            print("\n百度 OCR 实测:")
            print(f"- 接口: {source}")
            print(f"- 识别区域: {len(regions)}")
            if regions:
                sample = " / ".join(region.get("text", "") for region in regions[:3])
                print(f"- 识别样例: {sample}")
            if not regions:
                ok = False
                print("  已连通，但测试图片没有识别到文字。")
        except Exception as exc:
            ok = False
            print("\n百度 OCR 实测: 失败")
            print(f"  {exc}")
            print(f"  诊断: {classify_error(exc)}")
        finally:
            try:
                tmp_path.unlink()
            except OSError:
                pass

    print("\n结果:", "可运行" if ok else "需要处理上面的失败项")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
