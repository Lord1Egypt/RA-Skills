#!/usr/bin/env python3
"""
Voiceprint Manager - 声纹注册/识别/管理
使用 ONNX Runtime + ResNet34 声纹模型，无需 PyTorch

用法：
  python3 voiceprint-manager.py enroll --name "Jack" --audio /path/to/audio.wav
  python3 voiceprint-manager.py identify --audio /path/to/audio.wav
  python3 voiceprint-manager.py list
  python3 voiceprint-manager.py delete --name "Jack"
  python3 voiceprint-manager.py diarize --audio /path/to/audio.wav --segments segments.json
"""

import argparse
import json
import os
import sys
import numpy as np
import onnxruntime as ort
import soundfile as sf
from scipy.spatial.distance import cosine as cosine_distance

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
MODEL_PATH = os.path.join(WORKSPACE, "models/speaker-embedding/speaker_model.onnx")
VOICEPRINT_DIR = os.path.join(WORKSPACE, "memory/voiceprints")
SAMPLE_RATE = 16000
N_FFT = 400
HOP_LENGTH = 160
N_MELS = 80
SIMILARITY_THRESHOLD = 0.55  # cosine similarity threshold for matching

# ---------------------------------------------------------------------------
# Audio Processing (pure numpy, no librosa/torchaudio needed)
# ---------------------------------------------------------------------------

def load_audio(path, target_sr=SAMPLE_RATE):
    """Load audio file and convert to mono 16kHz."""
    data, sr = sf.read(path, dtype='float32')
    if len(data.shape) > 1:
        data = np.mean(data, axis=1)  # stereo -> mono
    if sr != target_sr:
        # Simple resampling via linear interpolation
        duration = len(data) / sr
        new_len = int(duration * target_sr)
        indices = np.linspace(0, len(data) - 1, new_len)
        data = np.interp(indices, np.arange(len(data)), data)
    return data


def mel_filterbank(sr, n_fft, n_mels):
    """Create mel filterbank matrix."""
    fmin, fmax = 0.0, sr / 2.0
    mel_min = 2595.0 * np.log10(1.0 + fmin / 700.0)
    mel_max = 2595.0 * np.log10(1.0 + fmax / 700.0)
    mels = np.linspace(mel_min, mel_max, n_mels + 2)
    freqs = 700.0 * (10.0 ** (mels / 2595.0) - 1.0)
    bins = np.floor((n_fft + 1) * freqs / sr).astype(int)
    
    fb = np.zeros((n_mels, n_fft // 2 + 1))
    for i in range(n_mels):
        lower, center, upper = bins[i], bins[i + 1], bins[i + 2]
        for j in range(lower, center):
            if center > lower:
                fb[i, j] = (j - lower) / (center - lower)
        for j in range(center, upper):
            if upper > center:
                fb[i, j] = (upper - j) / (upper - center)
    return fb


def compute_fbank(audio, sr=SAMPLE_RATE, n_fft=N_FFT, hop_length=HOP_LENGTH, n_mels=N_MELS):
    """Compute log mel-filterbank features."""
    # Pre-emphasis
    audio = np.append(audio[0], audio[1:] - 0.97 * audio[:-1])
    
    # STFT
    n_frames = 1 + (len(audio) - n_fft) // hop_length
    if n_frames <= 0:
        raise ValueError(f"Audio too short: {len(audio)} samples, need at least {n_fft}")
    
    frames = np.lib.stride_tricks.as_strided(
        audio,
        shape=(n_frames, n_fft),
        strides=(audio.strides[0] * hop_length, audio.strides[0])
    ).copy()
    
    # Hamming window
    window = np.hamming(n_fft)
    frames *= window
    
    # FFT
    spectrum = np.abs(np.fft.rfft(frames, n=n_fft))
    power = spectrum ** 2
    
    # Mel filterbank
    fb = mel_filterbank(sr, n_fft, n_mels)
    mel_spec = np.dot(power, fb.T)
    
    # Log
    mel_spec = np.log(np.maximum(mel_spec, 1e-10))
    
    # CMVN (Cepstral Mean and Variance Normalization)
    mel_spec = (mel_spec - np.mean(mel_spec, axis=0)) / (np.std(mel_spec, axis=0) + 1e-10)
    
    return mel_spec.astype(np.float32)


# ---------------------------------------------------------------------------
# Speaker Embedding
# ---------------------------------------------------------------------------

_session = None

def get_session():
    global _session
    if _session is None:
        if not os.path.exists(MODEL_PATH):
            print(f"Error: Model not found at {MODEL_PATH}", file=sys.stderr)
            sys.exit(1)
        _session = ort.InferenceSession(MODEL_PATH, providers=['CPUExecutionProvider'])
    return _session


def extract_embedding(audio_path):
    """Extract 256-dim speaker embedding from audio file."""
    audio = load_audio(audio_path)
    
    # Need at least 0.5s of audio
    if len(audio) < SAMPLE_RATE * 0.5:
        raise ValueError("Audio too short, need at least 0.5 seconds")
    
    fbank = compute_fbank(audio)
    
    # Add batch dimension: [1, T, 80]
    feats = fbank[np.newaxis, :, :]
    
    sess = get_session()
    outputs = sess.run(None, {'feats': feats})
    embedding = outputs[0][0]  # [256]
    
    # L2 normalize
    embedding = embedding / (np.linalg.norm(embedding) + 1e-10)
    
    return embedding


def extract_embedding_from_segment(audio_data, sr=SAMPLE_RATE):
    """Extract embedding from raw audio data (numpy array)."""
    if len(audio_data) < sr * 0.5:
        return None
    
    fbank = compute_fbank(audio_data, sr)
    feats = fbank[np.newaxis, :, :]
    
    sess = get_session()
    outputs = sess.run(None, {'feats': feats})
    embedding = outputs[0][0]
    embedding = embedding / (np.linalg.norm(embedding) + 1e-10)
    
    return embedding


# ---------------------------------------------------------------------------
# Voiceprint Store
# ---------------------------------------------------------------------------

def ensure_dir():
    os.makedirs(VOICEPRINT_DIR, exist_ok=True)


def save_voiceprint(name, embedding):
    ensure_dir()
    path = os.path.join(VOICEPRINT_DIR, f"{name}.json")
    data = {
        "name": name,
        "embedding": embedding.tolist(),
        "dim": len(embedding)
    }
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path


def load_voiceprint(name):
    path = os.path.join(VOICEPRINT_DIR, f"{name}.json")
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return np.array(data['embedding'], dtype=np.float32)


def load_all_voiceprints():
    ensure_dir()
    voiceprints = {}
    for fname in os.listdir(VOICEPRINT_DIR):
        if fname.endswith('.json'):
            name = fname[:-5]
            emb = load_voiceprint(name)
            if emb is not None:
                voiceprints[name] = emb
    return voiceprints


def compute_similarity(emb1, emb2):
    """Cosine similarity between two embeddings (1 = identical, 0 = unrelated)."""
    return 1.0 - cosine_distance(emb1, emb2)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_enroll(args):
    """Register a voiceprint from audio."""
    print(f"Extracting voiceprint for '{args.name}' from {args.audio}...")
    embedding = extract_embedding(args.audio)
    path = save_voiceprint(args.name, embedding)
    print(f"✅ Voiceprint saved: {path}")
    print(f"   Embedding dim: {len(embedding)}")


def cmd_identify(args):
    """Identify speaker from audio against stored voiceprints."""
    voiceprints = load_all_voiceprints()
    if not voiceprints:
        print("No voiceprints registered. Use 'enroll' first.")
        sys.exit(1)
    
    print(f"Extracting embedding from {args.audio}...")
    embedding = extract_embedding(args.audio)
    
    results = []
    for name, stored_emb in voiceprints.items():
        sim = compute_similarity(embedding, stored_emb)
        results.append((name, sim))
    
    results.sort(key=lambda x: x[1], reverse=True)
    
    print("\nSpeaker identification results:")
    for name, sim in results:
        match = "✅ MATCH" if sim >= SIMILARITY_THRESHOLD else "  "
        print(f"  {match} {name}: {sim:.4f}")
    
    best_name, best_sim = results[0]
    if best_sim >= SIMILARITY_THRESHOLD:
        print(f"\n→ Identified as: {best_name} (similarity: {best_sim:.4f})")
    else:
        print(f"\n→ Unknown speaker (best match: {best_name} at {best_sim:.4f})")
    
    if args.json:
        output = {
            "identified": best_name if best_sim >= SIMILARITY_THRESHOLD else None,
            "best_match": best_name,
            "best_similarity": float(best_sim),
            "all_scores": {name: float(sim) for name, sim in results}
        }
        print(json.dumps(output, ensure_ascii=False))


def cmd_list(args):
    """List registered voiceprints."""
    voiceprints = load_all_voiceprints()
    if not voiceprints:
        print("No voiceprints registered.")
        return
    
    print(f"Registered voiceprints ({len(voiceprints)}):")
    for name in sorted(voiceprints.keys()):
        emb = voiceprints[name]
        print(f"  • {name} (dim: {len(emb)})")


def cmd_delete(args):
    """Delete a voiceprint."""
    path = os.path.join(VOICEPRINT_DIR, f"{args.name}.json")
    if os.path.exists(path):
        os.remove(path)
        print(f"✅ Deleted voiceprint: {args.name}")
    else:
        print(f"Voiceprint not found: {args.name}")


def cmd_diarize(args):
    """
    Diarize audio using ASR segments + voiceprint matching.
    Expects --segments with a JSON file containing time-stamped segments.
    """
    voiceprints = load_all_voiceprints()
    
    # Load audio
    audio = load_audio(args.audio)
    
    # Load segments (from Step ASR or similar)
    if args.segments:
        with open(args.segments, 'r', encoding='utf-8') as f:
            segments = json.load(f)
    else:
        # Auto-segment by energy-based VAD
        segments = simple_vad_segments(audio)
    
    results = []
    for seg in segments:
        start_ms = seg.get('start_time', seg.get('start', 0))
        end_ms = seg.get('end_time', seg.get('end', 0))
        text = seg.get('text', '')
        
        # Extract audio segment
        start_sample = int(start_ms / 1000 * SAMPLE_RATE)
        end_sample = int(end_ms / 1000 * SAMPLE_RATE)
        segment_audio = audio[start_sample:end_sample]
        
        speaker = "Unknown"
        confidence = 0.0
        
        if len(segment_audio) >= SAMPLE_RATE * 0.5:  # at least 0.5s
            emb = extract_embedding_from_segment(segment_audio)
            if emb is not None and voiceprints:
                best_name, best_sim = None, -1
                for name, stored_emb in voiceprints.items():
                    sim = compute_similarity(emb, stored_emb)
                    if sim > best_sim:
                        best_name, best_sim = name, sim
                
                if best_sim >= SIMILARITY_THRESHOLD:
                    speaker = best_name
                    confidence = float(best_sim)
        
        results.append({
            "speaker": speaker,
            "confidence": confidence,
            "start_time": start_ms,
            "end_time": end_ms,
            "text": text
        })
    
    output = {"segments": results}
    
    if args.out:
        with open(args.out, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print(f"Saved to: {args.out}", file=sys.stderr)
    
    print(json.dumps(output, ensure_ascii=False, indent=2))


def simple_vad_segments(audio, frame_ms=500, threshold=0.01):
    """Simple energy-based VAD segmentation."""
    frame_len = int(SAMPLE_RATE * frame_ms / 1000)
    segments = []
    in_speech = False
    start = 0
    
    for i in range(0, len(audio) - frame_len, frame_len):
        frame = audio[i:i + frame_len]
        energy = np.sqrt(np.mean(frame ** 2))
        
        if energy > threshold and not in_speech:
            in_speech = True
            start = i
        elif energy <= threshold and in_speech:
            in_speech = False
            segments.append({
                "start_time": int(start / SAMPLE_RATE * 1000),
                "end_time": int(i / SAMPLE_RATE * 1000),
                "text": ""
            })
    
    if in_speech:
        segments.append({
            "start_time": int(start / SAMPLE_RATE * 1000),
            "end_time": int(len(audio) / SAMPLE_RATE * 1000),
            "text": ""
        })
    
    return segments


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Voiceprint Manager")
    sub = parser.add_subparsers(dest='command')
    
    # enroll
    p_enroll = sub.add_parser('enroll', help='Register voiceprint from audio')
    p_enroll.add_argument('--name', required=True, help='Speaker name')
    p_enroll.add_argument('--audio', required=True, help='Audio file path')
    
    # identify
    p_identify = sub.add_parser('identify', help='Identify speaker from audio')
    p_identify.add_argument('--audio', required=True, help='Audio file path')
    p_identify.add_argument('--json', action='store_true', help='Output as JSON')
    
    # list
    sub.add_parser('list', help='List registered voiceprints')
    
    # delete
    p_delete = sub.add_parser('delete', help='Delete voiceprint')
    p_delete.add_argument('--name', required=True, help='Speaker name')
    
    # diarize
    p_diarize = sub.add_parser('diarize', help='Diarize audio with voiceprint matching')
    p_diarize.add_argument('--audio', required=True, help='Audio file path')
    p_diarize.add_argument('--segments', help='ASR segments JSON file')
    p_diarize.add_argument('--out', help='Output file path')
    
    args = parser.parse_args()
    
    if args.command == 'enroll':
        cmd_enroll(args)
    elif args.command == 'identify':
        cmd_identify(args)
    elif args.command == 'list':
        cmd_list(args)
    elif args.command == 'delete':
        cmd_delete(args)
    elif args.command == 'diarize':
        cmd_diarize(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
