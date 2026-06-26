#!/usr/bin/env python3
"""
Multi-format live streaming server from a V4L2 webcam or RTSP camera.

Endpoints:
  /             MJPEG stream (works in any browser <img> tag)
  /snap         Single JPEG snapshot
  /hls          HLS stream page (adaptive bitrate, mobile-friendly)
  /hls/stream   HLS .m3u8 playlist
  /rtsp         Info about the RTSP re-stream (if enabled)

Supports:
  - USB webcams via V4L2
  - RTSP/IP cameras as input
  - MJPEG output for low-latency browser viewing
  - HLS output for mobile / remote viewing
  - RTSP re-stream via ffmpeg (optional)
"""

import argparse
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path


class MJPEGFrame:
    """Thread-safe holder for the latest JPEG frame."""

    def __init__(self):
        self._lock = threading.Lock()
        self._frame = None
        self._timestamp = 0.0

    def update(self, data: bytes):
        with self._lock:
            self._frame = data
            self._timestamp = time.monotonic()

    def get(self):
        with self._lock:
            return self._frame, self._timestamp


frame_holder = MJPEGFrame()
server_running = True
hls_dir = None


def build_ffmpeg_input(device: str, rtsp: str | None, width: int, height: int, fps: int):
    """Build the ffmpeg input arguments for either V4L2 or RTSP."""
    if rtsp:
        return ["-rtsp_transport", "tcp", "-i", rtsp]
    return [
        "-f", "v4l2",
        "-video_size", f"{width}x{height}",
        "-framerate", str(fps),
        "-i", device,
    ]


def capture_mjpeg(device: str, rtsp: str | None, width: int, height: int, fps: int):
    """Read JPEG frames from ffmpeg and store them in frame_holder."""
    cmd = [
        "ffmpeg", "-hide_banner", "-loglevel", "error",
        *build_ffmpeg_input(device, rtsp, width, height, fps),
        "-f", "mjpeg",
        "-q:v", "5",
        "-r", str(fps),
        "pipe:1",
    ]

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    buf = b""

    try:
        while server_running:
            chunk = proc.stdout.read(4096)
            if not chunk:
                break
            buf += chunk

            while True:
                start = buf.find(b"\xff\xd8")
                if start == -1:
                    break
                end = buf.find(b"\xff\xd9", start + 2)
                if end == -1:
                    break
                frame = buf[start:end + 2]
                buf = buf[end + 2:]
                frame_holder.update(frame)
    finally:
        proc.terminate()
        proc.wait()
        stderr = proc.stderr.read().decode(errors="replace").strip()
        if stderr:
            print(f"[mjpeg] ffmpeg stderr: {stderr}", file=sys.stderr)


def start_hls(device: str, rtsp: str | None, width: int, height: int, fps: int, hls_path: str):
    """Run an ffmpeg process that writes HLS segments to disk."""
    os.makedirs(hls_path, exist_ok=True)
    playlist = os.path.join(hls_path, "stream.m3u8")

    cmd = [
        "ffmpeg", "-hide_banner", "-loglevel", "error",
        *build_ffmpeg_input(device, rtsp, width, height, fps),
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-tune", "zerolatency",
        "-g", str(fps * 2),
        "-sc_threshold", "0",
        "-f", "hls",
        "-hls_time", "2",
        "-hls_list_size", "5",
        "-hls_flags", "delete_segments+append_list",
        "-hls_segment_filename", os.path.join(hls_path, "seg_%03d.ts"),
        playlist,
    ]

    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

    try:
        while server_running:
            time.sleep(1)
            if proc.poll() is not None:
                break
    finally:
        proc.terminate()
        proc.wait()
        stderr = proc.stderr.read().decode(errors="replace").strip()
        if stderr:
            print(f"[hls] ffmpeg stderr: {stderr}", file=sys.stderr)


def start_rtsp_restream(
    device: str, rtsp_in: str | None, width: int, height: int, fps: int, rtsp_port: int,
):
    """Re-stream the camera as RTSP using ffmpeg (requires ffmpeg with RTSP server support)."""
    rtsp_url = f"rtsp://0.0.0.0:{rtsp_port}/live"

    cmd = [
        "ffmpeg", "-hide_banner", "-loglevel", "error",
        *build_ffmpeg_input(device, rtsp_in, width, height, fps),
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-tune", "zerolatency",
        "-f", "rtsp",
        "-rtsp_transport", "tcp",
        rtsp_url,
    ]

    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

    try:
        while server_running:
            time.sleep(1)
            if proc.poll() is not None:
                break
    finally:
        proc.terminate()
        proc.wait()


HLS_PAGE = """<!DOCTYPE html>
<html><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Camera — HLS Live</title>
<script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
<style>
  body { margin:0; background:#111; display:flex; justify-content:center; align-items:center; height:100vh; }
  video { max-width:100%%; max-height:100vh; }
</style>
</head><body>
<video id="v" controls autoplay muted></video>
<script>
  const url = '/hls/stream.m3u8';
  const v = document.getElementById('v');
  if (Hls.isSupported()) {
    const hls = new Hls({ liveSyncDurationCount:2, liveMaxLatencyDurationCount:4 });
    hls.loadSource(url); hls.attachMedia(v);
  } else if (v.canPlayType('application/vnd.apple.mpegurl')) {
    v.src = url;
  }
</script>
</body></html>"""


class StreamHandler(SimpleHTTPRequestHandler):
    """HTTP handler for MJPEG, HLS, snapshots, and an info page."""

    def do_GET(self):
        if self.path == "/" or self.path == "/mjpeg":
            self._serve_mjpeg()
        elif self.path in ("/snap", "/snapshot"):
            self._serve_snapshot()
        elif self.path == "/hls":
            self._serve_hls_page()
        elif self.path.startswith("/hls/"):
            self._serve_hls_file()
        elif self.path == "/rtsp":
            self._serve_rtsp_info()
        elif self.path == "/status":
            self._serve_status()
        else:
            self.send_error(404)

    def _serve_snapshot(self):
        frame, ts = frame_holder.get()
        if frame is None:
            self.send_error(503, "No frame available yet")
            return
        self.send_response(200)
        self.send_header("Content-Type", "image/jpeg")
        self.send_header("Content-Length", str(len(frame)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(frame)

    def _serve_mjpeg(self):
        self.send_response(200)
        self.send_header("Content-Type", "multipart/x-mixed-replace; boundary=frame")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()

        target_interval = 1.0 / self.server.stream_fps
        try:
            while server_running:
                frame, _ = frame_holder.get()
                if frame is None:
                    time.sleep(0.05)
                    continue

                self.wfile.write(b"--frame\r\n")
                self.wfile.write(b"Content-Type: image/jpeg\r\n")
                self.wfile.write(f"Content-Length: {len(frame)}\r\n".encode())
                self.wfile.write(b"\r\n")
                self.wfile.write(frame)
                self.wfile.write(b"\r\n")
                time.sleep(target_interval)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def _serve_hls_page(self):
        body = HLS_PAGE.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _serve_hls_file(self):
        rel = self.path[len("/hls/"):]
        fpath = os.path.join(hls_dir, rel) if hls_dir else None
        if not fpath or not os.path.isfile(fpath):
            self.send_error(404)
            return

        ctype = "application/vnd.apple.mpegurl" if rel.endswith(".m3u8") else "video/mp2t"
        data = open(fpath, "rb").read()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(data)

    def _serve_rtsp_info(self):
        info = f"RTSP re-stream: rtsp://<this-host>:{self.server.rtsp_port}/live\n"
        body = info.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _serve_status(self):
        frame, ts = frame_holder.get()
        age = f"{time.monotonic() - ts:.1f}s ago" if frame else "no frame"
        info = {
            "status": "running",
            "last_frame": age,
            "frame_size": len(frame) if frame else 0,
            "hls_enabled": hls_dir is not None,
        }
        import json
        body = json.dumps(info, indent=2).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass


class StreamServer(HTTPServer):
    stream_fps = 15
    rtsp_port = 8554


def main():
    global server_running, hls_dir

    parser = argparse.ArgumentParser(
        description="Multi-format live camera streaming server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Endpoints:
  /              MJPEG stream (embed in <img> tag or open in browser)
  /snap          Single JPEG snapshot
  /hls           HLS live page (adaptive, mobile-friendly)
  /hls/stream    HLS .m3u8 playlist (for players like VLC)
  /rtsp          RTSP re-stream info
  /status        JSON status
        """,
    )
    parser.add_argument("--device", type=str, default="/dev/video0",
                        help="V4L2 device path (default: /dev/video0)")
    parser.add_argument("--rtsp", type=str, default=None,
                        help="RTSP input URL (use instead of --device for IP cameras)")
    parser.add_argument("--port", type=int, default=8090,
                        help="HTTP server port (default: 8090)")
    parser.add_argument("--width", type=int, default=640, help="Capture width (default: 640)")
    parser.add_argument("--height", type=int, default=480, help="Capture height (default: 480)")
    parser.add_argument("--fps", type=int, default=15, help="Target FPS (default: 15)")
    parser.add_argument("--enable-hls", action="store_true",
                        help="Enable HLS output (requires more CPU)")
    parser.add_argument("--enable-rtsp", action="store_true",
                        help="Enable RTSP re-stream output")
    parser.add_argument("--rtsp-port", type=int, default=8554,
                        help="RTSP server port (default: 8554)")
    args = parser.parse_args()

    if not args.rtsp and not os.path.exists(args.device):
        print(f"Device {args.device} not found. Run camera_list.py to see available cameras.",
              file=sys.stderr)
        sys.exit(1)

    source = args.rtsp or args.device
    threads = []

    # MJPEG capture thread (always on)
    t = threading.Thread(
        target=capture_mjpeg,
        args=(args.device, args.rtsp, args.width, args.height, args.fps),
        daemon=True,
    )
    t.start()
    threads.append(("mjpeg", t))

    # HLS thread (optional)
    if args.enable_hls:
        hls_dir = tempfile.mkdtemp(prefix="camera_hls_")
        t = threading.Thread(
            target=start_hls,
            args=(args.device, args.rtsp, args.width, args.height, args.fps, hls_dir),
            daemon=True,
        )
        t.start()
        threads.append(("hls", t))

    # RTSP re-stream thread (optional)
    if args.enable_rtsp:
        t = threading.Thread(
            target=start_rtsp_restream,
            args=(args.device, args.rtsp, args.width, args.height, args.fps, args.rtsp_port),
            daemon=True,
        )
        t.start()
        threads.append(("rtsp", t))

    print(f"Camera stream server started")
    print(f"  Source:    {source} ({args.width}x{args.height} @ {args.fps}fps)")
    print(f"  MJPEG:     http://0.0.0.0:{args.port}/")
    print(f"  Snapshot:  http://0.0.0.0:{args.port}/snap")
    print(f"  Status:    http://0.0.0.0:{args.port}/status")
    if args.enable_hls:
        print(f"  HLS page:  http://0.0.0.0:{args.port}/hls")
        print(f"  HLS m3u8:  http://0.0.0.0:{args.port}/hls/stream.m3u8")
    if args.enable_rtsp:
        print(f"  RTSP:      rtsp://0.0.0.0:{args.rtsp_port}/live")
    print(f"\nPress Ctrl+C to stop.\n")

    server = StreamServer(("0.0.0.0", args.port), StreamHandler)
    server.stream_fps = args.fps
    server.rtsp_port = args.rtsp_port

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping...")
        server_running = False
        server.shutdown()
    finally:
        if hls_dir and os.path.isdir(hls_dir):
            shutil.rmtree(hls_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
