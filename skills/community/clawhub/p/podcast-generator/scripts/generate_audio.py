#!/usr/bin/env python3
"""Generate audio from podcast script via edge-tts."""

import argparse, json, os, re, subprocess, sys

VOICE_A = "zh-CN-XiaoxiaoNeural"  # Female
VOICE_B = "zh-CN-YunxiNeural"     # Male


def parse(text):
    segs, speaker, buf = [], None, []
    for line in text.split("\n"):
        line = line.strip()
        if not line or line.startswith("#") or line == "---":
            if buf and speaker:
                segs.append({"speaker": speaker, "text": " ".join(buf)})
                buf = []
            continue
        m = re.match(r'\*\*(.+?)\*\*:\s*(.*)', line)
        if m:
            if buf and speaker:
                segs.append({"speaker": speaker, "text": " ".join(buf)})
                buf = []
            speaker = m.group(1)
            if m.group(2).strip():
                buf.append(m.group(2).strip())
        else:
            if line.startswith("- **") or line.startswith("*"):
                continue
            buf.append(line)
            if not speaker:
                speaker = "主播"
    if buf and speaker:
        segs.append({"speaker": speaker, "text": " ".join(buf)})
    return segs


def voice_for(speaker, custom=None):
    if custom:
        return custom
    return VOICE_B if "B" in speaker else VOICE_A


def synth(segs, output, custom_voice=None):
    has_tts = os.system("which edge-tts >/dev/null 2>&1") == 0
    if not has_tts:
        print("⚠️ edge-tts 未安装，运行: pip install edge-tts")
        print(f"📝 共 {len(segs)} 个片段待转换")
        for s in segs:
            print(f"  [{s['speaker']}] {s['text'][:50]}...")
        return {"segments": len(segs), "output": None, "error": "edge-tts not installed"}

    tmps = []
    for i, s in enumerate(segs):
        if not s["text"].strip():
            continue
        tmp = f"/tmp/pod_{i:03d}.mp3"
        v = voice_for(s["speaker"], custom_voice)
        try:
            subprocess.run(
                ["edge-tts", "--voice", v, "--text", s["text"], "--write-media", tmp],
                capture_output=True, timeout=60, check=True
            )
            tmps.append(tmp)
        except Exception as e:
            print(f"⚠️ 片段{i}失败: {e}")

    if not tmps:
        return {"segments": len(segs), "output": None, "error": "no segments generated"}

    has_ffmpeg = os.system("which ffmpeg >/dev/null 2>&1") == 0
    if has_ffmpeg and len(tmps) > 1:
        lst = "/tmp/pod_list.txt"
        with open(lst, "w") as f:
            for t in tmps:
                f.write(f"file '{t}'\n")
        subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", output],
                       capture_output=True, timeout=120)
    elif tmps:
        import shutil
        shutil.copy2(tmps[0], output)

    # Cleanup
    for t in tmps:
        try:
            os.remove(t)
        except:
            pass

    ok = os.path.exists(output)
    return {"segments": len(segs), "output": output if ok else None, "success": ok}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--script", required=True)
    p.add_argument("--voice", default=None)
    p.add_argument("--output", default="podcast.mp3")
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()

    text = open(a.script, encoding="utf-8").read()
    segs = parse(text)
    if not segs:
        print("Error: 未找到内容片段", file=sys.stderr)
        sys.exit(1)

    print(f"📝 解析到 {len(segs)} 个片段")
    if a.dry_run:
        for s in segs:
            print(f"  [{s['speaker']}] {s['text'][:60]}...")
        sys.exit(0)

    print("🎙️ 生成音频中...")
    r = synth(segs, a.output, a.voice)
    print(json.dumps(r, indent=2, ensure_ascii=False))
    if r.get("output"):
        print(f"\n✅ 音频: {r['output']}")
