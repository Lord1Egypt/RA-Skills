#!/usr/bin/env python3
"""Build out/subtitles.srt that matches the final timeline.

Modes
  script   (default) timings spread over each scene's narration by word length and punctuation. Needs no extra
           software; accurate to roughly a fraction of a second.
  whisper  transcribe each scene's audio with faster-whisper (pip install faster-whisper) for real word timings.
           The text is what Whisper heard, so proofread names and numbers.

Usage: subtitles.py PROJECT_DIR [--mode script|whisper] [--model small] [--max-words 8] [--max-chars 42] [--out PATH]
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as c  # noqa: E402


def script_words(scene, start, dur, pad):
    toks = re.findall(r"\S+", re.sub(r"\[[^\]]*\]", " ", scene.get("narration", "")))
    if not toks:
        return []
    span = max(dur - pad, dur * 0.5)
    weights = []
    for t in toks:
        w = len(t) + 2
        if re.search(r"[.!?…]$", t):
            w += 6
        elif re.search(r"[,;:]$", t):
            w += 3
        weights.append(w)
    total = sum(weights)
    out, cur = [], start
    for t, w in zip(toks, weights):
        step = span * w / total
        out.append((cur, cur + step, t))
        cur += step
    return out


def whisper_words(d, scene, start, model, lang):
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        raise c.Fail("faster-whisper is not installed. Run: pip install faster-whisper (or use --mode script).") from None
    segs, _ = model.transcribe(str(Path(d) / scene["audio_file"]), word_timestamps=True, language=lang or None)
    out = []
    for sg in segs:
        for w in sg.words or []:
            t = w.word.strip()
            if t:
                out.append((start + w.start, start + w.end, t))
    return out


def group(words, max_words, max_chars, max_gap=0.7):
    cues, cur = [], []
    for w in words:
        if cur:
            text = " ".join(x[2] for x in cur) + " " + w[2]
            if len(cur) >= max_words or len(text) > max_chars or w[0] - cur[-1][1] > max_gap:
                cues.append(cur)
                cur = []
        cur.append(w)
        if re.search(r"[.!?…]$", w[2]) and len(cur) >= 3:
            cues.append(cur)
            cur = []
    if cur:
        cues.append(cur)
    return cues


def wrap(text, width=28):
    if len(text) <= width:
        return text
    mid = len(text) // 2
    left = text.rfind(" ", 0, mid + 1)
    right = text.find(" ", mid)
    cut = left if left != -1 and (right == -1 or mid - left <= right - mid) else right
    return text if cut == -1 else text[:cut] + "\n" + text[cut + 1:]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dir")
    ap.add_argument("--mode", choices=["script", "whisper"], default="script")
    ap.add_argument("--model", default="small")
    ap.add_argument("--max-words", type=int, default=8)
    ap.add_argument("--max-chars", type=int, default=42)
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    try:
        project = c.load_project(a.dir)
        rows, total = c.timeline(project)
        pad = float((project.get("voice") or {}).get("pad", 0.4))
        model = None
        if a.mode == "whisper":
            try:
                from faster_whisper import WhisperModel
                model = WhisperModel(a.model, device="cpu", compute_type="int8")
            except ImportError:
                raise c.Fail("faster-whisper is not installed. Run: pip install faster-whisper (or use --mode script).") from None
        words = []
        for r in rows:
            s = r["scene"]
            if a.mode == "whisper":
                if not s.get("audio_file"):
                    raise c.Fail(f"Scene {s['id']} has no audio_file.")
                words += whisper_words(a.dir, s, r["start"], model, project.get("language"))
            else:
                words += script_words(s, r["start"], r["raw"], pad)
        cues = group(words, a.max_words, a.max_chars)
        lines = []
        for i, cue in enumerate(cues, 1):
            st, en = cue[0][0], cue[-1][1]
            nxt = cues[i][0][0] if i < len(cues) else total
            en = min(max(en + 0.15, st + 0.6), nxt - 0.02 if nxt - 0.02 > st + 0.3 else en)
            lines += [str(i), f"{c.fmt_srt(st)} --> {c.fmt_srt(en)}", wrap(" ".join(x[2] for x in cue)), ""]
        out = Path(a.out) if a.out else Path(a.dir) / "out" / "subtitles.srt"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text("\n".join(lines), encoding="utf-8")
        print(f"Wrote {out} ({len(cues)} cues, {c.fmt_clock(total)}). Proofread before publishing.")
        if c.has_rtl(" ".join(x[2] for x in words)):
            print("Note: right-to-left text detected; check burned-in subtitles carefully, or upload the SRT instead.")
        return 0
    except c.Fail as e:
        print(f"error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
