#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MiniMax Media Tool - 圖片生成 + 文字轉語音
用法：
  python minimax_media.py image <prompt>
  python minimax_media.py tts <text> [--voice voice_id] [--speed speed] [--output path]
"""
import sys, os, codecs, argparse, json, tempfile, shutil

try:
    import requests
except ImportError:
    print(json.dumps({"error": "requests library not found. Install with: pip install requests"}))
    sys.exit(1)

API_KEY = os.environ.get('MINIMAX_API_KEY', '')
BASE_URL = os.environ.get('MINIMAX_BASE_URL', 'https://api.minimax.io').rstrip('/v1').rstrip('/')


def generate_image(prompt: str, output_path: str = None) -> dict:
    """使用 MiniMax image-01 生成圖片"""
    url = f"{BASE_URL}/v1/image_generation"
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        'model': 'image-01',
        'prompt': prompt
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=60)
    if resp.status_code != 200:
        return {"error": f"API error {resp.status_code}: {resp.text[:200]}"}
    
    data = resp.json()
    image_urls = data.get('data', {}).get('image_urls', [])
    if not image_urls:
        return {"error": "No image URL returned"}
    
    # 下載圖片
    img_resp = requests.get(image_urls[0], timeout=60)
    if img_resp.status_code != 200:
        return {"error": f"Failed to download image: {img_resp.status_code}"}
    
    if output_path is None:
        output_path = tempfile.mktemp(suffix='.png')
    
    with open(output_path, 'wb') as f:
        f.write(img_resp.content)
    
    return {
        "image_path": output_path,
        "url": image_urls[0],
        "size_bytes": len(img_resp.content)
    }


def text_to_speech(text: str, voice_id: str = 'female-tianmei', speed: float = 1.0, output_path: str = None) -> dict:
    """使用 MiniMax speech-2.8-hd 生成語音"""
    url = f"{BASE_URL}/v1/t2a_v2"
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        'model': 'speech-2.8-hd',
        'text': text,
        'stream': False,
        'output_format': 'hex',
        'voice_setting': {
            'voice_id': voice_id,
            'speed': speed,
            'vol': 1,
            'pitch': 0
        },
        'language_boost': 'auto'
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=60)
    if resp.status_code != 200:
        return {"error": f"HTTP error {resp.status_code}: {resp.text[:200]}"}
    
    rdata = resp.json()
    base = rdata.get('base_resp', {})
    if base.get('status_code', 0) != 0:
        return {"error": f"API error {base.get('status_code')}: {base.get('status_msg', '')}"}
    
    audio_hex = rdata.get('data', {}).get('audio', '')
    if not audio_hex:
        return {"error": "No audio data returned"}
    
    # ⚠️ MiniMax TTS V2 回傳的是 hex 字串（不是 base64！），千萬不要用 base64.b64decode()
    audio_bytes = codecs.decode(audio_hex, 'hex')
    
    if output_path is None:
        output_path = tempfile.mktemp(suffix='.mp3')
    
    with open(output_path, 'wb') as f:
        f.write(audio_bytes)
    
    extra = rdata.get('data', {})
    return {
        "audio_path": output_path,
        "size_bytes": len(audio_bytes),
        "duration_hint": f"~{len(audio_bytes)/16000:.1f}s"
    }


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: minimax_media.py <image|tts> <args...>"}))
        sys.exit(1)
    
    cmd = sys.argv[1].lower()
    
    if cmd == 'image':
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Usage: minimax_media.py image <prompt>"}))
            sys.exit(1)
        prompt = ' '.join(sys.argv[2:])
        result = generate_image(prompt)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    elif cmd == 'tts':
        parser = argparse.ArgumentParser(description='MiniMax TTS')
        parser.add_argument('text', help='文字內容')
        parser.add_argument('--voice', default='female-tianmei', help='voice_id')
        parser.add_argument('--speed', type=float, default=1.0, help='速度 0.5-2.0')
        parser.add_argument('--output', default=None, help='輸出檔案路徑')
        args, unknown = parser.parse_known_args(sys.argv[2:])
        result = text_to_speech(args.text, args.voice, args.speed, args.output)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    else:
        print(json.dumps({"error": f"Unknown command: {cmd}"}))
        sys.exit(1)


if __name__ == '__main__':
    main()
