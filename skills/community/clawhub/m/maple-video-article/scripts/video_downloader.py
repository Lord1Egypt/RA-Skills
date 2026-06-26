#!/usr/bin/env python3
"""
Video Downloader - OpenClaw Skill
下载任意平台视频（YouTube、B站、抖音等），自动合并音视频，清理文件名。

用法：
  python video_downloader.py <视频URL> [分辨率] [输出目录]

示例：
  python video_downloader.py "https://youtu.be/xxx" "1080p"
  python video_downloader.py "https://www.bilibili.com/video/BV1xx" "720p" "./downloads"
"""

import os
import sys
import subprocess
import tempfile
import re
import importlib

# ===== 依赖检查 =====
REQUIRED_PACKAGES = {
    "yt_dlp": "yt-dlp",
}


def check_dependencies() -> list[str]:
    """Return list of missing required package names."""
    missing = []
    for module_name, pip_name in REQUIRED_PACKAGES.items():
        try:
            importlib.import_module(module_name)
        except ImportError:
            missing.append(pip_name)
    return missing


_missing = check_dependencies()
if _missing:
    print(
        f"ERROR: Missing required dependencies: {', '.join(_missing)}\n"
        f"Install them with:  pip install {' '.join(_missing)}",
        file=sys.stderr,
    )
    raise SystemExit(1)

# ===== 兼容性修复 =====
# Windows 上 yt-dlp 可能不在 PATH，用 python -m yt_dlp 更稳
YT_DLP_CMD = ['python3', '-m', 'yt_dlp']

# 通过 imageio-ffmpeg 获取 ffmpeg 路径（自带二进制，无需系统安装）
def get_ffmpeg_path():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        # fallback: 直接调用系统命令
        return 'ffmpeg'

def get_ffprobe_path():
    """ffprobe 路径，优先用 ffmpeg 目录下的 ffprobe，否则用 ffmpeg 替代"""
    ffmpeg_path = get_ffmpeg_path()
    ffmpeg_dir = os.path.dirname(ffmpeg_path)
    # 尝试找同目录的 ffprobe
    ffprobe_name = 'ffprobe.exe' if os.name == 'nt' else 'ffprobe'
    ffprobe_path = os.path.join(ffmpeg_dir, ffprobe_name)
    if os.path.exists(ffprobe_path):
        return ffprobe_path
    # 如果 imageio-ffmpeg 没带 ffprobe，尝试 Gyan.dev 的完整版
    if os.name == 'nt':
        gyandir = os.path.join(ffmpeg_dir.replace('imageio_ffmpeg\\binaries', 'ffmpeg-bin'))
        gyandir = os.path.join(os.environ.get('USERPROFILE', ''), 'ffmpeg-bin')
        gyandir = os.path.expanduser('~\\ffmpeg-bin')
        if os.path.isdir(gyandir):
            for f in os.listdir(gyandir):
                if f.lower().startswith('ffprobe') and f.lower().endswith('.exe'):
                    return os.path.join(gyandir, f)
    # fallback: 用 ffmpeg 替代（某些功能不支持）
    return ffmpeg_path

FFMPEG = get_ffmpeg_path()
FFPROBE = get_ffprobe_path()

def sanitize_filename(name, max_len=50):
    name = os.path.basename(name)
    name = re.sub(r'[^\w\u4e00-\u9fff\-\.]', '_', name)
    if len(name) > max_len:
        base, ext = os.path.splitext(name)
        base = base[:max_len - len(ext)]
        name = base + ext
    return name

def has_audio_stream(filepath):
    """检测文件是否有音频流（用 ffmpeg -i 输出判断）"""
    try:
        result = subprocess.run(
            [FFMPEG, '-i', filepath, '-hide_banner'],
            capture_output=True, text=True, timeout=15,
            encoding='utf-8', errors='replace'
        )
        # ffmpeg 输出在 stderr，检查是否有 Audio 流
        return 'Audio:' in result.stderr
    except Exception:
        return False

def has_video_stream(filepath):
    """检测文件是否有视频流（用 ffmpeg -i 输出判断）"""
    try:
        result = subprocess.run(
            [FFMPEG, '-i', filepath, '-hide_banner'],
            capture_output=True, text=True, timeout=15,
            encoding='utf-8', errors='replace'
        )
        return 'Video:' in result.stderr
    except Exception:
        return False

def merge_audio_video_if_needed(video_path, output_dir):
    if has_video_stream(video_path) and has_audio_stream(video_path):
        return video_path
    print('检测到音视频分离，尝试合并...')
    
    # 清理 format_id 后缀 (如 .f30016)
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    base_name = re.sub(r'\.f\d+$', '', base_name)  # 去掉 .f30016 这样的后缀
    
    dir_path = os.path.dirname(video_path)
    
    # 找匹配的音频/视频文件：清理 format_id 后匹配
    candidates = []
    for f in os.listdir(dir_path):
        f_full = os.path.join(dir_path, f)
        if f_full == video_path:
            continue
        f_base = os.path.splitext(f)[0]
        f_base_clean = re.sub(r'\.f\d+$', '', f_base)
        # 匹配：basename 相同（去掉 format_id 后）
        if f_base_clean == base_name:
            candidates.append(f_full)
        # 备选：同目录下只有两个媒体文件时也尝试合并
        elif len(candidates) == 0:
            ext = os.path.splitext(f)[1].lower()
            if ext in ('.m4a', '.mp3', '.webm', '.opus', '.aac'):
                candidates.append(f_full)
    
    if candidates:
        other_file = candidates[0]
        v_has = has_video_stream(video_path)
        a_has = has_audio_stream(video_path)
        o_has_a = has_audio_stream(other_file)
        o_has_v = has_video_stream(other_file)
        
        if (v_has and o_has_a) or (a_has and o_has_v):
            # 确定哪个是视频哪个是音频
            if v_has:
                vid_file, aud_file = video_path, other_file
            else:
                vid_file, aud_file = other_file, video_path
            
            merged_path = os.path.join(output_dir, f'{base_name}.mp4')
            cmd = [FFMPEG, '-y', '-i', vid_file, '-i', aud_file,
                   '-c:v', 'copy', '-c:a', 'aac', merged_path]
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, 
                                       timeout=120, encoding='utf-8', errors='replace')
                if os.path.exists(merged_path):
                    # 合并成功，删除临时文件
                    os.remove(video_path)
                    for c in candidates:
                        if os.path.exists(c):
                            os.remove(c)
                    print(f'合并完成: {merged_path}')
                    return merged_path
            except subprocess.CalledProcessError as e:
                print(f'合并失败: {e}')
    
    # 如果没有找到匹配的文件，直接重命名为干净的名字
    clean_name = re.sub(r'\.f\d+$', '', os.path.basename(video_path))
    clean_path = os.path.join(output_dir, clean_name)
    if clean_path != video_path:
        if os.path.exists(clean_path):
            os.remove(clean_path)
        os.rename(video_path, clean_path)
        return clean_path
    return video_path

def download_video(url, output_dir=None, resolution=None):
    """下载视频，返回文件路径"""
    if output_dir is None:
        output_dir = tempfile.mkdtemp(prefix='video_download_')

    print(f'使用 ffmpeg: {FFMPEG}')
    print('获取视频格式信息...')

    list_cmd = YT_DLP_CMD + ['-F', '--no-warnings', url]
    try:
        result = subprocess.run(list_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                                text=True, timeout=30, encoding='utf-8', errors='replace')
        if result.returncode != 0:
            raise Exception(result.stderr)
        lines = result.stdout.splitlines() if result.stdout else []
    except Exception as e:
        raise Exception(f'获取格式列表失败: {e}')

    video_formats = []  # (height, width, format_id, has_audio)
    audio_formats = []  # (asr, format_id)  - 用于检查是否有可用音频流
    for line in lines:
        parts = line.split()
        if len(parts) >= 3 and parts[1] in ['mp4', 'webm', 'mkv', 'm4a', 'mp3', 'aac', 'opus']:
            try:
                res_str = parts[2]
                format_id = parts[0]
                # 判断是否有 audio note
                has_audio = 'audio' in line.lower() or parts[1] in ['m4a', 'mp3', 'aac', 'opus']
                if 'x' in res_str:
                    width, height = map(int, res_str.split('x'))
                    video_formats.append((height, width, format_id, has_audio))
                elif parts[1] in ['m4a', 'mp3', 'aac', 'opus']:
                    # 纯音频流（分辨率列可能是 "audio only" 或采样率）
                    audio_formats.append((0, format_id))
            except:
                continue

    # 检查是否有独立音频流可用
    has_separate_audio = len(audio_formats) > 0

    if not video_formats:
        print('警告: 无法解析格式列表，使用默认 best')
        format_spec = 'bestvideo+bestaudio/best'
    else:
        video_formats.sort(reverse=True)
        chosen = None
        if resolution:
            target_height = int(resolution.rstrip('p'))
            for h, w, fid, ha in video_formats:
                if h <= target_height:
                    chosen = (h, w, fid, ha)
                    break
            if not chosen:
                chosen = video_formats[-1]
        else:
            for h, w, fid, ha in video_formats:
                if h == 1080:
                    chosen = (h, w, fid, ha)
                    break
            if not chosen:
                chosen = video_formats[0]

        height, width, fmt_id, is合一流 = chosen
        # 关键修复：只有在选中的是纯视频流且有独立音频流可用时，才拼接 +bestaudio
        if has_separate_audio and not is合一流:
            format_spec = f'{fmt_id}+bestaudio/best'
            print(f'选择格式: {fmt_id} ({width}x{height}) + bestaudio（音视频分离模式）')
        else:
            format_spec = fmt_id
            print(f'选择格式: {fmt_id} ({width}x{height})（合一/默认模式）')

    print('开始下载...')
    template = os.path.join(output_dir, '%(title)s.%(ext)s')
    download_cmd = YT_DLP_CMD + [
        '-f', format_spec,
        '--output', template,
        '--merge-output-format', 'mp4',
        '--restrict-filenames',
        '--no-warnings',
        url
    ]

    try:
        result = subprocess.run(download_cmd, capture_output=True, text=True, timeout=600, encoding='utf-8')
        if result.returncode != 0:
            raise Exception(result.stderr or result.stdout)
    except subprocess.CalledProcessError as e:
        raise Exception(f'下载失败: {e}')

    files = [f for f in os.listdir(output_dir)
             if f.endswith(('.mp4', '.mkv', '.webm', '.mov', '.avi'))]
    if not files:
        raise Exception('未找到下载的视频文件')

    video_path = os.path.join(output_dir, files[0])
    safe_name = sanitize_filename(files[0])
    if safe_name != files[0]:
        new_path = os.path.join(output_dir, safe_name)
        os.rename(video_path, new_path)
        video_path = new_path

    video_path = merge_audio_video_if_needed(video_path, output_dir)

    size_mb = os.path.getsize(video_path) / (1024*1024)
    print(f'下载完成: {video_path} ({size_mb:.1f} MB)')
    return video_path

def main():
    if len(sys.argv) < 2:
        print('用法: python video_downloader.py <视频URL> [分辨率] [输出目录]')
        print('示例: python video_downloader.py "https://youtu.be/xxx" "1080p"')
        print('      python video_downloader.py "https://www.bilibili.com/video/BV1xx" "720p" "./downloads"')
        sys.exit(1)

    url = sys.argv[1]
    resolution = sys.argv[2] if len(sys.argv) > 2 else None
    output_dir = sys.argv[3] if len(sys.argv) > 3 else None

    if output_dir and not os.path.isdir(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    try:
        result = download_video(url, output_dir, resolution)
        print(f'\n最终文件: {result}')
    except Exception as e:
        print(f'出错: {e}')
        sys.exit(1)

if __name__ == '__main__':
    main()
