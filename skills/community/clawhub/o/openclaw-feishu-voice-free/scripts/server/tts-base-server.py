#!/usr/bin/env python3
"""
Qwen-TTS 长驻内存服务端 - 模型只加载一次，接受请求直接生成，不用每次加载模型

Usage:
  python scripts/tts-base-server.py --port 8000 [--model /path/to/model]

API:
  POST /generate
  {
    "prompt": "Text to generate",
    "clone": "/path/to/cloned.pt",
    "output": "/path/to/output.mp3",
    "language": "Chinese",          // optional, default: Chinese
    "instruct": "excited moaning",                // optional
    "mp3": true                                 // optional, default: auto-detect by suffix
  }

Response:
  { "status": "ok", "path": "/path/to/output.mp3", "sample_rate": 16000 }
  or { "status": "error", "error": "error message"}
"""

import argparse
import sys
import json
from pathlib import Path
import torch
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
from qwen_tts import Qwen3TTSModel
from qwen_tts import VoiceClonePromptItem
import soundfile as sf
from pydub import AudioSegment
import time

# Start HTTP server
class TTSRequestHandler(BaseHTTPRequestHandler):
    global model, ref_dict

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode('utf-8')
        
        try:
            data = json.loads(body)
        except Exception as e:
            self.send_error(400, f"Invalid JSON: {e}")
            return
        
        # Required fields
        prompt = data.get('prompt')
        output_path = data.get('output')

        if prompt is None or output_path is None:
            self.send_error(400, "Missing required fields: prompt, clone, output are required")
            return
        
        # Optional fields with defaults
        language = data.get('language', 'Chinese')
        instruct = data.get('instruct')

        try:
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
                text=prompt,
                voice_clone_prompt=[prompt_item],
                language=language,
                instruct=instruct if instruct else None,
                # icl_mode=False
            )
            end = time.time()
            print('time used: ', end - start)

            # Save output
            output_path = Path(output_path).expanduser().resolve()
            output_path.parent.mkdir(parents=True, exist_ok=True)

            sf.write(str(output_path), wavs[0], sr)

            print(f"✅ Cloned audio saved: {output_path}", file=sys.stderr)

            # Send success response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = json.dumps({
                "status": "ok",
                "path": str(output_path),
                "sample_rate": sr,
            })
            self.wfile.write(response.encode('utf-8'))

        except Exception as e:
            import traceback
            traceback.print_exc()
            self.send_error(500, f"Generation failed: {e}")
            return

    def do_GET(self):
        # Health check
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        response = json.dumps({
            "status": "ok",
            "model_loaded": model is not None,
            "device": device,
        })
        self.wfile.write(response.encode('utf-8'))


def main():
    parser = argparse.ArgumentParser(
        description="Qwen-TTS server - keep model loaded in memory, serve requests",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--port", type=int, default=8000, help="Port to listen on")
    parser.add_argument("--model", default="/root/.openclaw/models/Qwen3-TTS/Qwen3-TTS-12Hz-1.7B-Base", help="Model path or name")
    parser.add_argument("--clone", default="/root/.openclaw/workspace/skills/openclaw-feishu-voice-free/voice_embedings/huopo_kexin.pt", help="Path to cloned voice embedding file (.pt format). If not specified, uses default voice.")
    args = parser.parse_args()

    global model, ref_dict, device
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

    # Load cloned embedding - exactly same as tts-base.py
    ref_dict = None
    if args.clone:
        clone_path = Path(args.clone)
        # Support relative paths from skill directory or voice_embedings directory
        clone_path_resolved = None
        if not clone_path.is_absolute():
            # Try relative to skill directory first
            skill_dir = Path(__file__).parent.parent.parent
            possible_paths = [
                skill_dir / clone_path,
                skill_dir / "voice_embedings" / clone_path,
                skill_dir / "voice_embedings" / clone_path.name,
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
            print(f"❌ Cloned embedding not found: {args.clone}", file=sys.stderr)
            if not Path(args.clone).is_absolute():
                print(f"   Tried paths: {[str(p) for p in possible_paths]}", file=sys.stderr)
            sys.exit(1)
        ref_dict = torch.load(clone_path_resolved, map_location=device)
        print(f"✓ Loaded cloned voice ref_dict: {clone_path_resolved}", file=sys.stderr)


    server = HTTPServer(('0.0.0.0', args.port), TTSRequestHandler)
    print(f"🚀 TTS server running on http://0.0.0.0:{args.port}", file=sys.stderr)
    print(f"   Example request:", file=sys.stderr)
    print(f"""   POST /generate
   {{
     "prompt": "your text",
     "clone": "/path/to/clone.pt",
     "output": "/path/to/output.mp3"
   }}""", file=sys.stderr)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print(f"\n👋 Server stopped", file=sys.stderr)

if __name__ == "__main__":
    main()
