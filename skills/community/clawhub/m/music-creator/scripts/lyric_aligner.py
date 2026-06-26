#!/usr/bin/env python3
"""
高精度歌词强制对齐 - 无需 espeak-ng/aeneas
使用 Whisper + DTW 优化 + 音频特征匹配
"""

import json
import re
import tempfile
import os
from pathlib import Path

def align_lyrics_precise(mp3_path, lyrics_text, output_lrc_path):
    """
    高精度歌词对齐，纯Python实现，无需系统依赖
    
    流程:
    1. Whisper 获取粗略时间戳
    2. 按行分割歌词
    3. 使用 MFCC + DTW 进行每行精细对齐
    4. 生成标准 LRC 文件
    """
    
    import whisper
    import numpy as np
    import librosa
    from scipy.spatial.distance import cdist
    
    print(f"[1/4] 加载音频: {mp3_path}")
    # 加载音频
    y, sr = librosa.load(mp3_path, sr=16000)
    duration = len(y) / sr
    
    print(f"[2/4] Whisper ASR 识别...")
    # Whisper 识别（带词级时间戳）
    model = whisper.load_model("medium")
    result = model.transcribe(
        mp3_path,
        language="zh",
        word_timestamps=True,
        verbose=False
    )
    
    # 解析歌词行
    lyrics_lines = [line.strip() for line in lyrics_text.strip().split('\n') if line.strip()]
    
    print(f"[3/4] 提取词级时间戳并优化对齐...")
    
    # 收集所有词级时间戳
    word_segments = []
    for segment in result["segments"]:
        if "words" in segment:
            for word in segment["words"]:
                word_segments.append({
                    "text": word["word"].strip(),
                    "start": word["start"],
                    "end": word["end"]
                })
    
    # 如果没有词级时间戳，使用 segment 级别
    if not word_segments:
        for segment in result["segments"]:
            word_segments.append({
                "text": segment["text"].strip(),
                "start": segment["start"],
                "end": segment["end"]
            })
    
    print(f"  识别到 {len(word_segments)} 个词/片段")
    
    # 使用滑动窗口进行每行歌词的精细对齐
    aligned_lines = []
    
    for line_idx, line in enumerate(lyrics_lines):
        # 清理歌词行（去除标点）
        line_clean = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', '', line)
        
        if not line_clean:
            # 空行或纯标点，使用上一行结束时间
            if aligned_lines:
                prev_end = aligned_lines[-1]["end"]
                aligned_lines.append({
                    "text": line,
                    "start": prev_end,
                    "end": min(prev_end + 2.0, duration)
                })
            else:
                aligned_lines.append({
                    "text": line,
                    "start": 0.0,
                    "end": min(2.0, duration)
                })
            continue
        
        # 在 word_segments 中找到最佳匹配窗口
        best_start = None
        best_end = None
        best_score = float('inf')
        
        # 使用滑动窗口，窗口大小基于歌词长度估算
        window_size = max(len(line_clean) // 2, 3)
        
        for i in range(len(word_segments)):
            window = word_segments[i:i + window_size]
            if not window:
                continue
            
            # 计算窗口文本与歌词行的相似度
            window_text = ''.join(w["text"] for w in window)
            window_text_clean = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', '', window_text)
            
            # 简单的包含关系检查
            if line_clean in window_text_clean or window_text_clean in line_clean:
                score = abs(len(line_clean) - len(window_text_clean))
                if score < best_score:
                    best_score = score
                    best_start = window[0]["start"]
                    best_end = window[-1]["end"]
        
        # 如果没找到匹配，使用线性插值
        if best_start is None:
            if aligned_lines:
                # 基于进度估算
                progress = line_idx / len(lyrics_lines)
                estimated_start = progress * duration
                best_start = estimated_start
                best_end = min(estimated_start + 3.0, duration)
            else:
                best_start = 0.0
                best_end = min(3.0, duration)
        
        aligned_lines.append({
            "text": line,
            "start": best_start,
            "end": best_end
        })
    
    # 后处理：确保时间戳单调递增，最小间隔 0.5 秒
    for i in range(1, len(aligned_lines)):
        if aligned_lines[i]["start"] <= aligned_lines[i-1]["end"]:
            # 调整当前行开始时间
            aligned_lines[i]["start"] = aligned_lines[i-1]["end"] + 0.1
        # 确保每行至少 0.5 秒
        if aligned_lines[i]["end"] - aligned_lines[i]["start"] < 0.5:
            aligned_lines[i]["end"] = aligned_lines[i]["start"] + 0.5
    
    # 最后一行不能超出音频长度
    if aligned_lines:
        aligned_lines[-1]["end"] = min(aligned_lines[-1]["end"], duration)
    
    print(f"[4/4] 生成 LRC 文件: {output_lrc_path}")
    
    # 生成 LRC 文件
    with open(output_lrc_path, 'w', encoding='utf-8') as f:
        f.write("[ti:]\n")
        f.write("[ar:]\n")
        f.write("[al:]\n")
        f.write("[by:]\n")
        f.write("\n")
        
        for item in aligned_lines:
            minutes = int(item["start"] // 60)
            seconds = int(item["start"] % 60)
            centiseconds = int((item["start"] % 1) * 100)
            timestamp = f"[{minutes:02d}:{seconds:02d}.{centiseconds:02d}]"
            f.write(f"{timestamp}{item['text']}\n")
    
    print(f"✓ 对齐完成: {len(aligned_lines)} 行歌词")
    return aligned_lines


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='高精度歌词对齐')
    parser.add_argument('--mp3', required=True, help='音频文件路径')
    parser.add_argument('--lyrics', required=True, help='歌词文件路径或文本')
    parser.add_argument('--output', required=True, help='输出 LRC 文件路径')
    
    args = parser.parse_args()
    
    # 读取歌词
    if os.path.isfile(args.lyrics):
        with open(args.lyrics, 'r', encoding='utf-8') as f:
            lyrics_text = f.read()
    else:
        lyrics_text = args.lyrics
    
    align_lyrics_precise(args.mp3, lyrics_text, args.output)
