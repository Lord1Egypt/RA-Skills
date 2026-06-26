#!/usr/bin/env python3
"""
视频生成脚本 - 融合版
支持命令行参数和配置文件
"""
import argparse
import asyncio
import aiohttp
import subprocess
import json
import random
from pathlib import Path
import shutil

# 配置
SKILL_DIR = Path(__file__).parent.parent
WORK_DIR = Path(__file__).parent.parent.parent.parent.parent / "workspace-kaifa" / "quick-test"
OUTPUT_DIR = SKILL_DIR / "output"
BGM_DIR = WORK_DIR / "out"  # BGM 目录
IMAGE_DIR = SKILL_DIR / "temp_images"
OUTPUT_DIR.mkdir(exist_ok=True)
IMAGE_DIR.mkdir(exist_ok=True)

# Edge TTS 声音映射
VOICE_MAP = {
    "male": "zh-CN-YunxiNeural",
    "female": "zh-CN-XiaoxiaoNeural",
    "zh-CN-YunxiNeural": "zh-CN-YunxiNeural",
    "zh-CN-XiaoxiaoNeural": "zh-CN-XiaoxiaoNeural",
    "zh-CN-YunjianNeural": "zh-CN-YunjianNeural",
    "zh-CN-XiaoyiNeural": "zh-CN-XiaoyiNeural",
}

# 营销文案模板
MARKETING_TEMPLATES = {
    "电动车": [
        "安全好骑，续航长久！动力强劲，品质可靠！舒适耐用，性价比高！欢迎到店咨询体验！",
        "选电动车就选品牌货！大容量电池续航久，强劲动力爬坡易！安全可靠，舒适好骑！",
        "专注电动车多年！安全制动系统，舒适减震设计，超长续航里程！值得信赖！",
    ]
}

def parse_args():
    parser = argparse.ArgumentParser(description="抖音视频生成脚本")
    
    # 必填参数
    parser.add_argument("--images", nargs="+", help="图片路径列表")
    parser.add_argument("--output", type=str, default="video.mp4", help="输出文件路径")
    
    # 可选参数
    parser.add_argument("--config", type=str, help="配置文件路径")
    parser.add_argument("--captions", nargs="+", help="自定义字幕（逐行）")
    parser.add_argument("--style", type=str, default="brand", choices=["brand", "promo"], help="文案风格")
    parser.add_argument("--voice", type=str, default="male", help="配音声音")
    parser.add_argument("--speed", type=int, default=5, help="语速 (4-6)")
    parser.add_argument("--duration", type=int, default=0, help="视频时长 (0=自适应)")
    parser.add_argument("--bgm-volume", type=float, default=0.2, help="BGM 音量 (0-1)")
    parser.add_argument("--random-bgm", type=bool, default=True, help="随机 BGM")
    
    # 促销参数
    parser.add_argument("--price", type=str, help="价格")
    parser.add_argument("--promotion", type=str, help="促销活动")
    parser.add_argument("--contact", type=str, help="联系方式")
    
    return parser.parse_args()

def load_config(config_file):
    """加载配置文件"""
    if config_file and Path(config_file).exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def get_audio_duration(audio_file):
    """获取音频时长"""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(audio_file)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return float(result.stdout.strip())

async def generate_tts_baidu(text, output_file, speed=5):
    """百度 TTS 生成配音（备用方案）"""
    async with aiohttp.ClientSession() as session:
        tts_url = "https://fanyi.baidu.com/tts"
        params = {'text': text, 'lan': 'zh', 'spd': speed}
        
        try:
            async with session.get(tts_url, params=params) as response:
                if response.status == 200:
                    audio_data = await response.read()
                    with open(output_file, 'wb') as f:
                        f.write(audio_data)
                    print(f"✅ 百度 TTS 生成成功：{output_file}")
                    duration = get_audio_duration(output_file)
                    print(f"📊 音频时长：{duration:.2f}秒")
                    return duration
        except Exception as e:
            print(f"❌ 百度 TTS 错误：{e}")
    return None

async def generate_tts_edge(text, output_file, voice="male", rate="+0%"):
    """Edge TTS 生成配音"""
    voice_name = VOICE_MAP.get(voice, "zh-CN-YunxiNeural")
    
    cmd = [
        "edge-tts",
        "--voice", voice_name,
        "--text", text,
        "--rate", rate,
        "--write-media", str(output_file)
    ]
    
    try:
        print(f"🎤 正在生成 Edge TTS 配音 ({voice}声)...")
        subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=30)
        if output_file.exists():
            print(f"✅ Edge TTS 生成成功：{output_file} ({voice}声)")
            duration = get_audio_duration(output_file)
            print(f"📊 音频时长：{duration:.2f}秒")
            return duration
    except subprocess.TimeoutExpired:
        print("⚠️ Edge TTS 超时，切换到百度 TTS...")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Edge TTS 失败，切换到百度 TTS...")
    except Exception as e:
        print(f"⚠️ Edge TTS 错误：{e}，切换到百度 TTS...")
    
    # 备用方案：百度 TTS
    print("🎤 使用百度 TTS 生成配音...")
    speed = 5  # 百度 TTS 语速
    return await generate_tts_baidu(text, output_file, speed=speed)

def generate_script(args, config):
    """生成或获取脚本"""
    # 优先使用命令行提供的 captions
    if args.captions:
        script = "！".join(args.captions) + "！"
        print(f"📝 使用提供的文案")
        return script
    
    # 其次使用配置文件
    if config and 'script' in config:
        if config['script'].get('content'):
            print(f"📝 使用配置文件文案")
            return config['script']['content']
    
    # 最后自动生成
    if args.style == "brand":
        templates = MARKETING_TEMPLATES.get("电动车", MARKETING_TEMPLATES["电动车"])
        script = random.choice(templates)
        print(f"📝 自动生成品牌宣传文案")
        return script
    
    # promo 风格需要用户提供信息
    if args.style == "promo":
        if not args.price:
            print("⚠️ promo 风格需要提供 --price")
        script = f"店庆大促！{args.price or '优惠价'}！{args.promotion or '欢迎咨询'}！{args.contact or '到店体验'}！"
        print(f"📝 生成促销文案")
        return script
    
    return ""

def optimize_script(script, target_duration, speaking_speed=5.5):
    """优化脚本字数"""
    current_chars = len(script.replace("!", "").replace("。", ""))
    target_chars = int(target_duration * speaking_speed)
    
    print(f"📊 当前字数：{current_chars}字")
    print(f"📊 目标字数：{target_chars}字")
    
    if abs(current_chars - target_chars) < 10:
        return script
    
    if current_chars > target_chars:
        print("⚠️ 脚本过长，精简中...")
        script = script.replace("惊爆价", "价").replace("仅需", "")
    else:
        print("⚠️ 脚本过短，扩展中...")
        script = script.replace("！", "！品质保证！")
    
    return script

def create_subtitle_srt(text, duration, output_file):
    """创建逐行字幕 SRT"""
    sentences = text.replace("!", "!").replace("。", ".").split("！")
    sentences = [s.strip() for s in sentences if s.strip()]
    
    total_chars = len(text.replace("!", "").replace("。", ""))
    time_per_char = duration / total_chars if total_chars > 0 else 0
    
    with open(output_file, 'w', encoding='utf-8') as f:
        start_time = 0
        for i, sentence in enumerate(sentences, 1):
            sentence_duration = len(sentence) * time_per_char if time_per_char > 0 else 2
            end_time = start_time + sentence_duration
            
            start_str = format_srt_time(start_time)
            end_str = format_srt_time(end_time)
            
            f.write(f"{i}\n")
            f.write(f"{start_str} --> {end_str}\n")
            f.write(f"{sentence}！\n\n")
            
            start_time = end_time
    
    print(f"📝 字幕已生成：{output_file} ({len(sentences)} 句，逐行显示)")

def format_srt_time(seconds):
    """转换为 SRT 时间格式"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def download_bgm_from_url(url, output_file):
    """从 URL 下载 BGM（使用 requests）"""
    try:
        print(f"🌐 正在下载 BGM: {url}")
        import requests
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'audio/webm,audio/ogg,audio/wav,audio/*;q=0.9,application/ogg;q=0.7,audio/*;q=0.6,*/*;q=0.5',
        }
        response = requests.get(url, headers=headers, timeout=30, stream=True)
        if response.status_code == 200:
            with open(output_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            if output_file.exists():
                print(f"✅ BGM 下载成功：{output_file}")
                return output_file
        else:
            print(f"❌ HTTP 错误：{response.status_code}")
    except ImportError:
        print("⚠️ requests 库未安装，使用备用下载方式...")
        return download_bgm_from_url_urllib(url, output_file)
    except Exception as e:
        print(f"❌ BGM 下载失败：{e}")
    return None

def download_bgm_from_url_urllib(url, output_file):
    """备用下载方式（urllib）"""
    import urllib.request
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as response:
            with open(output_file, 'wb') as f:
                f.write(response.read())
        if output_file.exists():
            print(f"✅ BGM 下载成功：{output_file}")
            return output_file
    except Exception as e:
        print(f"❌ 备用下载失败：{e}")
    return None

def get_bgm_from_internet(config):
    """从网络获取 BGM（多来源）"""
    audio_cfg = config.get('audio', {}).get('bgm', {}) if config else {}
    
    if not audio_cfg.get('from_internet', False):
        return None
    
    # 免费 BGM 来源 - Pixabay（免版权，可商用）
    pixabay_songs = [
        # 轻快/愉悦
        "https://cdn.pixabay.com/download/audio/2022/03/10/audio_c8c8a73467.mp3",
        "https://cdn.pixabay.com/download/audio/2021/08/04/audio_06d9c008a2.mp3",
        "https://cdn.pixabay.com/download/audio/2021/08/09/audio_09e3f06a25.mp3",
        # 激励/积极
        "https://cdn.pixabay.com/download/audio/2022/01/18/audio_d0a13f69d2.mp3",
        "https://cdn.pixabay.com/download/audio/2021/09/06/audio_34a15df1a9.mp3",
        # 流行/时尚
        "https://cdn.pixabay.com/download/audio/2022/03/24/audio_c610232532.mp3",
        "https://cdn.pixabay.com/download/audio/2021/11/27/audio_c2a5e1ae35.mp3",
        # 电子/动感
        "https://cdn.pixabay.com/download/audio/2022/01/02/audio_12e1a4f3f3.mp3",
        "https://cdn.pixabay.com/download/audio/2021/10/25/audio_5e3e4d3f3e.mp3",
        # 温馨/柔和
        "https://cdn.pixabay.com/download/audio/2021/07/12/audio_4e3f3d3f3e.mp3",
        "https://cdn.pixabay.com/download/audio/2021/06/08/audio_3e3f3d3f3e.mp3",
    ]
    
    # 随机选择一个
    url = random.choice(pixabay_songs)
    output_file = BGM_DIR / f"internet_bgm_{random.randint(1000,9999)}.mp3"
    
    print(f"🎵 从 Pixabay 随机选择 BGM")
    return download_bgm_from_url(url, output_file)

def adjust_bgm_duration(bgm_file, target_duration, output_file):
    """调整 BGM 时长以匹配视频（留 0.5 秒余量）"""
    bgm_duration = get_audio_duration(bgm_file)
    
    # 添加 0.5 秒余量，确保 BGM 不会比视频短
    target_with_buffer = target_duration + 0.5
    
    print(f"🎵 BGM 原始时长：{bgm_duration:.2f}秒")
    print(f"🎵 目标时长：{target_duration:.2f}秒 (+0.5 秒余量)")
    
    if bgm_duration >= target_with_buffer:
        # BGM 足够长，裁剪
        print(f"✂️ 裁剪 BGM 从 {bgm_duration:.2f}秒 到 {target_with_buffer:.2f}秒")
        cmd = [
            "ffmpeg", "-y",
            "-i", str(bgm_file),
            "-t", str(target_with_buffer),
            "-c", "copy",
            str(output_file)
        ]
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            if output_file.exists():
                actual_duration = get_audio_duration(output_file)
                print(f"✅ BGM 裁剪完成：{actual_duration:.2f}秒")
                return output_file
        except subprocess.CalledProcessError as e:
            print(f"❌ BGM 裁剪失败：{e.stderr}")
    
    # BGM 太短，循环
    loop_count = int(target_with_buffer / bgm_duration) + 1
    print(f"🔁 循环 BGM {loop_count} 次 ({bgm_duration:.2f}秒 × {loop_count})")
    
    # 创建文件列表
    list_file = SKILL_DIR / "bgm_loop_list.txt"
    with open(list_file, 'w') as f:
        for _ in range(loop_count):
            f.write(f"file '{bgm_file}'\n")
    
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(list_file),
        "-t", str(target_with_buffer),
        "-c", "copy",
        str(output_file)
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        if output_file.exists():
            actual_duration = get_audio_duration(output_file)
            print(f"✅ BGM 循环完成：{actual_duration:.2f}秒")
            return output_file
    except subprocess.CalledProcessError as e:
        print(f"❌ BGM 循环失败：{e.stderr}")
    
    return None

def get_random_bgm(args, config, target_duration=0):
    """获取随机 BGM（支持网络和时长匹配）"""
    if not args.random_bgm:
        print("⚠️ 已禁用随机 BGM")
        return None
    
    # 1. 优先使用已下载的网络 BGM
    all_mp3 = list(BGM_DIR.glob("*.mp3"))
    internet_bgm_files = [f for f in all_mp3 if 'internet_bgm' in f.name.lower()]
    
    if internet_bgm_files:
        selected = random.choice(internet_bgm_files)
        print(f"🎵 使用已下载的网络 BGM: {selected.name}")
        # 调整时长
        adjusted_bgm = SKILL_DIR / "output" / "bgm_adjusted.mp3"
        return adjust_bgm_duration(selected, target_duration, adjusted_bgm)
    
    # 2. 尝试从网络下载
    audio_cfg = config.get('audio', {}).get('bgm', {}) if config else {}
    if audio_cfg.get('from_internet', False):
        internet_bgm = get_bgm_from_internet(config)
        if internet_bgm:
            adjusted_bgm = SKILL_DIR / "output" / "bgm_adjusted.mp3"
            return adjust_bgm_duration(internet_bgm, target_duration, adjusted_bgm)
    
    # 3. 使用本地 BGM（备用）
    bgm_files = [f for f in all_mp3 if 'tts' not in f.name.lower()]
    
    if not bgm_files:
        print("⚠️ 未找到 BGM 文件")
        return None
    
    selected = random.choice(bgm_files)
    print(f"🎵 使用本地 BGM: {selected.name}")
    
    if target_duration > 0:
        adjusted_bgm = SKILL_DIR / "output" / "bgm_adjusted.mp3"
        return adjust_bgm_duration(selected, target_duration, adjusted_bgm)
    
    return selected

def generate_video_ffmpeg(images, audio_file, bgm_file, subtitle_file, output_file, image_duration, config):
    """生成视频"""
    temp_dir = SKILL_DIR / "temp_frames"
    temp_dir.mkdir(exist_ok=True)
    
    video_cfg = config.get('video', {}) if config else {}
    width = video_cfg.get('width', 1080)
    height = video_cfg.get('height', 1920)
    
    print("🖼️ 正在处理图片...")
    for i, img in enumerate(images):
        output_img = temp_dir / f"frame_{i:03d}.jpg"
        cmd = [
            "ffmpeg", "-y",
            "-i", str(img),
            "-vf", f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=black",
            "-q:v", "2",
            str(output_img)
        ]
        subprocess.run(cmd, capture_output=True, check=True)
    
    list_file = SKILL_DIR / "images_list.txt"
    with open(list_file, 'w') as f:
        for i in range(len(images)):
            f.write(f"file '{temp_dir}/frame_{i:03d}.jpg'\n")
            f.write(f"duration {image_duration}\n")
        f.write(f"file '{temp_dir}/frame_{len(images)-1:03d}.jpg'\n")
    
    # 字幕样式
    subtitle_filter = (
        f"subtitles={str(subtitle_file).replace("'", "'\\\\''")}:force_style='"
        f"FontSize=24,FontName=Microsoft YaHei,Bold=-1,"
        f"PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BackColour=&HC0000000,"
        f"Outline=1,Shadow=2,Alignment=2,MarginV=50,BorderStyle=4'"
    )
    
    print("🎬 正在生成视频...")
    
    bgm_volume = config.get('audio', {}).get('bgm', {}).get('volume', 0.2) if config else 0.2
    
    if bgm_file and bgm_volume > 0:
        cmd = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0", "-i", str(list_file),
            "-i", str(audio_file),
            "-i", str(bgm_file),
            "-filter_complex",
            f"[0:v]{subtitle_filter}[v];[1:a]volume=1.0[tts];[2:a]volume={bgm_volume}[bgm];[tts][bgm]amix=inputs=2:duration=shortest:dropout_transition=2[a]",
            "-map", "[v]", "-map", "[a]",
            "-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart",
            "-shortest",
            str(output_file)
        ]
    else:
        cmd = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0", "-i", str(list_file),
            "-i", str(audio_file),
            "-vf", subtitle_filter,
            "-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart",
            str(output_file)
        ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ 视频生成成功：{output_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg 错误：{e.stderr}")
        return False
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

def copy_to_windows(output_file, config):
    """复制到 Windows"""
    if config:
        out_cfg = config.get('output', {})
        if not out_cfg.get('copyToWindows', True):
            return
        win_path = out_cfg.get('windowsPath', '/mnt/f/Desktop/aima/新建文件夹')
    else:
        win_path = '/mnt/f/Desktop/aima/新建文件夹'
    
    win_dir = Path(win_path)
    if win_dir.exists():
        shutil.copy(output_file, win_dir / output_file.name)
        print(f"✅ 已复制到 Windows: {win_dir / output_file.name}")

async def main():
    args = parse_args()
    config = load_config(args.config)
    
    print("=" * 60)
    print("🎬 抖音视频生成脚本 - 融合版")
    print("=" * 60)
    
    # 获取图片
    images = []
    if args.images:
        images = [Path(p) for p in args.images if Path(p).exists()]
    elif config and 'images' in config:
        images = [Path(p) for p in config['images'] if Path(p).exists()]
    
    print(f"📸 找到 {len(images)} 张图片")
    
    if not images:
        print("❌ 未找到图片！")
        return
    
    # 生成/获取脚本
    script = generate_script(args, config)
    print(f"📝 文案字数：{len(script)}字")
    
    # 计算目标时长
    speaking_speed = args.speed if args.speed else 5.5
    target_duration = len(script) / speaking_speed
    
    if args.duration > 0:
        target_duration = args.duration
    elif config and 'duration' in config:
        target_duration = config['duration'].get('minSeconds', 15)
    
    target_duration = max(15, min(target_duration, 60))
    print(f"⏱️  目标时长：{target_duration:.2f}秒")
    
    # 优化脚本
    script = optimize_script(script, target_duration, speaking_speed)
    
    # 生成 TTS
    audio_file = SKILL_DIR / "output" / "tts.mp3"
    print("\n🎤 正在生成配音...")
    
    rate = f"+{(args.speed - 5) * 20}%"
    audio_duration = await generate_tts_edge(script, audio_file, voice=args.voice, rate=rate)
    
    if not audio_duration:
        print("❌ TTS 生成失败")
        return
    
    # 计算图片展示时长
    image_duration = audio_duration / len(images)
    print(f"📊 每张图片展示：{image_duration:.2f}秒")
    
    # 生成字幕
    subtitle_file = SKILL_DIR / "output" / "subtitle.srt"
    create_subtitle_srt(script, audio_duration, subtitle_file)
    
    # 获取 BGM（带时长匹配）
    bgm_file = get_random_bgm(args, config, target_duration=audio_duration)
    
    # 生成视频
    output_file = SKILL_DIR / "output" / args.output
    print("\n🎬 正在生成视频...")
    success = generate_video_ffmpeg(images, audio_file, bgm_file, subtitle_file, output_file, image_duration, config)
    
    if not success:
        print("❌ 视频生成失败")
        return
    
    # 复制到 Windows
    copy_to_windows(output_file, config)
    
    # 输出结果
    size = output_file.stat().st_size / 1024 / 1024
    print("\n" + "=" * 60)
    print("✅ 生成完成！")
    print("=" * 60)
    print(f"📹 视频：{output_file}")
    print(f"📊 大小：{size:.2f} MB")
    print(f"⏱️  时长：{audio_duration:.2f}秒")
    print(f"🎤 配音：{args.voice}声")
    print(f"🎵 BGM: {'已添加' if bgm_file else '未添加'}")
    print(f"📝 字幕：逐行显示")

if __name__ == "__main__":
    asyncio.run(main())
