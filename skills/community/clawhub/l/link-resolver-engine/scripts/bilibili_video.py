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
import re
import time
import hashlib
import urllib.parse
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

# ==================== WBI 动态签名核心算法 ====================
# B站对 wbi 接口的签名混淆表
MIXIN_KEY_ENC_TAB = [
    46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49,
    33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 54, 51,
    40, 62, 59, 11, 6, 61, 22, 55, 34, 44, 1, 52, 17, 30, 21, 36, 60, 4, 25,
    26, 57, 56, 14, 20, 0, 63, 63, 63, 63, 63, 63, 63, 63
]

def get_mixin_key(ae):
    """根据 img_key 和 sub_key 生成 mixin_key"""
    oe = []
    for i in MIXIN_KEY_ENC_TAB:
        oe.append(ae[i])
    return "".join(oe)[:32]

def enc_wbi(params: dict, img_key: str, sub_key: str) -> dict:
    """为请求参数字典添加 w_rid 和 wts 签名参数"""
    mixin_key = get_mixin_key(img_key + sub_key)
    curr_time = int(time.time())
    params['wts'] = curr_time
    # 按照 key 排序
    params = dict(sorted(params.items()))
    # 过滤特殊字符
    for k, v in params.items():
        if isinstance(v, str):
            params[k] = ''.join(c for c in v if c not in "!'()*")
    # 拼接字符串并计算 MD5
    query = urllib.parse.urlencode(params)
    w_rid = hashlib.md5((query + mixin_key).encode('utf-8')).hexdigest()
    params['w_rid'] = w_rid
    return params

def get_wbi_keys(session: requests.Session) -> tuple:
    """获取 B站当前生效的临时 img_key 和 sub_key"""
    try:
        resp = session.get("https://api.bilibili.com/x/web-interface/nav", timeout=5)
        res_json = resp.json()
        wbi_img = res_json.get("data", {}).get("wbi_img", {})
        img_url = wbi_img.get("img_url")
        sub_url = wbi_img.get("sub_url")
        if img_url and sub_url:
            img_key = img_url.split("/")[-1].split(".")[0]
            sub_key = sub_url.split("/")[-1].split(".")[0]
            return img_key, sub_key
    except Exception as e:
        logger.error(f"获取 WBI Keys 失败: {e}")
    # 获取失败时返回默认缺省 key（极少触发）
    return "72136226c6a0419d9da65b0cee931fe2", "1e66c0850c954e7f8664ecfc98f9c1b3"

# ==================== 核心视频提取主函数 ====================
def get_bilibili_no_wm(raw_url: str) -> dict | None:
    """
    B站视频下载地址提取器（避开10054全API版）
    """
    match = re.search(r'(BV[0-9a-zA-Z]{10})', raw_url)
    if not match:
        logger.error("❌ 未找到 BV 号")
        return None

    bvid = match.group(1)
    logger.info(f"✅ 开始处理 B站视频: {bvid}")

    # 规范化的混淆 Headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.bilibili.com/",
        "Origin": "https://www.bilibili.com",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Accept-Encoding": "gzip, deflate"
    }

    session = requests.Session()
    session.headers.update(headers)

    try:
        # 第一步：不再访问网页，直接通过无需鉴权的开放 view 接口拿 cid 和 title
        info_url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
        info_resp = session.get(info_url, timeout=10)
        info_resp.raise_for_status()
        
        info_json = info_resp.json()
        if info_json.get("code") != 0:
            logger.error(f"❌ 获取视频基础信息失败: {info_json.get('message')}")
            return None
            
        video_data = info_json.get("data", {})
        cid = video_data.get("cid")
        title = video_data.get("title") or "bilibili_video"
        
        if not cid:
            logger.error("❌ 无法获取有效的 cid")
            return None
        
        logger.info(f" 成功提取视频信息 -> Title: {title}, CID: {cid}")

        # 第二步：获取动态 Wbi 密钥并进行参数加签
        img_key, sub_key = get_wbi_keys(session)
        
        play_params = {
            "bvid": bvid,
            "cid": cid,
            "qn": 64,       # 画质代码（64为 720P，非会员无需登录可直接拿到的最高画质）
            "fnval": 4048,   # 4048 代表请求 DASH 流格式（音视频分离）
            "fourk": 1
        }
        # 注入 w_rid 和 wts 签名
        signed_params = enc_wbi(play_params, img_key, sub_key)

        # 第三步：请求 playurl 接口
        play_url = "https://api.bilibili.com/x/player/wbi/playurl"
        play_resp = session.get(play_url, params=signed_params, timeout=15)
        play_resp.raise_for_status()
        json_data = play_resp.json()

        if json_data.get("code") != 0:
            logger.error(f"❌ 播放列表接口返回错误: {json_data.get('message')}")
            return None

        data = json_data.get("data", {})
        dash = data.get("dash") or {}

        result = {
            "video_url": None,
            "audio_url": None,
            "title": title,
            "quality": None
        }

        # 优先解析 DASH (最高画质音视频分离)
        if dash and dash.get("video"):
            video_tracks = dash["video"]
            best_video = max(video_tracks, key=lambda x: x.get("bandwidth", 0))
            result["video_url"] = best_video.get("base_url") or best_video.get("baseUrl")
            result["quality"] = f"{best_video.get('height', 0)}p"

            audio_tracks = dash.get("audio") or []
            if audio_tracks:
                best_audio = max(audio_tracks, key=lambda x: x.get("bandwidth", 0))
                result["audio_url"] = best_audio.get("base_url") or best_audio.get("baseUrl")

        # 备用解析 durl (传统的 mp4/flv 单文件合一流)
        elif data.get("durl"):
            durls = data.get("durl") or []
            if durls:
                result["video_url"] = durls[0].get("url")
                result["quality"] = "720p"

        if result["video_url"]:
            logger.info(f" 成功获取无水印直链！清晰度: {result['quality']}")
            return result
        else:
            logger.warning("⚠️ 未找到任何有效的播放地址")
            return None

    except Exception as e:
        logger.error(f"❌ 捕获非预期请求异常: {e}")
        return None

def download_bilibili_video_request(play_info: dict, filename: str = None, download_dir: str = None) -> bool:
    """
    轻量容错版：下载 B站视频（支持仅包含 video_url 的极简 play_info）
    """
    # 核心安全检查：只要有视频地址就能跑
    if not play_info or not play_info.get("video_url"):
        logger.error("❌ 错误：play_info 中没有有效的 video_url")
        return False

    # ==================== 1. 容错提取参数 ====================
    video_url = play_info["video_url"]
    audio_url = play_info.get("audio_url")  # 如果没有，返回 None
    title = play_info.get("title") or "bilibili_video"  # 缺失 title 则使用默认名

    # ==================== 2. 目录与文件名处理 ====================
    if download_dir is None:
        download_dir = os.path.join(os.getcwd(), "downloads")
    os.makedirs(download_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if filename is None:
        # 过滤掉文件名中的非法字符
        safe_title = re.sub(r'[\\/:*?"<>|]', '_', title)
        filename = f"{safe_title}_{timestamp}.mp4"

    if not filename.endswith(".mp4"):
        filename += ".mp4"

    final_file = os.path.join(download_dir, filename)
    temp_video = os.path.join(download_dir, f"temp_video_{timestamp}.mp4")
    temp_audio = os.path.join(download_dir, f"temp_audio_{timestamp}.m4a") if audio_url else None

    logger.info(f"🚀 开始下载: {title}")
    logger.info(f"📁 保存目录: {download_dir}")

    # ==================== 3. 核心流式下载器（主动分片迭代版） ====================
    def _download_file_with_retry(url: str, save_path: str, max_retries: int = 7) -> bool:
        retries = 0
        force_fresh_start = False
        
        # 【核心改动】主动分片大小：每次只请求 5MB，避免单次连接传输时间过长被强杀
        CHUNK_SIZE = 5 * 1024 * 1024  

        while retries < max_retries:
            download_session = requests.Session()
            # 限制连接池，防止高并发被封
            adapter = requests.adapters.HTTPAdapter(pool_connections=2, pool_maxsize=2)
            download_session.mount("http://", adapter)
            download_session.mount("https://", adapter)
            
            download_session.headers.update({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
                "Referer": "https://www.bilibili.com/",
                "Origin": "https://www.bilibili.com",
                "Connection": "keep-alive",
                "Accept": "*/*",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Accept-Encoding": "identity"
            })

            try:
                # 异常强刷初始化
                if force_fresh_start and os.path.exists(save_path):
                    try: os.remove(save_path)
                    except: pass
                    force_fresh_start = False

                # 获取本地已下载的字节数
                downloaded_bytes = os.path.getsize(save_path) if os.path.exists(save_path) else 0
                
                # 计算当前切片的结束边界
                start_byte = downloaded_bytes
                end_byte = start_byte + CHUNK_SIZE - 1  # Range 是闭区间
                
                # 配置精确分片 Range 请求头
                download_session.headers["Range"] = f"bytes={start_byte}-{end_byte}"
                open_mode = "ab" if start_byte > 0 else "wb"

                # 发起连接，设置合理的超时时间
                r = download_session.get(url, stream=True, timeout=(10, 30))
                
                # 处理 416 范围错误（代表可能已经下载完毕，或者文件损坏）
                if r.status_code == 416:
                    if os.path.exists(save_path) and os.path.getsize(save_path) > 0:
                        # 尝试通过了边界，判定为下载完成
                        return True
                    logger.warning("⚠️ 收到 HTTP 416 错误，将清空临时文件重新下载...")
                    force_fresh_start = True
                    retries += 1
                    time.sleep(2)
                    continue
                    
                elif r.status_code not in (200, 206):
                    logger.warning(f"⚠️ 服务器响应异常，状态码: {r.status_code}，等待重试...")
                    retries += 1
                    time.sleep(3)
                    continue

                # 写入当前分片数据
                with open(save_path, open_mode) as f:
                    for chunk in r.iter_content(chunk_size=64 * 1024):
                        if chunk:
                            f.write(chunk)
                
                # 读取响应头中的 Content-Range，判断整个视频文件是否已经拉完
                # 示例格式: bytes 0-5242879/24859603
                content_range = r.headers.get("Content-Range", "")
                total_bytes = 0
                if content_range and "/" in content_range:
                    try:
                        total_bytes = int(content_range.split("/")[-1])
                    except:
                        pass
                
                current_size = os.path.getsize(save_path)
                
                # 结束条件 1：不支持 Range 返回了 200（直接拿到了全量）
                # 结束条件 2：当前本地文件大小已经等于或大于服务器声明的总大小
                if r.status_code == 200 or (total_bytes > 0 and current_size >= total_bytes):
                    if current_size > 0:
                        return True

                # 【重要逻辑】如果顺利走完当前分片，且文件没完：
                # 重置重试计数器（因为这一片成功了，证明连接有效），继续循环下载下一片
                retries = 0 
                time.sleep(0.5)  # 每次分片间歇 0.5 秒，温柔抓取，极大地降低被封几率
                continue

            except (requests.exceptions.RequestException, Exception) as e:
                retries += 1
                logger.warning(f"⚠️ 传输流中断 (次数 {retries}/{max_retries}): {e}")
                time.sleep(retries * 2)  # 阶梯式等待，给服务器风控解封的时间
            finally:
                download_session.close()
                
        return False
    # ==================== 4. 主下载调度逻辑 ====================
    try:
        # 下载视频轨
        logger.info("下载视频流...")
        if not _download_file_with_retry(video_url, temp_video):
            raise Exception("视频流下载失败，已达到最大重试次数。")

        # 判断是否存在音频轨
        if audio_url:
            logger.info("下载音频流...")
            if not _download_file_with_retry(audio_url, temp_audio):
                raise Exception("音频流下载失败，已达到最大重试次数。")

            # 音视频合并
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
                capture_output=True, 
                text=True, 
                encoding="utf-8", 
                errors="ignore", 
                timeout=180
            )

            if result.returncode == 0:
                logger.info(f"🎉 音视频完美合并完成：{final_file}")
                # 成功后清理临时文件
                for temp in [temp_video, temp_audio]:
                    if temp and os.path.exists(temp): os.remove(temp)
                return True
            else:
                logger.error(f"⚠️ ffmpeg 合并报错，降级保留原视频。")
                if os.path.exists(temp_video):
                    os.rename(temp_video, final_file)
                return False
        else:
            # 【核心改动】如果没有音频轨，直接将下载好的视频流文件重命名为最终的目标文件
            logger.info("检测到无独立音频流，直接生成视频文件...")
            if os.path.exists(final_file):
                os.remove(final_file)
            os.rename(temp_video, final_file)
            logger.info(f"🎉 视频下载完成：{final_file}")
            return True

    except Exception as e:
        logger.error(f"❌ 下载主进程异常: {e}")
        # 如果是彻头彻尾的失败，清理本次生成的残余垃圾临时文件
        for temp in [temp_video, temp_audio]:
            if temp and os.path.exists(temp):
                try: os.remove(temp)
                except: pass
        return False
    
def expand_bilibili_url(short_url):
    pattern = r'^https?://(?:www\.)?b23\.tv/[a-zA-Z0-9_-]{4,}(?:\?.*)?$'
    if not re.match(pattern, short_url.strip()):
        return False, "不是有效的Bilibili短链接 (必须是 b23.tv 格式)"
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.bilibili.com/"  # 加上 Referer 伪装成从B站内部跳转，提高成功率
        }
        
        # 1. 弃用 requests.head，改用 requests.get
        # 2. 将 allow_redirects 设置为 False，以便拦截 302 状态码并获取 Location
        response = requests.get(short_url, headers=headers, allow_redirects=False, timeout=10)
        
        # B站的 b23.tv 短链接通常会触发 302 重定向
        if response.status_code in (301, 302):
            real_url = response.headers.get('Location')
            return True, real_url
        elif response.status_code == 200:
            # 如果没有重定向，直接返回当前 URL
            return True, response.url
        else:
            return False, f"请求异常，HTTP状态码: {response.status_code}"
            
    except Exception as e:
        return False, f"请求失败: {str(e)}"
    
    
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
    