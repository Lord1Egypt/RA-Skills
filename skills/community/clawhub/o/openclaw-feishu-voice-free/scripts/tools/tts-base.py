#!/usr/bin/env python3
"""
Qwen3-TTS-12Hz-1.7B-Base: Voice Cloning

Usage:
  tts-base.py [options] --prompt "Text to synthesize" --audio REFERENCE_AUDIO.wav "reference_text"

Options:
  -o, --output PATH        Output file path (default: cloned_output.wav)
  -l, --language LANG      Language (default: Auto) - Auto/Chinese/English/Italian/etc.
  -i, --instruct TEXT      Additional instruction (e.g., "speak slowly")
  --remote URL             Use remote server (e.g., http://192.168.188.177:8765)
  --model NAME             Model name (default: Qwen/Qwen3-TTS-12Hz-1.7B-Base)
  --audio PATH             Path to reference audio file for cloning (required for local mode)
  --text TEXT              Reference transcription of the reference audio (required)
  --help                   Show this help message

Environment:
  QWEN_TTS_REMOTE          Default remote server URL

Examples:
  # Local clone
  tts-base.py --audio ./my_voice.wav --text "这是一段参考音频的文字内容" --output cloned.wav "今天天气真好"

  # Remote clone
  tts-base.py --audio ./my_voice.wav --text "参考文字" "你好世界" --remote http://192.168.188.177:8765
"""
import time
import argparse
import sys
import os
from pathlib import Path
from qwen_tts import VoiceClonePromptItem

# Find venv Python and re-exec if needed
SCRIPT_DIR = Path(__file__).parent  # scripts/tools
SKILL_DIR = SCRIPT_DIR.parent.parent  # skill root directory
VENV_PYTHON = SKILL_DIR / "venv" / "bin" / "python"

# Always use venv if available and not already active
if not os.environ.get("QWEN_TTS_VENV_ACTIVE") and VENV_PYTHON.exists():
    os.environ["QWEN_TTS_VENV_ACTIVE"] = "1"
    os.execv(str(VENV_PYTHON), [str(VENV_PYTHON)] + sys.argv)

# Check for remote mode
REMOTE_URL = os.environ.get("QWEN_TTS_REMOTE")

# Import dependencies based on mode
if REMOTE_URL or ("--remote" in sys.argv):
    # Remote mode: only need requests
    try:
        import requests
    except ImportError:
        print("❌ Error: requests module required for remote mode", file=sys.stderr)
        print("   Run: venv/bin/pip install requests", file=sys.stderr)
        sys.exit(1)
else:
    # Local mode: need full TTS stack
    if not VENV_PYTHON.parent.parent.exists():
        print("❌ Error: Virtual environment not found!", file=sys.stderr)
        print(f"   Expected at: {VENV_PYTHON.parent.parent}", file=sys.stderr)
        print("", file=sys.stderr)
        print("Run setup first:", file=sys.stderr)
        print(f"   cd {SKILL_DIR}", file=sys.stderr)
        print("   bash setup.sh", file=sys.stderr)
        sys.exit(1)

    try:
        import torch
        import soundfile as sf
        from qwen_tts import Qwen3TTSModel
    except ImportError as e:
        print(f"❌ Error: Missing dependency: {e}", file=sys.stderr)
        print("", file=sys.stderr)
        print("Run setup to install dependencies:", file=sys.stderr)
        print("   bash scripts/setup.sh", file=sys.stderr)
        sys.exit(1)


def clone_remote(remote_url, prompt_text, reference_audio_path, reference_text, language, instruct, model, output_path, mp3):
    """Voice cloning using remote server."""
    print(f"🌐 Using remote server: {remote_url}", file=sys.stderr)
    print(f"🎙️  Reference audio: {reference_audio_path}", file=sys.stderr)
    print(f"📝 Reference text: {reference_text[:60]}{'...' if len(reference_text) > 60 else ''}", file=sys.stderr)
    print(f"🔊 Generate text: {prompt_text[:60]}{'...' if len(prompt_text) > 60 else ''}", file=sys.stderr)

    # Read and encode reference audio
    try:
        import base64
        with open(reference_audio_path, 'rb') as f:
            audio_b64 = base64.b64encode(f.read()).decode('utf-8')
    except Exception as e:
        print(f"❌ Error reading reference audio: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        response = requests.post(
            f"{remote_url}/clone",
            json={
                "text": prompt_text,
                "reference_audio": audio_b64,
                "reference_text": reference_text,
                "language": language,
                "instruct": instruct,
                "model": model
            },
            timeout=300
        )

        if response.status_code != 200:
            print(f"❌ Server error: {response.status_code}", file=sys.stderr)
            print(response.text, file=sys.stderr)
            sys.exit(1)

        # Save output audio
        output_path = Path(output_path).expanduser().resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'wb') as f:
            f.write(response.content)

        # Convert to MP3 if requested
        if mp3:
            mp3_path = output_path.with_suffix('.mp3')
            print(f"🔄 Converting to MP3: {mp3_path}", file=sys.stderr)
            import subprocess
            try:
                subprocess.run([
                    'ffmpeg', '-y',
                    '-i', str(output_path),
                    '-codec:a', 'libmp3lame',
                    '-V', '2',
                    str(mp3_path)
                ], check=True, capture_output=True)
                # Remove original wav
                output_path.unlink()
                output_path = mp3_path
                print(f"✅ MP3 saved: {output_path}", file=sys.stderr)
            except subprocess.CalledProcessError as e:
                print(f"⚠️  MP3 conversion failed (need ffmpeg installed)", file=sys.stderr)
                print(f"    Keeping WAV: {output_path}", file=sys.stderr)

        print(f"✅ Cloned audio saved: {output_path}", file=sys.stderr)
        print(str(output_path))

    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}", file=sys.stderr)
        print(f"   Is server running at {remote_url}?", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Qwen3-TTS-12Hz-1.7B-Base: Voice Cloning",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument("-p", "--prompt", help="Text to synthesize after cloning (required unless only --save-clone)")
    parser.add_argument("--audio", help="Path to reference audio file for cloning (required if not using --clone)")
    parser.add_argument("--text", help="Transcription text of the reference audio (required if not using --clone)")
    parser.add_argument("-o", "--output", default="cloned_output.wav",
                       help="Output audio file path")
    parser.add_argument("--mp3", action="store_true",
                       help="Convert output to MP3 format (requires ffmpeg)")
    parser.add_argument("-l", "--language",
                       default=os.environ.get("QWEN_TTS_LANGUAGE", "Auto"),
                       help="Language (default: Auto)")
    parser.add_argument("-i", "--instruct", default="",
                       help="Additional instruction (e.g., 'speak slowly')")
    parser.add_argument("--remote",
                       default=os.environ.get("QWEN_TTS_REMOTE"),
                       help="Remote server URL (e.g., http://192.168.188.177:8765)")
    parser.add_argument("--model", default="/root/.openclaw/models/Qwen3-TTS/Qwen3-TTS-12Hz-1.7B-Base",
                       help="Model name or local path to model (should be Qwen3-TTS-12Hz-1.7B-Base for cloning)")
    parser.add_argument("--save-clone", 
                       help="Save cloned voice embedding to this file (.pt format, relative paths save to voice_embedings/)")
    parser.add_argument("--clone",
                       help="Load cloned voice embedding from this .pt file (supports relative paths from voice_embedings/ directory)")

    args = parser.parse_args()

    # Require prompt text, unless just saving clone (or using remote mode which handles differently)
    if not args.prompt and not args.save_clone and not args.remote:
        parser.error("--prompt is required (prompt text to generate, not required when using --save-clone only)")

    # Handle loading from existing clone
    clone_path_resolved = None
    ref_audio_path = None
    
    if args.clone:
        # Load pre-saved embedding
        clone_path = Path(args.clone)
        # Support relative paths from skill directory or voice_embedings directory
        if not clone_path.is_absolute():
            # Try relative to skill directory first
            possible_paths = [
                SKILL_DIR / clone_path,
                SKILL_DIR / "voice_embedings" / clone_path,
                SKILL_DIR / "voice_embedings" / clone_path.name,
            ]
            for p in possible_paths:
                if p.exists():
                    clone_path_resolved = p
                    break
            if clone_path_resolved is None:
                clone_path_resolved = clone_path
        else:
            clone_path_resolved = clone_path
        
        if not clone_path_resolved.exists():
            print(f"❌ Error: Cloned embedding not found: {args.clone}", file=sys.stderr)
            if not Path(args.clone).is_absolute():
                # Reconstruct possible_paths for error message
                possible_paths = [
                    SKILL_DIR / clone_path,
                    SKILL_DIR / "voice_embedings" / clone_path,
                    SKILL_DIR / "voice_embedings" / clone_path.name,
                ]
                print(f"   Tried paths: {[str(p) for p in possible_paths]}", file=sys.stderr)
            sys.exit(1)
        # Only load on CPU here, will reload on correct device later if needed
        voice_embedding = torch.load(clone_path_resolved, map_location='cpu')
        print(f"✓ Loaded cloned voice embedding from: {clone_path_resolved}", file=sys.stderr)
    else:
        # Check required arguments when not using --clone
        if not args.audio or not args.text:
            parser.error("--audio and --text are required when not using --clone")
        # Check reference audio exists for new clone
        ref_audio = Path(args.audio)
        if not ref_audio.exists():
            print(f"❌ Error: Reference audio not found: {args.audio}", file=sys.stderr)
            sys.exit(1)
        # Convert compressed audio (mp3/m4a) to wav if needed
        ref_audio_path = args.audio
        if ref_audio.suffix.lower() in ['.mp3', '.m4a']:
            print(f"🔄 Converting input MP3/M4A to WAV...", file=sys.stderr)
            import subprocess
            temp_wav = ref_audio.with_suffix('.tmp.wav')
            try:
                subprocess.run([
                    'ffmpeg', '-y',
                    '-i', str(ref_audio),
                    '-ac', '1',
                    '-ar', '16000',
                    str(temp_wav)
                ], check=True, capture_output=True)
                ref_audio_path = str(temp_wav)
                print(f"✓ Converted: {ref_audio_path}", file=sys.stderr)
            except subprocess.CalledProcessError as e:
                print(f"❌ MP3/M4A conversion failed (need ffmpeg installed)", file=sys.stderr)
                sys.exit(1)

    # Remote mode
    if args.remote:
        # Remote mode doesn't support --clone, need reference audio
        if args.clone:
            parser.error("Remote mode requires --audio and --text, not --clone")
        # For remote mode, ref_audio_path should be defined if we got here
        if ref_audio_path is None:
            parser.error("--audio and --text are required for remote mode")
        clone_remote(
            remote_url=args.remote,
            prompt_text=args.prompt if args.prompt else "",
            reference_audio_path=ref_audio_path,
            reference_text=args.text,
            language=args.language,
            instruct=args.instruct,
            model=args.model,
            output_path=args.output,
            mp3=args.mp3
        )
        # Clean up temp file
        if ref_audio_path and ref_audio_path.endswith('.tmp.wav'):
            temp_wav_path = Path(ref_audio_path)
            if temp_wav_path.exists():
                temp_wav_path.unlink()
        return

    # Local mode - Load model
    print(f"🔄 Loading {args.model}...", file=sys.stderr)
    print(f"   (First run downloads ~4GB)", file=sys.stderr)

    try:
        # Determine device and dtype
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        dtype = torch.bfloat16 if device != "cpu" else torch.float32

        # Try Flash attention if available (CUDA only)
        attn_impl = "flash_attention_2"
        try:
            import flash_attn
        except ImportError:
            print(f"⚠️  flash_attn not installed, falling back to eager attention", file=sys.stderr)
            attn_impl = "eager"

        if device == "cpu":
            attn_impl = "eager"

        model = Qwen3TTSModel.from_pretrained(
            args.model,
            device_map=device,
            dtype=dtype,
            attn_implementation=attn_impl,
        )
        print(f"✓ Model loaded on {device} with {attn_impl}", file=sys.stderr)
    except Exception as e:
        print(f"❌ Error loading model: {e}", file=sys.stderr)
        sys.exit(1)

    # Clone voice and generate speech
    if args.clone:
        print(f"🎙️  Generating speech from cloned voice embedding...", file=sys.stderr)
        print(f"   Cloned embedding: {clone_path_resolved if clone_path_resolved else args.clone}", file=sys.stderr)
    else:
        print(f"🎙️  Cloning voice and generating speech...", file=sys.stderr)
        print(f"   Reference audio: {args.audio}", file=sys.stderr)
        print(f"   Reference text: {args.text[:60]}{'...' if len(args.text) > 60 else ''}", file=sys.stderr)
    if args.prompt:
        print(f"   Generate text: {args.prompt[:60]}{'...' if len(args.prompt) > 60 else ''}", file=sys.stderr)
    if args.instruct:
        print(f"   Instruction: {args.instruct}", file=sys.stderr)

    try:
        if not args.clone:
            # Extract and save cloned voice embedding if requested
            if args.save_clone:
                print(f"💾 Extracting cloned voice embedding...", file=sys.stderr)
                # Use x-vector only mode for compatibility
                prompt_items = model.create_voice_clone_prompt(
                    ref_audio=ref_audio_path,
                    ref_text=args.text,
                    x_vector_only_mode=False
                )
                # Extract the embedding and save it (always returns list)
                prompt_item = prompt_items[0] if isinstance(prompt_items, list) else prompt_items

                ref_dict = {"ref_code": prompt_item.ref_code,
                            "ref_spk_embedding": prompt_item.ref_spk_embedding,
                            "ref_text": prompt_item.ref_text}

                save_path = Path(args.save_clone).expanduser()
                # If relative path, save to voice_embedings directory
                if not save_path.is_absolute():
                    voice_embedings_dir = SKILL_DIR / "voice_embedings"
                    voice_embedings_dir.mkdir(parents=True, exist_ok=True)
                    save_path = voice_embedings_dir / save_path.name
                else:
                    save_path = save_path.resolve()
                    save_path.parent.mkdir(parents=True, exist_ok=True)
                torch.save(ref_dict, save_path)
                print(f"✅ Cloned voice ref_dict saved to: {save_path}", file=sys.stderr)

        # Only generate audio if prompt is provided
        if args.prompt:
            if args.clone:
                # Use the resolved clone_path from earlier (already loaded, but need to load on correct device)
                if clone_path_resolved:
                    ref_dict = torch.load(clone_path_resolved, map_location=device)
                else:
                    # Fallback (should not happen if earlier check passed)
                    ref_dict = torch.load(Path(args.clone), map_location=device)

                start = time.time()
                # Use pre-loaded cloned embedding (x-vector only mode, stable)
                # Auto-detect: new dict format or old tensor-only format
                prompt_item = VoiceClonePromptItem(
                    ref_spk_embedding=ref_dict["ref_spk_embedding"],
                    ref_text=ref_dict["ref_text"],
                    ref_code=ref_dict["ref_code"],
                    x_vector_only_mode=False,
                    icl_mode=True
                )
                wavs, sr = model.generate_voice_clone(
                    text=args.prompt,
                    voice_clone_prompt=[prompt_item],
                    language=args.language,
                    instruct=args.instruct if args.instruct else None,
                    # icl_mode=False
                )
                end = time.time()
                print('time used: ', end - start)
            else:
                # Clone from reference audio
                wavs, sr = model.generate_voice_clone(
                    text=args.prompt,
                    ref_audio=ref_audio_path,
                    ref_text=args.text,
                    language=args.language,
                    instruct=args.instruct if args.instruct else None,
                )

            # Save output
            output_path = Path(args.output).expanduser().resolve()
            output_path.parent.mkdir(parents=True, exist_ok=True)

            sf.write(str(output_path), wavs[0], sr)

            print(f"✅ Cloned audio saved: {output_path}", file=sys.stderr)

        # Clean up temp file if we converted from MP3/M4A
        if ref_audio_path and ref_audio_path.endswith('.tmp.wav'):
            temp_wav_path = Path(ref_audio_path)
            if temp_wav_path.exists():
                temp_wav_path.unlink()

    except Exception as e:
        # Clean up temp file on error
        if ref_audio_path and ref_audio_path.endswith('.tmp.wav'):
            temp_wav_path = Path(ref_audio_path)
            if temp_wav_path.exists():
                temp_wav_path.unlink()
        print(f"❌ Error during cloning/generation: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
