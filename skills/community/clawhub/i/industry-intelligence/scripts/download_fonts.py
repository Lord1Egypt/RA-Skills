#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下载开源中文字体（思源宋体 + 思源黑体）

用法:
    python download_fonts.py

会将字体文件下载到 ../fonts/ 目录：
    - NotoSerifSC-Regular.ttf  （思源宋体，用于正文）
    - NotoSansSC-Bold.ttf      （思源黑体，用于标题）
"""

import os
import sys
import urllib.request
import zipfile
import shutil
from pathlib import Path

# 字体下载源：Google Fonts API
FONT_FAMILIES = {
    "Noto+Serif+SC": {
        "url": "https://fonts.google.com/download?family=Noto+Serif+SC",
        "needed": ["NotoSerifSC-Regular.ttf"],
    },
    "Noto+Sans+SC": {
        "url": "https://fonts.google.com/download?family=Noto+Sans+SC",
        "needed": ["NotoSansSC-Bold.ttf"],
    },
}

# 备用下载源：GitHub notofonts 仓库
FALLBACK_URLS = {
    "NotoSerifSC-Regular.ttf": "https://raw.githubusercontent.com/notofonts/noto-cjk/main/Serif/SubsetOTF/SC/NotoSerifSC-Regular.otf",
    "NotoSansSC-Bold.ttf": "https://raw.githubusercontent.com/notofonts/noto-cjk/main/Sans/SubsetOTF/SC/NotoSansSC-Bold.otf",
}


def get_fonts_dir():
    """获取字体目录路径"""
    script_dir = Path(__file__).resolve().parent
    return script_dir.parent / "fonts"


def download_file(url, dest_path, description=""):
    """下载文件"""
    print(f"  下载中: {description or url}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as response:
            with open(dest_path, "wb") as f:
                shutil.copyfileobj(response, f)
        return True
    except Exception as e:
        print(f"  下载失败: {e}")
        return False


def extract_fonts_from_zip(zip_path, fonts_dir, needed_files):
    """从 ZIP 文件中提取所需字体文件"""
    extracted = []
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            for name in zf.namelist():
                basename = os.path.basename(name)
                if basename in needed_files:
                    # 提取到字体目录
                    target = fonts_dir / basename
                    with zf.open(name) as src, open(target, "wb") as dst:
                        shutil.copyfileobj(src, dst)
                    extracted.append(basename)
                    print(f"  已提取: {basename}")

            # 如果没找到精确文件名，尝试模糊匹配
            if not extracted:
                for name in zf.namelist():
                    basename = os.path.basename(name)
                    if not basename.endswith((".ttf", ".otf")):
                        continue
                    for needed in needed_files:
                        # 匹配不含扩展名的部分
                        needed_stem = needed.rsplit(".", 1)[0]
                        if needed_stem in basename:
                            target = fonts_dir / needed
                            with zf.open(name) as src, open(target, "wb") as dst:
                                shutil.copyfileobj(src, dst)
                            extracted.append(needed)
                            print(f"  已提取: {basename} -> {needed}")
                            break
    except zipfile.BadZipFile:
        print(f"  ZIP 文件损坏: {zip_path}")
    return extracted


def main():
    fonts_dir = get_fonts_dir()
    fonts_dir.mkdir(parents=True, exist_ok=True)
    print(f"字体目录: {fonts_dir}\n")

    all_needed = {}
    for family, info in FONT_FAMILIES.items():
        for f in info["needed"]:
            all_needed[f] = False

    # 检查已存在的字体
    for font_file in all_needed:
        if (fonts_dir / font_file).exists():
            print(f"已存在: {font_file}，跳过")
            all_needed[font_file] = True

    if all(all_needed.values()):
        print("\n所有字体文件已就绪。")
        return

    # 从 Google Fonts 下载
    for family, info in FONT_FAMILIES.items():
        missing = [f for f in info["needed"] if not all_needed[f]]
        if not missing:
            continue

        print(f"\n下载字体族: {family.replace('+', ' ')}")
        zip_path = fonts_dir / f"{family.replace('+', '_')}.zip"

        if download_file(info["url"], zip_path, family.replace("+", " ")):
            extracted = extract_fonts_from_zip(zip_path, fonts_dir, missing)
            for f in extracted:
                all_needed[f] = True
            # 清理 ZIP
            zip_path.unlink(missing_ok=True)

    # 对仍然缺失的字体尝试备用源
    still_missing = [f for f, ok in all_needed.items() if not ok]
    if still_missing:
        print(f"\n尝试备用下载源...")
        for font_file in still_missing:
            if font_file in FALLBACK_URLS:
                target = fonts_dir / font_file
                if download_file(FALLBACK_URLS[font_file], target, font_file):
                    all_needed[font_file] = True

    # 汇总结果
    print("\n" + "=" * 40)
    final_missing = [f for f, ok in all_needed.items() if not ok]
    if final_missing:
        print(f"以下字体未能下载，请手动下载放入 {fonts_dir}：")
        for f in final_missing:
            print(f"  - {f}")
        print("\n手动下载地址：")
        print("  思源宋体: https://fonts.google.com/noto/specimen/Noto+Serif+SC")
        print("  思源黑体: https://fonts.google.com/noto/specimen/Noto+Sans+SC")
        sys.exit(1)
    else:
        print("所有字体下载完成！")
        for f in all_needed:
            print(f"  {fonts_dir / f}")


if __name__ == "__main__":
    main()
