#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Skill Name: link-resolver-engine
Author: 王岷瑞 / https://github.com/wangminrui2022
License: Apache License
Description: 这段代码是一个功能完备的 Bilibili（B站）视频下载工具集。
它提供了两种主要的解析和下载思路：一种是基于原生的 requests 手动解析与合并，另一种是调用成熟的 yt-dlp 库。
以下是代码的详细功能描述和逻辑拆解：
    1. 核心功能概述
        该代码库主要用于处理 B 站视频的链接转换、信息提取和媒体下载。它具备处理“短链接”、获取“无水印（DASH流）地址”以及“音视频自动合并”的能力。
    2. 主要函数解析
        A. 链接还原：expand_bilibili_url
            功能：将 B 站的短链接（如 b23.tv/xxxx）还原为完整的视频详情页 URL。
            逻辑：使用正则表达式验证短链接格式，通过 requests.head 请求获取重定向后的最终地址，避免了下载不必要的页面内容，提高效率。
    
        B. 视频信息解析：get_bilibili_no_wm
            功能：从视频链接中提取 BV 号，并获取视频和音频的分离下载地址（DASH 格式）。
            核心逻辑：正则匹配：提取 URL 中的 bvid。
            获取 CID：访问视频页源码，利用正则提取 cid（弹幕/播放标识符），若源码提取失败则调用 API 备用接口。
            调用 PlayURL 接口：访问 B 站官方接口获取播放地址。它优先尝试获取 DASH 格式（音视频分离，画质更高），如果没有则退而求其次选择 DURL（传统 MP4 格式）。
            最优选择：在返回的多个清晰度中，自动筛选带宽（bandwidth）最高的视频轨和音频轨。     
        
        C. 手动下载与合并：download_bilibili_video_request
            功能：使用 requests 流式下载音视频文件，并利用 ffmpeg 进行合并。
            关键步骤：
            流式下载：通过 stream=True 逐块写入文件，防止大视频占用过多内存。
            FFmpeg 合并：由于 DASH 格式音轨和视轨是分开的，代码调用系统命令 ffmpeg 将两者合成为一个 .mp4 文件，并设置 -movflags +faststart 以优化在线播放。
            容错处理：若 ffmpeg 合并失败，会保留原始视频文件作为备份。     

        D. 自动化工具封装：download_bilibili_video_yt_dlp
            功能：利用专业的开源工具 yt-dlp 进行下载。
            特点：这是一种更稳健的方案。它封装了 yt-dlp 的 API，支持自定义画质参数（format_spec），并能自动处理复杂的重试逻辑和格式转换。    
    3. 技术要点与亮点特性说明
        1、反爬避让模拟了真实的浏览器 User-Agent 和 Referer，并处理了 Accept-Encoding 以避免压缩格式导致的解码错误。
        2、目录管理自动创建 downloads 文件夹，并使用时间戳防止文件名冲突，同时对标题中的特殊非法字符（如 \/:*?）进行过滤。
        3、多方案互补既有轻量级的 requests 方案（无需重型依赖），也有强力的 yt-dlp 方案作为保障。
        4、日志追踪接入了 LoggerManager，对每一个关键步骤（获取 CID、下载、合并）都有详细的日志记录，方便排查问题。       
"""

from pathlib import Path
import subprocess
import sys
import re
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
import yt_dlp
from yt_dlp.utils import DownloadError  # 专门捕获 yt_dlp 下载错误

logger = LoggerManager.setup_logger(logger_name="link-resolver-engine")

def get_bilibili_no_wm(raw_url: str) -> dict | None:
    """
    B站视频下载地址提取器（纯 requests 版，避开 Playwright 解码问题）
    """
    match = re.search(r'(BV[0-9a-zA-Z]{10})', raw_url)
    if not match:
        logger.error("❌ 未找到 BV 号")
        return None

    bvid = match.group(1)
    logger.info(f"✅ 处理 B站视频: {bvid}")

    # 通用 Headers（模拟真实浏览器）
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "Referer": "https://www.bilibili.com/",
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",   # 避免 br 问题
        "Accept-Language": "zh-CN,zh;q=0.9",
    }

    session = requests.Session()
    session.headers.update(headers)

    try:
        # 第一步：访问页面获取必要的 cookie 和 aid（cid）
        page_url = f"https://www.bilibili.com/video/{bvid}"
        resp = session.get(page_url, timeout=15)
        resp.raise_for_status()

        # 简单提取 cid（从页面源码中找）
        cid_match = re.search(r'"cid":(\d+)', resp.text)
        if not cid_match:
            logger.info("⚠️ 无法提取 cid，尝试备用方式")
            # 备用：调用接口获取视频信息
            info_url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
            info_resp = session.get(info_url, timeout=10)
            data = info_resp.json().get("data", {})
            cid = data.get("cid") or (data.get("pages") or [{}])[0].get("cid")
        else:
            cid = cid_match.group(1)

        if not cid:
            logger.info("❌ 无法获取 cid")
            return None

        # 第二步：调用 playurl 接口（带简单 wbi 参数模拟）
        play_url = f"https://api.bilibili.com/x/player/wbi/playurl?bvid={bvid}&cid={cid}&qn=64&fnval=4048&fourk=1"
        
        play_resp = session.get(play_url, timeout=15)
        play_resp.raise_for_status()
        json_data = play_resp.json()

        if json_data.get("code") != 0:
            logger.info(f"❌ 接口返回错误: {json_data.get('message')}")
            return None

        data = json_data.get("data", {})
        dash = data.get("dash") or {}

        result = {
            "video_url": None,
            "audio_url": None,
            "title": data.get("title") or "bilibili_video",
            "quality": None
        }

        if dash and dash.get("video"):
            video_tracks = dash["video"]
            # 优先最高画质
            best_video = max(video_tracks, key=lambda x: x.get("bandwidth", 0))
            result["video_url"] = best_video.get("base_url") or best_video.get("baseUrl")
            result["quality"] = f"{best_video.get('height', 0)}p"

            audio_tracks = dash.get("audio") or []
            if audio_tracks:
                best_audio = max(audio_tracks, key=lambda x: x.get("bandwidth", 0))
                result["audio_url"] = best_audio.get("base_url") or best_audio.get("baseUrl")

        elif data.get("durl"):
            durls = data.get("durl") or []
            if durls:
                result["video_url"] = durls[0].get("url")
                result["quality"] = "720p"

        if result["video_url"]:
            logger.info(f"✅ 成功获取 B站地址！质量: {result['quality']}")
            return result
        else:
            logger.info("⚠️ 未找到有效播放地址")
            return None

    except Exception as e:
        logger.error(f"❌ 请求异常: {e}")
        return None

def download_bilibili_video_request(play_info: dict, filename: str = None, download_dir: str = None) -> bool:
    """
    下载 B站视频 + 自动合并音频
    支持自定义下载目录（默认 ./downloads）
    """

    if not play_info or not play_info.get("video_url"):
        logger.info("❌ 没有有效视频地址")
        return False

    # ==================== 目录处理 ====================
    if download_dir is None:
        download_dir = os.path.join(os.getcwd(), "downloads")

    os.makedirs(download_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # ==================== 文件名处理 ====================
    if filename is None:
        safe_title = re.sub(r'[\\/:*?"<>|]', '_', play_info.get('title', 'bilibili_video'))
        filename = f"{safe_title}_{timestamp}.mp4"

    if not filename.endswith(".mp4"):
        filename += ".mp4"

    final_file = os.path.join(download_dir, filename)

    # 临时文件也放目录里（避免污染当前目录）
    temp_video = os.path.join(download_dir, f"temp_video_{timestamp}.mp4")
    temp_audio = os.path.join(download_dir, f"temp_audio_{timestamp}.m4a") if play_info.get("audio_url") else None

    headers = {
        "Referer": "https://www.bilibili.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; Win64; x64) AppleWebKit/537.36",
    }

    video_url = play_info["video_url"]
    audio_url = play_info.get("audio_url")

    logger.info(f"🚀 开始下载: {play_info.get('title', 'bilibili_video')}")
    logger.info(f"📁 保存目录: {download_dir}")

    try:
        # ==================== 下载视频 ====================
        logger.info("下载视频轨...")
        r = requests.get(video_url, headers=headers, stream=True, timeout=120)
        r.raise_for_status()
        with open(temp_video, "wb") as f:
            for chunk in r.iter_content(chunk_size=512 * 1024):
                f.write(chunk)

        # ==================== 下载音频 ====================
        if audio_url:
            logger.info("下载音频轨...")
            r = requests.get(audio_url, headers=headers, stream=True, timeout=120)
            r.raise_for_status()
            with open(temp_audio, "wb") as f:
                for chunk in r.iter_content(chunk_size=512 * 1024):
                    f.write(chunk)

            # ==================== 合并 ====================
            logger.info("正在合并音视频（ffmpeg）...")

            cmd = [
                "ffmpeg", "-y",
                "-i", temp_video,
                "-i", temp_audio,
                "-c:v", "copy",
                "-c:a", "copy",
                "-movflags", "+faststart",
                final_file
            ]

            result = subprocess.run(
                cmd,
                capture_output=False,
                text=False,
                timeout=180
            )

            if result.returncode == 0:
                logger.info(f"🎉 合并完成：{final_file}")
            else:
                logger.info(f"⚠️ ffmpeg 失败: {result.returncode}")
                if os.path.exists(temp_video):
                    fallback = final_file.replace(".mp4", "_video_only.mp4")
                    os.rename(temp_video, fallback)
                return False

            # 清理
            for temp in [temp_video, temp_audio]:
                if temp and os.path.exists(temp):
                    os.remove(temp)

        else:
            # 无音频
            os.rename(temp_video, final_file)
            logger.info(f"🎉 下载完成：{final_file}")

        return True

    except Exception as e:
        logger.info(f"❌ 异常: {e}")
        for temp in [temp_video, temp_audio]:
            if temp and os.path.exists(temp):
                try:
                    os.remove(temp)
                except:
                    pass
        return False
    

def expand_bilibili_url(short_url):
    # 正则表达式验证是否为有效的 Bilibili 短链接（b23.tv）
    # 支持 http/https、可选 www. 前缀，路径为字母、数字、下划线、连字符组成（长度至少 4 位）
    # 示例：https://b23.tv/ReXDyVO、https://b23.tv/BV1xx...、https://b23.tv/av123...
    pattern = r'^https?://(?:www\.)?b23\.tv/[a-zA-Z0-9_-]{4,}(?:\?.*)?$'
    
    if not re.match(pattern, short_url.strip()):
        return False, "不是有效的Bilibili短链接 (必须是 b23.tv 格式)"
    
    try:
        # 使用 head 请求通常比 get 更快，因为不需要下载页面内容
        # allow_redirects=True 会自动追踪重定向
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.head(short_url, headers=headers, allow_redirects=True, timeout=10)
        
        # 最终的 URL 存储在 response.url 中
        return True,response.url
    except Exception as e:
        return False, f"{str(e)}"
    
def download_bilibili_video_yt_dlp(
    url: str,
    filename_prefix: str = None,
    download_dir: str = "downloads",
    format_spec: str = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
) -> tuple[bool, str]:
    """
    下载 Bilibili 视频（已封装，失败时返回结果，支持指定下载目录）
    
    返回值:
        (success: bool, message: str)
        - 成功时: (True, "下载成功！文件已保存为: xxx.mp4")
        - 失败时: (False, "下载失败: 具体错误信息")
    
    参数:
        url (str): 视频链接（支持完整 URL 或 b23.tv 短链接）
        filename_prefix (str): 文件名前缀，默认 "bilibili_video"
        add_timestamp (bool): 是否在文件名中添加时间戳（默认 True）
        download_dir (str): 下载目录，默认 "downloads"（相对当前工作目录）
                         如果目录不存在会自动创建
        format_spec (str): 视频格式选择
    
    用法示例:
        # 默认用法（下载到 ./downloads/ 目录，文件名带时间戳）
        success, msg = download_bilibili_video_yt_dlp("https://www.bilibili.com/video/BV1GYXKBzEvM/")
        # 生成的文件示例: download/bilibili_video_20260331_200512.mp4
        # 自定义下载目录
        success, msg = download_bilibili_video_yt_dlp(url, download_dir="F:/my_videos")
        # 自定义前缀 + 不加时间戳 + 指定目录
        success, msg = download_bilibili_video_yt_dlp(url, filename_prefix="我的视频", add_timestamp=False, download_dir="/absolute/path/to/folder")
    """
    # 确保下载目录存在（不存在则自动创建）
    os.makedirs(download_dir, exist_ok=True)
    
    # 生成文件名部分
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if filename_prefix is None:
        filename_part = f"bilibili_video_{timestamp}.mp4"
    else:
        filename_part = f"{filename_prefix}_{timestamp}.%(ext)s"
    # 完整输出模板（目录 + 文件名）
    output_template = os.path.join(download_dir, filename_part)
    
    ydl_opts = {
        'outtmpl': output_template,
        'format': format_spec,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # 下载成功，返回完整文件路径（假设为 mp4）
        actual_filename = output_template.replace('.%(ext)s', '.mp4')
        logger.info(f"下载成功: {actual_filename}")
        return True, f"下载成功！文件已保存为: {actual_filename}"
    
    except DownloadError as e:
        logger.error(f"下载失败（yt_dlp 错误）: {str(e)}")
        return False, f"{str(e)}"
    except Exception as e:  # 捕获其他意外错误
        logger.error(f"下载失败（未知错误）: {str(e)}")
        return False, f"{str(e)}"
    