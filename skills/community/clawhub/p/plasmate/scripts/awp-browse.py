#!/usr/bin/env python3
"""
awp-browse.py - Plasmate AWP client for agent use.

Usage:
    python3 awp-browse.py navigate <url> [--port 9222]
    python3 awp-browse.py click <url> --ref <element_ref> [--port 9222]
    python3 awp-browse.py type <url> --ref <element_ref> --text <text> [--port 9222]
    python3 awp-browse.py extract <url> [--port 9222]
    python3 awp-browse.py scroll <url> --direction <up|down> [--port 9222]

Starts Plasmate server if not already running. Outputs SOM JSON to stdout.
"""

import argparse
import asyncio
import json
import subprocess
import sys
import time
import uuid

try:
    import websockets
except ImportError:
    print("Installing websockets...", file=sys.stderr)
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "websockets"])
    import websockets


class AWPClient:
    def __init__(self, host: str = "127.0.0.1", port: int = 9222):
        self.url = f"ws://{host}:{port}"
        self.ws = None
        self._pending = {}

    async def connect(self):
        self.ws = await websockets.connect(self.url)
        asyncio.create_task(self._reader())
        return await self._request("awp.hello", {
            "client_name": "openclaw-plasmate-skill",
            "client_version": "0.1.0",
            "awp_version": "0.1"
        })

    async def _reader(self):
        try:
            async for msg in self.ws:
                data = json.loads(msg)
                req_id = data.get("id")
                if req_id and req_id in self._pending:
                    self._pending[req_id].set_result(data)
        except websockets.ConnectionClosed:
            pass

    async def _request(self, method: str, params: dict) -> dict:
        req_id = str(uuid.uuid4())
        self._pending[req_id] = asyncio.get_event_loop().create_future()
        await self.ws.send(json.dumps({
            "id": req_id,
            "method": method,
            "params": params
        }))
        result = await asyncio.wait_for(self._pending[req_id], timeout=30)
        del self._pending[req_id]
        if "error" in result:
            raise RuntimeError(f"AWP error: {result['error']}")
        return result.get("result", result)

    async def create_session(self) -> str:
        result = await self._request("session.create", {})
        return result["session_id"]

    async def close_session(self, session_id: str):
        return await self._request("session.close", {"session_id": session_id})

    async def navigate(self, session_id: str, url: str):
        return await self._request("page.navigate", {
            "session_id": session_id,
            "url": url,
            "timeout_ms": 15000
        })

    async def snapshot(self, session_id: str) -> dict:
        return await self._request("page.observe", {"session_id": session_id})

    async def click(self, session_id: str, ref: str):
        return await self._request("act.click", {
            "session_id": session_id,
            "ref": ref
        })

    async def type_text(self, session_id: str, ref: str, text: str):
        return await self._request("act.type", {
            "session_id": session_id,
            "ref": ref,
            "text": text
        })

    async def scroll(self, session_id: str, direction: str):
        return await self._request("act.scroll", {
            "session_id": session_id,
            "direction": direction
        })

    async def extract(self, session_id: str) -> dict:
        return await self._request("page.extract", {"session_id": session_id})

    async def close(self):
        if self.ws:
            await self.ws.close()


def ensure_server(port: int):
    """Start Plasmate server if not running."""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(("127.0.0.1", port))
        sock.close()
        return  # already running
    except ConnectionRefusedError:
        pass

    print(f"Starting Plasmate on port {port}...", file=sys.stderr)
    subprocess.Popen(
        ["plasmate", "serve", "--protocol", "awp", "--port", str(port)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    # Wait for server to be ready
    for _ in range(20):
        time.sleep(0.25)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(("127.0.0.1", port))
            sock.close()
            return
        except ConnectionRefusedError:
            continue
    print("Warning: server may not be ready", file=sys.stderr)


async def main():
    parser = argparse.ArgumentParser(description="Plasmate AWP browser client")
    parser.add_argument("action", choices=["navigate", "click", "type", "extract", "scroll"])
    parser.add_argument("url", help="URL to navigate to")
    parser.add_argument("--ref", help="Element ref ID for click/type")
    parser.add_argument("--text", help="Text to type")
    parser.add_argument("--direction", choices=["up", "down"], default="down", help="Scroll direction")
    parser.add_argument("--port", type=int, default=9222, help="Plasmate server port")
    parser.add_argument("--host", default="127.0.0.1", help="Plasmate server host")
    args = parser.parse_args()

    if args.action == "click" and not args.ref:
        parser.error("--ref required for click action")
    if args.action == "type" and (not args.ref or not args.text):
        parser.error("--ref and --text required for type action")

    ensure_server(args.port)

    client = AWPClient(args.host, args.port)
    try:
        await client.connect()
        session_id = await client.create_session()

        await client.navigate(session_id, args.url)

        if args.action == "navigate":
            result = await client.snapshot(session_id)
        elif args.action == "click":
            await client.click(session_id, args.ref)
            result = await client.snapshot(session_id)
        elif args.action == "type":
            await client.type_text(session_id, args.ref, args.text)
            result = await client.snapshot(session_id)
        elif args.action == "scroll":
            await client.scroll(session_id, args.direction)
            result = await client.snapshot(session_id)
        elif args.action == "extract":
            result = await client.extract(session_id)

        print(json.dumps(result, indent=2))

        await client.close_session(session_id)
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
