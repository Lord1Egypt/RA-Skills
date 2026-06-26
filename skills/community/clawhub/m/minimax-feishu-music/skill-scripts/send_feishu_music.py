#!/usr/bin/env python3
"""
Send Feishu music/audio attachment via MiniMax music-2.6 API.

Usage:
  python3 send_feishu_music.py --prompt <style> --lyrics <lyrics> --title <title> <user_id>

Example (full song structure):
  python3 send_feishu_music.py \
    --prompt "轻柔抒情流行，温柔女声，慢节奏" \
    --lyrics "[Intro]\n(Ooh-ooh)\n(Yeah)\n[Verse 1]\n黄昏的咖啡店门口\n风铃轻轻摇晃\n你从远处走来\n[Pre Chorus]\n心跳突然加速\n想说的话在嘴边\n[Chorus]\n风吹过街角\n带走了沉默\n你是我最想留住的温度\n[Outro]\n(Ooh-ooh-ooh)\n(Yeah)" \
    --title "song.mp3" \
    "<open_id>"
"""

import sys
import json
import base64
import argparse
import os
import tempfile

# Global temp file tracking
_temp_files = []

def cleanup_temp_files():
    """Remove all temp files created during execution."""
    for f in _temp_files:
        if os.path.exists(f):
            os.unlink(f)

def get_minimax_key(music_config_path: str) -> str:
    """Extract MiniMax API key from music_config.json."""
    with open(os.path.expanduser(music_config_path), 'r') as f:
        config = json.load(f)
    api_key = config.get('api_key')
    if not api_key:
        raise ValueError(f"No 'api_key' found in {music_config_path}")
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

def generate_music(prompt: str, lyrics: str, api_key: str, cover_audio_base64: str = None) -> tuple[bytes, int]:
    """Generate music via MiniMax API. Returns (mp3_data, duration_ms).
    
    If cover_audio_base64 is provided, uses music-cover model with the reference audio.
    """
    import urllib.request

    url = "https://api.minimaxi.com/v1/music_generation"
    
    if cover_audio_base64:
        # Cover mode: preserve melody/structure, swap lyrics
        payload = {
            "model": "music-cover",
            "prompt": prompt,
            "lyrics": lyrics,
            "audio_base64": cover_audio_base64,
            "audio_setting": {
                "sample_rate": 44100,
                "bitrate": 256000,
                "format": "mp3"
            }
        }
    else:
        # Normal generation
        payload = {
            "model": "music-2.6",
            "prompt": prompt,
            "lyrics": lyrics,
            "audio_setting": {
                "sample_rate": 44100,
                "bitrate": 256000,
                "format": "mp3"
            }
        }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        },
        method='POST'
    )

    print(f"Calling MiniMax music API...", file=sys.stderr)
    with urllib.request.urlopen(req, timeout=300) as resp:
        result = json.loads(resp.read())

    if result.get('base_resp', {}).get('status_code') != 0:
        raise ValueError(f"Music API error: {result}")

    # Audio is hex-encoded MP3 data (starts with 49443304 = MP3 magic)
    audio_hex = result['data']['audio']
    mp3_data = bytes.fromhex(audio_hex)
    duration_ms = result['extra_info']['music_duration']

    return mp3_data, duration_ms

def save_to_workspace(file_data: bytes, file_name: str) -> str:
    """Save music file to workspace directory for OpenClaw to send."""
    workspace_dir = os.path.expanduser('~/.openclaw/workspace/songs')
    os.makedirs(workspace_dir, exist_ok=True)
    file_path = os.path.join(workspace_dir, file_name)
    with open(file_path, 'wb') as f:
        f.write(file_data)
    return file_path

def send_feishu_file_message(file_key: str, file_name: str, user_id: str, token: str) -> str:
    """Send file attachment message to user via Feishu API."""
    import urllib.request

    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
    data = json.dumps({
        "receive_id": user_id,
        "msg_type": "file",
        "content": json.dumps({
            "file_key": file_key,
            "file_name": file_name
        })
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
    parser = argparse.ArgumentParser(description='Generate music via MiniMax and send to Feishu')
    parser.add_argument('user_id', help='Feishu open_id of recipient')
    parser.add_argument('--prompt', required=True, help='Music style prompt (English)')
    parser.add_argument('--lyrics', required=True, help='Song lyrics')
    parser.add_argument('--title', default='song.mp3', help='File name for the music file')
    parser.add_argument('--cover', help='Path to reference audio file for music-cover mode (preserves melody, swaps lyrics)')
    parser.add_argument('--config', default='~/.openclaw/openclaw.json', help='OpenClaw config path')
    parser.add_argument('--music-config', default='~/.openclaw/workspace/skills/minimax-feishu-music/music_config.json', help='Music config JSON path')
    args = parser.parse_args()

    try:
        config_path = os.path.expanduser(args.config)
        music_config_path = os.path.expanduser(args.music_config)

        minimax_key = get_minimax_key(music_config_path)
        feishu_creds = get_feishu_creds(config_path)
        token = get_tenant_token(feishu_creds['app_id'], feishu_creds['app_secret'])

        cover_audio_b64 = None
        if args.cover:
            with open(os.path.expanduser(args.cover), 'rb') as f:
                cover_audio_b64 = base64.b64encode(f.read()).decode('utf-8')
            print(f"Using cover mode with reference audio: {args.cover}", file=sys.stderr)

        print(f"Generating music with prompt: {args.prompt[:50]}...", file=sys.stderr)
        mp3_data, duration_ms = generate_music(args.prompt, args.lyrics, minimax_key, cover_audio_b64)
        print(f"Generated {len(mp3_data)} bytes, duration={duration_ms}ms", file=sys.stderr)

        print("Saving to workspace...", file=sys.stderr)
        file_path = save_to_workspace(mp3_data, args.title)
        print(f"Saved to: {file_path}", file=sys.stderr)

        print("Sending via openclaw...", file=sys.stderr)
        import subprocess
        result = subprocess.run(
            ['openclaw', 'message', 'send', '--channel', 'feishu', '--target', args.user_id, '--media', file_path],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"openclaw stderr: {result.stderr}", file=sys.stderr)
            raise ValueError(f"openclaw send failed: {result.stderr}")

        print(f"Sent! {args.title} to {args.user_id}", file=sys.stderr)
        print(file_path)
    finally:
        cleanup_temp_files()

if __name__ == '__main__':
    main()
