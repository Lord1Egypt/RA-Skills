#!/usr/bin/env python3
"""
OpenClaw mlx-audio STT Server (Lightweight)

Minimal HTTP server for STT.
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
import cgi

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("mlx-stt-server")

MODEL = os.getenv("STT_MODEL", "mlx-community/whisper-large-v3-turbo-asr-fp16")
LANGUAGE = os.getenv("STT_LANGUAGE", "zh")


class STTHandler(BaseHTTPRequestHandler):
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
        elif self.path == "/v1/stt/status":
            self.send_json({"status": "ready", "model": MODEL})
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == "/v1/audio/transcriptions":
            self.handle_transcription()
        else:
            self.send_error(404)

    def handle_transcription(self):
        content_type = self.headers.get("Content-Type", "")
        
        if "multipart/form-data" not in content_type:
            self.send_error(400, "Expected multipart/form-data")
            return

        # Parse multipart
        _, params = cgi.parse_header(content_type)
        boundary = params.get("boundary", "")
        if not boundary:
            self.send_error(400, "Missing boundary")
            return

        content_length = int(self.headers.get("Content-Length", 0))
        form_data = self.rfile.read(content_length)

        # Simple multipart parsing
        parts = form_data.split(b"--{boundary}".encode())
        audio_data = None
        model = MODEL
        language = LANGUAGE

        for part in parts:
            if not part.strip():
                continue
            
            # Parse headers
            header_end = part.find(b"\r\n\r\n")
            if header_end == -1:
                continue
            
            headers = part[:header_end].decode()
            body = part[header_end + 4:]

            if 'name="file"' in headers:
                # Extract filename and data
                filename_start = headers.find('filename="')
                if filename_start != -1:
                    filename_end = headers.find('"', filename_start + 10)
                    filename = headers[filename_start + 10:filename_end]
                    audio_data = body.rstrip(b"\r\n--")
            elif 'name="model"' in headers:
                model = body.decode().strip()
            elif 'name="language"' in headers:
                language = body.decode().strip()

        if not audio_data:
            self.send_error(400, "No audio file")
            return

        try:
            # Save to temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp.write(audio_data)
                tmp_path = tmp.name

            output_base = tempfile.mktemp()

            # Call CLI
            cmd = [
                "mlx_audio.stt.generate",
                "--model", model,
                "--audio", tmp_path,
                "--format", "txt",
                "--output", output_base
            ]

            if language:
                cmd.extend(["--language", language])

            logger.info(f"Running: {' '.join(cmd)}")
            subprocess.run(cmd, check=True, capture_output=True)

            # Read result
            txt_path = Path(f"{output_base}.txt")
            text = ""
            if txt_path.exists():
                text = txt_path.read_text(encoding="utf-8")
                txt_path.unlink()

            # Cleanup
            try:
                os.unlink(tmp_path)
            except:
                pass

            logger.info(f"Transcription complete: {text[:50]}...")

            # Send result
            self.send_json({
                "text": text,
                "language": language or "auto",
                "model": model
            })

        except subprocess.CalledProcessError as e:
            logger.error(f"CLI failed: {e.stderr}")
            try:
                os.unlink(tmp_path)
            except:
                pass
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
    parser = argparse.ArgumentParser(description="STT Server (Lightweight)")
    parser.add_argument("--model", default=MODEL, help="STT model")
    parser.add_argument("--port", type=int, default=19290, help="Server port")
    parser.add_argument("--language", default=LANGUAGE, help="Default language")
    parser.add_argument("--host", default="127.0.0.1", help="Server host")

    args = parser.parse_args()

    global MODEL, LANGUAGE
    MODEL = args.model
    LANGUAGE = args.language

    logger.info(f"Starting STT server on {args.host}:{args.port}")
    logger.info(f"Model: {MODEL}")

    server = HTTPServer((args.host, args.port), STTHandler)
    print(f"Server ready on http://{args.host}:{args.port}", flush=True)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Shutting down")
        server.shutdown()


if __name__ == "__main__":
    main()
