#!/usr/bin/env python3
"""Validate final video, cover, publishing copy, and QC status."""

import argparse
import json
import re
import shutil
import struct
import subprocess
from pathlib import Path


def run(command):
    return subprocess.run(command, capture_output=True, text=True, encoding="utf-8")


def png_dimensions(path: Path):
    data = path.read_bytes()[:24]
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", data[16:24])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--job-dir", required=True)
    parser.add_argument("--skip-decode", action="store_true")
    parser.add_argument("--skip-loudness", action="store_true")
    args = parser.parse_args()

    root = Path(args.job_dir).expanduser().resolve()
    video = root / "08-delivery" / "final.mp4"
    cover = root / "08-delivery" / "cover.png"
    publish = root / "08-delivery" / "publish-copy.json"
    qc = root / "07-qc" / "qc-report.json"
    required = [video, cover, publish, qc]
    missing = [path.relative_to(root).as_posix() for path in required if not path.is_file()]
    errors = []
    warnings = []
    evidence = {}

    if missing:
        errors.append("Missing required delivery artifacts")
    if not shutil.which("ffprobe") or not shutil.which("ffmpeg"):
        errors.append("ffmpeg and ffprobe are required")

    if video.is_file() and shutil.which("ffprobe"):
        probe = run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_streams",
                "-show_format",
                "-of",
                "json",
                str(video),
            ]
        )
        if probe.returncode:
            errors.append("ffprobe failed")
        else:
            metadata = json.loads(probe.stdout)
            streams = metadata.get("streams", [])
            visual = next((item for item in streams if item.get("codec_type") == "video"), {})
            audio = next((item for item in streams if item.get("codec_type") == "audio"), {})
            evidence["video"] = {
                "codec": visual.get("codec_name"),
                "width": visual.get("width"),
                "height": visual.get("height"),
                "pix_fmt": visual.get("pix_fmt"),
                "frame_rate": visual.get("r_frame_rate"),
                "audio_codec": audio.get("codec_name"),
                "audio_rate": audio.get("sample_rate"),
                "duration": metadata.get("format", {}).get("duration"),
            }
            if visual.get("codec_name") != "h264":
                errors.append("Final video is not H.264")
            if (visual.get("width"), visual.get("height")) != (1080, 1920):
                errors.append("Final video is not 1080x1920")
            if visual.get("pix_fmt") != "yuv420p":
                errors.append("Final video is not yuv420p")
            if visual.get("r_frame_rate") != "30/1":
                errors.append("Final video is not 30 fps")
            if not audio:
                errors.append("Final video has no audio stream")

        if not args.skip_decode and shutil.which("ffmpeg"):
            decode = run(["ffmpeg", "-v", "error", "-i", str(video), "-f", "null", "-"])
            if decode.returncode or decode.stderr.strip():
                errors.append("Full decode reported an error")

        if shutil.which("ffmpeg"):
            black = run(
                [
                    "ffmpeg",
                    "-hide_banner",
                    "-nostats",
                    "-i",
                    str(video),
                    "-vf",
                    "blackdetect=d=0.20:pix_th=0.02",
                    "-an",
                    "-f",
                    "null",
                    "-",
                ]
            )
            black_intervals = re.findall(r"black_start:[^\r\n]+", black.stderr)
            evidence["black_intervals"] = black_intervals
            if black.returncode:
                errors.append("Black-frame analysis failed")
            elif black_intervals:
                errors.append("Video contains a black interval of 0.20 seconds or longer")

        if not args.skip_loudness and shutil.which("ffmpeg"):
            loudness = run(
                [
                    "ffmpeg",
                    "-hide_banner",
                    "-nostats",
                    "-i",
                    str(video),
                    "-map",
                    "0:a:0",
                    "-af",
                    "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json",
                    "-f",
                    "null",
                    "-",
                ]
            )
            match_i = re.search(r'"input_i"\s*:\s*"([^"]+)"', loudness.stderr)
            match_tp = re.search(r'"input_tp"\s*:\s*"([^"]+)"', loudness.stderr)
            if not match_i or not match_tp:
                errors.append("Loudness measurement failed")
            else:
                integrated, peak = float(match_i.group(1)), float(match_tp.group(1))
                evidence["loudness"] = {"integrated_lufs": integrated, "true_peak_dbtp": peak}
                if not -18.0 <= integrated <= -14.0:
                    errors.append("Integrated loudness is outside -18 to -14 LUFS")
                if peak > -1.0:
                    errors.append("True peak is above -1.0 dBTP")

    if cover.is_file():
        evidence["cover"] = png_dimensions(cover)
        if evidence["cover"] != (1080, 1920):
            errors.append("Cover is not a 1080x1920 PNG")

    if publish.is_file():
        try:
            copy = json.loads(publish.read_text(encoding="utf-8"))
            fields = {
                "title",
                "description",
                "hashtags",
                "pinned_comment",
                "reply_prompt",
                "cover_title",
                "cover_subtitle",
            }
            absent = sorted(fields - set(copy))
            if absent:
                errors.append(f"Publish copy is missing fields: {', '.join(absent)}")
            if not isinstance(copy.get("hashtags"), list) or not 5 <= len(copy.get("hashtags", [])) <= 8:
                errors.append("Publish copy must contain 5-8 hashtags")
        except Exception as exc:
            errors.append(f"Publish copy is invalid JSON: {exc}")

    if qc.is_file():
        try:
            qc_data = json.loads(qc.read_text(encoding="utf-8"))
            if qc_data.get("status") not in {"pass", "needs-human"}:
                errors.append("QC report is not pass or needs-human")
            if qc_data.get("status") == "needs-human":
                warnings.append("QC requires human confirmation, usually for source-media rights")
            metrics = qc_data.get("metrics", qc_data)
            source_video_count = int(metrics.get("source_video_count", 0) or 0)
            if source_video_count:
                if metrics.get("narration_during_source_video") is not False:
                    errors.append("Narration must be absent during source-video playback")
                if metrics.get("captions_during_source_video") is not False:
                    errors.append("Narration captions must be absent during source-video playback")
                if metrics.get("source_video_audio") != "original-only":
                    errors.append("Source-video interludes must use original-only audio")
                if metrics.get("resume_continuity") != "pass":
                    errors.append("Narration resume continuity is not verified")
        except Exception as exc:
            errors.append(f"QC report is invalid JSON: {exc}")

    result = {
        "status": "pass" if not errors else "fail",
        "missing": missing,
        "errors": errors,
        "warnings": warnings,
        "evidence": evidence,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
