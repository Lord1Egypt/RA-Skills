#!/usr/bin/env python3
"""
视频批量压缩脚本 - 使用NVIDIA AV1硬件编码
支持交互式选择压缩方案，带实时进度显示

作者: 北京老李 (beijingLL)
"""

import os
import sys
import time
import json
import subprocess
import argparse
import shutil
import tempfile
from pathlib import Path
from datetime import datetime, timedelta

try:
    from tqdm import tqdm
except ImportError:
    print("正在安装依赖库 tqdm...")
    subprocess.run([sys.executable, "-m", "pip", "install", "tqdm", "-i", "https://pypi.tuna.tsinghua.edu.cn/simple"], 
                   capture_output=True)
    from tqdm import tqdm

# 注意：本脚本通过FFmpeg调用NVIDIA硬件编码，不需要pynvvideocodec库
# 只需确保：1. NVIDIA显卡驱动已安装  2. FFmpeg已安装

# ============================================
# 配置区 - 可修改
# ============================================

# 压缩方案预设
COMPRESSION_PROFILES = {
    "A": {
        "name": "保守压缩",
        "description": "保持1080p，视觉质量无损",
        "resolution": "keep",  # 保持原分辨率
        "crf": 23,
        "fps": "keep",  # 保持原帧率
        "audio_bitrate": "128k",
        "preset": "p4",  # NVENC预设 (p1-p7，p4平衡)
        "expected_ratio": "40-60%",
    },
    "B": {
        "name": "平衡压缩（推荐）",
        "description": "720p + CRF24，质量几乎无感",
        "resolution": "1280x720",
        "crf": 24,
        "fps": 24,
        "audio_bitrate": "96k",
        "preset": "p4",
        "expected_ratio": "65-75%",
    },
    "C": {
        "name": "激进压缩",
        "description": "720p + CRF28，最大节省空间",
        "resolution": "1280x720",
        "crf": 28,
        "fps": 15,
        "audio_bitrate": "64k",
        "preset": "p5",  # 更快但质量略低
        "expected_ratio": "78-85%",
    },
}

# 输入目录（可通过命令行参数覆盖）
INPUT_DIR = None

# 输出目录（可通过命令行参数覆盖，默认为输入目录_compressed）
OUTPUT_DIR = None

# 视频文件扩展名
VIDEO_EXTENSIONS = ['.mp4', '.MP4', '.mkv', '.avi', '.mov']


# ============================================
# 工具函数
# ============================================

def check_environment():
    """检查运行环境，对比FFmpeg和pynvvideocodec方案"""
    print("=" * 80)
    print("🔧 环境检查与方案对比")
    print("=" * 80)
    
    env_info = {
        'ffmpeg': {'available': False, 'version': '', 'av1_nvenc': False},
        'pynvvideocodec': {'available': False, 'version': ''},
        'gpu': {'available': False, 'name': '', 'driver': ''},
    }
    
    # 1. 检查FFmpeg
    print("\n[1/3] 检查 FFmpeg...")
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                               capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            env_info['ffmpeg']['available'] = True
            env_info['ffmpeg']['version'] = version_line
            print(f"  ✓ FFmpeg 已安装")
            print(f"    {version_line}")
            
            # 检查是否支持av1_nvenc
            enc_result = subprocess.run(['ffmpeg', '-encoders'], 
                                       capture_output=True, text=True, timeout=10)
            if 'av1_nvenc' in enc_result.stdout:
                env_info['ffmpeg']['av1_nvenc'] = True
                print(f"  ✓ 支持 av1_nvenc (NVIDIA AV1硬件编码)")
            else:
                print(f"  ⚠️ 不支持 av1_nvenc")
        else:
            print(f"  ❌ FFmpeg 未安装或不可用")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print(f"  ❌ FFmpeg 未找到")
    
    # 2. 检查pynvvideocodec
    print("\n[2/3] 检查 PyNvVideoCodec...")
    try:
        import PyNvVideoCodec
        env_info['pynvvideocodec']['available'] = True
        env_info['pynvvideocodec']['version'] = getattr(PyNvVideoCodec, '__version__', 'unknown')
        print(f"  ✓ PyNvVideoCodec 已安装 (版本: {env_info['pynvvideocodec']['version']})")
    except ImportError as e:
        print(f"  ⚠️ PyNvVideoCodec 未安装或导入失败")
        print(f"    原因: {e}")
        print(f"    说明: 本脚本使用FFmpeg方案，不需要此库")
    
    # 3. 检查GPU
    print("\n[3/3] 检查 NVIDIA GPU...")
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=name,driver_version,memory.total', 
                                '--format=csv,noheader'], 
                               capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            gpu_info = result.stdout.strip()
            env_info['gpu']['available'] = True
            print(f"  ✓ GPU检测通过: {gpu_info}")
        else:
            print(f"  ❌ 未检测到NVIDIA GPU")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print(f"  ❌ nvidia-smi 命令不可用")
        print(f"    Windows: 请安装NVIDIA显卡驱动")
        print(f"    Linux: sudo apt install nvidia-utils-xxx")
    
    # 方案对比
    print(f"\n{'=' * 80}")
    print("📊 FFmpeg vs PyNvVideoCodec 性能对比")
    print(f"{'=' * 80}")
    
    print("""
┌──────────────────┬─────────────────────┬─────────────────────┐
│      特性        │     FFmpeg 方案     │  PyNvVideoCodec     │
├──────────────────┼─────────────────────┼─────────────────────┤
│ 安装难度         │ ★☆☆ (简单)          │ ★★★ (复杂)          │
│                  │ 只需ffmpeg二进制    │ 需CUDA+驱动+编译    │
├──────────────────┼─────────────────────┼─────────────────────┤
│ 跨平台支持       │ ★★★★★               │ ★★☆               │
│                  │ Win/Mac/Linux       │ 主要Win/Linux       │
├──────────────────┼─────────────────────┼─────────────────────┤
│ 编码性能         │ ★★★★★               │ ★★★★★               │
│                  │ 直接调用NVENC       │ 直接调用NVENC       │
│                  │ (底层相同)          │ (底层相同)          │
├──────────────────┼─────────────────────┼─────────────────────┤
│ 功能完整性       │ ★★★★★               │ ★★★☆              │
│                  │ 完整音视频处理      │ 偏重编解码          │
├──────────────────┼─────────────────────┼─────────────────────┤
│ 易用性           │ ★★★★★               │ ★★☆               │
│                  │ 命令行即可用        │ 需Python API        │
├──────────────────┼─────────────────────┼─────────────────────┤
│ 本脚本采用       │ ✅ 是               │ ❌ 否               │
└──────────────────┴─────────────────────┴─────────────────────┘

💡 结论:
  - FFmpeg方案: 简单、可靠、跨平台、功能完整 → 本脚本采用
  - PyNvVideoCodec: 适合需要在Python中直接操作帧缓冲的场景
  - 性能: 两者底层都调用NVIDIA NVENC，编码速度基本一致
  - 本脚本选择FFmpeg: 更易用，维护成本低，适合批量处理
""")
    
    # 判断是否可以继续
    can_proceed = env_info['ffmpeg']['available'] and env_info['ffmpeg']['av1_nvenc']
    
    if can_proceed:
        print("✅ 环境检查通过！可以进行视频压缩")
    else:
        print("❌ 环境不满足要求")
        if not env_info['ffmpeg']['available']:
            print("   请安装FFmpeg: https://ffmpeg.org/download.html")
        if not env_info['ffmpeg']['av1_nvenc']:
            print("   FFmpeg不支持av1_nvenc，请安装更新版本")
        if not env_info['gpu']['available']:
            print("   未检测到NVIDIA GPU，无法使用硬件编码")
    
    print("=" * 80)
    
    return can_proceed, env_info


def check_gpu():
    """检查NVIDIA GPU是否可用（支持Windows和Linux）"""
    try:
        # Windows和Linux都支持nvidia-smi
        result = subprocess.run(['nvidia-smi', '--query-gpu=name,driver_version,memory.total', 
                                '--format=csv,noheader'], 
                               capture_output=True, text=True)
        if result.returncode == 0:
            gpu_info = result.stdout.strip()
            print(f"✓ GPU检测通过: {gpu_info}")
            return True
        else:
            print("❌ 未检测到NVIDIA GPU")
            print("   请确保已安装NVIDIA驱动: https://www.nvidia.com/Download/index.aspx")
            return False
    except FileNotFoundError:
        print("❌ 未找到 nvidia-smi 命令")
        print("   Windows: 请安装NVIDIA显卡驱动")
        print("   Linux: 请运行 sudo apt install nvidia-utils-xxx (根据你的驱动版本)")
        return False
    except Exception as e:
        print(f"❌ GPU检测失败: {e}")
        return False


def get_video_info(file_path):
    """获取视频信息"""
    try:
        cmd = [
            'ffprobe',
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_format',
            '-show_streams',
            file_path
        ]
        result = subprocess.run(cmd, capture_output=True, timeout=30)
        if result.returncode != 0:
            return None
        
        data = json.loads(result.stdout.decode('utf-8'))
        
        video_stream = None
        audio_stream = None
        for stream in data.get('streams', []):
            if stream.get('codec_type') == 'video' and not video_stream:
                video_stream = stream
            elif stream.get('codec_type') == 'audio' and not audio_stream:
                audio_stream = stream
        
        if not video_stream:
            return None
        
        file_size = int(data.get('format', {}).get('size', 0))
        duration = float(data.get('format', {}).get('duration', 0))
        
        # 获取原始帧率
        fps_str = video_stream.get('r_frame_rate', '30/1')
        fps_parts = fps_str.split('/')
        if len(fps_parts) == 2:
            original_fps = float(fps_parts[0]) / float(fps_parts[1])
        else:
            original_fps = 30.0
        
        return {
            'width': int(video_stream.get('width', 1920)),
            'height': int(video_stream.get('height', 1080)),
            'fps': original_fps,
            'duration': duration,
            'file_size': file_size,
            'file_size_mb': file_size / (1024 * 1024),
            'codec': video_stream.get('codec_name', 'h264'),
        }
    except Exception as e:
        print(f"  ⚠️ 获取视频信息失败: {e}")
        return None


def format_size(size_mb):
    """格式化大小显示"""
    if size_mb >= 1024:
        return f"{size_mb/1024:.2f} GB"
    else:
        return f"{size_mb:.1f} MB"


def format_duration(seconds):
    """格式化时间显示"""
    return str(timedelta(seconds=int(seconds)))


def compress_single_ffmpeg(input_file, output_file, profile, video_info):
    """使用ffmpeg压缩单个视频（调用NVIDIA硬件编码）"""
    
    # 构建ffmpeg命令
    cmd = ['ffmpeg', '-i', input_file]
    
    # 视频滤镜和编码参数
    video_filters = []
    
    # 分辨率设置
    if profile['resolution'] != 'keep':
        width, height = profile['resolution'].split('x')
        video_filters.append(f"scale={width}:{height}")
    
    # 帧率设置
    if profile['fps'] != 'keep':
        video_filters.append(f"fps={profile['fps']}")
    
    # 应用滤镜
    if video_filters:
        cmd.extend(['-vf', ','.join(video_filters)])
    
    # NVIDIA AV1硬件编码参数
    cmd.extend([
        '-c:v', 'av1_nvenc',  # NVIDIA AV1编码器
        '-cq:v', str(profile['crf']),  # 质量模式
        '-preset', profile['preset'],  # 预设
        '-rc', 'vbr',  # 可变码率
    ])
    
    # 音频编码
    cmd.extend([
        '-c:a', 'aac',
        '-b:a', profile['audio_bitrate'],
    ])
    
    # 覆盖输出文件
    cmd.extend(['-y', output_file])
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            timeout=600,  # 10分钟超时
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"  ⚠️ 超时，跳过此文件")
        return False
    except Exception as e:
        print(f"  ❌ 压缩失败: {e}")
        return False


def show_profile_comparison():
    """显示压缩方案对比"""
    print("\n" + "=" * 80)
    print("📊 压缩方案对比")
    print("=" * 80)
    print(f"{'方案':<6} {'名称':<20} {'分辨率':<12} {'CRF':<6} {'帧率':<8} {'音频':<10} {'预估节省':<10}")
    print("-" * 80)
    
    for key, profile in COMPRESSION_PROFILES.items():
        res = "原分辨率" if profile['resolution'] == 'keep' else profile['resolution']
        fps = "原帧率" if profile['fps'] == 'keep' else f"{profile['fps']}fps"
        print(f"{key:<6} {profile['name']:<20} {res:<12} {profile['crf']:<6} {fps:<8} {profile['audio_bitrate']:<10} {profile['expected_ratio']:<10}")
    
    print("-" * 80)
    print("\n详细说明:")
    for key, profile in COMPRESSION_PROFILES.items():
        print(f"\n方案 {key}: {profile['name']}")
        print(f"  {profile['description']}")
        print(f"  适合: {'追求质量' if key == 'A' else '平衡质量和空间' if key == 'B' else '最大化节省空间'}")
    
    print("\n" + "=" * 80)


def select_profile():
    """交互式选择压缩方案"""
    while True:
        show_profile_comparison()
        choice = input("\n请选择压缩方案 [A/B/C] (默认B): ").strip().upper()
        
        if not choice:
            choice = 'B'
        
        if choice in COMPRESSION_PROFILES:
            profile = COMPRESSION_PROFILES[choice]
            print(f"\n✓ 已选择方案 {choice}: {profile['name']}")
            print(f"  {profile['description']}")
            return choice, profile
        else:
            print("❌ 无效选择，请输入 A、B 或 C")


def get_video_files(directory):
    """获取目录下所有视频文件"""
    video_files = []
    for file in sorted(os.listdir(directory)):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path) and any(file.endswith(ext) for ext in VIDEO_EXTENSIONS):
            video_files.append(file_path)
    return video_files


def validate_compression(video_file, profile, temp_output_dir):
    """
    验证压缩是否真的节省空间
    返回: (是否节省, 原始大小MB, 压缩后大小MB, 节省百分比)
    """
    print(f"\n{'=' * 60}")
    print("🔍 验证压缩效果...")
    print(f"{'=' * 60}")
    
    # 获取原始视频信息
    video_info = get_video_info(video_file)
    if not video_info:
        print("❌ 无法读取测试视频")
        return False, 0, 0, 0
    
    original_size = video_info['file_size_mb']
    filename = os.path.basename(video_file)
    temp_output = os.path.join(temp_output_dir, f"_test_{filename}")
    
    print(f"测试文件: {filename}")
    print(f"原始大小: {format_size(original_size)}")
    print(f"压缩方案: {profile['name']}")
    
    # 执行压缩
    print("正在压缩测试文件...")
    start_time = time.time()
    success = compress_single_ffmpeg(video_file, temp_output, profile, video_info)
    elapsed = time.time() - start_time
    
    if not success or not os.path.exists(temp_output):
        print("❌ 压缩失败")
        return False, original_size, 0, 0
    
    # 获取压缩后大小
    compressed_size = os.path.getsize(temp_output) / (1024 * 1024)
    saved_percent = ((original_size - compressed_size) / original_size) * 100
    
    print(f"压缩后大小: {format_size(compressed_size)}")
    print(f"节省空间: {format_size(original_size - compressed_size)} ({saved_percent:.1f}%)")
    print(f"用时: {elapsed:.1f}秒")
    
    # 判断是否值得继续
    if saved_percent > 5:  # 至少节省5%才继续
        print(f"\n✅ 验证通过！压缩可节省 {saved_percent:.1f}% 空间")
        print("   继续批量压缩...")
        return True, original_size, compressed_size, saved_percent
    elif saved_percent > -10:  # 增加不超过10%也可以接受
        print(f"\n⚠️ 压缩效果一般（{'节省' if saved_percent > 0 else '增加'} {abs(saved_percent):.1f}%）")
        print("   说明：原视频可能已经被高效压缩过（如B站视频）")
        print("   可以继续，但空间节省有限")
        return True, original_size, compressed_size, saved_percent
    else:
        print(f"\n⚠️ 压缩后文件变大（增加 {abs(saved_percent):.1f}%）")
        print("   说明：原视频已经是高效编码，无需再次压缩")
        print("   建议：")
        print("   1. 保持原视频不变")
        print("   2. 或者尝试更激进的方案（降低分辨率/码率）")
        return False, original_size, compressed_size, saved_percent


def compress_batch(video_files, profile, output_dir, test_mode=False, test_count=3):
    """批量压缩视频"""
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 测试模式
    if test_mode:
        video_files = video_files[:test_count]
        print(f"\n🧪 测试模式: 只处理前 {test_count} 个视频")
    
    total_files = len(video_files)
    total_original_size = 0
    total_compressed_size = 0
    success_count = 0
    failed_count = 0
    failed_files = []
    
    print(f"\n{'=' * 80}")
    print(f"🎬 开始批量压缩")
    print(f"{'=' * 80}")
    print(f"输入目录: {INPUT_DIR}")
    print(f"输出目录: {output_dir}")
    print(f"压缩方案: {profile['name']}")
    print(f"视频总数: {total_files}")
    print(f"{'=' * 80}\n")
    
    # 使用tqdm显示进度
    with tqdm(total=total_files, desc="压缩进度", unit="个", ncols=100) as pbar:
        for idx, input_file in enumerate(video_files, 1):
            filename = os.path.basename(input_file)
            output_file = os.path.join(output_dir, filename)
            
            # 获取视频信息
            video_info = get_video_info(input_file)
            if not video_info:
                print(f"\n[{idx}/{total_files}] ⚠️ 跳过 {filename} (无法读取)")
                failed_count += 1
                failed_files.append(filename)
                pbar.update(1)
                continue
            
            original_size_mb = video_info['file_size_mb']
            total_original_size += original_size_mb
            
            pbar.set_description(f"[{idx}/{total_files}] {filename[:40]}")
            
            # 压缩视频
            start_time = time.time()
            success = compress_single_ffmpeg(input_file, output_file, profile, video_info)
            elapsed = time.time() - start_time
            
            if success and os.path.exists(output_file):
                compressed_size = os.path.getsize(output_file) / (1024 * 1024)
                total_compressed_size += compressed_size
                
                # 计算压缩比
                ratio = (1 - compressed_size / original_size_mb) * 100
                speed = original_size_mb / elapsed if elapsed > 0 else 0
                
                # 更新进度条显示
                pbar.set_postfix({
                    '原始': format_size(original_size_mb),
                    '压缩后': format_size(compressed_size),
                    '节省': f"{ratio:.0f}%"
                })
                
                success_count += 1
            else:
                print(f"\n  ❌ 失败: {filename}")
                failed_count += 1
                failed_files.append(filename)
            
            pbar.update(1)
    
    # 输出报告
    print(f"\n{'=' * 80}")
    print("📊 压缩完成报告")
    print(f"{'=' * 80}")
    print(f"总视频数: {total_files}")
    print(f"成功: {success_count} | 失败: {failed_count}")
    
    if success_count > 0:
        print(f"\n原始总大小: {format_size(total_original_size)}")
        print(f"压缩后大小: {format_size(total_compressed_size)}")
        saved_size = total_original_size - total_compressed_size
        saved_ratio = (saved_size / total_original_size * 100) if total_original_size > 0 else 0
        print(f"节省空间: {format_size(saved_size)} ({saved_ratio:.1f}%)")
    
    if failed_files:
        print(f"\n❌ 失败的文件:")
        for f in failed_files:
            print(f"  - {f}")
    
    print(f"{'=' * 80}")
    
    return {
        'total': total_files,
        'success': success_count,
        'failed': failed_count,
        'original_size': total_original_size,
        'compressed_size': total_compressed_size,
        'failed_files': failed_files,
    }


# ============================================
# 主函数
# ============================================

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='🎬 NVIDIA AV1 视频批量压缩工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 交互式模式（会提示选择）
  python compress_videos.py

  # 指定输入输出目录和方案
  python compress_videos.py -i "E:\\视频" -o "E:\\压缩后" -p B

  # 测试模式（只压缩前3个）
  python compress_videos.py -i "E:\\视频" -p B --test

  # 非交互模式（跳过确认）
  python compress_videos.py -i "E:\\视频" -p A --no-confirm

压缩方案:
  A - 保守压缩（保持1080p，CRF23）
  B - 平衡压缩（720p，CRF24，推荐）
  C - 激进压缩（720p，CRF28，最大节省）
        """
    )
    
    parser.add_argument(
        '-i', '--input',
        type=str,
        help='输入视频目录路径'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='输出目录路径（默认：输入目录_compressed_方案名）'
    )
    
    parser.add_argument(
        '-p', '--profile',
        type=str,
        choices=['A', 'B', 'C'],
        help='压缩方案（A=保守，B=平衡推荐，C=激进）'
    )
    
    parser.add_argument(
        '--test',
        action='store_true',
        help='测试模式（只压缩前3个视频）'
    )
    
    parser.add_argument(
        '--test-count',
        type=int,
        default=3,
        help='测试模式处理的视频数量（默认3）'
    )
    
    parser.add_argument(
        '--no-confirm',
        action='store_true',
        help='跳过确认提示（非交互模式）'
    )
    
    return parser.parse_args()


def main():
    # 解析命令行参数
    args = parse_args()
    
    print("=" * 80)
    print("🎬 NVIDIA AV1 视频批量压缩工具")
    print("=" * 80)
    
    # 确定输入目录
    if args.input:
        input_dir = args.input
        print(f"\n输入目录 (命令行): {input_dir}")
    else:
        input_dir = input("\n请输入输入视频目录路径 (默认: 当前目录): ").strip()
        if not input_dir:
            input_dir = r"E:\视频输出\docker-2021"
        print(f"输入目录: {input_dir}")
    
    # 验证输入目录
    if not os.path.exists(input_dir):
        print(f"\n❌ 输入目录不存在: {input_dir}")
        sys.exit(1)
    
    if not os.path.isdir(input_dir):
        print(f"\n❌ 输入路径不是目录: {input_dir}")
        sys.exit(1)
    
    # 获取视频文件
    video_files = get_video_files(input_dir)
    if not video_files:
        print(f"\n❌ 在 {input_dir} 中未找到视频文件")
        sys.exit(1)
    
    print(f"\n✓ 找到 {len(video_files)} 个视频文件")
    
    # 计算总大小
    total_size = sum(os.path.getsize(f) for f in video_files) / (1024 * 1024 * 1024)
    print(f"  总大小: {total_size:.2f} GB")
    
    # 选择压缩方案
    if args.profile:
        profile_key = args.profile
        profile = COMPRESSION_PROFILES[profile_key]
        print(f"\n✓ 使用命令行指定方案 {profile_key}: {profile['name']}")
        print(f"  {profile['description']}")
    else:
        print("\n请选择压缩方案:")
        profile_key, profile = select_profile()
    
    # 确定输出目录
    if args.output:
        output_dir = args.output
        print(f"\n输出目录 (命令行): {output_dir}")
    else:
        # 自动生成输出目录名
        output_dir = os.path.join(
            os.path.dirname(input_dir),
            f"{os.path.basename(input_dir)}_compressed_{profile_key}_{profile['name']}"
        )
        # 清理目录名
        output_dir = output_dir.replace(" ", "_").replace("（", "(").replace("）", ")")
        print(f"\n输出目录 (自动生成): {output_dir}")
    
    # 测试模式
    test_mode = args.test
    test_count = args.test_count
    
    if not test_mode and not args.no_confirm:
        test_mode_input = input("\n是否启用测试模式？(只压缩前几个) [y/N]: ").strip().lower()
        if test_mode_input == 'y':
            test_mode = True
            test_count_input = input(f"  处理几个视频？(默认{test_count}): ").strip()
            if test_count_input:
                test_count = int(test_count_input)
    
    if test_mode:
        print(f"\n🧪 测试模式: 将处理前 {test_count} 个视频")
        print("确认效果后再进行完整压缩")
    
    # 确认开始
    if not args.no_confirm:
        print(f"\n{'=' * 80}")
        confirm = input("确认开始压缩？[y/N]: ").strip().lower()
        if confirm != 'y':
            print("\n❌ 已取消压缩")
            sys.exit(0)
    else:
        print(f"\n{'=' * 80}")
        print("⚡ 非交互模式，直接开始...")
    
    # 环境检查（包含FFmpeg vs PyNvVideoCodec对比）
    can_proceed, env_info = check_environment()
    if not can_proceed:
        print("\n❌ 环境检查未通过，无法继续")
        sys.exit(1)
    
    # ========================================
    # 验证压缩效果
    # ========================================
    print(f"\n{'=' * 80}")
    print("📋 压缩前验证")
    print(f"{'=' * 80}")
    
    # 选择最小的视频进行验证（节省时间）
    print("\n正在选择最小的视频进行验证测试...")
    video_sizes = [(f, os.path.getsize(f)) for f in video_files]
    video_sizes.sort(key=lambda x: x[1])
    smallest_video = video_sizes[0][0]
    
    print(f"选择测试视频: {os.path.basename(smallest_video)}")
    print(f"  大小: {format_size(os.path.getsize(smallest_video) / (1024 * 1024))}")
    
    # 创建临时输出目录
    temp_output_dir = os.path.join(output_dir, "_temp_validation")
    os.makedirs(temp_output_dir, exist_ok=True)
    
    # 执行验证
    is_worthwhile, orig_size, comp_size, saved_pct = validate_compression(
        smallest_video, profile, temp_output_dir
    )
    
    # 清理临时文件
    shutil.rmtree(temp_output_dir, ignore_errors=True)
    
    if not is_worthwhile:
        print(f"\n{'=' * 80}")
        print("❌ 压缩验证未通过")
        print(f"{'=' * 80}")
        print(f"\n建议:")
        print(f"  1. 当前方案 {profile_key} 压缩效果不佳")
        print(f"  2. 可以尝试更激进的方案:")
        if profile_key == 'A':
            print(f"     运行: python compress_videos.py -i \"{input_dir}\" -p B")
        elif profile_key == 'B':
            print(f"     运行: python compress_videos.py -i \"{input_dir}\" -p C")
        print(f"  3. 或者原视频已经高效编码，无需压缩")
        sys.exit(0)
    
    # 验证通过，显示预估结果
    print(f"\n{'=' * 80}")
    print("✅ 压缩验证通过！")
    print(f"{'=' * 80}")
    print(f"\n基于测试结果预估:")
    estimated_total_original = total_size
    estimated_total_compressed = total_size * (1 - saved_pct / 100)
    estimated_saved = total_size - estimated_total_compressed
    
    print(f"  原始总大小: {total_size:.2f} GB")
    print(f"  预估压缩后: {estimated_total_compressed:.2f} GB")
    print(f"  预估节省: {estimated_saved:.2f} GB ({saved_pct:.1f}%)")
    print()
    
    # 开始压缩
    start_time = time.time()
    result = compress_batch(video_files, profile, output_dir, test_mode, test_count)
    total_elapsed = time.time() - start_time
    
    # 最终统计
    print(f"\n⏱️ 总用时: {format_duration(total_elapsed)}")
    
    if test_mode and result['success'] > 0:
        print(f"\n💡 测试完成！")
        print(f"请检查输出目录: {output_dir}")
        print(f"如果满意效果，请再次运行此脚本，关闭测试模式进行完整压缩")
        print(f"  命令: python compress_videos.py -i \"{input_dir}\" -p {profile_key} --no-confirm")
    
    print(f"\n{'=' * 80}")
    print("✅ 全部完成！")
    print(f"{'=' * 80}")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断，已停止压缩")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
