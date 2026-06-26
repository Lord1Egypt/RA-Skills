#!/usr/bin/env python3
# -*- coding: utf-8, -*-

"""
Skill Name: MP4-To-MP3-Extractor
Author: 王岷瑞/https://github.com/wangminrui2022
License: Apache License
Description: 这段代码是一个基于 Python 的自动化视频转音频（MP4 转 MP3）提取工具。
它不仅实现了核心的转换功能，还集成了一套生产级的环境管理和日志监控机制。
1、该程序的主要任务是遍历指定的源目录，将其中的所有 .mp4 视频文件通过 FFmpeg 工具提取为高质量的 .mp3 音频文件（192kbps），并保持原有的目录结构输出到目标文件夹。
2、鲁棒的日志系统：通过 LoggerManager 实现结构化日志记录，包含任务开始、扫描进度、处理状态及最终汇总，便于无人值守时排查问题。
3、环境自动管理：在执行前调用 env_manager 检查 Python 版本并自动设置虚拟环境（venv），甚至包含 GPU 硬件检测的预处理。
4、递归处理与结构保持：使用 pathlib 模块进行递归扫描（rglob），确保子文件夹中的视频也能被发现，并在目标路径下重建相同的子目录结构。
5、错误容错机制：采用 try-except 捕获单文件处理中的异常，确保某个文件损坏或转换失败时，程序不会崩溃，而是继续处理下一个任务。
6、非阻塞式命令执行：使用 subprocess.run 调用系统级 FFmpeg，并实时捕获错误输出（stderr）以便在日志中记录具体的转换失败原因。
"""

import os
import sys
import subprocess
from pathlib import Path
from logger_manager import LoggerManager
import env_manager
import ensure_package
ensure_package.pip("tqdm", "tqdm")
ensure_package.pip("ffmpeg-downloader")
ensure_package.pip("pydub", "pydub", "AudioSegment")
from pydub import AudioSegment
# 现在添加所有导入语句
from tqdm import tqdm
import ffmpeg_downloader as ffdl
import importlib

# --- 日志系统初始化 ---
logger = LoggerManager.setup_logger(logger_name="mp4-to-mp3-extractor")

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

def extract_audio(src_dir, dest_dir):
    src_path = Path(src_dir).resolve()
    dest_path = Path(dest_dir).resolve()

    logger.info(f"--- 开始任务: 从 {src_path} 提取音频 ---")

    if not src_path.is_dir():
        logger.error(f"源目录不存在: {src_path}")
        sys.exit(1)

    mp4_files = list(src_path.rglob("*.mp4"))
    if not mp4_files:
        logger.warning("扫描完成：未发现任何 .mp4 文件。")
        sys.exit(0)

    logger.info(f"扫描完成，发现 {len(mp4_files)} 个视频文件。目标路径: {dest_path}")

    success = 0
    fail = 0

    # 2. 使用 tqdm 包装循环
    # unit="file" 定义单位，desc 定义前缀
    pbar = tqdm(mp4_files, desc="处理进度", unit="file", ncols=100)

    for mp4_file in pbar:
        rel_path = mp4_file.relative_to(src_path)
        out_file = dest_path / rel_path.with_suffix(".mp3")
        
        # 3. 更新进度条左侧的动态描述（可选，显示当前文件名）
        pbar.set_postfix_str(f"正在处理: {mp4_file.name[:20]}...")
        logger.info(f"正在处理: {mp4_file.name[:50]}...")
        try:
            out_file.parent.mkdir(parents=True, exist_ok=True)
            
            # ✅ 修复后的正确命令（已测试可直接用）
            cmd = [
                "ffmpeg", "-y", "-i", str(mp4_file),
                "-vn",                    # 去除视频流
                "-c:a", "libmp3lame",     # 使用 MP3 编码器
                "-b:a", "192k",           # 192kbps 音质（可改成 128k / 256k）
                str(out_file),
                "-loglevel", "error"
            ]
            
            # 使用 capture_output 避免 ffmpeg 日志刷屏
            process = subprocess.run(cmd, capture_output=True, text=True, check=False)
            
            if process.returncode == 0:
                success += 1
                # 可选：进度条显示成功
                pbar.set_postfix_str(f"✅ {mp4_file.name[:25]}")
            else:
                tqdm.write(f" [错误] FFmpeg 报错 ({mp4_file.name}): {process.stderr.strip()}")
                logger.error(f"FFmpeg 报错 ({mp4_file.name}): {process.stderr.strip()}")
                fail += 1
                
        except Exception as e:
            tqdm.write(f" [严重错误] {mp4_file.name}: {str(e)}")
            logger.error(f"系统错误 ({mp4_file.name}): {str(e)}")
            fail += 1

    pbar.close() # 显式关闭
    
    logger.info(f"--- 任务结束: 成功 {success}, 失败 {fail} ---")

if __name__ == "__main__":
    env_manager.check_python_version()
    env_manager.setup_venv()# 必须最先执行（包含 GPU 自动检测）
    ensure_ffmpeg()

    if len(sys.argv) < 2:
        print("用法: python extract.py <源目录> [目标目录]")
        sys.exit(1)

    src_dir = sys.argv[1]

    # 如果没传目标目录，自动生成
    if len(sys.argv) >= 3:
        dst_dir = sys.argv[2]
    else:
        dst_dir = str(Path(src_dir).parent / f"{Path(src_dir).name}_audio")#输出目录和源目录在同一层级
    extract_audio(src_dir, dst_dir)