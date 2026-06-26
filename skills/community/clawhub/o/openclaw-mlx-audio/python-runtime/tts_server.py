#!/usr/bin/env python3
"""
OpenClaw mlx-audio TTS Server (Lightweight)

Minimal HTTP server for TTS.
Uses CLI calls for maximum stability.
"""

import argparse
import logging
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("mlx-tts-server")

MODEL = os.getenv("TTS_MODEL", "mlx-community/Kokoro-82M-bf16")
LANG_CODE = os.getenv("TTS_LANG_CODE", "a")


class TTSHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        logger.info(f"{self.address_string()} - {format % args}")

    def do_GET(self):
        if self.path == "/health":
            self.send_json({"status": "healthy", "model": MODEL})
        elif self.path == "/v1/models":
            self.send_json({
                "object": "list",
                "data": [{"id": MODEL, "object": "model"}]
            })
        elif self.path == "/v1/tts/status":
            self.send_json({"status": "ready", "model": MODEL})
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == "/v1/audio/speech":
            self.handle_speech()
        else:
            self.send_error(404)

    def handle_speech(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            req = json.loads(body)

            text = req.get("input", "")
            voice = req.get("voice", "af_heart")
            speed = req.get("speed", 1.0)
            language = req.get("language", LANG_CODE)
            output_format = req.get("response_format", "mp3")

            if not text:
                self.send_error(400, "Text is required")
                return

            # Generate output path
            output_dir = Path("/tmp/mlx-tts")
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"speech_{os.getpid()}.{output_format}"

            # Call CLI
            cmd = [
                "mlx_audio.tts.generate",
                "--model", req.get("model", MODEL),
                "--text", text,
                "--voice", voice,
                "--speed", str(speed),
                "--lang_code", language,
                "--output_path", str(output_path),
                "--audio_format", output_format
            ]

            logger.info(f"Running: {' '.join(cmd)}")
            subprocess.run(cmd, check=True, capture_output=True)

            if not output_path.exists():
                # Try wav fallback
                output_path = output_path.with_suffix(".wav")

            if not output_path.exists():
                self.send_error(500, "Audio not generated")
                return

            # Send file
            self.send_response(200)
            self.send_header("Content-Type", "audio/mpeg")
            self.send_header("Content-Length", output_path.stat().st_size)
            self.end_headers()

            with open(output_path, "rb") as f:
                self.wfile.write(f.read())

            logger.info(f"Sent: {output_path}")

        except subprocess.CalledProcessError as e:
            logger.error(f"CLI failed: {e.stderr}")
            self.send_error(500, str(e.stderr))
        except Exception as e:
            logger.error(f"Error: {e}")
            self.send_error(500, str(e))

    def send_json(self, data):
        body = json.dumps(data).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def send_error(self, code, message=""):
        logger.error(f"Error {code}: {message}")
        super().send_error(code, message)


def main():
    parser = argparse.ArgumentParser(description="TTS Server (Lightweight)")
    parser.add_argument("--model", default=MODEL, help="TTS model")
    parser.add_argument("--port", type=int, default=19280, help="Server port")
    parser.add_argument("--lang-code", default=LANG_CODE, help="Language code")
    parser.add_argument("--host", default="127.0.0.1", help="Server host")

    args = parser.parse_args()

    global MODEL, LANG_CODE
    MODEL = args.model
    LANG_CODE = args.lang_code

    logger.info(f"Starting TTS server on {args.host}:{args.port}")
    logger.info(f"Model: {MODEL}")

    server = HTTPServer((args.host, args.port), TTSHandler)
    print(f"Server ready on http://{args.host}:{args.port}", flush=True)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Shutting down")
        server.shutdown()


if __name__ == "__main__":
    main()
