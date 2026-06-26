#!/usr/bin/env python3
"""
Send Feishu native voice bubble message.

Usage:
  python3 send_feishu_voice.py <text> <user_id> [openclaw_config_path]

Flow:
  1. Generate speech via MiniMax TTS API (hex audio)
  2. Decode hex → MP3 data
  3. Decode MP3 → raw PCM using ffmpeg (16kHz, mono)
  4. Convert PCM → opus audio in OGG container
  5. Upload to Feishu → get file_key (with duration)
  6. Send audio message via Feishu API
"""

import sys
import json
import subprocess
import tempfile
import os
import wave
import argparse
import math

def get_minimax_token(voice_config_path: str) -> str:
    """Extract MiniMax API key from voice_config.json."""
    with open(os.path.expanduser(voice_config_path), 'r') as f:
        voice_config = json.load(f)
    api_key = voice_config.get('api_key')
    if not api_key:
        raise ValueError(f"No 'api_key' found in {voice_config_path}")
    return api_key

def get_feishu_creds(openclaw_config_path: str) -> dict:
    """Extract Feishu app credentials from openclaw config."""
    with open(openclaw_config_path, 'r') as f:
        config = json.load(f)
    
    feishu = config.get('channels', {}).get('feishu', {})
    return {
        'app_id': feishu.get('appId'),
        'app_secret': feishu.get('appSecret')
    }

def get_tenant_token(app_id: str, app_secret: str) -> str:
    """Get Feishu tenant access token."""
    import urllib.request
    
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    data = json.dumps({
        "app_id": app_id,
        "app_secret": app_secret
    }).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=10) as resp:
        result = json.loads(resp.read())
    
    if result.get('code') != 0:
        raise ValueError(f"Failed to get token: {result}")
    
    return result['tenant_access_token']

def get_voice_config(voice_config_path: str) -> dict:
    """Load voice settings from JSON config file."""
    voice_config_path = os.path.expanduser(voice_config_path)
    if os.path.exists(voice_config_path):
        with open(voice_config_path, 'r') as f:
            return json.load(f)
    # Default values if config file doesn't exist
    return {"voice_id": "female-tianmei", "speed": 1.0, "vol": 1.0, "pitch": 0}

def generate_tts(text: str, api_key: str, voice_config: dict, base_url: str = "https://api.minimaxi.com") -> bytes:
    """Generate TTS audio via MiniMax API, return MP3 data."""
    import urllib.request
    
    url = f"{base_url}/v1/t2a_v2"
    data = json.dumps({
        "model": "speech-2.8-hd",
        "text": text,
        "voice_setting": {
            "voice_id": voice_config.get("voice_id", "female-tianmei"),
            "speed": voice_config.get("speed", 1.0),
            "vol": voice_config.get("vol", 1.0),
            "pitch": voice_config.get("pitch", 0)
        },
        "audio_setting": {
            "format": "mp3",
            "sample_rate": 32000
        }
    }).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    })
    
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read())
    
    if result.get('base_resp', {}).get('status_code') != 0:
        raise ValueError(f"TTS API error: {result}")
    
    hex_audio = result['data']['audio']
    return bytes.fromhex(hex_audio)

def convert_mp3_to_opus(mp3_data: bytes) -> tuple[bytes, int]:
    """Convert MP3 data to opus format. Returns (opus_data, duration_ms)."""
    import urllib.request
    
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as mp3_file:
        mp3_file.write(mp3_data)
        mp3_path = mp3_file.name
    
    pcm_path = mp3_path + '_pcm.wav'
    opus_path = mp3_path + '.opus'
    
    try:
        # Step 1: Decode MP3 to WAV (PCM) at 16kHz (Feishu requirement)
        cmd_decode = [
            'ffmpeg', '-y', '-i', mp3_path,
            '-f', 'wav',
            '-acodec', 'pcm_s16le',
            '-ar', '16000',       # Feishu requires 16kHz
            '-ac', '1',           # mono
            '-v', 'error',
            pcm_path
        ]
        result = subprocess.run(cmd_decode, capture_output=True, timeout=30)
        if result.returncode != 0:
            raise ValueError(f"MP3 decode failed: {result.stderr.decode()}")
        
        # Calculate duration in ms from the WAV file
        with wave.open(pcm_path, 'rb') as wav:
            frames = wav.getnframes()
            rate = wav.getframerate()
            duration_ms = int(frames / rate * 1000)
        
        # Step 2: Encode PCM WAV to OGG/opus container at 16kHz
        cmd_encode = [
            'ffmpeg', '-y', '-i', pcm_path,
            '-ar', '16000',
            '-ac', '1',
            '-c:a', 'libopus',
            '-b:a', '20k',
            '-v', 'error',
            '-f', 'ogg',
            opus_path
        ]
        result = subprocess.run(cmd_encode, capture_output=True, timeout=30)
        if result.returncode != 0:
            raise ValueError(f"OGG encode failed: {result.stderr.decode()}")
        
        with open(opus_path, 'rb') as f:
            opus_data = f.read()
        
        return opus_data, duration_ms
    finally:
        for p in [mp3_path, pcm_path, opus_path]:
            if os.path.exists(p):
                os.unlink(p)

def upload_feishu_audio(opus_data: bytes, duration_ms: int, token: str) -> str:
    """Upload audio to Feishu and return file_id."""
    import urllib.request
    
    boundary = '----FeishuBoundary7jSkF0dHsF3R'
    
    with tempfile.NamedTemporaryFile(suffix='.opus', delete=False) as f:
        f.write(opus_data)
        file_path = f.name
    
    try:
        with open(file_path, 'rb') as audio_file:
            audio_content = audio_file.read()
        
        # Build multipart form data with duration
        body_parts = [
            f'--{boundary}\r\n'.encode('utf-8'),
            f'Content-Disposition: form-data; name="file_type"\r\n\r\n'.encode('utf-8'),
            b'opus',
            f'\r\n--{boundary}\r\n'.encode('utf-8'),
            f'Content-Disposition: form-data; name="file_name"\r\n\r\n'.encode('utf-8'),
            b'voice.ogg',
            f'\r\n--{boundary}\r\n'.encode('utf-8'),
            f'Content-Disposition: form-data; name="duration"\r\n\r\n'.encode('utf-8'),
            str(duration_ms).encode('utf-8'),
            f'\r\n--{boundary}\r\n'.encode('utf-8'),
            f'Content-Disposition: form-data; name="file"; filename="voice.ogg"\r\n'.encode('utf-8'),
            b'Content-Type: audio/ogg\r\n\r\n',
            audio_content,
            f'\r\n--{boundary}--\r\n'.encode('utf-8')
        ]
        body = b''.join(body_parts)
        
        url = "https://open.feishu.cn/open-apis/im/v1/files"
        req = urllib.request.Request(url, data=body, method='POST', headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': f'multipart/form-data; boundary={boundary}'
        })
        
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read())
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            raise ValueError(f"Upload HTTP {e.code}: {error_body}")
        
        if result.get('code') != 0:
            raise ValueError(f"Upload failed: {result}")
        
        return result['data']['file_key']
    finally:
        os.unlink(file_path)

def send_feishu_audio_message(file_key: str, user_id: str, token: str) -> str:
    """Send audio message to user via Feishu API."""
    import urllib.request
    
    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
    data = json.dumps({
        "receive_id": user_id,
        "msg_type": "audio",
        "content": json.dumps({"file_key": file_key})
    }).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    })
    
    with urllib.request.urlopen(req, timeout=10) as resp:
        result = json.loads(resp.read())
    
    if result.get('code') != 0:
        raise ValueError(f"Send failed: {result}")
    
    return result['data']['message_id']

def main():
    parser = argparse.ArgumentParser(description='Send Feishu native voice bubble')
    parser.add_argument('text', help='Text to convert to voice')
    parser.add_argument('user_id', help='Feishu open_id of recipient')
    parser.add_argument('--config', default='~/.openclaw/openclaw.json', help='OpenClaw config path')
    parser.add_argument('--voice-config', default='~/.openclaw/workspace/skills/minimax-feishu-voice/voice_config.json', help='Voice config JSON path')
    args = parser.parse_args()
    
    config_path = os.path.expanduser(args.config)
    voice_config_path = os.path.expanduser(args.voice_config)
    
    minimax_key = get_minimax_token(voice_config_path)
    feishu_creds = get_feishu_creds(config_path)
    token = get_tenant_token(feishu_creds['app_id'], feishu_creds['app_secret'])
    voice_config = get_voice_config(voice_config_path)
    
    print(f"Generating TTS for: {args.text[:50]}...", file=sys.stderr)
    print(f"Using voice: {voice_config.get('voice_id')} (config: {voice_config_path})", file=sys.stderr)
    mp3_data = generate_tts(args.text, minimax_key, voice_config)
    print(f"Generated {len(mp3_data)} bytes of MP3", file=sys.stderr)
    
    print("Converting to opus (16kHz, Feishu-native)...", file=sys.stderr)
    opus_data, duration_ms = convert_mp3_to_opus(mp3_data)
    print(f"Converted to {len(opus_data)} bytes opus, duration={duration_ms}ms", file=sys.stderr)
    
    print("Uploading to Feishu...", file=sys.stderr)
    file_key = upload_feishu_audio(opus_data, duration_ms, token)
    print(f"Uploaded with file_key: {file_key}", file=sys.stderr)
    
    print("Sending audio message...", file=sys.stderr)
    msg_id = send_feishu_audio_message(file_key, args.user_id, token)
    print(f"Sent! message_id: {msg_id}", file=sys.stderr)
    
    print(msg_id)

if __name__ == '__main__':
    main()
