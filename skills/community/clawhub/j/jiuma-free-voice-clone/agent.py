#!/usr/bin/env python3
"""
九马AI语音克隆技能 - 主脚本
输入文本和音频参考或音色ID，生成语音并返回URL
"""
import argparse
import json
import os
import sys
from pathlib import Path
from utils import jiuma_request, get_jiuma_api_key, output_result

# 常量定义
SUBMIT_API = "https://api.jiuma.com/api/voiceClone"
VOICES_API = "https://api.jiuma.com/api/describeVoices"
VOICES_CACHE_FILE = "voices.json"

# 支持的音频格式和MIME类型
MIME_TYPES = {
    '.mp3': 'audio/mpeg',
    '.wav': 'audio/wav',
    '.ogg': 'audio/ogg',
    '.m4a': 'audio/mp4',
    '.flac': 'audio/flac',
    '.aac': 'audio/aac',
    '.aiff': 'audio/aiff',
    '.opus': 'audio/opus',
    '.weba': 'audio/webm',
}

headers = {
    "X-Secret-Key": get_jiuma_api_key()
}


def load_voices_cache():
    """加载音色缓存文件"""
    cache_file = Path(__file__).parent / VOICES_CACHE_FILE
    if cache_file.exists():
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"警告: 加载音色缓存失败: {e}", file=sys.stderr)
    return None


def save_voices_cache(voices_data):
    """保存音色缓存文件"""
    cache_file = Path(__file__).parent / VOICES_CACHE_FILE
    try:
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(voices_data, f, ensure_ascii=False, indent=2)
        return True
    except IOError as e:
        print(f"警告: 保存音色缓存失败: {e}", file=sys.stderr)
        return False


def get_available_voices():
    """获取可用音色列表"""

    data, message = jiuma_request(VOICES_API, headers=headers)
    if not data:
        return
    return data


def check_and_load_voices():
    """检查并加载音色，如无则下载"""
    cached_voices = load_voices_cache()
    if cached_voices:
        return cached_voices

    print("本地音色缓存不存在，正在从API获取音色列表...", file=sys.stderr)
    voices = get_available_voices()
    if voices:
        if save_voices_cache(voices):
            print(f"已获取并保存 {len(voices)} 个音色", file=sys.stderr)
        return voices
    else:
        print("无法获取音色列表，请检查网络或API", file=sys.stderr)
        return None


def submit(text, sample_audio=None, timbre_id=None):
    """主函数：生成语音"""
    print(f"text: {text}, sample_audio: {sample_audio}, timbre_id: {timbre_id}", file=sys.stderr)

    # 生成语音
    if not text:
        output_result({
            "status": "error",
            "error": "missing_text",
            "message": "必须提供要转换的文本",
            "data": {}
        })
        return

    # 检查是否需要音色选择（没有提供音频或音色ID时）
    if not sample_audio and timbre_id == 0:
        # 先检查音色缓存
        voices = check_and_load_voices()
        if voices:
            print(f"提示: 没有指定音色，共有 {len(voices)} 个可用音色", file=sys.stderr)
            print("请使用 --timbre_id 参数指定音色ID，或使用 --sample_audio 指定参考音频", file=sys.stderr)
            print("使用 --list_voices 查看可用音色列表", file=sys.stderr)

        output_result({
            "status": "error",
            "error": "missing_source",
            "message": "必须提供参考音频或音色ID",
            "data": {}
        })
        return
    # 参数验证
    if not sample_audio and (timbre_id is None or timbre_id == 0):
        output_result({
            "status": "error",
            "error": 101,
            "message": "请提供参考音频或来自九马网站的音色ID",
            "data": {}
        })
        return
    audio_files = {}
    request_data = {
        "text": text
    }

    if sample_audio:
        # 检查文件是否存在
        if not os.path.exists(sample_audio):
            output_result({
                "status": "error",
                "error": "file_not_found",
                "message": f"音频文件不存在: {sample_audio}",
                "data": {}
            })
            return

        # 获取文件扩展名和MIME类型
        file_ext = os.path.splitext(sample_audio)[1].lower()
        content_type = MIME_TYPES.get(file_ext, 'application/octet-stream')
        audio_files = {'reference_audio': (os.path.basename(sample_audio), open(sample_audio, 'rb'), content_type)}
    else:
        request_data["timbre_id"] = timbre_id
    data, message = jiuma_request(SUBMIT_API, data=request_data, files=audio_files, headers=headers)
    if not data:
        return
    output_result({
        "status": "success",
        "message": "语音生成成功",
        "data": {
            "audio_url": data.get("audio_url", ""),
            "text": text,
            "source": "reference_audio" if sample_audio else "timbre_id"
        }
    })


def list_voices():
    """列出可用音色"""
    voices = check_and_load_voices()
    if voices:
        output_result({
            "status": "success",
            "message": f"找到 {len(voices)} 个可用音色",
            "data": {
                "voices": voices,
                "count": len(voices)
            }
        })
    else:
        output_result({
            "status": "error",
            "message": "无法获取音色列表",
            "data": {}
        })


def main():
    parser = argparse.ArgumentParser(description="九码AI语音克隆工具")

    # 主要参数组
    parser.add_argument('--text', type=str, default="", help="要转换为语音的文本内容")
    parser.add_argument('--sample_audio', type=str, default="", help="本地参考音频文件路径")
    parser.add_argument('--timbre_id', type=int, default=0, help="九马网站的音色ID")

    # 音色管理参数
    parser.add_argument('--list_voices', action='store_true', help="列出可用音色")
    parser.add_argument('--refresh_voices', action='store_true', help="刷新音色缓存")

    args = parser.parse_args()

    # 处理音色管理命令
    if args.list_voices:
        list_voices()
        return

    if args.refresh_voices:
        print("正在刷新音色缓存...", file=sys.stderr)
        voices = get_available_voices()
        if voices and save_voices_cache(voices):
            print(f"已刷新并保存 {len(voices)} 个音色", file=sys.stderr)
        else:
            print("刷新音色缓存失败", file=sys.stderr)
        return

    submit(args.text, args.sample_audio if args.sample_audio else None,
           args.timbre_id if args.timbre_id != 0 else None)


if __name__ == '__main__':
    main()
