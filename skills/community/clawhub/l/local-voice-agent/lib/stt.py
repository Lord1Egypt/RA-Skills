#!/usr/bin/env python3
"""
STT Wrapper - Whisper.cpp Speech-to-Text Interface
Provides Python interface to Whisper.cpp for audio transcription
"""

import os
import sys
import subprocess
import tempfile
import hashlib
import yaml
from pathlib import Path

# Configuration
CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'config', 'voices.yaml')
CACHE_DIR = None
CACHE_ENABLED = False


def load_config():
    """Load STT configuration from voices.yaml"""
    global CACHE_DIR, CACHE_ENABLED

    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(f"Configuration file not found: {CONFIG_PATH}")

    with open(CONFIG_PATH, 'r') as f:
        config = yaml.safe_load(f)

    stt_config = config.get('stt', {})
    perf_config = config.get('performance', {})

    return {
        'model': stt_config.get('model', 'tiny'),
        'language': stt_config.get('language', 'en'),
        'whisper_dir': os.path.expanduser(stt_config.get('whisper_dir', '~/.local/whisper.cpp')),
        'threads': stt_config.get('threads', 4),
        'cache_enabled': perf_config.get('cache_stt', False),
        'cache_dir': os.path.expanduser(perf_config.get('cache_dir', '~/.cache/voice-agent'))
    }


def _get_whisper_executable(whisper_dir):
    """Find whisper-cli executable"""
    candidates = [
        os.path.join(whisper_dir, 'build', 'bin', 'whisper-cli'),
        os.path.join(whisper_dir, 'whisper-cli'),
        os.path.join(whisper_dir, 'main'),
    ]

    for path in candidates:
        if os.path.exists(path) and os.access(path, os.X_OK):
            return path

    # Try system path
    if subprocess.run(['which', 'whisper-cli'], capture_output=True).returncode == 0:
        return 'whisper-cli'

    raise FileNotFoundError(
        "Whisper CLI not found. Please install Whisper.cpp:\n"
        "git clone https://github.com/ggerganov/whisper.cpp ~/.local/whisper.cpp\n"
        "cd ~/.local/whisper.cpp && make -j4"
    )


def _convert_to_wav(audio_path):
    """Convert audio file to WAV format using ffmpeg"""
    if audio_path.lower().endswith('.wav'):
        return audio_path

    # Create temp WAV file
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
        wav_path = tmp.name

    try:
        subprocess.run([
            'ffmpeg', '-i', audio_path,
            '-ar', '16000',  # 16kHz sample rate
            '-ac', '1',      # Mono
            '-y',            # Overwrite
            wav_path
        ], check=True, capture_output=True)

        return wav_path
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to convert audio: {e.stderr.decode()}")


def _get_cache_key(audio_path, model):
    """Generate cache key for audio file"""
    hasher = hashlib.sha256()
    hasher.update(os.path.basename(audio_path).encode())
    hasher.update(model.encode())

    stat = os.stat(audio_path)
    hasher.update(str(stat.st_size).encode())
    hasher.update(str(stat.st_mtime).encode())

    return hasher.hexdigest()


def _load_from_cache(cache_key):
    """Load transcription from cache"""
    if not CACHE_ENABLED or not CACHE_DIR:
        return None

    cache_file = os.path.join(CACHE_DIR, f"{cache_key}.txt")

    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            return f.read()

    return None


def _save_to_cache(cache_key, transcription):
    """Save transcription to cache"""
    if not CACHE_ENABLED or not CACHE_DIR:
        return

    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_file = os.path.join(CACHE_DIR, f"{cache_key}.txt")

    with open(cache_file, 'w') as f:
        f.write(transcription)


def transcribe_audio(audio_path, model=None, language=None, use_cache=None):
    """
    Transcribe audio file to text using Whisper.cpp

    Args:
        audio_path: Path to audio file (WAV, OGG, MP3, MP4, etc.)
        model: Whisper model to use (tiny, small, medium, etc.)
        language: Language code (en, ne, hi, etc.)
        use_cache: Override cache setting (True/False)

    Returns:
        str: Transcribed text
    """
    global CACHE_DIR, CACHE_ENABLED

    # Load config
    config = load_config()

    # Use config values if not specified
    model = model or config['model']
    language = language or config['language']
    whisper_dir = config['whisper_dir']
    threads = config['threads']

    # Cache settings
    if use_cache is not None:
        CACHE_ENABLED = use_cache
    else:
        CACHE_ENABLED = config['cache_enabled']

    CACHE_DIR = os.path.expanduser(config['cache_dir'])

    # Check cache first
    if CACHE_ENABLED:
        cache_key = _get_cache_key(audio_path, model)
        cached = _load_from_cache(cache_key)
        if cached:
            return cached

    # Find whisper-cli
    whisper_exec = _get_whisper_executable(whisper_dir)

    # Get model path
    model_path = os.path.join(whisper_dir, 'models', f'ggml-{model}.bin')
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Model not found: {model_path}\n"
            f"Download it with: bash {whisper_dir}/models/download-ggml-model.sh {model}"
        )

    # Convert to WAV if needed
    needs_conversion = not audio_path.lower().endswith('.wav')
    wav_path = _convert_to_wav(audio_path) if needs_conversion else audio_path

    try:
        # Run whisper-cli
        cmd = [
            whisper_exec,
            '-m', model_path,
            '-f', wav_path,
            '-l', language,
            '-t', str(threads),
            '--no-timestamps'  # Clean output without timestamps
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        # Extract transcription (last line after processing info)
        output_lines = result.stdout.strip().split('\n')

        # Whisper.cpp outputs transcription on lines starting without brackets
        transcription_lines = []
        for line in output_lines:
            line = line.strip()
            if line and not line.startswith('[') and not line.startswith('whisper'):
                transcription_lines.append(line)

        transcription = ' '.join(transcription_lines).strip()

        # Save to cache
        if CACHE_ENABLED and transcription:
            cache_key = _get_cache_key(audio_path, model)
            _save_to_cache(cache_key, transcription)

        return transcription

    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else str(e)
        raise RuntimeError(f"Whisper transcription failed: {error_msg}")

    finally:
        # Clean up temp WAV file
        if needs_conversion and os.path.exists(wav_path):
            os.remove(wav_path)


def transcribe_from_microphone(duration=5, output_file=None):
    """
    Record audio from microphone and transcribe it

    Args:
        duration: Recording duration in seconds
        output_file: Optional path to save recording

    Returns:
        str: Transcribed text
    """
    if not output_file:
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            output_file = tmp.name

    try:
        # Record audio using ffmpeg
        print(f"Recording for {duration} seconds... (speak now)")
        subprocess.run([
            'ffmpeg', '-f', 'dshow',
            '-i', 'audio=Microphone',  # Windows microphone
            '-t', str(duration),
            '-y',
            output_file
        ], check=True, capture_output=True)

        print("Transcribing...")
        return transcribe_audio(output_file)

    except subprocess.CalledProcessError as e:
        # Try ALSA for Linux
        try:
            subprocess.run([
                'ffmpeg', '-f', 'alsa',
                '-i', 'default',
                '-t', str(duration),
                '-y',
                output_file
            ], check=True, capture_output=True)

            return transcribe_audio(output_file)
        except:
            raise RuntimeError("Failed to record audio. Please ensure ffmpeg is installed and microphone is available.")


def main():
    """Command-line interface for testing"""
    if len(sys.argv) < 2:
        print("Usage: python3 stt.py <audio_file> [model] [language]")
        sys.exit(1)

    audio_path = sys.argv[1]
    model = sys.argv[2] if len(sys.argv) > 2 else None
    language = sys.argv[3] if len(sys.argv) > 3 else None

    try:
        text = transcribe_audio(audio_path, model, language)
        print(text)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
