#!/usr/bin/env python3
"""
Local TTS wrapper for Linux/Windows using qwen-tts library.

This script provides a simplified interface for Qwen3-TTS on Linux and Windows
with automatic optimizations: FlashAttention, bfloat16, and auto device selection.

Features:
- FlashAttention for faster inference
- bfloat16 for better precision
- Automatic device selection (CUDA > CPU)
- Automatic mixed precision
"""

import argparse
import sys
import os
import warnings
import torch

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

DEFAULT_FEMALE_VOICE = "Chelsie"
DEFAULT_MALE_VOICE = "Aiden"

MODELS = {
    "base": "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
    "voicedesign": "Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign",
    "customvoice": "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice",
    "base-small": "Qwen/Qwen3-TTS-12Hz-0.6B-Base",
    "voicedesign-small": "Qwen/Qwen3-TTS-12Hz-0.6B-VoiceDesign",
    "customvoice-small": "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice",
}


def get_optimal_device():
    """Automatically select the best available device."""
    if torch.cuda.is_available():
        device = "cuda"
        # Print GPU info
        gpu_name = torch.cuda.get_device_name(0)
        vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        print(f" Using CUDA device: {gpu_name} ({vram_gb:.1f} GB VRAM)")
        return device
    else:
        print(" CUDA not available, using CPU (will be slower)")
        return "cpu"


def get_optimal_dtype(device):
    """Get optimal dtype for the device with bfloat16 support."""
    if device == "cuda":
        # Check if bfloat16 is supported (Ampere architecture and newer)
        capability = torch.cuda.get_device_capability()
        if capability[0] >= 8:  # Ampere (SM 8.0+) supports bfloat16
            print(" Using bfloat16 for optimal precision and speed")
            return torch.bfloat16
        else:
            print(" Using float16 (bfloat16 not supported on this GPU)")
            return torch.float16
    else:
        print(" Using float32 for CPU")
        return torch.float32


def check_flash_attention():
    """Check if FlashAttention is available."""
    try:
        import flash_attn
        print(" FlashAttention available - using for faster inference")
        return True
    except ImportError:
        print(" FlashAttention not installed (optional, for faster inference)")
        print("  Install with: pip install flash-attn --no-build-isolation")
        return False


def run_tts(args):
    """Run TTS with the given arguments and optimizations."""
    
    try:
        from qwen_tts import Qwen3TTSModel, Qwen3TTSTokenizer
        import soundfile as sf
        import numpy as np
    except ImportError as e:
        print(f"Error: Missing dependency - {e}")
        print("\nPlease install qwen-tts:")
        print("  pip install qwen-tts")
        print("\nFor optimal performance, also install:")
        print("  pip install flash-attn --no-build-isolation")
        return 1
    
    # Check optimizations
    has_flash_attn = check_flash_attention()
    
    # Get optimal device and dtype
    device = get_optimal_device()
    dtype = get_optimal_dtype(device)
    
    # Get model ID
    model_id = MODELS.get(args.model, args.model)
    print(f"\nLoading model: {model_id}")
    
    # Load model with optimizations
    try:
        # Enable FlashAttention if available
        model_kwargs = {
            "torch_dtype": dtype,
            "device_map": "auto" if device == "cuda" else None,
        }
        
        # Add FlashAttention config if available
        if has_flash_attn:
            model_kwargs["attn_implementation"] = "flash_attention_2"
        
        model = Qwen3TTSModel.from_pretrained(model_id, **model_kwargs)
        tokenizer = Qwen3TTSTokenizer.from_pretrained(model_id)
        
        if device == "cpu":
            model = model.to(device)
        
        print(f" Model loaded successfully")
        
    except Exception as e:
        print(f"Error loading model: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure you have enough GPU memory (6-8GB for 1.7B models)")
        print("2. Try using smaller models: --model base-small")
        print("3. Check internet connection for model download")
        return 1
    
    # Prepare generation kwargs
    gen_kwargs = {
        "language": args.lang_code,
    }
    
    # Add voice parameters based on model type
    if "voicedesign" in args.model:
        if args.instruct:
            gen_kwargs["instruct"] = args.instruct
        elif args.female:
            gen_kwargs["instruct"] = "A warm female voice, clear and friendly"
        elif args.male:
            gen_kwargs["instruct"] = "A deep male voice, warm and professional"
    else:
        # CustomVoice or Base
        if args.voice:
            gen_kwargs["voice"] = args.voice
        elif args.female:
            gen_kwargs["voice"] = DEFAULT_FEMALE_VOICE
        elif args.male:
            gen_kwargs["voice"] = DEFAULT_MALE_VOICE
    
    # Add optional parameters
    if args.speed is not None:
        gen_kwargs["speed"] = args.speed
    if args.pitch is not None:
        gen_kwargs["pitch"] = args.pitch
    if args.temperature is not None:
        gen_kwargs["temperature"] = args.temperature
    
    # Handle reference audio for cloning
    if args.ref_audio:
        try:
            import librosa
            ref_audio, sr = librosa.load(args.ref_audio, sr=24000)
            gen_kwargs["ref_audio"] = ref_audio
            if args.ref_text:
                gen_kwargs["ref_text"] = args.ref_text
        except ImportError:
            print("Warning: librosa not installed. Install with: pip install librosa")
    
    # Tokenize input
    print(f"Synthesizing: '{args.text[:50]}{'...' if len(args.text) > 50 else ''}'")
    inputs = tokenizer(args.text, return_tensors="pt").to(device)
    
    # Generate audio with mixed precision for speed
    try:
        with torch.no_grad():
            if device == "cuda" and dtype != torch.float32:
                # Use automatic mixed precision for faster inference
                with torch.cuda.amp.autocast(dtype=dtype):
                    audio = model.generate(**inputs, **gen_kwargs)
            else:
                audio = model.generate(**inputs, **gen_kwargs)
        
        # Convert to numpy
        if isinstance(audio, torch.Tensor):
            audio = audio.cpu().numpy()
        
        # Ensure correct shape
        if audio.ndim == 1:
            audio = audio.reshape(-1)
        
        # Save output
        output_path = args.output or "output.wav"
        sf.write(output_path, audio, 24000)
        print(f" Audio saved to: {output_path}")
        
        return 0
        
    except torch.cuda.OutOfMemoryError:
        print("\n CUDA Out of Memory!")
        print("Suggestions:")
        print("1. Use a smaller model: --model customvoice-small")
        print("2. Close other GPU applications")
        print("3. Use CPU instead (slow): --device cpu")
        return 1
        
    except Exception as e:
        print(f"Error generating audio: {e}")
        return 1


def main():
    parser = argparse.ArgumentParser(
        description="Local TTS using Qwen3-TTS with qwen-tts (Linux/Windows). "
                    "Auto-optimizations: FlashAttention, bfloat16, auto-device.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage with optimizations
  python tts_linux.py "Hello world" --female
  
  # Voice design
  python tts_linux.py "Hello world" --model voicedesign --instruct "A warm male voice"
  
  # Voice cloning  
  python tts_linux.py "Cloned voice" --ref_audio sample.wav --ref_text "Sample text"
  
  # Chinese TTS
  python tts_linux.py "" --voice Aiden --lang_code zh-CN
        """
    )
    
    # Required arguments
    parser.add_argument("text", help="Text to synthesize")
    
    # Model selection
    parser.add_argument(
        "--model", "-m",
        default="customvoice",
        choices=list(MODELS.keys()),
        help="Model to use (default: customvoice)"
    )
    
    # Output
    parser.add_argument(
        "--output", "-o",
        default="output.wav",
        help="Output audio file path (default: output.wav)"
    )
    
    # Voice selection (mutually exclusive)
    voice_group = parser.add_mutually_exclusive_group()
    voice_group.add_argument(
        "--voice", "-v",
        help="Preset voice name (for CustomVoice model): Chelsie, Breeze, Ryan, Aiden"
    )
    voice_group.add_argument(
        "--instruct", "-i",
        help="Voice description (for VoiceDesign model), e.g., 'A warm female voice'"
    )
    
    # Quick voice presets
    parser.add_argument(
        "--female", "-f",
        action="store_true",
        help="Use default female voice (Chelsie)"
    )
    parser.add_argument(
        "--male", "-M",
        action="store_true",
        help="Use default male voice (Ryan)"
    )
    
    # Voice cloning
    parser.add_argument(
        "--ref_audio", "-r",
        help="Reference audio file for voice cloning"
    )
    parser.add_argument(
        "--ref_text",
        help="Reference text for voice cloning"
    )
    
    # Voice parameters
    parser.add_argument(
        "--speed", "-s",
        type=float,
        help="Speaking speed (0.5-2.0, default: 1.0)"
    )
    parser.add_argument(
        "--pitch", "-p",
        type=float,
        help="Voice pitch (0.5-2.0, default: 1.0)"
    )
    parser.add_argument(
        "--lang_code", "-l",
        default="en-US",
        help="Language code (default: en-US, use 'zh-CN' for Chinese)"
    )
    parser.add_argument(
        "--temperature", "-t",
        type=float,
        help="Sampling temperature (default: 0.7)"
    )
    
    args = parser.parse_args()
    
    # Run TTS
    return run_tts(args)


if __name__ == "__main__":
    sys.exit(main())
