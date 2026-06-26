#!/usr/bin/env python3
"""
ASR 歌词时序对齐工具

将 Whisper ASR 输出的 segment 时间戳与原始歌词文本对齐，
生成带精确时间信息的歌词 JSON。

用法：
  python3 align_lyrics.py \
    --asr /tmp/whisper-output/song.json \
    --lyrics /tmp/song-lyrics.txt \
    --duration 169.8 \
    --output /tmp/song-lyrics-timed.json

  # 也支持直接传 mp3 文件（自动运行 whisper）
  python3 align_lyrics.py \
    --mp3 /tmp/song.mp3 \
    --lyrics /tmp/song-lyrics.txt \
    --output /tmp/song-lyrics-timed.json
"""

import argparse
import json
import os
import re
import subprocess
import sys


def run_whisper(mp3_path, output_dir):
    """运行 whisper ASR"""
    os.makedirs(output_dir, exist_ok=True)
    cmd = [
        'whisper', mp3_path,
        '--model', 'tiny',
        '--language', 'zh',
        '--word_timestamps', 'True',
        '--output_format', 'json',
        '--output_dir', output_dir,
        '--device', 'cpu'
    ]
    print(f"🎵 Running ASR: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

    # 找到输出文件
    base = os.path.splitext(os.path.basename(mp3_path))[0]
    json_path = os.path.join(output_dir, f'{base}.json')
    if not os.path.exists(json_path):
        # whisper 有时会用不同命名
        for f in os.listdir(output_dir):
            if f.endswith('.json'):
                json_path = os.path.join(output_dir, f)
                break
    return json_path


def parse_lyrics_text(text):
    """解析纯文本歌词，返回 [(section_or_none, text), ...]"""
    lines = text.strip().split('\n')
    result = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # 检查是否是 section 标签
        m = re.match(r'^\[(.+?)\]$', line)
        if m:
            result.append(('section', m.group(1).strip()))
        else:
            result.append(('lyric', line))
    return result


def extract_asr_segments(asr_path):
    """从 ASR JSON 提取 segment 列表"""
    with open(asr_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    segments = []
    for seg in data.get('segments', []):
        segments.append({
            'start': seg['start'],
            'end': seg['end'],
            'text': seg['text'].strip()
        })
    return segments


def align_lyrics(lyrics_entries, asr_segments, total_duration=None):
    """
    将歌词行与 ASR segment 对齐。

    策略：按顺序匹配，利用 ASR 的 segment 时间作为歌词行的时间。
    - Section 标签继承下一段歌词的时间
    - 重复段（如 Chorus 出现多次）需要根据 ASR 时间位置正确分配
    """
    # 分离 section 标签和歌词行
    lyrics_lines = [e for e in lyrics_entries if e[0] == 'lyric']
    section_map = {}  # lyrics_line_index -> section_name

    current_section = 'Intro'
    lyric_idx = 0
    for entry_type, text in lyrics_entries:
        if entry_type == 'section':
            current_section = text
        else:
            section_map[lyric_idx] = current_section
            lyric_idx += 1

    num_lyrics = len(lyrics_lines)
    num_segments = len(asr_segments)

    if num_segments == 0:
        print("⚠️  No ASR segments found, using proportional timing")
        return proportional_timing(lyrics_entries, total_duration or 240)

    # 找出 ASR 中较大的停顿（>1.5s），这些通常是段落分隔
    pauses = []
    for i in range(1, num_segments):
        gap = asr_segments[i]['start'] - asr_segments[i-1]['end']
        if gap > 1.5:
            pauses.append((i, gap, asr_segments[i-1]['end'], asr_segments[i]['start']))

    # 将 ASR segments 分组（按停顿位置分割）
    groups = []
    group_start = 0
    for pause_idx, gap, _, _ in pauses:
        groups.append(asr_segments[group_start:pause_idx])
        group_start = pause_idx
    groups.append(asr_segments[group_start:])

    # 将歌词也按 section 分组
    lyrics_groups = []
    current_group_lines = []
    current_group_section = None
    for entry_type, text in lyrics_entries:
        if entry_type == 'section':
            if current_group_lines:
                lyrics_groups.append({
                    'section': current_group_section,
                    'lines': current_group_lines
                })
                current_group_lines = []
            current_group_section = text
        else:
            current_group_lines.append(text)
    if current_group_lines:
        lyrics_groups.append({
            'section': current_group_section,
            'lines': current_group_lines
        })

    # 对齐：将 ASR 组与歌词组按顺序匹配
    result = []
    seg_global_idx = 0  # 全局 segment 索引

    for g_idx, lyrics_group in enumerate(lyrics_groups):
        lines = lyrics_group['lines']
        section_name = lyrics_group['section']

        # 确定对应的 ASR segments
        # 每个 segment 大致对应一行歌词
        # 需要匹配的 segment 数量 = len(lines)
        needed = len(lines)
        available = num_segments - seg_global_idx

        if available <= 0:
            # ASR segments 用完了，用最后的时间 + 递增
            last_time = result[-1]['time'] if result else (total_duration or 169.8)
            result.append({'time': round(last_time, 1), 'text': section_name, 'isSection': True})
            for line in lines:
                last_time += 3.0
                result.append({'time': round(last_time, 1), 'text': line, 'isSection': False})
            continue

        # 取需要的 segments
        matched_segs = asr_segments[seg_global_idx:seg_global_idx + needed]
        if len(matched_segs) < needed:
            # segments 不够，补上剩余的
            matched_segs.extend([asr_segments[-1]] * (needed - len(matched_segs)))

        # Section 标签用第一个 segment 的时间
        first_time = matched_segs[0]['start']
        result.append({'time': round(first_time, 1), 'text': section_name, 'isSection': True})

        # 每行歌词用对应 segment 的时间
        for i, line in enumerate(lines):
            seg_time = matched_segs[i]['start'] if i < len(matched_segs) else first_time
            result.append({'time': round(seg_time, 1), 'text': line, 'isSection': False})

        seg_global_idx += needed

    return result


def proportional_timing(lyrics_entries, total_duration):
    """无 ASR 时按比例分配时间"""
    lyrics_lines = [e for e in lyrics_entries if e[0] == 'lyric']
    total_lines = len(lyrics_lines)
    if total_lines == 0:
        return []

    time_per_line = total_duration / total_lines
    result = []
    elapsed = 0.0
    current_section = 'Intro'

    for entry_type, text in lyrics_entries:
        if entry_type == 'section':
            current_section = text
            result.append({'time': round(elapsed, 1), 'text': text, 'isSection': True})
        else:
            result.append({'time': round(elapsed, 1), 'text': text, 'isSection': False})
            elapsed += time_per_line

    return result


def main():
    parser = argparse.ArgumentParser(description='ASR 歌词时序对齐工具')
    parser.add_argument('--asr', help='Whisper ASR 输出的 JSON 文件')
    parser.add_argument('--mp3', help='MP3 文件（自动运行 whisper）')
    parser.add_argument('--lyrics', required=True, help='纯文本歌词文件')
    parser.add_argument('--duration', type=float, default=None, help='歌曲时长（秒）')
    parser.add_argument('--output', required=True, help='输出 JSON 文件')

    args = parser.parse_args()

    # 获取 ASR 结果
    if args.asr:
        asr_path = args.asr
    elif args.mp3:
        output_dir = f'/tmp/whisper-{os.path.splitext(os.path.basename(args.mp3))[0]}'
        asr_path = run_whisper(args.mp3, output_dir)
    else:
        print("❌ 需要 --asr 或 --mp3 参数")
        sys.exit(1)

    # 获取时长
    if args.duration:
        total_duration = args.duration
    elif args.mp3:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', args.mp3],
            capture_output=True, text=True
        )
        total_duration = float(result.stdout.strip())
    else:
        total_duration = None

    # 解析歌词
    with open(args.lyrics, 'r', encoding='utf-8') as f:
        lyrics_text = f.read()
    lyrics_entries = parse_lyrics_text(lyrics_text)

    # 提取 ASR segments
    asr_segments = extract_asr_segments(asr_path)

    print(f"📝 歌词行数: {len([e for e in lyrics_entries if e[0] == 'lyric'])}")
    print(f"🎤 ASR 段数: {len(asr_segments)}")
    if total_duration:
        print(f"⏱️  时长: {total_duration:.1f}s")

    # 对齐
    result = align_lyrics(lyrics_entries, asr_segments, total_duration)

    # 输出
    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"✅ 歌词时序已保存: {args.output}")
    print(f"   条目数: {len(result)}")
    if result:
        print(f"   时间范围: {result[0]['time']}s - {result[-1]['time']}s")


if __name__ == '__main__':
    main()
