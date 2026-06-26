#!/usr/bin/env python3
"""
将 SRT 字幕转换为 ASS 格式，支持：
- 儿童字体（圆体/Noto Sans CJK）
- 彩色文字（暖黄色，温馨感）
- 描边阴影（清晰可读）
- 长文本自动拆分（拆分 Dialogue 条目，确保 ffmpeg 正确渲染）
"""

import re
import sys
import os


def parse_srt(srt_path):
    with open(srt_path, 'r', encoding='utf-8') as f:
        content = f.read()
    segments = []
    for block in re.split(r'\n\n+', content.strip()):
        lines = block.strip().split('\n')
        if len(lines) >= 3:
            m = re.match(r'(\d{2}):(\d{2}):(\d{2}),(\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2}),(\d{3})', lines[1])
            if m:
                g = m.groups()
                start = int(g[0])*3600 + int(g[1])*60 + int(g[2]) + int(g[3])/1000
                end = int(g[4])*3600 + int(g[5])*60 + int(g[6]) + int(g[7])/1000
                text = '\n'.join(lines[2:]).strip()
                segments.append((start, end, text))
    return segments


def split_long_text(start, end, text, max_chars=24):
    """将长文本拆分为多个 Dialogue 条目，每条不超过 max_chars 字符。
    
    使用拆分时间条目的方式（而非反斜杠N），确保 ffmpeg ASS 渲染器正确处理。
    1920宽 × 80号中文字 ≈ 一行最多 24 个字符。
    """
    if len(text) <= max_chars:
        return [(start, end, text)]
    
    entries = []
    remaining = text
    total_dur = end - start
    
    while remaining:
        if len(remaining) <= max_chars:
            entries.append((start, end, remaining))
            break
        
        # 在不超过 max_chars 的范围内找最右标点
        split_idx = None
        for punct in ['，', '。', '！', '？', '、', ',', '.', '!', '?']:
            idx = remaining.rfind(punct, 0, max_chars + 1)  # +1 因为 rfind end 是开区间
            if idx > 0:  # 找到任何正位置的标点都行
                split_idx = idx + 1
                break
        
        if split_idx is None:
            mid = len(remaining) // 2
            for punct in ['，', '。', '！', '？', '、', ',', '.', '!', '?', ' ']:
                idx = remaining.rfind(punct, 0, mid + 5)
                if idx > max_chars // 2:
                    split_idx = idx + 1
                    break
        
        if split_idx is None:
            split_idx = max_chars
        
        line = remaining[:split_idx].rstrip()
        remaining = remaining[split_idx:].lstrip()
        
        # 按比例分配时间
        char_ratio = len(line) / (len(line) + len(remaining)) if remaining else 1.0
        line_dur = total_dur * char_ratio
        line_end = start + line_dur
        entries.append((start, line_end, line))
        start = line_end
        total_dur = end - line_end
    
    return entries


def srt_to_ass(srt_path, ass_path, width=1920, height=1080, font_size=80):
    segments = parse_srt(srt_path)
    
    scale = min(width, height) / 1080.0
    outline_w = max(2, round(3 * scale))
    shadow_w = max(2, round(2 * scale))
    margin_v = max(40, int(80 * scale))
    margin_lr = max(30, int(60 * scale))
    
    font_name = "Noto Sans CJK SC"
    font_paths = [
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc',
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
    ]
    font_path = None
    for fp in font_paths:
        if os.path.exists(fp):
            font_path = fp
            break
    
    ass = f"""[Script Info]
Title: 琪琪的魔法故事屋
ScriptType: v4.00+
PlayResX: {width}
PlayResY: {height}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{font_name},{font_size},&H00FFE4B5,&H000000FF,&H00332211,&H80000000,0,0,0,0,100,100,0,0,1,{outline_w},{shadow_w},2,{margin_lr},{margin_lr},{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    
    for start, end, text in segments:
        start_str = format_ass_time(start)
        end_str = format_ass_time(end)
        text = text.replace('"', "'")
        
        # 长文本拆分为多个 Dialogue 条目
        entries = split_long_text(start, end, text)
        for s, e, line in entries:
            ass += f"Dialogue: 0,{format_ass_time(s)},{format_ass_time(e)},Default,,0,0,0,,{line}\n"
    
    with open(ass_path, 'w', encoding='utf-8') as f:
        f.write(ass)
    
    print(f"✅ ASS 字幕已生成: {ass_path}")
    print(f"   字体: {font_name}, 字号: {font_size}, 颜色: 暖黄 #FFE4B5")
    print(f"   描边: {outline_w}px, 阴影: {shadow_w}px, 底部边距: {margin_v}px")


def format_ass_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int((seconds % 1) * 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--srt", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--width", type=int, default=1920)
    p.add_argument("--height", type=int, default=1080)
    p.add_argument("--font-size", type=int, default=80, help="字幕字号 (默认 80)")
    args = p.parse_args()
    srt_to_ass(args.srt, args.output, args.width, args.height, args.font_size)


if __name__ == "__main__":
    main()
