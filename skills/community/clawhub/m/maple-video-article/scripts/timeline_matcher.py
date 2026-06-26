#!/usr/bin/env python3
"""
时间轴匹配脚本：将视频帧截图与SRT字幕按时间轴自动匹配。

用法：
    python timeline_matcher.py --frames-dir "<帧截图目录>" --srt "<SRT文件路径>" --max-images 8

功能：
1. 解析帧截图文件名中的时间戳 (格式：视频名_00h01m30s_0003.jpg)
2. 解析SRT字幕文件的所有时间段
3. 将每张图片匹配到最近的字幕段落（15秒误差内）
4. 输出JSON格式的配对结果
5. 筛选出均匀分布在时间轴上的代表性图片
"""

import os
import re
import json
import argparse
from pathlib import Path


def parse_frame_timestamp(filename: str) -> float | None:
    """
    从帧截图文件名中提取时间戳（秒）。
    格式：视频名_00h01m30s_0003.jpg
    """
    match = re.search(r'_(\d{2})h(\d{2})m(\d{2})s', filename)
    if not match:
        return None
    h, m, s = int(match.group(1)), int(match.group(2)), int(match.group(3))
    return float(h * 3600 + m * 60 + s)


def parse_srt_time(time_str: str) -> float:
    """
    解析SRT时间格式为秒数。
    格式：00:02:15,000
    """
    time_str = time_str.strip()
    match = re.match(r'(\d{2}):(\d{2}):(\d{2}),(\d{3})', time_str)
    if not match:
        return 0.0
    h = int(match.group(1))
    m = int(match.group(2))
    s = int(match.group(3))
    ms = int(match.group(4))
    return h * 3600 + m * 60 + s + ms / 1000.0


def parse_srt(srt_path: str) -> list[dict]:
    """
    解析SRT字幕文件，返回字幕块列表。
    每个字幕块包含：start_sec, end_sec, text
    """
    with open(srt_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # SRT块分割：序号、时间轴、文本、空行
    blocks = re.split(r'\n\n+', content.strip())
    subtitles = []

    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) < 3:
            continue

        # 第二行是时间轴：00:00:32,000 --> 00:00:38,000
        time_match = re.match(
            r'(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})',
            lines[1]
        )
        if not time_match:
            continue

        start_sec = parse_srt_time(time_match.group(1))
        end_sec = parse_srt_time(time_match.group(2))
        text = ' '.join(lines[2:]).strip()

        subtitles.append({
            'start_sec': start_sec,
            'end_sec': end_sec,
            'text': text
        })

    return subtitles


def match_frames_to_subtitles(
    frames_dir: str,
    srt_path: str,
    max_images: int = 8,
    tolerance_sec: int = 15
) -> list[dict]:
    """
    将帧截图与字幕按时间轴匹配。

    Args:
        frames_dir: 帧截图目录
        srt_path: SRT字幕文件路径
        max_images: 最终筛选的图片数量（均匀分布）
        tolerance_sec: 时间匹配容忍秒数

    Returns:
        配对结果列表，包含图片路径、时间戳、对应字幕
    """
    # 1. 收集所有帧截图
    frames_dir = Path(frames_dir)
    frame_files = []
    for f in frames_dir.iterdir():
        if f.suffix.lower() in ('.jpg', '.jpeg', '.png', '.webp'):
            ts = parse_frame_timestamp(f.name)
            if ts is not None:
                frame_files.append({'path': str(f), 'timestamp_sec': ts})

    if not frame_files:
        print(f"[ERROR] 未找到带时间戳的帧截图: {frames_dir}")
        return []

    # 按时间排序
    frame_files.sort(key=lambda x: x['timestamp_sec'])
    total_duration = frame_files[-1]['timestamp_sec']

    print(f"[INFO] 找到 {len(frame_files)} 张帧截图")
    print(f"[INFO] 视频总时长: {total_duration // 60}分{total_duration % 60}秒")

    # 2. 解析字幕
    subtitles = parse_srt(srt_path)
    if not subtitles:
        print(f"[ERROR] 未解析到有效字幕: {srt_path}")
        return []

    print(f"[INFO] 找到 {len(subtitles)} 条字幕")

    # 3. 匹配：每张图片找到最合适的字幕
    results = []
    for frame in frame_files:
        frame_ts = frame['timestamp_sec']
        
        # 首先找到包含图片时间戳的字幕段
        best_sub = None
        for sub in subtitles:
            if sub['start_sec'] <= frame_ts <= sub['end_sec']:
                best_sub = sub
                break
        
        # 如果没有找到包含的，则找时间上最接近的字幕
        if not best_sub:
            best_diff = float('inf')
            for sub in subtitles:
                # 计算图片时间与字幕开始时间的差距
                diff_start = abs(frame_ts - sub['start_sec'])
                diff_end = abs(frame_ts - sub['end_sec'])
                diff = min(diff_start, diff_end)
                if diff < best_diff and diff <= tolerance_sec:
                    best_diff = diff
                    best_sub = sub
        
        # 如果找到匹配的字幕
        if best_sub:
            # 计算精确的时间差
            diff = abs(frame_ts - best_sub['start_sec'])
            
            # 格式化时间字符串（用于显示）
            start_h = int(best_sub['start_sec'] // 3600)
            start_m = int((best_sub['start_sec'] % 3600) // 60)
            start_s = int(best_sub['start_sec'] % 60)
            start_ms = int((best_sub['start_sec'] % 1) * 1000)
            
            end_h = int(best_sub['end_sec'] // 3600)
            end_m = int((best_sub['end_sec'] % 3600) // 60)
            end_s = int(best_sub['end_sec'] % 60)
            end_ms = int((best_sub['end_sec'] % 1) * 1000)
            
            srt_time_str = f"{start_h:02d}:{start_m:02d}:{start_s:02d},{start_ms:03d} --> {end_h:02d}:{end_m:02d}:{end_s:02d},{end_ms:03d}"
        else:
            srt_time_str = ''
            diff = tolerance_sec + 1
        
        # 格式化图片时间戳字符串
        frame_h = int(frame_ts // 3600)
        frame_m = int((frame_ts % 3600) // 60)
        frame_s = int(frame_ts % 60)
        
        results.append({
            'image': os.path.basename(frame['path']),
            'image_path': frame['path'],
            'timestamp_sec': frame_ts,
            'timestamp_str': f"{frame_h:02d}h{frame_m:02d}m{frame_s:02d}s",
            'subtitle_text': best_sub['text'] if best_sub else '',
            'srt_time': srt_time_str,
            'has_match': best_sub is not None,
            'selected': False
        })

    # 4. 筛选出均匀分布的N张图片（用于文章配图）
    matched = [r for r in results if r['has_match']]
    if not matched:
        print("[WARN] 没有任何图片成功匹配到字幕")
        return results

    if len(matched) <= max_images:
        for r in matched:
            r['selected'] = True
    else:
        # 均匀采样
        step = len(matched) / max_images
        for i in range(max_images):
            idx = int(i * step)
            matched[idx]['selected'] = True

    selected_count = sum(1 for r in results if r['selected'])
    matched_count = sum(1 for r in results if r['has_match'])
    print(f"[INFO] 匹配成功: {matched_count}/{len(results)} 张图片")
    print(f"[INFO] 已筛选: {selected_count} 张用于文章配图")

    return results


def main():
    parser = argparse.ArgumentParser(description='时间轴匹配：帧截图与SRT字幕自动配对')
    parser.add_argument('--frames-dir', required=True, help='帧截图目录')
    parser.add_argument('--srt', required=True, help='SRT字幕文件路径')
    parser.add_argument('--max-images', type=int, default=8, help='筛选的配图数量（默认8）')
    parser.add_argument('--tolerance', type=int, default=15, help='时间匹配容忍秒数（默认15）')
    parser.add_argument('--output', default=None, help='输出JSON文件路径（默认打印到stdout）')

    args = parser.parse_args()

    results = match_frames_to_subtitles(
        frames_dir=args.frames_dir,
        srt_path=args.srt,
        max_images=args.max_images,
        tolerance_sec=args.tolerance
    )

    output_json = json.dumps(results, ensure_ascii=False, indent=2)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output_json)
        print(f"[INFO] 结果已保存: {args.output}")
    else:
        print("\n" + output_json)


if __name__ == '__main__':
    main()
