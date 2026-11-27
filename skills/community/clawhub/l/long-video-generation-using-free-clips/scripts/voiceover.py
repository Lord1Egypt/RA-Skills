#!/usr/bin/env python3
"""Generate one narration file per scene and record exact durations in project.json.

Engines (project.json -> voice.engine, or --engine)
  piper       free, local. Needs `pip install piper-tts` and a downloaded voice. The command line differs between
              versions: check `python -m piper --help`, then override with PIPER_CMD, e.g.
              PIPER_CMD="python -m piper -m {voice} -f {out}"   (text is sent on stdin)
              Check the licence of the voice you use before publishing commercially.
  elevenlabs  paid API. Needs ELEVENLABS_API_KEY and voice.voice_id. Optional voice.model (default eleven_multilingual_v2).
  own         your own recordings: put audio/<scene_id>.wav (or .mp3/.m4a/.flac) in the project folder.
  silent      silence of the estimated length (layout tests, or to add a recording later).

Output: audio/<scene_id>.wav, mono 48 kHz, with voice.pad seconds of silence at the end.

Usage: voiceover.py PROJECT_DIR [--engine E] [--scene ID] [--force] [--dry-run]
"""
import argparse
import json
import os
import re
import shlex
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as c  # noqa: E402

OWN_EXT = (".wav", ".mp3", ".m4a", ".flac", ".ogg", ".aac")


def clean_text(t):
    t = re.sub(r"\[[^\]]*\]", " ", t or "")        # [stage directions]
    t = re.sub(r"[*_#`>]+", "", t)
    return re.sub(r"\s+", " ", t).strip()


def normalise(src, dest, pad):
    c.ffmpeg(["-i", src, "-vn", "-ac", "1", "-ar", c.SAMPLE_RATE, "-af", f"apad=pad_dur={pad}", "-c:a", "pcm_s16le", dest])


def synth_piper(text, tmp, voice):
    # -X utf8: without it Piper reads stdin in the Windows code page and fails on Urdu/Hindi text.
    tpl = os.environ.get("PIPER_CMD", "{python} -X utf8 -m piper -m {voice} -f {out}")
    # Split the template first, then fill each token: shlex would strip backslashes from Windows paths.
    cmd = [t.format(python=sys.executable, voice=voice, out=str(tmp)) for t in shlex.split(tpl)]
    try:
        c.run(cmd, input_text=text, timeout=900)
    except c.Fail as e:
        raise c.Fail(f"{e}\nPiper command used: {' '.join(cmd)}\nCheck `python -m piper --help`, download the voice, "
                     "and set PIPER_CMD if your version differs.") from None
    if not Path(tmp).exists():
        raise c.Fail("Piper ran but wrote no file; check PIPER_CMD.")


def synth_eleven(text, tmp, v):
    key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not key:
        raise c.Fail("Set ELEVENLABS_API_KEY to use ElevenLabs.")
    vid = v.get("voice_id")
    if not vid:
        raise c.Fail("Set voice.voice_id in project.json for ElevenLabs.")
    body = json.dumps({"text": text, "model_id": v.get("model", "eleven_multilingual_v2")}).encode()
    data = c.http_bytes(f"https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128",
                        headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"},
                        data=body, timeout=300)
    Path(tmp).write_bytes(data)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dir")
    ap.add_argument("--engine", choices=["piper", "elevenlabs", "own", "silent"])
    ap.add_argument("--scene")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    try:
        project = c.load_project(a.dir)
        v = project.get("voice") or {}
        engine = a.engine or v.get("engine", "piper")
        pad = float(v.get("pad", 0.4))
        d = Path(a.dir)
        c.ensure_dirs(d)
        scenes = [s for s in project["scenes"] if not a.scene or s["id"] == a.scene]
        if not scenes:
            raise c.Fail(f"No scene '{a.scene}'.")
        chars = sum(len(clean_text(s.get("narration", ""))) for s in scenes)
        print(f"Engine: {engine}; {len(scenes)} scene(s), {chars} characters.")
        if a.dry_run:
            if engine == "elevenlabs":
                print("ElevenLabs bills by characters: check your plan's quota before running.")
            return 0
        done = 0
        for s in scenes:
            text = clean_text(s.get("narration", ""))
            out = d / "audio" / f"{s['id']}.wav"
            h = c.sha([engine, v.get("voice"), v.get("voice_id"), v.get("model"), text, pad])
            if out.exists() and s.get("audio_hash") == h and not a.force:
                continue
            tmp = d / "audio" / f"{s['id']}.raw"
            if engine == "own":
                src = next((d / "audio" / f"{s['id']}{e}" for e in OWN_EXT if (d / "audio" / f"{s['id']}{e}").exists()), None)
                if not src:
                    raise c.Fail(f"Missing recording audio/{s['id']}.wav (or .mp3/.m4a/.flac).")
                normalise(str(src), str(out), pad)
                h = c.sha([engine, str(src.stat().st_mtime_ns), pad])
            elif engine == "silent":
                dur = max(1.0, c.est_seconds(text, project.get("wpm", 150)))
                c.ffmpeg(["-f", "lavfi", "-i", f"anullsrc=r={c.SAMPLE_RATE}:cl=mono", "-t", f"{dur + pad:.3f}",
                          "-c:a", "pcm_s16le", out])
            else:
                if not text:
                    raise c.Fail(f"Scene {s['id']} has no narration.")
                if engine == "piper":
                    tmp = d / "audio" / f"{s['id']}.piper.wav"
                    synth_piper(text, tmp, v.get("voice", "en_US-lessac-medium"))
                else:
                    tmp = d / "audio" / f"{s['id']}.eleven.mp3"
                    synth_eleven(text, tmp, v)
                normalise(str(tmp), str(out), pad)
                tmp.unlink(missing_ok=True)
            info = c.probe(str(out))
            s["audio_file"] = f"audio/{s['id']}.wav"
            s["audio_duration"] = round(info["duration"], 3)
            s["audio_hash"] = h
            c.save_project(a.dir, project)
            done += 1
            print(f"{s['id']}: {s['audio_duration']:.1f}s")
        total = sum(s.get("audio_duration") or 0 for s in project["scenes"])
        print(f"Generated {done} file(s). Total narration so far: {c.fmt_clock(total)}.")
        return 0
    except c.Fail as e:
        print(f"error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
