"""
简单高效的回声消除方案：半双工切换 + 音量归一化。

原理：
- 扬声器（BlackHole）有声音 → 麦克风有回声 → 只取扬声器
- 扬声器（BlackHole）无声 → 麦克风录到人声 → 只取麦克风
- 两者音量归一化到同一级别

优点：O(n) 线性时间，再长的录音也是秒级完成。
"""

import sys
import wave
from pathlib import Path

import numpy as np


def read_wav(path):
    with wave.open(str(path), 'rb') as w:
        sr = w.getframerate()
        raw = w.readframes(w.getnframes())
        samples = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    return sr, samples


def write_wav(path, sr, samples):
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((samples * 32767).astype(np.int16).tobytes())


def rms_energy(x):
    """计算 RMS 能量 (dB)。"""
    return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-10)


def normalize_to_target(x, target_rms_db=-20):
    """将信号 RMS 归一化到目标电平。"""
    current_db = rms_energy(x)
    gain = 10 ** ((target_rms_db - current_db) / 20)
    return np.clip(x * gain, -0.99, 0.99)


def echo_cancel(sys_path, mic_path, output_path, frame_ms=30):
    """
    半双工回声消除 + 音量归一化。
    
    策略：逐帧分析系统音频能量，决定当前帧用哪个源。
    - frame_ms: 分析帧长（毫秒），默认 30ms
    """
    sr, sys_audio = read_wav(sys_path)
    sr2, mic_audio = read_wav(mic_path)
    
    if sr != sr2:
        sr = min(sr, sr2)
    
    min_len = min(len(sys_audio), len(mic_audio))
    sys_audio = sys_audio[:min_len]
    mic_audio = mic_audio[:min_len]
    
    # 帧参数
    frame_size = max(1, int(sr * frame_ms / 1000))
    n_frames = max(1, (min_len + frame_size - 1) // frame_size)

    # 用原始系统音频做门限判断，避免 normalize 把 BlackHole 底噪放大后误判为“系统有声”。
    sys_frame_db = np.array([
        rms_energy(sys_audio[i * frame_size:min((i + 1) * frame_size, min_len)])
        for i in range(n_frames)
    ])
    noise_floor = float(np.percentile(sys_frame_db, 20))
    sys_threshold = max(-50.0, min(-30.0, noise_floor + 12.0))
    sys_active_flags = sys_frame_db > sys_threshold

    # 音量归一化到同一目标
    print("🎚️ 音量归一化...")
    sys_norm = normalize_to_target(sys_audio, -20)
    mic_norm = normalize_to_target(mic_audio, -20)
    
    # 逐帧处理：用平滑的 mic_ratio 做交叉混合
    # sys 有声 → mic_ratio=0（100% 系统音频）
    # sys 无声 → mic_ratio 0→1 渐变过渡（0.5s 从系统切到麦克风）
    # sys 又响 → mic_ratio 立即归 0（切回系统音频）
    output = np.zeros(min_len, dtype=np.float32)
    fade_samples = int(sr * 0.5)  # 0.5s 渐变长度
    attack = 1.0 / fade_samples  # 每采样点增量
    
    print(f"🔇 半双工混合 (帧长={frame_ms}ms, 噪声底={noise_floor:.1f}dB, 阈值={sys_threshold:.1f}dB, 渐变=0.5s)...")
    
    mic_ratio = 0.0  # 0=纯系统音频, 1=纯麦克风
    sys_active = False  # 系统当前是否有声
    
    for i in range(min_len):
        frame_idx = i // frame_size
        frame_start = frame_idx * frame_size
        
        # 每帧计算一次系统音频能量
        if i == frame_start:
            sys_active = bool(sys_active_flags[min(frame_idx, n_frames - 1)])
        
        if sys_active:
            # 系统有声音：mic_ratio 立即清零（切回系统音频）
            mic_ratio = 0.0
        else:
            # 系统无声：mic_ratio 渐增（麦克风慢慢变强）
            mic_ratio = min(1.0, mic_ratio + attack)
        
        # 交叉混合
        output[i] = (1.0 - mic_ratio) * sys_norm[i] + mic_ratio * mic_norm[i]
    
    # 统计
    sys_cnt = int(np.count_nonzero(sys_active_flags))
    print(f"📊 组成: 系统音频 {sys_cnt/n_frames*100:.0f}% | 麦克风 {(1-sys_cnt/n_frames)*100:.0f}%")
    
    # 最终音量提升
    output = np.clip(output * 1.5, -0.99, 0.99)
    
    write_wav(output_path, sr, output)
    size_mb = Path(output_path).stat().st_size / 1024 / 1024
    print(f"✅ 完成: {output_path} ({size_mb:.1f}MB)")
    return str(output_path)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: echo_cancel.py <sys_audio.wav> <mic_audio.wav> [output.wav]", file=sys.stderr)
        sys.exit(1)
    sys_path = sys.argv[1]
    mic_path = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) > 3 else \
        str(Path(mic_path).with_suffix(".mic_clean.wav"))
    echo_cancel(sys_path, mic_path, output_path)
