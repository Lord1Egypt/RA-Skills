#!/usr/bin/env python3
"""
TRTC 推流守护进程 — v23 纯 Python 帧生成版
- 移除 Xvfb + tkinter Dashboard + FFmpeg 屏幕采集的整条链路
- 直接用 Pillow (FrameRenderer) 在内存中绘制 Dashboard 画面
- PyAV 编码 → RTMP 推流（保持不变）
- AudioMixer TTS 音频混入（保持不变）
- 自动重连（保持不变）
- 进程数从 6-7 个缩减到 2-3 个
"""
import av
import json
import numpy as np
import time
import sys
import os
import signal
import fractions
import datetime
from pathlib import Path

try:
    from platform_utils import (
        get_work_dir, get_platform_tag,
        register_signal_handlers,
        get_rotating_logger
    )
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from platform_utils import (
        get_work_dir, get_platform_tag,
        register_signal_handlers,
        get_rotating_logger
    )

try:
    from frame_renderer import FrameRenderer
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from frame_renderer import FrameRenderer

# ── 配置 ──────────────────────────────────────────────────
# deploy_scripts() 会在部署时用 config.json 中的真实 RTMP URL 替换此占位符
RTMP_URL = "__RTMP_URL_PLACEHOLDER__"
WIDTH, HEIGHT = 1920, 1080
FPS = 20

WORK_DIR = get_work_dir()
WORK_DIR.mkdir(parents=True, exist_ok=True)
PID_FILE = str(WORK_DIR / "daemon.pid")
LOG_FILE = str(WORK_DIR / "daemon.log")
RECONNECT_DELAY = 3   # 断流后等待秒数再重连
MAX_RETRIES = 999     # 最大重连次数
AUDIO_QUEUE_DIR = WORK_DIR / "audio_queue"  # TTS 语音文件队列目录


# ── AudioMixer — 从 TTS 队列读取语音，无语音时填充静默 ─────
class AudioMixer:
    """
    从 audio_queue/ 目录读取 TTS 生成的 .npy 文件，
    按顺序混入推流音轨。无语音时输出静默帧。
    """

    def __init__(self):
        self._buffer = np.array([], dtype=np.float32)
        self._silence_cache = {}
        self._tts_flag_file = WORK_DIR / "tts_playing.flag"
        self._last_flag_state = None

    def _get_silence(self, num_samples: int) -> np.ndarray:
        if num_samples not in self._silence_cache:
            self._silence_cache[num_samples] = np.zeros((1, num_samples), dtype=np.float32)
        return self._silence_cache[num_samples]

    @property
    def has_audio(self) -> bool:
        if len(self._buffer) > 0:
            return True
        try:
            qdir = str(AUDIO_QUEUE_DIR)
            if os.path.isdir(qdir):
                with os.scandir(qdir) as entries:
                    for entry in entries:
                        if entry.name.endswith('.npy') and entry.is_file():
                            return True
        except Exception:
            pass
        return False

    def get_samples(self, num_samples: int) -> np.ndarray:
        while len(self._buffer) < num_samples:
            chunk = self._load_next()
            if chunk is None:
                break
            self._buffer = np.concatenate([self._buffer, chunk])

        if len(self._buffer) >= num_samples:
            out = self._buffer[:num_samples]
            self._buffer = self._buffer[num_samples:]
            self._update_tts_flag(True)
            return out.reshape(1, -1)

        if len(self._buffer) > 0:
            pad = np.zeros(num_samples - len(self._buffer), dtype=np.float32)
            out = np.concatenate([self._buffer, pad])
            self._buffer = np.array([], dtype=np.float32)
            self._update_tts_flag(True)
            return out.reshape(1, -1)

        self._update_tts_flag(False)
        return self._get_silence(num_samples)

    def _update_tts_flag(self, playing: bool):
        """写入 tts_playing.flag 时间戳（由 /api/agent-state 判断 2 秒消退）"""
        try:
            if playing:
                # 每次有音频输出时更新时间戳
                self._tts_flag_file.write_text(str(time.time()))
                self._last_flag_state = True
            elif self._last_flag_state is True:
                # 停止时也写一次最终时间戳（让 API 端延迟 2 秒后判定结束）
                self._tts_flag_file.write_text(str(time.time()))
                self._last_flag_state = False
        except Exception:
            pass

    def _load_next(self) -> np.ndarray | None:
        qdir = str(AUDIO_QUEUE_DIR)
        if not os.path.isdir(qdir):
            return None
        try:
            npy_files = sorted(
                entry.path for entry in os.scandir(qdir)
                if entry.name.endswith('.npy') and entry.is_file()
            )
        except OSError:
            return None
        if not npy_files:
            return None
        target = npy_files[0]
        try:
            audio = np.load(target, allow_pickle=False)
            os.remove(target)
            if audio.dtype != np.float32:
                audio = audio.astype(np.float32)
            return audio
        except Exception as e:
            log(f"AudioMixer: failed to load {Path(target).name}: {e}", "WARN")
            try:
                os.remove(target)
            except OSError:
                pass
            return None

# ── 日志（带轮转，最大 5MB × 3 备份 = 15MB）──────────────
_logger = get_rotating_logger("stream_daemon", LOG_FILE,
                              max_bytes=5 * 1024 * 1024, backup_count=3)

def log(msg, level="INFO"):
    if level == "ERROR":
        _logger.error(msg)
    elif level == "WARN":
        _logger.warning(msg)
    else:
        _logger.info(msg)

# ── 信号处理 ─────────────────────────────────────────────
_running = True

def _sig_handler(signum, frame):
    global _running
    log(f"Received signal {signum}, shutting down...", "WARN")
    _running = False

# 忽略 SIGTERM（抗 OpenClaw 容器定期清理非自管进程）
# 只响应 SIGINT（调试）或 SIGKILL（setup.py --stop 强制杀）
signal.signal(signal.SIGTERM, signal.SIG_IGN)
signal.signal(signal.SIGINT, _sig_handler)

# ── 写 PID ────────────────────────────────────────────────
with open(PID_FILE, 'w') as f:
    f.write(str(os.getpid()))
log(f"Daemon started. PID={os.getpid()}  Platform={get_platform_tag()}")
log("Mode: Pillow frame rendering (no Xvfb/tkinter/FFmpeg)")

# ── RTMP URL 校验（启动阶段诊断）──────────────────────────
if "__RTMP_URL_PLACEHOLDER__" in RTMP_URL or not RTMP_URL.startswith("rtmp://"):
    log(f"FATAL: RTMP_URL is invalid or still a placeholder: {RTMP_URL[:80]}", "ERROR")
    log("Hint: deploy_scripts() may not have patched this file. "
        "Re-run setup.py --sdkappid/--secret to regenerate.", "ERROR")
    sys.exit(1)
else:
    log(f"RTMP URL validated: {RTMP_URL[:80]}...")

# ── 初始化 FrameRenderer ──────────────────────────────────
renderer = FrameRenderer(logger=log)
log("FrameRenderer initialized ✓")

# ── RTMP 连接预检（避免 av.open 长时间阻塞被平台 SIGTERM 杀死）──
def _check_rtmp_reachable(url: str, timeout: int = 5) -> bool:
    """用 TCP socket 预检 RTMP 服务器是否可达（默认 5 秒超时）。
    避免 av.open() 在 TCP SYN 重传阶段阻塞 ~28 秒，
    期间进程无法响应外部信号，被 OpenClaw 平台超时杀死。
    """
    import socket
    from urllib.parse import urlparse
    try:
        parsed = urlparse(url)
        host = parsed.hostname or "rtmp.rtc.qq.com"
        port = parsed.port or 1935
        log(f"Pre-check RTMP server {host}:{port} (timeout={timeout}s)...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))
        sock.close()
        log(f"RTMP server {host}:{port} reachable ✓")
        return True
    except (socket.timeout, socket.error, OSError) as e:
        log(f"RTMP server {host}:{port} unreachable: {e}", "ERROR")
        return False

# ── 单次推流 session ──────────────────────────────────────
def run_stream_session():
    log("Opening RTMP output...")

    # 预检：TCP 连通性测试（快速失败，避免 av.open 阻塞 ~28s 被平台杀死）
    if not _check_rtmp_reachable(RTMP_URL, timeout=8):
        log("RTMP pre-check failed, skipping this session (will retry)", "ERROR")
        return

    output = av.open(RTMP_URL, mode='w', format='flv',
                     options={
                         'flvflags': 'no_duration_filesize',
                         'timeout': '10000000',    # TCP 连接超时 10 秒（单位微秒）
                         'rw_timeout': '10000000',  # 读写超时 10 秒（单位微秒）
                     })

    vstream = output.add_stream('libx264', rate=FPS)
    vstream.width = WIDTH
    vstream.height = HEIGHT
    vstream.pix_fmt = 'yuv420p'
    vstream.options = {
        'preset': 'medium',
        'profile': 'baseline',
        'tune': 'zerolatency',
        'g': str(FPS * 2),
        'bf': '0',
        'sc_threshold': '0',
        'maxrate': '1500k',
        'bufsize': '3000k',
    }
    vstream.bit_rate = 1_500_000

    astream = output.add_stream('aac', rate=44100, layout='mono')
    astream.bit_rate = 64_000

    # 预缓存常量
    _video_time_base = fractions.Fraction(1, FPS)
    _audio_time_base = fractions.Fraction(1, 44100)
    _frame_interval = 1.0 / FPS

    frame_count = 0
    samples_sent = 0
    audio_samples = 1024
    mixer = AudioMixer()
    start = time.time()

    log("Streaming started ✓")

    while _running:
        frame_start = time.time()

        # ── 直接从 FrameRenderer 获取帧（零拷贝，无 pipe）──
        arr = renderer.render_frame()

        vframe = av.VideoFrame.from_ndarray(arr, format='rgb24')
        vframe = vframe.reformat(format='yuv420p')
        vframe.pts = frame_count
        vframe.time_base = _video_time_base

        for packet in vstream.encode(vframe):
            output.mux(packet)

        # ── 音频同步 ──
        target_samples = int((frame_count + 1) / FPS * 44100)
        while samples_sent < target_samples:
            audio_data = mixer.get_samples(audio_samples)
            aframe = av.AudioFrame.from_ndarray(audio_data, format='fltp', layout='mono')
            aframe.sample_rate = 44100
            aframe.pts = samples_sent
            aframe.time_base = _audio_time_base
            for packet in astream.encode(aframe):
                output.mux(packet)
            samples_sent += audio_samples

        frame_count += 1

        # ── 帧率控制（精确 sleep 到下一帧时间点）──
        elapsed = time.time() - frame_start
        sleep_time = _frame_interval - elapsed
        if sleep_time > 0.001:
            time.sleep(sleep_time)

        # ── 健康日志（每 30 秒）──
        if frame_count % (FPS * 30) == 0:
            total_elapsed = time.time() - start
            fps = frame_count / total_elapsed
            log(f"Frames={frame_count} Elapsed={total_elapsed:.0f}s FPS={fps:.1f}")

    # cleanup
    try:
        for pkt in vstream.encode(): output.mux(pkt)
        for pkt in astream.encode(): output.mux(pkt)
    except: pass
    output.close()
    log("Stream session closed")


# ── 主循环（自动重连）────────────────────────────────────
retry = 0
while _running and retry < MAX_RETRIES:
    try:
        run_stream_session()
    except Exception as e:
        log(f"Stream error: {e}", "ERROR")
        import traceback
        _logger.error(traceback.format_exc())

    if not _running:
        break
    retry += 1
    log(f"Reconnecting in {RECONNECT_DELAY}s (attempt {retry}/{MAX_RETRIES})...", "WARN")
    time.sleep(RECONNECT_DELAY)

log("Daemon exiting.")
try: os.remove(PID_FILE)
except: pass
