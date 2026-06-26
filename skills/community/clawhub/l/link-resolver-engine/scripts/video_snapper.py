#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Skill Name: link-resolver-engine
Author: 王岷瑞 / https://github.com/wangminrui2022
License: Apache License
Description: 这段代码实现了一个高性能、高鲁棒性的多平台视频解析与下载引擎，专门针对哔哩哔哩 (Bilibili) 和 抖音 (Douyin) 进行了深度优化。
它不仅是一个简单的下载工具，更像是一个具备“自我修复”和“多级备选方案”的智能工作流。
核心功能亮点
1. 自动化环境配置 (ensure_ffmpeg)
    零配置启动：自动检测系统是否安装了 FFmpeg。如果没有，它会自动从对应的操作系统镜像源（Windows/Linux/macOS）下载便携版。
    静默安装：通过 subprocess 模拟交互输入，实现无人值守的自动化部署
    动态加载：下载完成后自动刷新模块路径并强制关联 pydub 等音频处理库。
2. 智能双模下载策略
    代码为每个平台都设计了“首选+备用”的阶梯式下载逻辑，确保极高的成功率：
    Bilibili 模块 (download_bilibili_video_smart)
        方案 A (yt-dlp)：优先使用最成熟的开源工具，支持高码率和复杂格式。
        方案 B (解析直链)：若 A 失败，则自动展开 b23.tv 短链，通过 API 获取无水印直链，利用 requests 进行分段下载并合成。
    抖音 模块 (download_douyin_video_auto)
        方案 A (PC高画质)：尝试获取最高清晰度的无水印原片。
        方案 B (移动端轻量级)：若高画质解析受阻，立即切换至兼容性更强的移动端解析模式，确保“至少能下到”。
3. 智能平台识别 (identify_platform_with_redirect)
    防屏蔽追踪：通过 requests.head 追踪 URL 的最终重定向地址，能够精准识别各种短链接（如 b23.tv 或 v.douyin.com）背后的真实平台。
"""

import os
import argparse
import subprocess
from urllib.parse import urlparse
from pathlib import Path
import env_manager
from datetime import datetime
from config import MODEL_DIR, SKILL_ROOT, VENV_DIR
from logger_manager import LoggerManager
import bilibili_video
import douyin_video
import ensure_package
ensure_package.pip("requests")
ensure_package.pip("ffmpeg-downloader")
ensure_package.pip("pydub", "pydub", "AudioSegment")
from pydub import AudioSegment
import ffmpeg_downloader as ffdl
import importlib
import requests

logger = LoggerManager.setup_logger(logger_name="link-resolver-engine")

def ensure_ffmpeg():
    """自动检测 + 下载 ffmpeg（已彻底修复 --quiet 错误 + 更稳定）"""
    # 关键修复：判断 None + 移除 --quiet
    if ffdl.ffmpeg_path is None or not os.path.exists(ffdl.ffmpeg_path):
        logger.info("⚠️  未检测到 ffmpeg，正在自动下载便携版到本地（只需一次，约 100-200MB）...")
        logger.info("   下载来源：Windows=gyan.dev | Linux=johnvansickle | macOS=evermeet")
        
        # 🔥 关键：自动输入 Y（默认 yes），彻底无交互
        logger.info("   自动确认下载中...")
        subprocess.run(["ffdl", "install"], input="Y\n", text=True, check=True)
        
        # 下载完后刷新模块
        importlib.reload(ffdl)
        
        logger.info("✅ 下载 + 安装完成！") 
        #C:\Users\Administrator\AppData\Local\ffmpegio\ffmpeg-downloader\ffmpeg\bin

    # 添加到 PATH + 强制 pydub 使用
    ffdl.add_path()
    AudioSegment.converter = ffdl.ffmpeg_path

    logger.info(f"✅ ffmpeg 已就绪 → {ffdl.ffmpeg_path}")
    return True

def download_bilibili_video_smart(
    url: str,
    filename_prefix: str = None,
    download_dir: str = "downloads",
    format_spec: str = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
) -> tuple[bool, str]:
    """
    智能 B站视频下载方法（一键封装）
    
    流程：
    1. 第一步：优先使用 yt-dlp 下载（最稳定、最快）
    2. 失败 → 第二步：自动展开 b23.tv 短链接 → 获取无水印直链 → requests 下载 + ffmpeg 合并
    3. 两步都失败 → 返回失败提示
    
    返回值：
        (success: bool, message: str)
        成功时：(True, "下载成功！文件已保存为: xxx.mp4")
        失败时：(False, "下载失败: 具体原因")
    
    参数与之前完全一致，方便直接替换原来的调用。
    """
    # ==================== 第一步：优先 yt-dlp ====================
    logger.info("🚀 第一步：尝试使用 yt-dlp 下载...")
    success_yt, msg_yt = bilibili_video.download_bilibili_video_yt_dlp(
        url=url,
        filename_prefix=filename_prefix,
        download_dir=download_dir,
        format_spec=format_spec
    )

    if success_yt:
        return True, msg_yt

    logger.info(f"⚠️ yt-dlp 下载失败: {msg_yt}")
    logger.info("🔄 切换到第二步备用方案（requests + 直链）...")

    # ==================== 第二步：展开短链接 → 获取直链 → requests 下载 ====================
    # 2.1 展开 b23.tv
    expand_ok, expanded_url = bilibili_video.expand_bilibili_url(url)
    if not expand_ok:
        return False, f"短链接展开失败: {expanded_url}，请重试"

    logger.info(f"✅ 短链接已展开: {expanded_url}")

    # 2.2 获取无水印直链
    play_info = bilibili_video.get_bilibili_no_wm(expanded_url)
    if not play_info or not play_info.get("video_url"):
        return False, "获取 B站直链失败，请重试"

    logger.info(f"✅ 已获取直链，质量: {play_info.get('quality', '未知')}")

    # 2.3 执行 requests 下载
    success_request = bilibili_video.download_bilibili_video_request(
        play_info=play_info,
        filename=filename_prefix,
        download_dir=download_dir
    )

    if success_request:
        return True, "下载成功！"
    else:
        return False, "第二步备用下载也失败，请重试"
    

def download_douyin_video_auto(
    url: str,
    filename: str = None,
    download_dir: str = "downloads"
) -> tuple[bool, str]:
    """
    【推荐调用入口】自动双模式抖音无水印视频下载
    下载流程（已按要求切换顺序）：
        1. 第一步：优先尝试高画质模式（短链展开 → 最高画质直链 → 下载）
        2. 第一步失败后 → 第二步：尝试移动端轻量模式下载
        3. 两步均失败 → 返回失败信息

    返回值：(success: bool, result: str)
        成功时：result 为完整文件路径
        失败时：result 为错误提示信息
    """    
    logger.info(f"🚀 开始处理抖音链接: {url}")
    
    # ==================== 第一步：短链展开 → 高画质直链 → 下载 ====================
    logger.info("🔄 第一步：尝试PC高画质下载模式...")
    target_url = url
    
    # 如果是短链接，先展开
    expand_success, expand_result = douyin_video.expand_douyin_url(url)
    if expand_success:
        target_url = expand_result
        logger.info(f"✅ 短链接展开成功 → {target_url}")
    else:
        logger.error(f"❌ 短链接展开失败: {expand_result}")
        # 展开失败仍继续尝试解析原始URL

    logger.info("🔄 获取最高画质无水印直链...")
    no_wm_url = douyin_video.get_douyin_no_wm(target_url)
    if not no_wm_url:
        logger.warning("⚠️ 第一步未能获取无水印直链，切换到移动端轻量模式...")
    else:
        logger.info("✅ 已获取最高画质无水印直链，开始下载...")
        download_success = douyin_video.download_douyin_video(
            no_wm_url=no_wm_url,
            filename=filename,
            download_dir=download_dir
        )
        if download_success:
            # download_douyin_video 内部会打印路径，这里返回实际保存路径（兼容旧逻辑）
            import os
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            final_filename = filename or f"douyin_video_{timestamp}.mp4"
            if not final_filename.endswith(".mp4"):
                final_filename += ".mp4"
            final_path = os.path.join(download_dir, final_filename)
            logger.info("🎉 第一步高画质下载成功！")
            return True, final_path
        else:
            logger.warning("⚠️ 第一步高画质下载失败，切换到移动端轻量模式...")

    # ==================== 第二步：优先移动端轻量下载 ====================
    logger.info("🔄 第二步：尝试移动端轻量下载模式...")
    mobile_success, mobile_result = douyin_video.download_douyin_video_mobile(
        short_url=url,
        filename=filename,
        download_dir=download_dir
    )
    if mobile_success:
        logger.info("🎉 第二步移动端下载成功！")
        return True, mobile_result
    else:
        error_msg = f"❌ 第二步移动端下载也失败: {mobile_result}"
        logger.error(error_msg)
        return False, error_msg

def identify_platform_with_redirect(url: str, timeout=5) -> str:
    try:
        resp = requests.head(url, allow_redirects=True, timeout=timeout)
        final_url = resp.url
    except:
        final_url = url
    
    parsed = urlparse(final_url)
    domain = parsed.netloc.lower()
    
    if any(d in domain for d in ['douyin.com', 'v.douyin', 'iesdouyin.com', 'tiktok.com']):
        return "抖音"
    elif any(d in domain for d in ['b23.tv', 'bilibili.com', 'bili']):
        return "B站"
    return "未知平台"

# 测试一下
if __name__ == "__main__":
    env_manager.check_python_version()
    env_manager.setup_venv()    
    ensure_ffmpeg()
    
    parser = argparse.ArgumentParser(
        description="抖音（Douyin）与哔哩哔哩（Bilibili）高性能、智能、双平台视频链接解析与下载引擎",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument("-u", "--url", type=str, required=True, help="视频链接")
    parser.add_argument("-p", "--filename-prefix", type=str, default=None, help="文件名前缀")
    parser.add_argument("-d", "--download-dir", type=str, default="downloads", help="下载目录")
    parser.add_argument("-f", "--format", type=str, default="bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best", help="yt-dlp 格式")
    
    args = parser.parse_args()
    
    platform = identify_platform_with_redirect(args.url) 
    if platform == "抖音":
        success, result = download_douyin_video_auto(
            url=args.url,
            filename=args.filename_prefix,
            download_dir=args.download_dir
        )
        if success:
            logger.info(f"\n✅ 下载完成！文件路径：{result}")
        else:
            logger.info(f"\n❌ 下载失败：{result}")
    elif platform == "B站":
        success, message = download_bilibili_video_smart(
            url=args.url,
            filename_prefix=args.filename_prefix,
            download_dir=args.download_dir,
            format_spec=args.format
        )
        logger.info("✅ " + message if success else "❌ " + message)
    else:
        logger.info(f"未知:{args.url}")