#!/usr/bin/env python3
"""Render a workspace-relative JSON timeline with CPU FFmpeg and Pillow.

No media uploads, source mutation, implicit music gain or private machine paths.
Run --help; see docs/时间线格式.md for supported fields and explicit limitations.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import json
import math
import os
from pathlib import Path, PureWindowsPath
import shutil
import stat
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

from PIL import Image, ImageColor

from vlog_effects import composite, fit_image, load_image, prepare_overlay


class TimelineError(ValueError):
    pass


def read_json(path):
    with open(path, encoding="utf-8-sig") as handle:
        return json.load(handle)


def reject_links(path: Path):
    for part in (path, *path.parents):
        if part.exists() or part.is_symlink():
            info = part.lstat()
            if part.is_symlink() or getattr(info, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400):
                raise TimelineError(f"Symlink/junction/reparse point is not allowed: {part.name}")


def within(path, root):
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def workspace_path(root, value, must_exist=True):
    if not isinstance(value, str) or not value.strip():
        raise TimelineError("A nonempty workspace-relative path is required")
    portable = value.replace("\\", "/")
    if Path(portable).is_absolute() or PureWindowsPath(value).drive or ".." in Path(portable).parts:
        raise TimelineError(f"Path must be relative to workspace_root without '..': {value}")
    path = root / portable
    reject_links(path)
    path = path.resolve()
    if not within(path, root):
        raise TimelineError("Path escapes workspace_root")
    if must_exist and not path.is_file():
        raise TimelineError(f"Missing file: {value}")
    return path


def number(value, label, minimum=0, maximum=None, positive=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise TimelineError(f"{label} must be a finite number")
    if value < minimum or (positive and value <= minimum) or (maximum is not None and value > maximum):
        raise TimelineError(f"{label} is out of range")
    return value


def pair(value, label, minimum=0, maximum=1):
    if not isinstance(value, list) or len(value) != 2:
        raise TimelineError(f"{label} must be a two-element array")
    for item in value:
        number(item, label, minimum, maximum)


def check_keys(value, allowed, label):
    if not isinstance(value, dict):
        raise TimelineError(f"{label} must be an object")
    unknown = set(value) - set(allowed)
    if unknown:
        raise TimelineError(f"Unsupported {label} fields: {', '.join(sorted(unknown))}")


def run(command, timeout=None):
    result = subprocess.run([str(item) for item in command], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, timeout=timeout)
    if result.returncode:
        # Commands can contain local paths; public manifests store only a short diagnostic.
        raise TimelineError(result.stderr.decode("utf-8", errors="replace")[-5000:])
    return result.stdout


def find_executable(root, name, override, config, local):
    value = override or local.get("executables", {}).get(name) or local.get(name) or config.get("executables", {}).get(name) or name
    value = str(value)
    if Path(value).is_absolute() or PureWindowsPath(value).drive:
        candidate = Path(value)
    elif "/" in value or "\\" in value:
        candidate = workspace_path(root, value)
    else:
        found = shutil.which(value)
        if not found:
            raise TimelineError(f"{name} unavailable. Install it or pass --{name} / executable config.")
        candidate = Path(found)
    if not candidate.is_file():
        raise TimelineError(f"Executable unavailable: {name}")
    return str(candidate)


def probe(path, ffprobe):
    return json.loads(run([ffprobe, "-v", "error", "-show_streams", "-show_format", "-of", "json", path]))


def media_duration(info, stream):
    raw = stream.get("duration", info.get("format", {}).get("duration"))
    try:
        value = float(raw)
        return value if math.isfinite(value) else None
    except (TypeError, ValueError):
        return None


def get_stream(info, kind):
    matches = [stream for stream in info.get("streams", []) if stream.get("codec_type") == kind]
    if not matches:
        raise TimelineError(f"Input has no {kind} stream")
    return matches[0]


def assert_sdr(stream, source, warnings):
    transfer = stream.get("color_transfer", "unknown")
    primaries = stream.get("color_primaries", "unknown")
    side = json.dumps(stream.get("side_data_list", []), ensure_ascii=True).lower()
    if transfer in {"smpte2084", "arib-std-b67"} or "dovi" in side or "dolby" in side or "mastering display" in side or "content light level" in side:
        raise TimelineError(f"HDR input requires a reviewed HDR-to-SDR preprocessing step: {source}")
    if primaries in {"bt2020", "smpte431", "smpte432"}:
        raise TimelineError(f"Wide-gamut input requires preprocessing to SDR Rec.709: {source}")
    if transfer not in {"unknown", "unspecified", "bt709", "smpte170m", "smpte240m", "iec61966-2-1", "bt470m", "bt470bg"}:
        raise TimelineError(f"Unsupported transfer function {transfer}; preprocess to SDR Rec.709: {source}")
    if transfer in {"unknown", "unspecified"}:
        warnings.append(f"Unspecified color transfer: {source}; treated as SDR, inspect the original and colors.")


def validate(timeline, root, config, ffprobe):
    check_keys(timeline, {"schema_version", "name", "canvas", "clips", "overlays", "audio", "notes"}, "timeline")
    if timeline.get("schema_version") != 1:
        raise TimelineError("schema_version must be 1")
    defaults = config.get("defaults", {})
    canvas = timeline.get("canvas", {})
    check_keys(canvas, {"width", "height", "fps", "background"}, "canvas")
    width, height = canvas.get("width", defaults.get("width", 1080)), canvas.get("height", defaults.get("height", 1920))
    fps = canvas.get("fps", defaults.get("fps", 30))
    for value, key in ((width, "width"), (height, "height")):
        number(value, key, 64, 4096)
        if int(value) != value or value % 2:
            raise TimelineError(f"{key} must be an even integer")
    number(fps, "fps", 1, 60)
    if int(fps) != fps:
        raise TimelineError("v1 supports integer fps only (1 to 60)")
    width, height, fps = int(width), int(height), int(fps)
    background = canvas.get("background", "#17221f")
    ImageColor.getrgb(background)
    warnings, sources, cached = [], set(), {}
    def resolve(value):
        path = workspace_path(root, value)
        sources.add(path)
        return path
    def metadata(value):
        path = resolve(value)
        if path not in cached:
            cached[path] = probe(path, ffprobe)
        return cached[path]
    clips = timeline.get("clips")
    if not isinstance(clips, list) or not clips:
        raise TimelineError("clips must be a nonempty array")
    compiled, frames = [], 0
    for index, clip in enumerate(clips):
        label = f"clip[{index}]"
        check_keys(clip, {"id", "type", "source", "duration", "source_in", "fit", "crop_center", "color", "audio", "note"}, label)
        kind = clip.get("type")
        if kind not in {"image", "video", "color"}:
            raise TimelineError(f"{label}: type must be image, video or color")
        duration = number(clip.get("duration"), label + ".duration", positive=True)
        count = round(duration * fps)
        if count < 1:
            raise TimelineError(f"{label} duration is shorter than one frame")
        quantized = count / fps
        if abs(quantized - duration) > 1e-7:
            warnings.append(f"{label} duration quantized to {quantized:.6f}s ({count} frames)")
        start = number(clip.get("source_in", 0), label + ".source_in")
        if kind != "video" and start:
            raise TimelineError(f"{label}: source_in applies only to video")
        if clip.get("audio", False) is not False:
            raise TimelineError(f"{label}: use audio.tracks explicitly for original sound; clip.audio must be false")
        fit = clip.get("fit", "cover")
        if fit not in {"cover", "contain"}:
            raise TimelineError(f"{label}.fit must be cover or contain")
        pair(clip.get("crop_center", [0.5, 0.5]), label + ".crop_center")
        if kind == "color":
            ImageColor.getrgb(clip.get("color", background))
            if "source" in clip:
                raise TimelineError(f"{label}: a color clip cannot have source")
        elif kind == "image":
            image = load_image(resolve(clip.get("source")))
            if image.width < 1 or image.height < 1:
                raise TimelineError(f"{label}: invalid image")
        else:
            info = metadata(clip.get("source"))
            stream = get_stream(info, "video")
            assert_sdr(stream, clip["source"], warnings)
            length = media_duration(info, stream)
            if length is None or start + quantized > length + 1 / fps:
                raise TimelineError(f"{label}: source_in + duration exceeds the source video or its duration is unknown")
        compiled.append(dict(clip, start_frame=frames, frames=count, duration=quantized))
        frames += count
    total = frames / fps
    overlays = timeline.get("overlays", [])
    if not isinstance(overlays, list):
        raise TimelineError("overlays must be an array")
    for index, item in enumerate(overlays):
        label = f"overlay[{index}]"
        common = {"id", "type", "start", "duration", "center", "note"}
        photo_fields = {"source", "max_size", "entry", "expand", "angle", "crop_center", "paper_color", "fade_out", "motion_samples"}
        text_fields = {"text", "font", "font_size", "color", "outline", "shadow", "max_width", "angle", "direction"}
        kind = item.get("type") if isinstance(item, dict) else None
        if kind not in {"photo_card", "full_photo", "sticker_title", "subtitle"}:
            raise TimelineError(f"{label}: unsupported overlay type")
        check_keys(item, common | (photo_fields if kind in {"photo_card", "full_photo"} else text_fields), label)
        start = number(item.get("start"), label + ".start")
        length = number(item.get("duration"), label + ".duration", positive=True)
        if start + length > total + 1e-6:
            raise TimelineError(f"{label} extends beyond the timeline ({total:.6f}s)")
        pair(item.get("center", [0.5, 0.5]), label + ".center")
        if kind in {"photo_card", "full_photo"}:
            load_image(resolve(item.get("source")))
            entry = number(item.get("entry", 0.65), label + ".entry", positive=True)
            expand = number(item.get("expand", 0.28), label + ".expand", positive=True)
            if length <= entry + (expand if kind == "full_photo" else 0):
                raise TimelineError(f"{label}: duration must leave a stable hold after placement/expansion")
            number(item.get("fade_out", 0), label + ".fade_out", 0, length)
            number(item.get("angle", -1.2), label + ".angle", -30, 30)
            if item.get("motion_samples", 3) not in {1, 3}:
                raise TimelineError(f"{label}.motion_samples must be 1 or 3")
            pair(item.get("max_size", [0.82, 0.53]), label + ".max_size", 0.1, 1)
            pair(item.get("crop_center", [0.5, 0.5]), label + ".crop_center")
            ImageColor.getrgb(item.get("paper_color", "#F6F4EE"))
        else:
            resolve(item.get("font"))
            if not isinstance(item.get("text"), str) or not item["text"].strip():
                raise TimelineError(f"{label}.text must be nonempty")
            number(item.get("font_size", 48), label + ".font_size", 6, 800)
            number(item.get("max_width", 0.9), label + ".max_width", 0.1, 1)
            number(item.get("angle", -2), label + ".angle", -30, 30)
            if item.get("direction", -1) not in {-1, 1}:
                raise TimelineError(f"{label}.direction must be -1 or 1")
            for key in ("color", "outline", "shadow"):
                if key in item:
                    ImageColor.getrgb(item[key])
        # Validate font decoding and layout now, without making a result file.
        prepare_overlay(item, width, height, resolve)
    audio = timeline.get("audio", {})
    check_keys(audio, {"master_audio", "tracks", "sample_rate", "bitrate"}, "audio")
    if "master_audio" in audio and "tracks" in audio:
        raise TimelineError("Choose audio.master_audio or audio.tracks, not both")
    number(audio.get("sample_rate", defaults.get("audio_sample_rate", 48000)), "audio.sample_rate", 8000, 96000)
    rate = audio.get("sample_rate", defaults.get("audio_sample_rate", 48000))
    if int(rate) != rate:
        raise TimelineError("audio.sample_rate must be an integer")
    if not str(audio.get("bitrate", "192k")).isdigit() and not (str(audio.get("bitrate", "192k")).endswith("k") and str(audio.get("bitrate", "192k"))[:-1].isdigit()):
        raise TimelineError("audio.bitrate must be a number or values such as 192k")
    master = audio.get("master_audio")
    if master is not None:
        check_keys(master, {"source", "source_in", "copy_aac"}, "master_audio")
        start = number(master.get("source_in", 0), "master_audio.source_in")
        info = metadata(master.get("source"))
        stream = get_stream(info, "audio")
        duration = media_duration(info, stream)
        if not isinstance(master.get("copy_aac", True), bool):
            raise TimelineError("master_audio.copy_aac must be boolean")
        if master.get("copy_aac", True):
            if stream.get("codec_name") != "aac" or start != 0:
                raise TimelineError("Exact AAC copy requires an AAC source with source_in=0")
            if abs(float(stream.get("start_time", 0))) > 0.001:
                raise TimelineError("Exact AAC copy requires an audio stream starting at timeline zero; a nonzero start_time needs explicit preprocessing")
            if duration is None or abs(duration - total) > 0.08:
                raise TimelineError("Exact AAC copy requires matching timeline duration (tolerance 0.08s); do not trim an accepted master implicitly")
        elif duration is None or start + total > duration + 0.025:
            raise TimelineError("master_audio is too short for the timeline")
    tracks = audio.get("tracks", [])
    if not isinstance(tracks, list):
        raise TimelineError("audio.tracks must be an array")
    for index, track in enumerate(tracks):
        label = f"audio.tracks[{index}]"
        check_keys(track, {"source", "source_in", "timeline_in", "duration", "volume", "role", "fade_in", "fade_out", "note"}, label)
        start = number(track.get("source_in", 0), label + ".source_in")
        at = number(track.get("timeline_in", 0), label + ".timeline_in")
        length = number(track.get("duration"), label + ".duration", positive=True)
        number(track.get("volume"), label + ".volume", 0, 16)
        if track.get("role", "original") not in {"original", "voiceover", "bgm"}:
            raise TimelineError(f"{label}.role must be original, voiceover or bgm")
        for key in ("fade_in", "fade_out"):
            number(track.get(key, 0), label + "." + key, 0, length)
        if at + length > total + 1e-6:
            raise TimelineError(f"{label} extends beyond the timeline")
        info = metadata(track.get("source"))
        stream = get_stream(info, "audio")
        duration = media_duration(info, stream)
        if duration is None or start + length > duration + 0.025:
            raise TimelineError(f"{label}: source_in + duration exceeds source audio")
    return dict(width=width, height=height, fps=fps, background=background, clips=compiled,
                overlays=overlays, audio=audio, frames=frames, duration=total,
                warnings=warnings, sources=sources, sample_rate=int(audio.get("sample_rate", defaults.get("audio_sample_rate", 48000))))


def stop_process(process):
    if process is None:
        return
    for pipe in (process.stdin, process.stdout):
        if pipe:
            try:
                pipe.close()
            except (OSError, BrokenPipeError):
                pass
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)


def read_exact(pipe, count):
    result = bytearray()
    while len(result) < count:
        chunk = pipe.read(count - len(result))
        if not chunk:
            raise TimelineError("Video decoder ended early; no repeated/frozen frames were inserted")
        result.extend(chunk)
    return bytes(result)


def video_filter(clip, plan):
    width, height = plan["width"], plan["height"]
    center = clip.get("crop_center", [0.5, 0.5])
    # Normalize sample aspect before fitting; autorotation remains enabled in FFmpeg.
    filters = ["scale=trunc(iw*sar/2)*2:ih", "setsar=1"]
    if clip.get("fit", "cover") == "cover":
        filters += [f"scale={width}:{height}:force_original_aspect_ratio=increase:flags=lanczos:out_color_matrix=bt709:out_range=full",
                    f"crop={width}:{height}:(iw-ow)*{center[0]}:(ih-oh)*{center[1]}"]
    else:
        color = ImageColor.getrgb(plan["background"])
        hexcolor = "0x%02x%02x%02x" % color[:3]
        filters += [f"scale={width}:{height}:force_original_aspect_ratio=decrease:flags=lanczos:out_color_matrix=bt709:out_range=full",
                    f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color={hexcolor}"]
    filters += [f"fps={plan['fps']}", "format=rgb24"]
    return ",".join(filters)


def render_picture(plan, root, ffmpeg, destination, tempdir, crf, preset):
    width, height, fps = plan["width"], plan["height"], plan["fps"]
    resolve = lambda value: workspace_path(root, value)
    effects = [prepare_overlay(spec, width, height, resolve) for spec in plan["overlays"]]
    encoder = decoder = None
    with open(tempdir / "encode.log", "wb") as log:
        try:
            command = [ffmpeg, "-hide_banner", "-loglevel", "error", "-n", "-f", "rawvideo", "-pixel_format", "rgb24",
                       "-video_size", f"{width}x{height}", "-framerate", fps, "-i", "pipe:0", "-an",
                       "-vf", "scale=in_range=full:out_range=tv:out_color_matrix=bt709,format=yuv420p",
                       "-c:v", "libx264", "-preset", preset, "-crf", crf, "-pix_fmt", "yuv420p",
                       "-x264-params", "colorprim=bt709:transfer=bt709:colormatrix=bt709",
                       "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv",
                       "-movflags", "+faststart", destination]
            encoder = subprocess.Popen([str(value) for value in command], stdin=subprocess.PIPE, stderr=log)
            for index, clip in enumerate(plan["clips"]):
                decoder = None
                with open(tempdir / f"decode-{index}.log", "wb") as decode_log:
                    try:
                        if clip["type"] == "video":
                            command = [ffmpeg, "-hide_banner", "-loglevel", "error", "-ss", clip.get("source_in", 0),
                                       "-i", resolve(clip["source"]), "-map", "0:v:0", "-an", "-sn", "-dn",
                                       "-vf", video_filter(clip, plan), "-frames:v", clip["frames"], "-f", "rawvideo", "-pix_fmt", "rgb24", "pipe:1"]
                            decoder = subprocess.Popen([str(value) for value in command], stdout=subprocess.PIPE, stderr=decode_log)
                        elif clip["type"] == "image":
                            still = fit_image(load_image(resolve(clip["source"])), (width, height), clip.get("fit", "cover"),
                                              clip.get("crop_center", [0.5, 0.5]), plan["background"])
                        else:
                            still = Image.new("RGB", (width, height), clip.get("color", plan["background"]))
                        for frame in range(clip["frames"]):
                            if decoder:
                                picture = Image.frombytes("RGB", (width, height), read_exact(decoder.stdout, width * height * 3))
                            else:
                                picture = still.copy()
                            timestamp = (clip["start_frame"] + frame) / fps
                            for effect in effects:
                                picture = composite(picture, effect, timestamp)
                            encoder.stdin.write(picture.tobytes())
                        if decoder:
                            decoder.stdout.close()
                            if decoder.wait(timeout=30):
                                raise TimelineError(f"Video decoder failed for clip {index}")
                        print(f"Rendered clip {index + 1}/{len(plan['clips'])}", file=sys.stderr, flush=True)
                    finally:
                        stop_process(decoder)
                        decoder = None
            encoder.stdin.close()
            if encoder.wait(timeout=120):
                raise TimelineError("FFmpeg picture encoding failed")
        except (BrokenPipeError, OSError) as exc:
            log.flush()
            detail = (tempdir / "encode.log").read_text(encoding="utf-8", errors="replace")[-1500:]
            raise TimelineError(f"FFmpeg pipeline failed: {exc}\n{detail}") from exc
        finally:
            stop_process(decoder)
            stop_process(encoder)


def encoded_audio_hash(path, ffmpeg):
    return run([ffmpeg, "-v", "error", "-i", path, "-map", "0:a:0", "-c:a", "copy",
                "-f", "hash", "-hash", "sha256", "-"]).decode().strip()


def audio_packet_evidence(path, ffprobe):
    data = json.loads(run([ffprobe, "-v", "error", "-select_streams", "a:0", "-show_packets",
                           "-show_data_hash", "sha256", "-show_entries",
                           "packet=pts_time,dts_time,duration_time,size,data_hash:packet_side_data",
                           "-of", "json", path]))
    packets = data.get("packets", [])
    if not packets or any(any(key not in item for key in ("pts_time", "dts_time", "duration_time", "data_hash")) for item in packets):
        raise TimelineError("AAC packet timestamp/hash evidence is unavailable")
    return packets


def mux_audio(plan, root, ffmpeg, ffprobe, picture, destination):
    audio, total = plan["audio"], plan["duration"]
    resolve = lambda value: workspace_path(root, value)
    master = audio.get("master_audio")
    tracks = audio.get("tracks", [])
    if master:
        source = resolve(master["source"])
        if master.get("copy_aac", True):
            run([ffmpeg, "-v", "error", "-n", "-i", picture, "-i", source,
                 "-map", "0:v:0", "-map", "1:a:0", "-c", "copy", "-map_metadata", "-1",
                 "-movflags", "+faststart", destination])
            before, after = encoded_audio_hash(source, ffmpeg), encoded_audio_hash(destination, ffmpeg)
            if before != after:
                raise TimelineError("AAC packet hash changed; the requested exact master reuse failed")
            before_packets = audio_packet_evidence(source, ffprobe)
            after_packets = audio_packet_evidence(destination, ffprobe)
            if before_packets != after_packets:
                raise TimelineError("AAC packet PTS/DTS/duration/side data or payload changed; exact master reuse failed")
            evidence_hash = hashlib.sha256(json.dumps(after_packets, sort_keys=True).encode()).hexdigest()
            return {"mode": "master_aac_copy", "encoded_audio_sha256": after, "encoded_packets_identical": True,
                    "packet_timestamps_identical": True, "packet_side_data_identical": True,
                    "packet_count": len(after_packets), "packet_evidence_sha256": evidence_hash}
        tracks = [{"source": master["source"], "source_in": master.get("source_in", 0), "timeline_in": 0,
                   "duration": total, "volume": 1, "role": "original"}]
    if not tracks:
        shutil.copyfile(picture, destination)
        return {"mode": "silent", "note": "No audio was requested"}
    command = [ffmpeg, "-v", "error", "-n", "-i", picture]
    chains = []
    total_samples = round(total * plan["sample_rate"])
    for index, track in enumerate(tracks):
        command += ["-i", resolve(track["source"])]
        length = track["duration"]
        source_first_sample = round(track.get("source_in", 0) * plan["sample_rate"])
        source_last_sample = source_first_sample + round(length * plan["sample_rate"])
        filters = [f"aresample={plan['sample_rate']}",
                   f"atrim=start_sample={source_first_sample}:end_sample={source_last_sample}", "asetpts=N/SR/TB",
                   "aformat=sample_fmts=fltp:channel_layouts=stereo",
                   f"volume={track['volume']}"]
        if track.get("fade_in", 0):
            filters.append(f"afade=t=in:ss=0:ns={round(track['fade_in']*plan['sample_rate'])}")
        if track.get("fade_out", 0):
            filters.append(f"afade=t=out:ss={round((length-track['fade_out'])*plan['sample_rate'])}:ns={round(track['fade_out']*plan['sample_rate'])}")
        delay = round(track.get("timeline_in", 0) * plan["sample_rate"])
        filters += [f"adelay={delay}S:all=1", f"apad=whole_len={total_samples}",
                    f"atrim=end_sample={total_samples}", "asetpts=N/SR/TB"]
        chains.append(f"[{index+1}:a:0]" + ",".join(filters) + f"[a{index}]")
    labels = "".join(f"[a{index}]" for index in range(len(tracks)))
    chains.append(labels + f"amix=inputs={len(tracks)}:normalize=0:dropout_transition=0,atrim=end_sample={total_samples},asetpts=N/SR/TB[mix]")
    command += ["-filter_complex", ";".join(chains), "-map", "0:v:0", "-map", "[mix]", "-c:v", "copy", "-c:a", "aac",
                "-b:a", audio.get("bitrate", "192k"), "-ar", plan["sample_rate"], "-map_metadata", "-1",
                "-movflags", "+faststart", destination]
    run(command)
    return {"mode": "explicit_track_mix", "normalization": False, "automatic_bgm_reduction": False,
            "automatic_ducking": False, "limiter": False, "tracks": tracks}


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def reserve_publish(tempfile_path, destination):
    # Exclusive creation makes a competing render fail instead of overwriting it.
    created = False
    try:
        with open(destination, "xb") as target, open(tempfile_path, "rb") as source:
            created = True
            shutil.copyfileobj(source, target, 1024 * 1024)
    except BaseException:
        if created:
            destination.unlink(missing_ok=True)
        raise


@contextmanager
def checked_temporary_directory(parent):
    parent = parent.resolve()
    reject_links(parent)
    directory = Path(tempfile.mkdtemp(prefix=".render-", dir=parent))
    try:
        yield directory
    finally:
        # Verify the exact resolved target before recursive deletion on Windows.
        reject_links(directory)
        resolved = directory.resolve()
        if resolved.parent != parent or not resolved.name.startswith(".render-") or resolved == parent:
            raise TimelineError("Temporary cleanup target failed workspace boundary verification")
        shutil.rmtree(resolved)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-root", default=".", help="Workspace/package directory")
    parser.add_argument("--timeline", required=True, help="Timeline JSON, relative to workspace root")
    parser.add_argument("--output", help="New .mp4 path within workspace, outside source folders")
    parser.add_argument("--ffmpeg")
    parser.add_argument("--ffprobe")
    parser.add_argument("--validate-only", action="store_true", help="Read/probe and validate; write nothing")
    parser.add_argument("--crf", type=int, default=20)
    parser.add_argument("--preset", choices=["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow"], default="medium")
    args = parser.parse_args(argv)
    root = Path(args.workspace_root).absolute()
    reject_links(root)
    root = root.resolve()
    if not root.is_dir():
        raise TimelineError("workspace_root must exist")
    config_path = workspace_path(root, "workspace_config.json", False)
    local_path = workspace_path(root, "environment.local.json", False)
    config = read_json(config_path) if config_path.exists() else {}
    local = read_json(local_path) if local_path.exists() else {}
    ffmpeg = find_executable(root, "ffmpeg", args.ffmpeg, config, local)
    ffprobe = find_executable(root, "ffprobe", args.ffprobe, config, local)
    timeline_path = workspace_path(root, args.timeline)
    timeline = read_json(timeline_path)
    plan = validate(timeline, root, config, ffprobe)
    if not 0 <= args.crf <= 51:
        raise TimelineError("crf must be between 0 and 51")
    output = manifest_path = None
    if args.output:
        output = workspace_path(root, args.output, False)
        sources_root = workspace_path(root, config.get("paths", {}).get("sources", "素材"), False)
        if within(output, sources_root) or within(output, root / "素材"):
            raise TimelineError("Output inside the original-media folder is forbidden")
        if output.suffix.lower() != ".mp4":
            raise TimelineError("Output must have .mp4 extension")
        manifest_path = output.with_suffix(".manifest.json")
        if output in plan["sources"] or manifest_path in plan["sources"] or output == timeline_path or manifest_path == timeline_path:
            raise TimelineError("Output would overwrite an input")
        if output.exists() or manifest_path.exists():
            raise TimelineError("Output or manifest already exists; choose a new version filename")
    elif not args.validate_only:
        raise TimelineError("--output is required for rendering")
    summary = {"valid": True, "duration": plan["duration"], "frames": plan["frames"],
               "width": plan["width"], "height": plan["height"], "fps": plan["fps"], "warnings": plan["warnings"]}
    if args.validate_only:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0
    output.parent.mkdir(parents=True, exist_ok=True)
    reject_links(output.parent)
    with checked_temporary_directory(output.parent) as tempdir:
        picture, result = tempdir / "picture.mp4", tempdir / "result.mp4"
        render_picture(plan, root, ffmpeg, picture, tempdir, args.crf, args.preset)
        audio_evidence = mux_audio(plan, root, ffmpeg, ffprobe, picture, result)
        # Full decode is a program check, never a claim of watching/listening.
        run([ffmpeg, "-v", "error", "-xerror", "-i", result, "-map", "0:v:0", "-map", "0:a?", "-f", "null", "-"])
        final_probe = probe(result, ffprobe)
        video = get_stream(final_probe, "video")
        if video.get("codec_name") != "h264" or int(video["width"]) != plan["width"] or int(video["height"]) != plan["height"]:
            raise TimelineError("Encoded output does not match the requested canvas/codec")
        if int(video.get("nb_frames", -1)) != plan["frames"]:
            raise TimelineError("Encoded video frame count does not match the timeline")
        if any(video.get(key) != "bt709" for key in ("color_space", "color_transfer", "color_primaries")):
            raise TimelineError("Encoded output does not carry the requested SDR Rec.709 color metadata")
        if audio_evidence["mode"] != "silent":
            audio_stream = get_stream(final_probe, "audio")
            audio_length = media_duration(final_probe, audio_stream)
            if audio_stream.get("codec_name") != "aac" or audio_length is None or abs(audio_length - plan["duration"]) > 0.08:
                raise TimelineError("Encoded audio codec or duration does not match the timeline")
        manifest = {"schema_version": 1, "renderer_version": "1.0.0", "created_at": datetime.now(timezone.utc).isoformat(),
                    "timeline": args.timeline.replace("\\", "/"), "timeline_sha256": sha256_file(timeline_path),
                    "output": output.relative_to(root).as_posix(), "output_sha256": sha256_file(result),
                    "render": summary, "encoder": {"name": "libx264", "crf": args.crf, "preset": args.preset},
                    "tool_versions": {"ffmpeg": run([ffmpeg, "-version"]).decode(errors="replace").splitlines()[0],
                                      "ffprobe": run([ffprobe, "-version"]).decode(errors="replace").splitlines()[0]},
                    "sources": sorted(path.relative_to(root).as_posix() for path in plan["sources"]),
                    "audio": audio_evidence,
                    "checks": {"full_decode": True, "frame_count": True, "rec709_metadata": True, "continuous_playback": False,
                               "listening": False, "sampled_frames_visually_reviewed": False},
                    "limitations": ["Review framing, overlays, cuts, motion and sound on the exported version before acceptance.",
                                    "No automatic color grading, stabilization, HDR conversion, ducking or brush-image generation."]}
        manifest_temp = tempdir / "manifest.json"
        manifest_temp.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        reserve_publish(result, output)
        try:
            reserve_publish(manifest_temp, manifest_path)
        except BaseException:
            # Only this invocation's newly created output is removed on a failed transaction.
            output.unlink(missing_ok=True)
            raise
    print(json.dumps({"output": output.relative_to(root).as_posix(), "manifest": manifest_path.relative_to(root).as_posix()},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    try:
        raise SystemExit(main())
    except (TimelineError, OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(2)
