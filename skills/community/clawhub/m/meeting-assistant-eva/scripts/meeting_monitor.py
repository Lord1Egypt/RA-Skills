#!/usr/bin/env python3
"""
Meeting Monitor — 会议监控主控脚本
负责协调截屏、录音、转录、分析的完整流程。
"""

import argparse
import json
import os
import signal
import subprocess
import sys
import time
import threading
from datetime import datetime
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = SKILL_DIR / "config.json"
PID_FILE = SKILL_DIR / ".monitor.pid"
SESSION_FILE = None  # set at runtime


def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)


def get_conda_bin(config, name):
    """Get path to an executable from the conda env config."""
    conda = config.get("conda_env", {})
    # Direct path override in config
    if name in conda:
        return conda[name]
    # Try Scripts dir
    scripts_dir = conda.get("scripts_dir", "")
    if scripts_dir:
        candidate = Path(scripts_dir) / f"{name}.exe"
        if candidate.exists():
            return str(candidate)
    return name  # fallback to system PATH


def get_session_dir(config, custom_dir=None):
    if custom_dir:
        p = Path(custom_dir)
    else:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        p = SKILL_DIR / config["output_base_dir"] / ts
    p.mkdir(parents=True, exist_ok=True)
    for sub in ["audio", "audio/chunks", "screenshots", "transcripts", "analysis"]:
        (p / sub).mkdir(parents=True, exist_ok=True)
    return p


def save_session_meta(session_dir, config, mode, extra=None):
    meta = {
        "start_time": datetime.now().isoformat(),
        "mode": mode,
        "config": config,
        "status": "recording",
    }
    if extra:
        meta.update(extra)
    with open(session_dir / "session.json", "w") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
    return meta


def update_session_status(session_dir, status):
    meta_path = session_dir / "session.json"
    if meta_path.exists():
        with open(meta_path) as f:
            meta = json.load(f)
    else:
        meta = {}
    meta["status"] = status
    meta["end_time"] = datetime.now().isoformat()
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)


# ─── Audio Recording ────────────────────────────────────────

class AudioRecorder:
    """Record system audio via ffmpeg (PulseAudio monitor on Linux, WASAPI loopback on Windows)."""

    def __init__(self, session_dir, config):
        self.session_dir = session_dir
        self.config = config
        self.process = None
        self.output_path = session_dir / "audio" / "full_recording.wav"

    def _detect_audio_source(self):
        """Detect the best audio source for recording system audio."""
        device = self.config.get("audio", {}).get("device", "default")
        if device != "default":
            return device

        ffmpeg = get_conda_bin(self.config, "ffmpeg")
        is_windows = sys.platform == "win32" or ffmpeg.endswith(".exe")

        if is_windows:
            # On Windows, list dshow audio devices
            try:
                result = subprocess.run(
                    [ffmpeg, "-list_devices", "true", "-f", "dshow", "-i", "dummy"],
                    capture_output=True, text=True, timeout=10
                )
                # Parse stderr for audio devices
                lines = result.stderr.split("\n")
                audio_section = False
                for line in lines:
                    if "audio" in line.lower() and "DirectShow" in line:
                        audio_section = True
                    if audio_section and '"' in line:
                        # Extract device name between quotes
                        start = line.index('"') + 1
                        end = line.index('"', start)
                        device_name = line[start:end]
                        if device_name and "video" not in device_name.lower():
                            return device_name
            except (FileNotFoundError, subprocess.TimeoutExpired, ValueError):
                pass
            # Windows fallback: Stereo Mix (common loopback name)
            return "Stereo Mix (Realtek(R) Audio)"

        # Linux: Try PulseAudio monitor source (captures system output)
        try:
            result = subprocess.run(
                ["pactl", "list", "short", "sources"],
                capture_output=True, text=True, timeout=5
            )
            for line in result.stdout.strip().split("\n"):
                if ".monitor" in line:
                    return line.split("\t")[1]
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        # Fallback: try pipewire
        try:
            result = subprocess.run(
                ["pw-cli", "list-objects"],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                return "pipewire"
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        return "default"

    def start(self):
        source = self._detect_audio_source()
        sample_rate = self.config.get("audio", {}).get("sample_rate", 16000)
        channels = self.config.get("audio", {}).get("channels", 1)
        ffmpeg = get_conda_bin(self.config, "ffmpeg")

        # On Windows (conda env), use dshow for audio capture
        is_windows = sys.platform == "win32" or ffmpeg.endswith(".exe")
        if is_windows:
            cmd = [
                ffmpeg, "-y",
                "-f", "dshow",
                "-i", f"audio={source}",
                "-ac", str(channels),
                "-ar", str(sample_rate),
                "-acodec", "pcm_s16le",
                str(self.output_path)
            ]
        else:
            cmd = [
                ffmpeg, "-y",
                "-f", "pulse",
                "-i", source,
                "-ac", str(channels),
                "-ar", str(sample_rate),
                "-acodec", "pcm_s16le",
                str(self.output_path)
            ]

        print(f"[Audio] Recording from: {source}")
        print(f"[Audio] Output: {self.output_path}")

        self.process = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )

    def stop(self):
        if self.process:
            self.process.send_signal(signal.SIGINT)
            try:
                self.process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.process.kill()
            print(f"[Audio] Recording saved: {self.output_path}")

    def split_chunks(self):
        """Split full recording into chunks for Whisper processing."""
        chunk_minutes = self.config.get("audio_chunk_minutes", 5)
        chunks_dir = self.session_dir / "audio" / "chunks"
        full_audio = self.output_path

        if not full_audio.exists():
            print("[Audio] No recording found to split")
            return []

        ffmpeg = get_conda_bin(self.config, "ffmpeg")
        cmd = [
            ffmpeg, "-y",
            "-i", str(full_audio),
            "-f", "segment",
            "-segment_time", str(chunk_minutes * 60),
            "-c", "copy",
            str(chunks_dir / "chunk_%03d.wav")
        ]

        subprocess.run(cmd, capture_output=True)
        chunks = sorted(chunks_dir.glob("chunk_*.wav"))
        print(f"[Audio] Split into {len(chunks)} chunks")
        return chunks


# ─── Screenshot Capture ─────────────────────────────────────

class ScreenCapture:
    """Capture screenshots periodically, using pc-control skill or ffmpeg."""

    def __init__(self, session_dir, config):
        self.session_dir = session_dir
        self.config = config
        self.screenshots_dir = session_dir / "screenshots"
        self.counter = 0
        self._stop_event = threading.Event()
        self._thread = None

    def _capture_one(self):
        """Take a single screenshot."""
        self.counter += 1
        filename = f"screen_{self.counter:04d}.png"
        filepath = self.screenshots_dir / filename

        use_pc_control = self.config.get("screenshot", {}).get("use_pc_control", True)

        if use_pc_control:
            # Use pc-control skill's client
            try:
                pc_scripts = SKILL_DIR.parent / "pc-control" / "scripts"
                sys.path.insert(0, str(pc_scripts))
                from client import PCControl
                pc = PCControl()
                scale = self.config.get("screenshot", {}).get("scale", 0.5)
                quality = self.config.get("screenshot", {}).get("quality", 70)
                tmp_path = pc.screenshot(scale=scale, quality=quality)
                if tmp_path and Path(tmp_path).exists():
                    Path(tmp_path).rename(filepath)
                    return filepath
            except Exception as e:
                print(f"[Screenshot] pc-control failed: {e}, falling back to ffmpeg")

        # Fallback: ffmpeg screen grab (Windows via gdigrab)
        try:
            powershell = "/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe"
            win_path = str(filepath).replace("/", "\\")
            # Use PowerShell to take screenshot
            ps_script = f"""
Add-Type -AssemblyName System.Windows.Forms
$screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$bitmap = New-Object System.Drawing.Bitmap($screen.Width, $screen.Height)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.CopyFromScreen($screen.Location, [System.Drawing.Point]::Empty, $screen.Size)
$bitmap.Save('{win_path}')
$graphics.Dispose()
$bitmap.Dispose()
"""
            subprocess.run(
                [powershell, "-Command", ps_script],
                capture_output=True, timeout=15
            )
            if filepath.exists():
                return filepath
        except Exception as e:
            print(f"[Screenshot] PowerShell capture failed: {e}")

        # Last fallback: import/scrot on Linux
        try:
            subprocess.run(
                ["scrot", str(filepath)],
                capture_output=True, timeout=10
            )
            if filepath.exists():
                return filepath
        except FileNotFoundError:
            pass

        print(f"[Screenshot] All capture methods failed for {filename}")
        return None

    def _loop(self, interval):
        while not self._stop_event.is_set():
            path = self._capture_one()
            ts = datetime.now().strftime("%H:%M:%S")
            if path:
                print(f"[Screenshot] {ts} → {path.name}")
            self._stop_event.wait(interval)

    def start(self, interval=30):
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._loop, args=(interval,), daemon=True)
        self._thread.start()
        print(f"[Screenshot] Capturing every {interval}s")

    def stop(self):
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=5)
        print(f"[Screenshot] Stopped. Total captures: {self.counter}")

    def snapshot(self):
        """Take a single immediate screenshot."""
        return self._capture_one()


# ─── Whisper Transcription ──────────────────────────────────

class Transcriber:
    """Transcribe audio chunks using OpenAI Whisper."""

    def __init__(self, session_dir, config):
        self.session_dir = session_dir
        self.config = config
        self.transcripts_dir = session_dir / "transcripts"

    def transcribe_chunk(self, audio_path):
        """Transcribe a single audio file."""
        model = self.config.get("whisper_model", "base")
        language = self.config.get("whisper_language", "zh")
        whisper_bin = get_conda_bin(self.config, "whisper")

        output_name = audio_path.stem
        output_path = self.transcripts_dir / f"{output_name}.txt"

        cmd = [
            whisper_bin,
            str(audio_path),
            "--model", model,
            "--language", language,
            "--output_format", "txt",
            "--output_dir", str(self.transcripts_dir),
        ]

        device = self.config.get("integration", {}).get("whisper_device", "cpu")
        if device != "cpu":
            cmd.extend(["--device", device])

        print(f"[Whisper] Transcribing: {audio_path.name}")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"[Whisper] Error: {result.stderr[:200]}")
            return None

        if output_path.exists():
            return output_path
        # whisper may name output differently
        candidates = list(self.transcripts_dir.glob(f"{output_name}*"))
        return candidates[0] if candidates else None

    def transcribe_all(self, chunks):
        """Transcribe all audio chunks and merge into full transcript."""
        transcripts = []
        for chunk in sorted(chunks):
            result = self.transcribe_chunk(chunk)
            if result:
                transcripts.append(result)

        # Merge into full transcript
        full_path = self.transcripts_dir / "full_transcript.txt"
        with open(full_path, "w", encoding="utf-8") as out:
            for i, t in enumerate(transcripts):
                text = t.read_text(encoding="utf-8").strip()
                chunk_min = i * self.config.get("audio_chunk_minutes", 5)
                out.write(f"\n--- [{chunk_min}-{chunk_min + 5} min] ---\n")
                out.write(text + "\n")

        print(f"[Whisper] Full transcript: {full_path}")
        return full_path

    def transcribe_recent(self, full_audio_path, last_minutes=5):
        """Transcribe only the last N minutes of audio."""
        temp_path = self.session_dir / "audio" / "_recent_clip.wav"
        ffmpeg = get_conda_bin(self.config, "ffmpeg")
        cmd = [
            ffmpeg, "-y",
            "-sseof", f"-{last_minutes * 60}",
            "-i", str(full_audio_path),
            "-c", "copy",
            str(temp_path)
        ]
        subprocess.run(cmd, capture_output=True)
        if temp_path.exists():
            result = self.transcribe_chunk(temp_path)
            temp_path.unlink(missing_ok=True)
            return result
        return None


# ─── Main Monitor Controller ────────────────────────────────

class MeetingMonitor:
    """Orchestrates the full meeting monitoring pipeline."""

    def __init__(self, config, session_dir, mode="general"):
        self.config = config
        self.session_dir = session_dir
        self.mode = mode
        self.audio = AudioRecorder(session_dir, config)
        self.screen = ScreenCapture(session_dir, config)
        self.transcriber = Transcriber(session_dir, config)
        self._running = False

    def start(self, interval=30):
        """Start recording audio and capturing screenshots."""
        self._running = True
        save_session_meta(self.session_dir, self.config, self.mode)

        # Save PID for external stop
        with open(PID_FILE, "w") as f:
            json.dump({
                "pid": os.getpid(),
                "session_dir": str(self.session_dir),
                "start_time": datetime.now().isoformat()
            }, f)

        print(f"[Monitor] Starting meeting monitor")
        print(f"[Monitor] Mode: {self.mode}")
        print(f"[Monitor] Session: {self.session_dir}")
        print(f"[Monitor] Screenshot interval: {interval}s")

        # Start audio recording
        try:
            self.audio.start()
        except Exception as e:
            print(f"[Monitor] Audio recording failed to start: {e}")
            print("[Monitor] Continuing with screenshots only")

        # Start screenshot loop
        self.screen.start(interval=interval)

        # Keep running until signaled
        def handle_stop(signum, frame):
            print(f"\n[Monitor] Received stop signal")
            self.stop()
            sys.exit(0)

        signal.signal(signal.SIGINT, handle_stop)
        signal.signal(signal.SIGTERM, handle_stop)

        print("[Monitor] Running... (Ctrl+C or `meeting_monitor.py stop` to end)")

        # Block until stopped
        try:
            while self._running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """Stop all recording and generate outputs."""
        self._running = False
        print("[Monitor] Stopping...")

        self.screen.stop()
        self.audio.stop()

        # Split audio and transcribe
        print("[Monitor] Processing audio...")
        chunks = self.audio.split_chunks()
        if chunks:
            self.transcriber.transcribe_all(chunks)

        update_session_status(self.session_dir, "completed")
        PID_FILE.unlink(missing_ok=True)

        print(f"[Monitor] Session complete: {self.session_dir}")
        self._print_summary()

    def snapshot(self):
        """Take immediate screenshot for analysis."""
        path = self.screen.snapshot()
        if path:
            print(f"[Snapshot] Saved: {path}")
            print(f"[Snapshot] Use Claude to analyze: Read {path}")
        return path

    def get_recent_transcript(self, minutes=5):
        """Get transcript of last N minutes."""
        audio_path = self.session_dir / "audio" / "full_recording.wav"
        if audio_path.exists():
            return self.transcriber.transcribe_recent(audio_path, minutes)
        print("[Transcript] No audio recording found")
        return None

    def _print_summary(self):
        screenshots = list((self.session_dir / "screenshots").glob("*.png"))
        transcripts = list((self.session_dir / "transcripts").glob("*.txt"))
        print(f"\n{'='*50}")
        print(f"  Meeting Session Summary")
        print(f"{'='*50}")
        print(f"  Screenshots captured: {len(screenshots)}")
        print(f"  Transcript files:     {len(transcripts)}")
        print(f"  Output directory:     {self.session_dir}")
        print(f"{'='*50}")
        print(f"\nTo generate AI summary, ask the agent to:")
        print(f"  1. Read {self.session_dir}/transcripts/full_transcript.txt")
        print(f"  2. Analyze screenshots in {self.session_dir}/screenshots/")
        print(f"  3. Generate meeting_summary.md")


# ─── CLI ────────────────────────────────────────────────────

def cmd_start(args):
    config = load_config()
    if args.mode == "medical":
        config["medical"]["enabled"] = True
    session_dir = get_session_dir(config, args.output_dir)
    interval = args.interval or config.get("screenshot_interval", 30)
    monitor = MeetingMonitor(config, session_dir, mode=args.mode)
    monitor.start(interval=interval)


def cmd_stop(args):
    if not PID_FILE.exists():
        print("[Monitor] No active session found")
        return

    with open(PID_FILE) as f:
        info = json.load(f)

    pid = info["pid"]
    print(f"[Monitor] Sending stop signal to PID {pid}")
    try:
        os.kill(pid, signal.SIGTERM)
        print("[Monitor] Stop signal sent")
    except ProcessLookupError:
        print("[Monitor] Process not found, cleaning up")
        PID_FILE.unlink(missing_ok=True)


def cmd_snapshot(args):
    if not PID_FILE.exists():
        # No active session, just take a one-off screenshot
        config = load_config()
        session_dir = get_session_dir(config)
        screen = ScreenCapture(session_dir, config)
        path = screen.snapshot()
        if path:
            print(f"Screenshot saved: {path}")
        return

    with open(PID_FILE) as f:
        info = json.load(f)
    session_dir = Path(info["session_dir"])
    config = load_config()
    screen = ScreenCapture(session_dir, config)
    path = screen.snapshot()
    if path:
        print(f"Screenshot saved: {path}")


def cmd_transcript(args):
    config = load_config()
    if PID_FILE.exists():
        with open(PID_FILE) as f:
            info = json.load(f)
        session_dir = Path(info["session_dir"])
    else:
        # Find most recent session
        base = SKILL_DIR / config["output_base_dir"]
        sessions = sorted(base.iterdir(), reverse=True) if base.exists() else []
        if not sessions:
            print("No sessions found")
            return
        session_dir = sessions[0]

    transcriber = Transcriber(session_dir, config)
    audio_path = session_dir / "audio" / "full_recording.wav"
    if audio_path.exists():
        result = transcriber.transcribe_recent(audio_path, args.last)
        if result:
            print(f"\n--- Last {args.last} minutes ---")
            print(result.read_text(encoding="utf-8"))
    else:
        print("No audio recording found in current session")


def cmd_status(args):
    if PID_FILE.exists():
        with open(PID_FILE) as f:
            info = json.load(f)
        print(f"[Status] Active session")
        print(f"  PID:     {info['pid']}")
        print(f"  Dir:     {info['session_dir']}")
        print(f"  Started: {info['start_time']}")

        session_dir = Path(info["session_dir"])
        screenshots = list((session_dir / "screenshots").glob("*.png"))
        print(f"  Screenshots so far: {len(screenshots)}")

        audio_path = session_dir / "audio" / "full_recording.wav"
        if audio_path.exists():
            size_mb = audio_path.stat().st_size / (1024 * 1024)
            print(f"  Audio size: {size_mb:.1f} MB")
    else:
        print("[Status] No active session")


def main():
    parser = argparse.ArgumentParser(description="Meeting Monitor — 会议监控")
    sub = parser.add_subparsers(dest="command")

    p_start = sub.add_parser("start", help="Start meeting monitoring")
    p_start.add_argument("--interval", type=int, help="Screenshot interval in seconds")
    p_start.add_argument("--audio-device", help="Audio input device")
    p_start.add_argument("--output-dir", help="Custom output directory")
    p_start.add_argument("--mode", choices=["general", "medical"], default="general")

    sub.add_parser("stop", help="Stop monitoring and generate summary")
    sub.add_parser("snapshot", help="Take immediate screenshot")

    p_trans = sub.add_parser("transcript", help="Get recent transcript")
    p_trans.add_argument("--last", type=int, default=5, help="Last N minutes")

    sub.add_parser("status", help="Check monitor status")

    args = parser.parse_args()

    commands = {
        "start": cmd_start,
        "stop": cmd_stop,
        "snapshot": cmd_snapshot,
        "transcript": cmd_transcript,
        "status": cmd_status,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
