"""Gumtree Extension Bridge Server."""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import sys
import uuid
from typing import Any

import websockets
from websockets.server import ServerConnection

logger = logging.getLogger("gumtree-bridge")


class BridgeServer:
    def __init__(self) -> None:
        self._extension_ws: ServerConnection | None = None
        self._pending: dict[str, asyncio.Future[Any]] = {}

    async def handle(self, ws: ServerConnection) -> None:
        try:
            raw = await asyncio.wait_for(ws.recv(), timeout=10)
        except (asyncio.TimeoutError, Exception) as exc:
            logger.warning("握手超时或失败: %s", exc)
            return

        try:
            msg = json.loads(raw)
        except json.JSONDecodeError:
            return

        role = msg.get("role")
        if role == "extension":
            await self._handle_extension(ws)
        elif role == "cli":
            await self._handle_cli(ws, msg)
        else:
            logger.warning("未知 role: %s", role)

    async def _handle_extension(self, ws: ServerConnection) -> None:
        logger.info("Extension 已连接")
        self._extension_ws = ws
        try:
            async for raw in ws:
                try:
                    msg = json.loads(raw)
                except json.JSONDecodeError:
                    continue
                msg_id = msg.get("id")
                if msg_id and msg_id in self._pending:
                    future = self._pending.pop(msg_id)
                    if not future.done():
                        future.set_result(msg)
        finally:
            self._extension_ws = None
            logger.info("Extension 已断开")
            for future in self._pending.values():
                if not future.done():
                    future.set_exception(ConnectionError("Extension 断开连接"))
            self._pending.clear()

    async def _handle_cli(self, ws: ServerConnection, msg: dict[str, Any]) -> None:
        if msg.get("method") == "ping_server":
            await ws.send(
                json.dumps(
                    {"result": {"extension_connected": self._extension_ws is not None}},
                    ensure_ascii=False,
                )
            )
            return

        if not self._extension_ws:
            await ws.send(
                json.dumps(
                    {"error": "Extension 未连接，请确认浏览器已安装并启用 Gumtree Bridge 扩展"},
                    ensure_ascii=False,
                )
            )
            return

        msg_id = str(uuid.uuid4())
        msg["id"] = msg_id
        loop = asyncio.get_event_loop()
        future: asyncio.Future[Any] = loop.create_future()
        self._pending[msg_id] = future

        await self._extension_ws.send(json.dumps(msg, ensure_ascii=False))

        try:
            result = await asyncio.wait_for(future, timeout=90.0)
            await ws.send(json.dumps(result, ensure_ascii=False))
        except asyncio.TimeoutError:
            self._pending.pop(msg_id, None)
            await ws.send(json.dumps({"error": "命令执行超时（90s）"}, ensure_ascii=False))
        except ConnectionError as exc:
            await ws.send(json.dumps({"error": str(exc)}, ensure_ascii=False))


async def main(port: int) -> None:
    server = BridgeServer()
    async with websockets.serve(server.handle, "localhost", port):
        logger.info("Bridge server 已启动: ws://localhost:%d", port)
        logger.info("等待浏览器扩展连接...")
        await asyncio.Future()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    if sys.stdout and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Gumtree Extension Bridge Server")
    parser.add_argument("--port", type=int, default=9335, help="监听端口（默认 9335）")
    args = parser.parse_args()

    asyncio.run(main(args.port))
