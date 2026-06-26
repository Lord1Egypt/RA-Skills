#!/usr/bin/env python3
"""
Patch poker_clipper.py to:
1. Load hooks from clips_analysis.json
2. Overlay hook text on first 3 seconds in top black area of each clip
3. Generate a publish-ready report
"""
import json, re, subprocess, sys
from pathlib import Path

WORKDIR = Path(__file__).parent.parent.parent  # dynamic
OUT = WORKDIR / 'clips'

# Canvas geometry (must match poker_clipper.py)
CW, CH = 1080, 1920
VH = 607
VY = (CH - VH) // 2  # 656
SUB_Y = VY + VH + 120  # 1383
HOOK_Y = VY // 2  # 328 — center of top black area

def ass_time(t):
    h = int(t // 3600); m = int((t % 3600) // 60)
    s = int(t % 60); cs = int(round((t % 1) * 100))
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def wrap(text, mx=22):
    words = text.strip().split(); lines = []; cur = ""
    for w in words:
        if len(cur) + len(w) + (1 if cur else 0) <= mx:
            cur = (cur + " " + w).strip()
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return "\\N".join(lines[:3])

def build_ass_with_hook(segs, s0, dur, num, hook_text):
    """Build ASS with two styles: subtitle in bottom black, hook in top black."""
    ap = OUT / f"clip_{num:02d}.ass"

    # Two styles:
    # Sub: bottom black area, small-medium font
    # Hook: top black area, large bold font, shown only first 3s
    style_sub  = "Sub,Arial,44,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,2,0,5,0,0,0,1"
    style_hook = "Hook,Arial,52,&H00FFFFFF,&H000000FF,&H00000000,&HB4000000,-1,0,0,0,100,100,0,0,1,3,0,5,0,0,0,1"

    hdr = (
        "[Script Info]\n"
        "ScriptType: v4.00+\n"
        f"PlayResX: {CW}\n"
        f"PlayResY: {CH}\n"
        "ScaledBorderAndShadow: yes\n\n"
        "[V4+ Styles]\n"
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
        f"Style: {style_sub}\n"
        f"Style: {style_hook}\n\n"
        "[Events]\n"
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    )

    events = []

    # Hook overlay: first 3 seconds, fixed at top black area center
    hook_wrapped = wrap(hook_text, mx=22)
    hook_pos = '{\\pos(' + str(CW // 2) + ',' + str(HOOK_Y) + ')}'
    events.append(f"Dialogue: 1,{ass_time(0)},{ass_time(min(3.0, dur))},Hook,,0,0,0,,{hook_pos}{hook_wrapped}")

    # Subtitles: fixed at SUB_Y in bottom black area
    for seg in segs:
        if seg['end'] < s0 or seg['start'] > s0 + dur:
            continue
        ts = max(0, seg['start'] - s0)
        te = min(dur, seg['end'] - s0)
        if te <= ts:
            continue
        wrapped = wrap(seg['text'], mx=18)
        sub_pos = '{\\pos(' + str(CW // 2) + ',' + str(SUB_Y) + ')}'
        events.append(f"Dialogue: 0,{ass_time(ts)},{ass_time(te)},Sub,,0,0,0,,{sub_pos}{wrapped}")

    ap.write_text(hdr + "\n".join(events) + "\n", encoding='utf-8')
    return ap


def recut_with_hooks():
    """Re-cut all clips using hooks from clips_analysis.json."""
    analysis = json.loads((OUT / 'clips_analysis.json').read_text(encoding='utf-8'))
    hooks = {c['clip_number']: c.get('hook_v2', c.get('title', '')) for c in analysis}

    # Find transcript and video
    transcripts = [f for f in OUT.glob('*_transcript.json') if 'reference' not in f.name]
    if not transcripts:
        print('No transcript found'); return
    segs = json.loads(transcripts[0].read_text(encoding='utf-8'))

    downloads = WORKDIR / 'downloads'
    mp4s = [f for f in downloads.glob('*.mp4') if 'reference' not in f.name]
    if not mp4s:
        print('No source video found'); return
    vp = max(mp4s, key=lambda p: p.stat().st_mtime)
    print(f'Source: {vp.name}')

    done = []
    for clip in analysis:
        n = clip['clip_number']
        s0 = clip['start_seconds']
        e0 = clip['end_seconds']
        dur = e0 - s0
        hook = hooks.get(n, '')
        slug = re.sub(r'[^\w\s-]', '', clip['title'])[:55].strip()
        mp4 = OUT / f"clip_{n:02d}_{slug}.mp4"

        ass = build_ass_with_hook(segs, s0, dur, n, hook)
        ass_esc = str(ass).replace('\\', '/').replace(':', '\\:')

        vf = (
            f"[0:v]scale={CW}:-2[sc];"
            f"[sc]pad={CW}:{CH}:(ow-iw)/2:(oh-ih)/2:black[pad];"
            f"[pad]ass='{ass_esc}'"
        )
        cmd = ['ffmpeg', '-y', '-ss', str(s0), '-i', str(vp), '-t', str(dur),
               '-filter_complex', vf, '-s', f'{CW}x{CH}',
               '-c:v', 'libx264', '-crf', '23', '-preset', 'fast',
               '-c:a', 'aac', '-b:a', '128k', str(mp4)]

        print(f"  [{n}] {hook[:60]}")
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print(f'      [WARN] {r.stderr[-200:]}')
        else:
            done.append(mp4)
            print(f'      OK ({dur:.0f}s)')

    # Publish report
    report = []
    for clip in analysis:
        report.append({
            'clip': clip['clip_number'],
            'file': f"clip_{clip['clip_number']:02d}_{re.sub(chr(91)+r'^\w\s-'+chr(93), '', clip['title'])[:55].strip()}.mp4",
            'youtube_title': clip.get('yt_title', clip['title']),
            'hook': clip.get('hook_v2', ''),
            'tags': clip.get('yt_desc', ''),
            'duration': round(clip['end_seconds'] - clip['start_seconds'], 1),
        })
    rp = OUT / 'publish_report.json'
    rp.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'\nDone! {len(done)} clips. Publish report: {rp.name}')
    for r in report:
        print(f"  [{r['clip']}] {r['youtube_title']}")
        print(f"        {r['tags']}")


if __name__ == '__main__':
    recut_with_hooks()
