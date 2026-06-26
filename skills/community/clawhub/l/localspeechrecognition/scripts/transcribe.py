#!/usr/bin/env python3
"""本地语音识别脚本 - 优化版，模型缓存+错误处理"""

import os
import sys

# 模型缓存（全局变量）
_cached_model = None

def get_model():
    """获取或加载模型（带缓存）"""
    global _cached_model
    if _cached_model is not None:
        return _cached_model
    
    from faster_whisper import WhisperModel
    print("首次加载模型中...")
    _cached_model = WhisperModel(
        "base", 
        device="auto", 
        compute_type="int8"
    )
    return _cached_model

def transcribe(audio_file, language="zh"):
    """转录音频文件"""
    # 检查文件存在
    if not os.path.exists(audio_file):
        return f"错误：文件不存在: {audio_file}"
    
    # 检查文件大小（25MB限制）
    file_size = os.path.getsize(audio_file)
    if file_size > 25 * 1024 * 1024:
        return f"错误：文件过大({file_size/1024/1024:.1f}MB)，最大25MB"
    
    # 检查格式
    ext = os.path.splitext(audio_file)[1].lower()
    if ext not in ['.ogg', '.m4a', '.mp3', '.wav']:
        return f"错误：不支持的格式{ext}，支持.ogg/.m4a/.mp3/.wav"
    
    try:
        model = get_model()
        print(f"正在转录: {audio_file}")
        
        segments, info = model.transcribe(
            audio_file, 
            language=language if language != "auto" else None,
            beam_size=1,
            vad_filter=True,
        )
        
        print(f"检测到语言: {info.language} (概率: {info.language_probability:.2f})")
        
        text = "".join(seg.text.strip() for seg in segments)
        return text if text else "（未能识别出文字）"
        
    except Exception as e:
        return f"错误：{str(e)}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 transcribe.py <audio_file> [language]")
        print("language: zh(默认)/en/ja/auto")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else "zh"
    
    result = transcribe(audio_file, language)
    print("=" * 50)
    print("转录结果:")
    print(result)
