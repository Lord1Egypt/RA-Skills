#!/usr/bin/env python3
"""
LegionSpace 大群空间版本查询工具
查询 com.tongfudun.legion 在 7 大应用商店的最新版本号。
"""

import os
import sys
import json
import re
import time
import requests
from datetime import datetime

# ── 强制关闭代理 ──────────────────────────────────────────────
os.environ["no_proxy"] = "*"
os.environ["NO_PROXY"] = "*"


def strip_version(v: str) -> str:
    """清洗版本号字符串"""
    if not v:
        return "N/A"
    v = v.strip()
    # 去掉前缀非数字字符（如 "V", "v"）
    v = re.sub(r"^[Vv]\.?\s*", "", v)
    return v if v else "N/A"


# ── 1. Apple App Store ─────────────────────────────────────────
def check_apple() -> str:
    """通过 iTunes Lookup API 查询"""
    try:
        url = "https://itunes.apple.com/cn/lookup?bundleId=com.tongfudun.legion"
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        data = r.json()
        if data.get("resultCount", 0) > 0:
            return strip_version(data["results"][0].get("version", "N/A"))
        return "N/A (未上架)"
    except Exception as e:
        return f"错误: {e}"


# ── 2. Tencent MyApp (应用宝) ──────────────────────────────────
def check_myapp() -> str:
    """通过应用宝网页抓取"""
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(
                "https://sj.qq.com/appdetail/com.tongfudun.legion",
                wait_until="domcontentloaded",
                timeout=30000,
            )
            page.wait_for_timeout(3000)
            html = page.content()
            browser.close()

        # 尝试多种模式匹配版本号
        patterns = [
            r'版本[:：]\s*([\d.]+)',
            r'version["\s:=]+([\d.]+)',
            r'"versionName"\s*:\s*"([\d.]+)"',
        ]
        for pat in patterns:
            m = re.search(pat, html, re.IGNORECASE)
            if m:
                return strip_version(m.group(1))
        return "N/A (未找到版本号)"
    except ImportError:
        return "N/A (playwright 未安装)"
    except Exception as e:
        return f"错误: {e}"


# ── 3. Xiaomi (小米) ───────────────────────────────────────────
def check_xiaomi() -> str:
    """通过小米应用商店网页抓取"""
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(
                "https://app.mi.com/details?id=com.tongfudun.legion",
                wait_until="domcontentloaded",
                timeout=30000,
            )
            page.wait_for_timeout(3000)
            html = page.content()
            browser.close()

        patterns = [
            r'版本[:：]\s*([\d.]+)',
            r'version["\s:=]+([\d.]+)',
            r'"versionName"\s*:\s*"([\d.]+)"',
        ]
        for pat in patterns:
            m = re.search(pat, html, re.IGNORECASE)
            if m:
                return strip_version(m.group(1))
        return "N/A (未找到版本号)"
    except ImportError:
        return "N/A (playwright 未安装)"
    except Exception as e:
        return f"错误: {e}"


# ── 4. vivo ────────────────────────────────────────────────────
def check_vivo() -> str:
    """通过 vivo 应用商店网页抓取"""
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(
                "https://h5.appstore.vivo.com.cn/#/appinfo?appId=com.tongfudun.legion",
                wait_until="domcontentloaded",
                timeout=40000,
            )
            page.wait_for_timeout(5000)
            html = page.content()
            browser.close()

        patterns = [
            r'版本[:：]\s*([\d.]+)',
            r'version["\s:=]+([\d.]+)',
            r'"versionName"\s*:\s*"([\d.]+)"',
        ]
        for pat in patterns:
            m = re.search(pat, html, re.IGNORECASE)
            if m:
                return strip_version(m.group(1))
        return "N/A (未找到版本号)"
    except ImportError:
        return "N/A (playwright 未安装)"
    except Exception as e:
        return f"错误: {e}"


# ── 5. Honor (荣耀) ────────────────────────────────────────────
def check_honor() -> str:
    """通过荣耀应用商店网页抓取"""
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(
                "https://app.honor.com/appDetail/com.tongfudun.legion",
                wait_until="domcontentloaded",
                timeout=40000,
            )
            page.wait_for_timeout(5000)
            html = page.content()
            browser.close()

        patterns = [
            r'版本[:：]\s*([\d.]+)',
            r'version["\s:=]+([\d.]+)',
            r'"versionName"\s*:\s*"([\d.]+)"',
        ]
        for pat in patterns:
            m = re.search(pat, html, re.IGNORECASE)
            if m:
                return strip_version(m.group(1))
        return "N/A (未找到版本号)"
    except ImportError:
        return "N/A (playwright 未安装)"
    except Exception as e:
        return f"错误: {e}"


# ── 6. Huawei AppGallery (华为) ─────────────────────────────────
def check_huawei() -> str:
    """通过华为应用商店网页抓取"""
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(
                "https://appgallery.huawei.com/app/C109776267",
                wait_until="domcontentloaded",
                timeout=40000,
            )
            page.wait_for_timeout(5000)
            html = page.content()
            browser.close()

        patterns = [
            r'版本[:：]\s*([\d.]+)',
            r'version["\s:=]+([\d.]+)',
            r'"versionName"\s*:\s*"([\d.]+)"',
        ]
        for pat in patterns:
            m = re.search(pat, html, re.IGNORECASE)
            if m:
                return strip_version(m.group(1))
        return "N/A (未找到版本号)"
    except ImportError:
        return "N/A (playwright 未安装)"
    except Exception as e:
        return f"错误: {e}"


# ── 7. OPPO ────────────────────────────────────────────────────
def check_oppo() -> str:
    """通过 OPPO 软件商店网页抓取（PC 端可能受限）"""
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(
                "https://store.oppo.com/app/com.tongfudun.legion",
                wait_until="domcontentloaded",
                timeout=30000,
            )
            page.wait_for_timeout(3000)
            html = page.content()
            browser.close()

        patterns = [
            r'版本[:：]\s*([\d.]+)',
            r'version["\s:=]+([\d.]+)',
            r'"versionName"\s*:\s*"([\d.]+)"',
        ]
        for pat in patterns:
            m = re.search(pat, html, re.IGNORECASE)
            if m:
                return strip_version(m.group(1))
        return "N/A (PC端限制，仅手机端可访问)"
    except ImportError:
        return "N/A (playwright 未安装)"
    except Exception as e:
        return f"错误: {e}"


# ── 主流程 ─────────────────────────────────────────────────────
STORE_HANDLERS = [
    ("Apple App Store", check_apple),
    ("Tencent MyApp (应用宝)", check_myapp),
    ("Xiaomi (小米)", check_xiaomi),
    ("vivo", check_vivo),
    ("Honor (荣耀)", check_honor),
    ("Huawei AppGallery (华为)", check_huawei),
    ("OPPO", check_oppo),
]


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, "LegionSpace_versions.txt")

    results = []
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("=" * 60)
    print("  LegionSpace 大群空间版本查询")
    print(f"  查询时间: {now_str}")
    print(f"  包名: com.tongfudun.legion")
    print("=" * 60)
    print()

    for i, (name, handler) in enumerate(STORE_HANDLERS, 1):
        print(f"[{i}/7] 正在查询 {name} ...", flush=True)
        version = handler()
        results.append((name, version))
        print(f"  → {version}")
        print()

    print("=" * 60)
    print("  查询结果汇总")
    print("=" * 60)

    lines = []
    lines.append(f"LegionSpace 大群空间版本查询报告")
    lines.append(f"查询时间: {now_str}")
    lines.append(f"包名: com.tongfudun.legion")
    lines.append("=" * 60)
    lines.append("")

    for name, version in results:
        line = f"  {name:35s} : {version}"
        print(line)
        lines.append(line.strip())

    lines.append("")
    lines.append("=" * 60)
    lines.append(f"报告生成时间: {now_str}")

    # 保存到文件
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print()
    print(f"报告已保存到: {output_file}")
    return results


if __name__ == "__main__":
    main()
