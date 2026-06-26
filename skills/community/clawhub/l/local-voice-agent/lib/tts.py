#!/usr/bin/env python3
"""
TTS Wrapper - Pocket-TTS Text-to-Speech Interface
Provides Python client for Pocket-TTS server
"""

import os
import sys
import requests
import yaml
import hashlib
import tempfile
from pathlib import Path

# Configuration
CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'config', 'voices.yaml')
CACHE_DIR = None
CACHE_ENABLED = False


def load_config():
    """Load TTS configuration from voices.yaml"""
    global CACHE_DIR, CACHE_ENABLED

    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(f"Configuration file not found: {CONFIG_PATH}")

    with open(CONFIG_PATH, 'r') as f:
        config = yaml.safe_load(f)

    tts_config = config.get('tts', {})
    perf_config = config.get('performance', {})

    return {
        'url': tts_config.get('url', 'http://localhost:5000'),
        'voice': tts_config.get('voice', 'alba'),
        'format': tts_config.get('format', 'wav'),
        'sample_rate': tts_config.get('sample_rate', 24000),
        'cache_enabled': perf_config.get('cache_tts', True),
        'cache_dir': os.path.expanduser(perf_config.get('cache_dir', '~/.cache/voice-agent'))
    }


def _get_cache_key(text, voice):
    """Generate cache key for text+voice combination"""
    hasher = hashlib.sha256()
    hasher.update(text.encode('utf-8'))
    hasher.update(voice.encode('utf-8'))
    return hasher.hexdigest()


def _load_from_cache(cache_key, format='wav'):
    """Load audio from cache"""
    if not CACHE_ENABLED or not CACHE_DIR:
        return None

    cache_file = os.path.join(CACHE_DIR, f"{cache_key}.{format}")

    if os.path.exists(cache_file):
        return cache_file

    return None


def _save_to_cache(cache_key, audio_data, format='wav'):
    """Save audio to cache"""
    if not CACHE_ENABLED or not CACHE_DIR:
        return None

    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_file = os.path.join(CACHE_DIR, f"{cache_key}.{format}")

    with open(cache_file, 'wb') as f:
        f.write(audio_data)

    return cache_file


def generate_speech(text, voice=None, format=None, sample_rate=None, use_cache=None):
    """
    Generate speech from text using Pocket-TTS

    Args:
        text: Text to convert to speech
        voice: Voice ID to use (default from config)
        format: Output format (wav, mp3)
        sample_rate: Audio sample rate in Hz
        use_cache: Override cache setting (True/False)

    Returns:
        bytes: Audio data
    """
    global CACHE_DIR, CACHE_ENABLED

    # Load config
    config = load_config()

    # Use config values if not specified
    voice = voice or config['voice']
    format = format or config['format']
    sample_rate = sample_rate or config['sample_rate']

    # Cache settings
    if use_cache is not None:
        CACHE_ENABLED = use_cache
    else:
        CACHE_ENABLED = config['cache_enabled']

    CACHE_DIR = os.path.expanduser(config['cache_dir'])

    # Check cache first
    if CACHE_ENABLED:
        cache_key = _get_cache_key(text, voice)
        cached_file = _load_from_cache(cache_key, format)
        if cached_file:
            with open(cached_file, 'rb') as f:
                return f.read()

    # Get TTS URL
    tts_url = config['url']
    endpoint = f"{tts_url.rstrip('/')}/v1/tts"

    # Prepare request
    payload = {
        'text': text,
        'voice': voice,
        'format': format,
        'sample_rate': sample_rate
    }

    try:
        response = requests.post(endpoint, json=payload, timeout=30)

        if response.status_code == 404:
            # Try alternative endpoint
            endpoint = f"{tts_url.rstrip('/')}/synthesize"
            response = requests.post(endpoint, json=payload, timeout=30)

        if response.status_code == 200:
            audio_data = response.content

            # Save to cache
            if CACHE_ENABLED and audio_data:
                cache_key = _get_cache_key(text, voice)
                _save_to_cache(cache_key, audio_data, format)

            return audio_data
        else:
            raise RuntimeError(f"TTS request failed: {response.status_code} - {response.text}")

    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            f"Cannot connect to TTS server at {tts_url}\n"
            "Start Pocket-TTS server: python3 -m app.main --host 0.0.0.0 --port 5000"
        )
    except requests.exceptions.Timeout:
        raise RuntimeError("TTS request timed out. Server may be overloaded.")
    except Exception as e:
        raise RuntimeError(f"TTS generation failed: {e}")


def list_voices():
    """
    List available TTS voices from server

    Returns:
        dict: Voice information
    """
    config = load_config()
    tts_url = config['url']
    endpoint = f"{tts_url.rstrip('/')}/v1/voices"

    try:
        response = requests.get(endpoint, timeout=5)

        if response.status_code == 200:
            return response.json()
        else:
            raise RuntimeError(f"Failed to list voices: {response.status_code}")

    except requests.exceptions.ConnectionError:
        raise RuntimeError(f"Cannot connect to TTS server at {tts_url}")
    except Exception as e:
        raise RuntimeError(f"Failed to list voices: {e}")


def save_audio(audio_data, output_path):
    """
    Save audio data to file

    Args:
        audio_data: Audio bytes
        output_path: Output file path
    """
    with open(output_path, 'wb') as f:
        f.write(audio_data)

    print(f"Audio saved to: {output_path}")


def play_audio(audio_path):
    """
    Play audio file using system player

    Args:
        audio_path: Path to audio file
    """
    import platform
    import subprocess

    system = platform.system()

    try:
        if system == 'Windows':
            import winsound
            winsound.PlaySound(audio_path, winsound.SND_FILENAME)
        elif system == 'Darwin':  # macOS
            subprocess.run(['afplay', audio_path], check=True)
        else:  # Linux
            # Try various players
            players = ['paplay', 'aplay', 'ffplay', 'mpv']
            for player in players:
                try:
                    if player == 'ffplay':
                        subprocess.run([player, '-nodisp', '-autoexit', audio_path],
                                     check=True, capture_output=True)
                    elif player == 'mpv':
                        subprocess.run([player, '--no-video', '--quiet', audio_path],
                                     check=True, capture_output=True)
                    else:
                        subprocess.run([player, audio_path], check=True, capture_output=True)
                    break
                except (FileNotFoundError, subprocess.CalledProcessError):
                    continue
            else:
                print(f"Audio saved to {audio_path} (no player found)")

    except Exception as e:
        print(f"Failed to play audio: {e}")
        print(f"Audio saved to {audio_path}")


def speak(text, voice=None, format='wav', play=True):
    """
    Generate and optionally play speech

    Args:
        text: Text to speak
        voice: Voice ID to use
        format: Output format
        play: Whether to play the audio (True) or just return it (False)

    Returns:
        str: Path to audio file if play=False, None if play=True
    """
    try:
        audio_data = generate_speech(text, voice, format)

        # Save to temp file
        with tempfile.NamedTemporaryFile(suffix=f'.{format}', delete=False) as tmp:
            tmp_path = tmp.name
            tmp.write(audio_data)

        if play:
            play_audio(tmp_path)
            os.remove(tmp_path)
            return None
        else:
            return tmp_path

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return None


def main():
    """Command-line interface for testing"""
    if len(sys.argv) < 2:
        print("Usage: python3 tts.py <text> [voice] [output_file]")
        sys.exit(1)

    text = sys.argv[1]
    voice = sys.argv[2] if len(sys.argv) > 2 else None
    output_file = sys.argv[3] if len(sys.argv) > 3 else None

    try:
        if output_file:
            audio_data = generate_speech(text, voice)
            save_audio(audio_data, output_file)
        else:
            speak(text, voice)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
