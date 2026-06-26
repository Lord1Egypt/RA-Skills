#!/usr/bin/env python3
"""
Whisper ASR 长驻内存服务端 - 模型只加载一次，接受请求直接转换，不用每次加载
使用 HuggingFace transformers 加载，不依赖 openai-whisper 包

Usage:
  python scripts/whisper-server.py --port 8001 [--model /path/to/model]

API:
  POST /transcribe
  {
    "audio_path": "/path/to/audio.mp3",
    "language": "Chinese"          // optional, default: Chinese
  }

Response:
  { "status": "ok", "text": "识别出的文字" }
  or { "status": "error", "error": "error message"}
"""

import argparse
import sys
import json
from pathlib import Path
import torch
from http.server import HTTPServer, BaseHTTPRequestHandler
import soundfile as sf
import time
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline


class ASRRequestHandler(BaseHTTPRequestHandler):
    global pipe

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode('utf-8')

        try:
            data = json.loads(body)
        except Exception as e:
            self.send_error(400, f"Invalid JSON: {e}")
            return

        # Required fields
        audio_path = data.get('audio_path')

        if audio_path is None:
            self.send_error(400, "Missing required field: audio_path")
            return

        # Optional fields with defaults
        language = data.get('language', default_language)

        try:
            start = time.time()

            # 读取音频文件
            audio_input, sample_rate = sf.read(audio_path)

            # 如果是立体声转单声道
            if len(audio_input.shape) > 1:
                audio_input = audio_input.mean(axis=1)

            # 语言代码映射到 HF pipeline 识别
            lang_code_map = {
                "Chinese": "zh",
                "English": "en",
                "Japanese": "ja",
                "Korean": "ko",
                "French": "fr",
                "German": "de",
                "Italian": "it",
                "Spanish": "es",
                "Portuguese": "pt",
                "Russian": "ru",
            }
            lang_code = lang_code_map.get(language, language[:2].lower())

            # 识别
            result = pipe(
                {"raw": audio_input, "sampling_rate": sample_rate},
                generate_kwargs={"language": lang_code}
            )
            text = result["text"].strip()

            end = time.time()
            # 日志只输出开头，避免长文本刷屏
            if len(text) > 60:
                display_text = text[:57] + "..."
            else:
                display_text = text
            print(f'[whisper-server] time used: {end - start:.2f}s')
            print(f'[whisper-server] transcribed: "{display_text}"')

            # Send success response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            response = json.dumps({
                "status": "ok",
                "text": text,
            }, ensure_ascii=False)
            self.wfile.write(response.encode('utf-8'))

        except Exception as e:
            import traceback
            traceback.print_exc()
            self.send_error(500, f"Transcription failed: {e}")
            return

    def do_GET(self):
        # Health check
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        response = json.dumps({
            "status": "ok",
            "model_loaded": pipe is not None,
            "device": device,
            "model_path": model_path,
        })
        self.wfile.write(response.encode('utf-8'))


def main():
    global pipe, model_path, default_language, device

    parser = argparse.ArgumentParser(
        description="Whisper ASR server (transformers version) - keep model loaded in memory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--port", type=int, default=8001, help="Port to listen on")
    parser.add_argument("--model", default="/root/.openclaw/models/whisper/whisper-large-v3-turbo", help="Model path or huggingface repo id")
    parser.add_argument("--language", default="Chinese", help="Default language")
    parser.add_argument("--batch-size", type=int, default=16, help="Batch size for inference")
    args = parser.parse_args()

    model_path = args.model
    default_language = args.language

    try:
        # Determine device and dtype
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

        print(f"[whisper-server] Loading Whisper model: {model_path}", file=sys.stderr)

        # Load model via transformers
        model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_path,
            torch_dtype=torch_dtype,
            low_cpu_mem_usage=True,
        )
        model.to(device)

        processor = AutoProcessor.from_pretrained(model_path)

        # Create pipeline
        pipe = pipeline(
            "automatic-speech-recognition",
            model=model,
            tokenizer=processor.tokenizer,
            feature_extractor=processor.feature_extractor,
            chunk_length_s=30,
            batch_size=args.batch_size,
            torch_dtype=torch_dtype,
            device=device,
        )

        print(f"[whisper-server] ✓ Model loaded on {device}", file=sys.stderr)
    except Exception as e:
        print(f"[whisper-server] ❌ Error loading model: {e}", file=sys.stderr)
        sys.exit(1)

    server = HTTPServer(('0.0.0.0', args.port), ASRRequestHandler)
    print(f"[whisper-server] 🚀 ASR server running on http://0.0.0.0:{args.port}", file=sys.stderr)
    print(f"""[whisper-server] Example request:
   POST /transcribe
   {{
     "audio_path": "/path/to/audio.mp3",
     "language": "Chinese"
   }}""", file=sys.stderr)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print(f"\n[whisper-server] 👋 Server stopped", file=sys.stderr)


if __name__ == "__main__":
    main()
