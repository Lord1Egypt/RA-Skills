#!/usr/bin/env python3
"""
RunPod Serverless Handler for Qwen3-TTS (All Modes)

Supports:
1. Voice Clone (Base model) - clone voice from reference audio
2. Custom Voice - preset voices with style instructions  
3. Voice Design - generate voice from text description

Auto-detects mode based on parameters, or use explicit "mode" param.
"""

import os
import sys
import base64
import tempfile
import traceback
from typing import Optional, Tuple, Dict, Any

import runpod
import torch
import numpy as np
import soundfile as sf

# Global model cache
_models: Dict[str, Any] = {}

# Config from environment
DEFAULT_MODEL_SIZE = os.environ.get("MODEL_SIZE", "1.7B")
HF_CACHE = os.environ.get("HF_HOME", "/runpod-volume/huggingface")

# Available speakers for CustomVoice
SPEAKERS = ["Vivian", "Serena", "Uncle_Fu", "Dylan", "Eric", "Ryan", "Aiden", "Ono_Anna", "Sohee"]
SPEAKER_ALIASES = {
    "vivian": "Vivian",
    "serena": "Serena",
    "uncle_fu": "Uncle_Fu",
    "uncle-fu": "Uncle_Fu",
    "dylan": "Dylan",
    "eric": "Eric",
    "ryan": "Ryan",
    "aiden": "Aiden",
    "ono_anna": "Ono_Anna",
    "ono-anna": "Ono_Anna",
    "sohee": "Sohee",
}

# Preset styles
STYLES = {
    "neutral": "Speak with warmth and a gentle smile",
    "excited": "Speak with excitement and high energy",
    "calm": "Speak slowly and calmly, relaxed tone",
    "confident": "Speak with authority and confidence",
    "whisper": "Speak softly, like telling a secret",
    "sad": "Speak with sadness in voice",
    "angry": "Speak angrily with sharp emphasis",
    "playful": "Speak in a playful, teasing manner",
    "serious": "Speak in a serious, professional tone",
    "cheerful": "Speak cheerfully with a bright voice",
}


def log(msg: str):
    """Print with flush for RunPod logs."""
    print(msg, flush=True)


def get_device() -> str:
    """Get compute device."""
    if torch.cuda.is_available():
        log(f"🎮 CUDA: {torch.cuda.get_device_name(0)}")
        log(f"📊 VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
        return "cuda"
    log("⚠️ CUDA not available, using CPU")
    return "cpu"


def normalize_model_size(value: Optional[str]) -> str:
    raw = str(value or "").strip().lower()
    if raw in {"0.6b", "0.6", "06", "600m"}:
        return "0.6B"
    if raw in {"1.7b", "1.7", "17", "1700m"}:
        return "1.7B"
    return "1.7B"


def normalize_speaker(value: Optional[str]) -> str:
    if not value:
        return "Ono_Anna"
    cleaned = str(value).strip()
    if cleaned in SPEAKERS:
        return cleaned
    return SPEAKER_ALIASES.get(cleaned.lower(), "Ono_Anna")


def load_model(model_type: str = "base", model_size: Optional[str] = None):
    """
    Load Qwen3-TTS model.
    
    Args:
        model_type: "base" (voice clone), "custom" (preset voices), "design" (voice design)
    """
    global _models
    
    resolved_model_size = normalize_model_size(model_size or DEFAULT_MODEL_SIZE)
    cache_key = f"{resolved_model_size}_{model_type}"
    if cache_key in _models:
        return _models[cache_key]
    
    log(f"📥 Loading Qwen3-TTS {model_type.upper()} {resolved_model_size}...")
    
    from huggingface_hub import snapshot_download
    from qwen_tts import Qwen3TTSModel
    
    # Model repo mapping
    repo_map = {
        "base": f"Qwen/Qwen3-TTS-12Hz-{resolved_model_size}-Base",
        "custom": f"Qwen/Qwen3-TTS-12Hz-{resolved_model_size}-CustomVoice",
        "design": f"Qwen/Qwen3-TTS-12Hz-{resolved_model_size}-VoiceDesign",
    }
    
    repo_id = repo_map.get(model_type, repo_map["base"])
    model_path = snapshot_download(repo_id, cache_dir=HF_CACHE)
    log(f"📂 Model path: {model_path}")
    
    device = get_device()
    dtype = torch.bfloat16 if device == "cuda" else torch.float32
    
    # Try flash attention
    attn_impl = None
    if device == "cuda":
        try:
            import flash_attn
            attn_impl = "flash_attention_2"
            log("⚡ Using Flash Attention 2")
        except ImportError:
            attn_impl = "sdpa"
            log("ℹ️ Using SDPA attention")
    
    model = Qwen3TTSModel.from_pretrained(
        model_path,
        device_map=device,
        dtype=dtype,
        attn_implementation=attn_impl,
    )
    
    _models[cache_key] = model
    log(f"✅ Model loaded: {model_type} {resolved_model_size}")
    return model


def decode_audio(audio_data: str) -> Tuple[np.ndarray, int]:
    """Decode base64 audio to numpy array."""
    # Strip data URL prefix if present
    if audio_data.startswith("data:"):
        audio_data = audio_data.split(",", 1)[1]
    
    audio_bytes = base64.b64decode(audio_data)
    
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        f.write(audio_bytes)
        temp_path = f.name
    
    try:
        audio, sr = sf.read(temp_path)
        if audio.ndim > 1:
            audio = np.mean(audio, axis=1)
        return audio.astype(np.float32), sr
    finally:
        os.unlink(temp_path)


def encode_audio(audio: np.ndarray, sr: int) -> str:
    """Encode numpy audio to base64 data URL."""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        sf.write(f.name, audio, sr)
        temp_path = f.name
    
    try:
        with open(temp_path, "rb") as f:
            audio_bytes = f.read()
        audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
        return f"data:audio/wav;base64,{audio_b64}"
    finally:
        os.unlink(temp_path)


def detect_mode(job_input: dict) -> str:
    """Auto-detect mode from input parameters."""
    # Explicit mode
    if "mode" in job_input:
        return job_input["mode"].lower()
    
    # Voice clone: has ref_audio
    if job_input.get("ref_audio"):
        return "clone"
    
    # Voice design: has voice_description
    if job_input.get("voice_description"):
        return "design"
    
    # Default: custom voice (preset speakers)
    return "custom"


def generate_voice_clone(model, job_input: dict) -> dict:
    """Generate with voice cloning (Base model)."""
    text = job_input["text"]
    ref_audio_b64 = job_input["ref_audio"]
    ref_text = job_input.get("ref_text", "")
    x_vector_only = job_input.get("x_vector_only_mode", False)
    language = job_input.get("language", "Auto")
    
    # Validate
    has_ref_text = ref_text and str(ref_text).strip()
    if not x_vector_only and not has_ref_text:
        return {"error": "ref_text is required when x_vector_only_mode is false"}
    
    # Decode reference audio
    log(f"🎤 Decoding reference audio...")
    ref_audio, ref_sr = decode_audio(ref_audio_b64)
    log(f"📊 Ref: {len(ref_audio)/ref_sr:.1f}s @ {ref_sr}Hz")
    
    # Generate
    log(f"🔊 Voice Clone: '{text[:50]}...'")
    wavs, sr = model.generate_voice_clone(
        text=text,
        language=language,
        ref_audio=(ref_audio, ref_sr),
        ref_text=ref_text if has_ref_text else None,
        x_vector_only_mode=x_vector_only,
        max_new_tokens=job_input.get("max_tokens", 2048),
        temperature=job_input.get("temperature", 0.7),
        top_p=job_input.get("top_p", 0.9),
        top_k=job_input.get("top_k", 50),
        repetition_penalty=job_input.get("repetition_penalty", 1.05),
    )
    
    return {
        "audio": wavs[0],
        "sample_rate": sr,
        "mode": "clone",
        "x_vector_only_mode": x_vector_only,
    }


def generate_custom_voice(model, job_input: dict) -> dict:
    """Generate with preset voice (CustomVoice model)."""
    text = job_input["text"]
    speaker = normalize_speaker(job_input.get("speaker", job_input.get("voice", "Ono_Anna")))
    language = job_input.get("language", "Auto")
    
    # Style handling
    style = job_input.get("style", "neutral")
    instruct = job_input.get("instruct", job_input.get("style_text"))
    if not instruct:
        instruct = STYLES.get(style, STYLES["neutral"])
    
    # Validate speaker
    if speaker not in SPEAKERS:
        log(f"⚠️ Unknown speaker '{speaker}', using Ono_Anna")
        speaker = "Ono_Anna"
    
    log(f"🔊 Custom Voice: '{text[:50]}...' speaker={speaker}")
    wavs, sr = model.generate_custom_voice(
        text=text,
        language=language,
        speaker=speaker.lower(),
        instruct=instruct,
        max_new_tokens=job_input.get("max_tokens", 2048),
        temperature=job_input.get("temperature", 0.7),
        top_p=job_input.get("top_p", 0.9),
        top_k=job_input.get("top_k", 50),
        repetition_penalty=job_input.get("repetition_penalty", 1.05),
    )
    
    return {
        "audio": wavs[0],
        "sample_rate": sr,
        "mode": "custom",
        "speaker": speaker,
        "instruct": instruct,
    }


def generate_voice_design(model, job_input: dict) -> dict:
    """Generate with voice design (VoiceDesign model)."""
    text = job_input["text"]
    voice_description = job_input["voice_description"]
    language = job_input.get("language", "Auto")
    
    log(f"🔊 Voice Design: '{text[:50]}...' desc='{voice_description[:50]}...'")
    wavs, sr = model.generate_voice_design(
        text=text,
        language=language,
        voice_description=voice_description,
        max_new_tokens=job_input.get("max_tokens", 2048),
        temperature=job_input.get("temperature", 0.7),
        top_p=job_input.get("top_p", 0.9),
        top_k=job_input.get("top_k", 50),
        repetition_penalty=job_input.get("repetition_penalty", 1.05),
    )
    
    return {
        "audio": wavs[0],
        "sample_rate": sr,
        "mode": "design",
        "voice_description": voice_description,
    }


def handler(job):
    """
    RunPod handler - supports all Qwen3-TTS modes.
    
    Mode detection (auto or explicit via "mode" param):
    - "clone": Voice cloning (requires ref_audio)
    - "custom": Preset voices (speaker + style)
    - "design": Voice from description (requires voice_description)
    
    Common parameters:
    - text: Text to synthesize (required)
    - language: Auto, Russian, English, Chinese, Japanese, Korean
    - max_tokens, temperature, top_p, top_k, repetition_penalty
    
    Clone mode:
    - ref_audio: Base64 encoded audio
    - ref_text: Transcript of ref_audio (required unless x_vector_only_mode=true)
    - x_vector_only_mode: Use only speaker embedding
    
    Custom mode:
    - speaker/voice: Vivian, Serena, Uncle_Fu, Dylan, Eric, Ryan, Aiden, Ono_Anna, Sohee
    - style: neutral, excited, calm, confident, whisper, sad, angry, playful, serious, cheerful
    - instruct/style_text: Custom instruction (overrides style)
    
    Design mode:
    - voice_description: Text description of desired voice
    """
    job_input = job.get("input", {})
    
    # Required: text
    text = job_input.get("text", "").strip()
    if not text:
        return {"error": "Missing required parameter: text"}
    
    try:
        # Detect mode
        mode = detect_mode(job_input)
        log(f"📋 Mode: {mode}")
        
        # Load appropriate model
        model_size = normalize_model_size(job_input.get("model_size", DEFAULT_MODEL_SIZE))
        model_type_map = {
            "clone": "base",
            "custom": "custom", 
            "design": "design",
        }
        model_type = model_type_map.get(mode, "custom")
        model = load_model(model_type, model_size=model_size)
        
        # Generate based on mode
        if mode == "clone":
            if not job_input.get("ref_audio"):
                return {"error": "ref_audio is required for clone mode"}
            result = generate_voice_clone(model, job_input)
        elif mode == "design":
            if not job_input.get("voice_description"):
                return {"error": "voice_description is required for design mode"}
            result = generate_voice_design(model, job_input)
        else:  # custom
            result = generate_custom_voice(model, job_input)
        
        # Check for errors
        if "error" in result:
            return result
        
        # Encode audio
        audio = result.pop("audio")
        sr = result["sample_rate"]
        duration = len(audio) / sr
        
        log(f"✅ Generated {duration:.2f}s @ {sr}Hz")
        
        result["audio"] = encode_audio(audio, sr)
        result["duration"] = duration
        result["text"] = text
        result["language"] = job_input.get("language", "Auto")
        result["model_size"] = model_size
        
        return result
        
    except Exception as e:
        log(f"❌ Error: {e}")
        traceback.print_exc()
        return {
            "error": str(e),
            "traceback": traceback.format_exc()
        }


# Startup
if __name__ == "__main__":
    log("🚀 Qwen3-TTS RunPod Worker (All Modes)")
    log(f"📦 Default model size: {DEFAULT_MODEL_SIZE}")
    log(f"💾 HF cache: {HF_CACHE}")
    log(f"🎤 Speakers: {', '.join(SPEAKERS)}")
    log(f"🎨 Styles: {', '.join(STYLES.keys())}")
    
    # Pre-load default model (custom voice is most common)
    try:
        load_model("custom", model_size=DEFAULT_MODEL_SIZE)
    except Exception as e:
        log(f"⚠️ Model pre-load skipped: {e}")
    
    runpod.serverless.start({"handler": handler})
