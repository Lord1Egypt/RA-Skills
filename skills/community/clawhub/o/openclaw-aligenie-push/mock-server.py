#!/usr/bin/env python3
"""
本地测试用 Mock 服务器（无依赖版本）
模拟云服务器推送服务，接收 OpenClaw 请求并打印日志
不调用真实阿里云 API，用于测试调用链路

用法:
    python mock-server.py --port 5000
"""

import argparse
import json
import time
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
_LOGGER = logging.getLogger(__name__)


class PushHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/push":
            self.send_error(404)
            return

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": "Invalid JSON"}).encode())
            return

        text = data.get("text", "")
        open_id = data.get("openId", "")
        device_type = data.get("deviceType", "speaker")
        app_id = data.get("appId", "")

        _LOGGER.info("=" * 50)
        _LOGGER.info("📢 [MOCK] 收到推送请求（未真实发送）")
        _LOGGER.info(f"   AppId:   {app_id}")
        _LOGGER.info(f"   OpenId:  {open_id}")
        _LOGGER.info(f"   Device:  {device_type}")
        _LOGGER.info(f"   Text:    {text}")
        _LOGGER.info("=" * 50)

        response = {
            "success": True,
            "messageId": f"mock_{open_id}_{int(time.time())}",
            "mock": True,
        }

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "mock": True}).encode())
        else:
            self.send_error(404)

    def log_message(self, format, *args):
        # 抑制 HTTP 日志，使用自己的 logging
        pass


def main():
    parser = argparse.ArgumentParser(description="Aligenie Push Mock Server（本地测试用）")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--host", default="0.0.0.0")
    args = parser.parse_args()

    print("=" * 60)
    print("🧪 Aligenie Push Mock 服务器（本地测试）")
    print("   不会真实调用阿里云 API，仅打印日志")
    print(f"   监听: http://{args.host}:{args.port}")
    print("=" * 60)

    server = HTTPServer((args.host, args.port), PushHandler)
    _LOGGER.info(f"服务器启动，监听 {args.host}:{args.port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
