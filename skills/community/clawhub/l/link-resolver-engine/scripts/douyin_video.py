#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Skill Name: link-resolver-engine
Author: 王岷瑞 / https://github.com/wangminrui2022
License: Apache License
Description: 这段代码是一个功能完备的 抖音（Douyin）无水印视频解析与下载工具。
它结合了自动化浏览器（Playwright）和轻量级请求（Requests）两种策略，旨在从抖音链接中提取最高画质的无水印视频地址并保存到本地。
以下是该代码的核心功能和技术亮点描述：

1. 核心功能
    短链接解析：能够将抖音分享的短链接（v.douyin.com）还原为原始的长 URL。
    无水印提取：通过解析视频接口数据，获取不带水印的视频直链。
    高质量选择：代码会遍历视频比特率（Bitrate），优先选择画质最高的资源。
    自动化下载：支持带 Referer 防盗链校验的流式下载，确保视频能成功写入本地。
    环境自适应：内置了自动安装依赖（pip）和浏览器内核（chromium）的逻辑。

2. 技术方案
    代码采用了 “双轨制” 解析方案，提高了解析的成功率：
        方案 A：桌面端自动化解析 (get_douyin_no_wm)
        技术栈：Playwright + playwright-stealth。
        原理：启动一个无头浏览器模拟真实用户访问。使用 Stealth 插件 绕过抖音的反爬虫检测。
    核心逻辑：
        监听网络响应（page.on("response")），捕获包含视频详情的 JSON 接口（如 aweme/detail）。
        通过模拟鼠标滚轮滑动触发页面加载。
        从响应数据中提取 url_list，并将 playwm（带水印）替换为 play（无水印）。
    方案 B：移动端轻量级解析 (download_douyin_video_mobile)
    技术栈：Requests + Regex (正则表达式)。
    原理：模拟 iPhone 用户代理（User-Agent）访问移动版分享页面。
    核心逻辑：
        直接请求页面并解析 HTML 源码。
        利用正则从 window._ROUTER_DATA 或 HTML 标签中提取视频地址。
        这种方法不需要启动浏览器，速度更快，适合简单场景。

3. 代码结构分解
    依赖管理：使用 ensure_package 在运行时动态安装 playwright、requests 等库，减少了手动配置环境的麻烦。
    日志系统：集成 LoggerManager，全程记录解析进度、错误信息和下载状态。
    健壮性设计：
    异常处理：在浏览器操作和文件下载处使用了 try-except。
    超时控制：设置了合理的 timeout，防止程序因网络问题永久卡死。
    文件管理：自动创建 downloads 目录，并以时间戳或视频 ID 命名文件防止冲突。    
"""


import json
from pathlib import Path
import subprocess
import sys
import re
import time
import ensure_package
from datetime import datetime
from config import MODEL_DIR, SKILL_ROOT, VENV_DIR
import os  # 用于跨平台换行符）
from logger_manager import LoggerManager
ensure_package.pip("requests")  
ensure_package.pip("playwright")  
ensure_package.pip("tf-playwright-stealth")
ensure_package.pip("yt-dlp")
# 安装 chromium 浏览器
subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
import requests
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync  # tf-playwright-stealth 版本

logger = LoggerManager.setup_logger(logger_name="link-resolver-engine")

def get_douyin_no_wm(raw_url: str) -> str | None:
    """返回抖音最高画质无水印直链（稳定版）"""
    match = re.search(r'(?:modal_id=|/video/|douyin\.com/)(?P<id>\d{19})', raw_url)
    if not match:
        logger.error("❌ 未找到视频 ID")
        return None

    video_id = match.group("id")
    clean_url = f"https://www.douyin.com/video/{video_id}"
    logger.info(f"✅ 正在解析: {clean_url}")

    result = {"url": None}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            locale="zh-CN",
        )
        page = context.new_page()
        stealth_sync(page)

        def handle_response(response):
            if any(k in response.url for k in ["aweme/detail", "item/detail"]):
                try:
                    data = response.json()
                    aweme = (
                        data.get("aweme_detail")
                        or (data.get("item_list") or [{}])[0]
                        or data.get("aweme")
                    )
                    if not aweme:
                        return

                    video = aweme.get("video") or {}
                    bit_rates = video.get("bit_rate") or []

                    if bit_rates:
                        # 优先最高比特率（这就是 SnapAny 风格的高质量来源）
                        best = max(bit_rates, key=lambda x: x.get("bit_rate", 0))
                        url_list = best.get("play_addr", {}).get("url_list") or []
                    else:
                        url_list = (video.get("play_addr") or {}).get("url_list") or []

                    if url_list:
                        no_wm_url = url_list[0].replace("playwm", "play")
                        result["url"] = no_wm_url
                except:
                    pass

        page.on("response", handle_response)

        try:
            page.goto(clean_url, wait_until="domcontentloaded", timeout=45000)
            time.sleep(2.5)
            for _ in range(6):
                page.mouse.wheel(0, 600)
                time.sleep(1.2)
            time.sleep(3)
        except Exception as e:
            logger.error(f"加载异常: {e}")
        finally:
            browser.close()

    if result["url"]:
        logger.info("\n🎉 最高画质无水印直链（直接复制）：")
        logger.info(result["url"])
        logger.info("\n下载命令（推荐在 CMD/PowerShell 中运行）：")
        logger.info(f'curl -H "Referer: https://www.douyin.com/" -H "User-Agent: Mozilla/5.0" -o "抖音_{video_id}.mp4" "{result["url"]}"')
        return result["url"]
    else:
        return None

def download_douyin_video(no_wm_url: str, filename: str = None, download_dir: str = None) -> bool:
    """带 Referer 下载（支持自定义下载目录）"""
    
    if not no_wm_url:
        logger.info("❌ 没有有效链接")
        return False

    # ==================== 处理下载目录 ====================
    if download_dir is None:
        download_dir = os.path.join(os.getcwd(), "downloads")

    os.makedirs(download_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # ==================== 处理文件名 ====================
    if filename is None:
        filename = f"douyin_video_{timestamp}.mp4"

    if not filename.endswith(".mp4"):
        filename += ".mp4"

    file_path = os.path.join(download_dir, filename)

    headers = {
        "Referer": "https://www.douyin.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }

    logger.info(f"🚀 开始下载 → {file_path}")

    try:
        r = requests.get(no_wm_url, headers=headers, stream=True, timeout=60)
        r.raise_for_status()

        with open(file_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 512):
                if chunk:
                    f.write(chunk)

        logger.info(f"🎉 下载完成！文件：{file_path}")
        return True

    except Exception as e:
        logger.error(f"❌ 下载失败: {e}")
        return False

def expand_douyin_url(short_url: str):
    """
    展开抖音短链接 (v.douyin.com)
    返回: (bool, url或错误信息)
    """

    # ✅ 匹配抖音短链
    pattern = r'^https?://v\.douyin\.com/[a-zA-Z0-9]+/?(?:\?.*)?$'

    if not re.match(pattern, short_url.strip()):
        return False, "不是有效的抖音短链接 (必须是 v.douyin.com 格式)"

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        # ⚠️ 抖音有时候 HEAD 不稳定，建议 fallback 到 GET
        try:
            response = requests.head(short_url, headers=headers, allow_redirects=True, timeout=10)
            final_url = response.url
        except:
            response = requests.get(short_url, headers=headers, allow_redirects=True, timeout=10)
            final_url = response.url

        return True, final_url

    except Exception as e:
        return False, str(e)
 
def download_douyin_video_mobile(short_url: str, filename: str = None,download_dir: str = "downloads"):
    """
    下载抖音视频
    short_url: 抖音短链接，如 https://v.douyin.com/ezOqxZPY3kc/
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }

    # ---------- 第1步：跟踪短链接，获取完整URL和视频ID ----------
    session = requests.Session()
    response = session.get(short_url, headers=headers, allow_redirects=True, timeout=15)
    full_url = response.url
    logger.info(f"重定向后URL: {full_url}")

    # 从URL中提取视频ID
    video_id_match = re.search(r'/video/(\d+)', full_url)
    if not video_id_match:
        return False, f"无法从URL中提取视频ID: {full_url}"
    video_id = video_id_match.group(1)
    logger.info(f"视频ID: {video_id}")

    # ---------- 第2步：请求移动版页面，获取视频信息 ----------
    mobile_url = f"https://m.douyin.com/share/video/{video_id}/"
    mobile_resp = session.get(mobile_url, headers=headers, timeout=15)
    html = mobile_resp.text

    # ---------- 第3步：从 HTML 中提取视频直链 ----------
    # 方法1：直接在HTML里搜索 playwm URL
    playwm_match = re.search(r'https://aweme\.snssdk\.com/aweme/v1/playwm/\?[^"]+', html)
    # 方法2：从 window._ROUTER_DATA 中提取（更可靠）
    router_match = re.search(r'window\._ROUTER_DATA\s*=\s*({.+?})\s*</script>', html, re.DOTALL)
    video_url = None

    if playwm_match:
        video_url = playwm_match.group(0)
        logger.info(f"方法1找到视频链接: {video_url}")
    elif router_match:
        try:
            router_data = json.loads(router_match.group(1))
            # 沿着嵌套结构找视频URL
            item_list = router_data.get("loaderData", {}).get("video_(id)/page", {}).get("videoInfoRes", {}).get("item_list", [])
            if item_list:
                play_addr = item_list[0].get("video", {}).get("play_addr", {})
                url_list = play_addr.get("url_list", [])
                if url_list:
                    video_url = url_list[0]
                    logger.info(f"方法2找到视频链接: {video_url}")
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"JSON解析失败: {e}")

    if not video_url:
        # 备用：直接从HTML所有https://aweme.snssdk.com链接中找
        all_matches = re.findall(r'https://aweme\.snssdk\.com[^\s"\\]+', html)
        for m in all_matches:
            if "playwm" in m or "play" in m:
                video_url = m
                logger.info(f"备用方法找到: {video_url}")
                break

    if not video_url:
        return False, "无法找到视频下载链接，可能需要登录cookies"

    # ---------- 第4步：清理并补全参数，下载视频 ----------
    # 有些链接可能缺少必要参数，补全一下
    if "line=0" not in video_url:
        video_url = video_url + ("&" if "?" in video_url else "?") + "line=0"

    logger.info(f"最终下载链接: {video_url}")

    # 下载
    video_resp = session.get(video_url, headers=headers, timeout=60, stream=True)
    video_resp.raise_for_status()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if filename is None:
        filename = f"{video_id}_{timestamp}.mp4"

    if not filename.endswith(".mp4"):
        filename += ".mp4"

    # 确保下载目录存在（不存在则自动创建）
    os.makedirs(download_dir, exist_ok=True)
    filepath = download_dir.rstrip("/") + "/" + filename
    with open(filepath, "wb") as f:
        for chunk in video_resp.iter_content(chunk_size=8192):
            f.write(chunk)

    logger.info(f"下载完成: {filepath} ({len(open(filepath,'rb').read())} bytes)")
    return True, filepath