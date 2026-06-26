#!/usr/bin/env python3
"""
Manim Animation Pipeline — Render + Subtitle Burn-in

Usage:
    python run_pipeline.py --scene_file scene.py --scene_name MyScene
    python run_pipeline.py --scene_file scene.py --scene_name MyScene --quality high --burn_subtitles
"""

import argparse
import subprocess
import sys
import os
import glob
import re
import shlex


# Quality mapping
QUALITY_MAP = {
    "low": {"flag": "-ql", "cfg": "low_quality", "dir": "480p15"},
    "medium": {"flag": "-qm", "cfg": "medium_quality", "dir": "720p30"},
    "high": {"flag": "-qh", "cfg": "high_quality", "dir": "1080p60"},
    "production": {"flag": "-qp", "cfg": "production_quality", "dir": "2160p60"},
}

# Strict pattern for scene class names (valid Python identifiers)
SCENE_NAME_PATTERN = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')


def validate_scene_name(name):
    """Validate that scene_name is a safe Python identifier."""
    if not SCENE_NAME_PATTERN.match(name):
        raise ValueError(
            f"Invalid scene name: {name!r}. "
            "Scene name must be a valid Python identifier "
            "(letters, digits, underscores; cannot start with a digit)."
        )
    return name


def validate_file_path(path):
    """Validate that a file path does not contain shell metacharacters."""
    # Allow typical path characters only
    if re.search(r'[;&|`$(){}\[\]!#~]', path):
        raise ValueError(
            f"Invalid file path: {path!r}. "
            "Path contains disallowed shell metacharacters."
        )
    return path


def run_cmd(cmd_args, desc=None, cwd=None):
    """Run a command as an argument list (shell=False), print output, return success status."""
    if desc:
        print(f"\n{'='*50}")
        print(f"  {desc}")
        print(f"{'='*50}\n")
    # Display the command in a human-readable form
    display_cmd = " ".join(shlex.quote(str(a)) for a in cmd_args)
    print(f"  $ {display_cmd}\n")
    result = subprocess.run(cmd_args, cwd=cwd)
    return result.returncode == 0


def find_output_files(scene_file, scene_name, quality_dir):
    """Find rendered video and SRT file."""
    base = os.path.splitext(os.path.basename(scene_file))[0]
    media_dir = os.path.join("media", "videos", base, quality_dir)

    video_file = os.path.join(media_dir, f"{scene_name}.mp4")
    srt_file = os.path.join(media_dir, f"{scene_name}.srt")

    # Also check for SRT in media/voiceovers or same directory
    if not os.path.exists(srt_file):
        # Search for any .srt file in the media directory
        srt_candidates = glob.glob(os.path.join(media_dir, "*.srt"))
        if srt_candidates:
            srt_file = srt_candidates[0]

    return video_file, srt_file, media_dir


def render_scene(scene_file, scene_name, quality, working_dir=None):
    """Render manim scene."""
    q = QUALITY_MAP.get(quality, QUALITY_MAP["high"])
    validate_scene_name(scene_name)
    validate_file_path(scene_file)

    cmd_args = ["manim", "render", q["flag"], scene_file, scene_name]

    success = run_cmd(cmd_args, f"Rendering: {scene_name} ({quality} quality)", cwd=working_dir)
    return success


def burn_subtitles(video_file, srt_file, output_file=None, font_size=22, margin_v=30):
    """Burn SRT subtitles into video using ffmpeg."""
    if not os.path.exists(srt_file):
        print(f"  ⚠️  SRT file not found: {srt_file}")
        print("  Skipping subtitle burn-in.")
        return False

    if output_file is None:
        base, ext = os.path.splitext(video_file)
        output_file = f"{base}_subtitled{ext}"

    abs_srt = os.path.abspath(srt_file)
    # Escape special characters in path for ffmpeg subtitles filter
    abs_srt_escaped = abs_srt.replace("'", "'\\''").replace(":", "\\:")

    force_style = (
        f"FontSize={font_size},"
        f"PrimaryColour=&H00FFFFFF,"
        f"OutlineColour=&H00000000,"
        f"Outline=2,"
        f"BackColour=&H80000000,"
        f"BorderStyle=4,"
        f"MarginV={margin_v}"
    )

    vf_filter = f"subtitles='{abs_srt_escaped}':force_style='{force_style}'"

    cmd_args = [
        "ffmpeg", "-y", "-i", video_file,
        "-vf", vf_filter,
        "-c:a", "copy", output_file
    ]

    success = run_cmd(cmd_args, "Burning SRT subtitles into video")

    if success:
        print(f"\n  ✅ Subtitled video: {output_file}")
    else:
        print(f"\n  ❌ Subtitle burn failed.")
        print("  Make sure ffmpeg has libass + libx264 support.")
        print("  macOS: brew tap homebrew-ffmpeg/ffmpeg && brew install homebrew-ffmpeg/ffmpeg/ffmpeg-full")
        print(f"  SRT file available at: {srt_file}")

    return success


def copy_to_output(files, output_dir):
    """Copy output files to specified directory."""
    import shutil
    os.makedirs(output_dir, exist_ok=True)
    copied = []
    for f in files:
        if os.path.exists(f):
            dest = os.path.join(output_dir, os.path.basename(f))
            shutil.copy2(f, dest)
            copied.append(dest)
    return copied


def main():
    parser = argparse.ArgumentParser(
        description="Manim Animation Pipeline — Render + Subtitle Burn-in"
    )
    parser.add_argument("--scene_file", required=True, help="Manim scene Python file")
    parser.add_argument("--scene_name", required=True, help="Scene class name")
    parser.add_argument(
        "--quality", default="high", choices=["low", "medium", "high", "production"],
        help="Render quality (default: high)"
    )
    parser.add_argument(
        "--burn_subtitles", action="store_true",
        help="Burn SRT subtitles into video using ffmpeg"
    )
    parser.add_argument("--preview", action="store_true", help="Open video after rendering")
    parser.add_argument("--output_dir", default=None, help="Copy output files to this directory")
    parser.add_argument("--font_size", type=int, default=22, help="Subtitle font size (default: 22)")
    parser.add_argument("--margin_v", type=int, default=30, help="Subtitle bottom margin (default: 30)")
    parser.add_argument("--working_dir", default=None, help="Working directory for rendering")
    parser.add_argument(
        "--speed", type=float, default=1.35,
        help="Playback speed multiplier (default: 1.35). Set to 1.0 to disable speed-up."
    )

    args = parser.parse_args()

    # Validate inputs before proceeding
    try:
        validate_scene_name(args.scene_name)
        validate_file_path(args.scene_file)
        if args.working_dir:
            validate_file_path(args.working_dir)
        if args.output_dir:
            validate_file_path(args.output_dir)
    except ValueError as e:
        print(f"\n❌ Input validation error: {e}")
        return 1

    print("=" * 60)
    print("  Manim Animation Pipeline")
    print("=" * 60)
    print(f"  Scene: {args.scene_file} → {args.scene_name}")
    print(f"  Quality: {args.quality}")
    print(f"  Subtitles: {'burn' if args.burn_subtitles else 'skip'}")
    print(f"  Speed:     {args.speed}x")

    # Step 1: Render
    quality_dir = QUALITY_MAP[args.quality]["dir"]

    if not render_scene(args.scene_file, args.scene_name, args.quality, args.working_dir):
        print("\n❌ Render failed!")
        return 1

    # Find output files
    working_dir = args.working_dir or os.path.dirname(os.path.abspath(args.scene_file))
    original_dir = os.getcwd()
    os.chdir(working_dir)

    video_file, srt_file, media_dir = find_output_files(
        args.scene_file, args.scene_name, quality_dir
    )

    if not os.path.exists(video_file):
        print(f"\n❌ Video file not found: {video_file}")
        print(f"  Check media directory: {media_dir}")
        os.chdir(original_dir)
        return 1

    print(f"\n  ✅ Video rendered: {video_file}")

    # Step 2: Burn subtitles
    subtitled_file = None
    if args.burn_subtitles:
        base, ext = os.path.splitext(video_file)
        subtitled_file = f"{base}_subtitled{ext}"
        burn_subtitles(video_file, srt_file, subtitled_file, args.font_size, args.margin_v)

    # Step 3: Speed up video
    fast_file = None
    if args.speed and args.speed != 1.0:
        speed = args.speed
        # Determine input for speed-up:
        # If scene code has built-in subtitles (_make_subtitle), use original video
        # to avoid double subtitles. Otherwise use subtitled version if available.
        if args.burn_subtitles and subtitled_file and os.path.exists(subtitled_file):
            speed_input = subtitled_file
        else:
            speed_input = video_file

        base, ext = os.path.splitext(video_file)
        fast_file = f"{base}_fast{ext}"

        # Build atempo filter chain: atempo only supports [0.5, 100.0] range
        # For speed > 2.0, chain multiple atempo filters
        atempo_filters = []
        remaining = speed
        while remaining > 2.0:
            atempo_filters.append("atempo=2.0")
            remaining /= 2.0
        atempo_filters.append(f"atempo={remaining}")
        atempo_chain = ",".join(atempo_filters)

        filter_complex = f"[0:v]setpts=PTS/{speed}[v];[0:a]{atempo_chain}[a]"

        speed_cmd = [
            "ffmpeg", "-y", "-i", speed_input,
            "-filter_complex", filter_complex,
            "-map", "[v]", "-map", "[a]", fast_file
        ]

        success = run_cmd(speed_cmd, f"Speed up video to {speed}x")
        if success:
            print(f"\n  ✅ Fast video ({speed}x): {fast_file}")
        else:
            print(f"\n  ❌ Speed-up failed.")
            fast_file = None

    # Step 4: Copy to output directory
    if args.output_dir:
        files_to_copy = [video_file]
        if os.path.exists(srt_file):
            files_to_copy.append(srt_file)
        if subtitled_file and os.path.exists(subtitled_file):
            files_to_copy.append(subtitled_file)
        if fast_file and os.path.exists(fast_file):
            files_to_copy.append(fast_file)
        copied = copy_to_output(files_to_copy, args.output_dir)
        print(f"\n  📁 Copied to {args.output_dir}:")
        for c in copied:
            print(f"     - {os.path.basename(c)}")

    # Step 5: Preview
    if args.preview:
        # Prefer fast > subtitled > original
        preview_file = (
            fast_file if fast_file and os.path.exists(fast_file)
            else subtitled_file if subtitled_file and os.path.exists(subtitled_file)
            else video_file
        )
        if sys.platform == "darwin":
            subprocess.run(["open", preview_file])
        elif sys.platform == "linux":
            subprocess.run(["xdg-open", preview_file])

    # Summary
    print(f"\n{'='*60}")
    print("  Done!")
    print(f"  Video:     {video_file}")
    if os.path.exists(srt_file):
        print(f"  Subtitle:  {srt_file}")
    if subtitled_file and os.path.exists(subtitled_file):
        print(f"  Subtitled: {subtitled_file}")
    if fast_file and os.path.exists(fast_file):
        print(f"  Fast:      {fast_file}")
    print(f"{'='*60}")

    os.chdir(original_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
