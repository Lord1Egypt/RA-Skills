"""CDP client using raw WebSocket + HTTP devtools protocol.

Manages two connections:
- Browser-level: for listing / creating targets, getting version info
- Page-level:  for Fetch domain interception on a specific tab
"""

from __future__ import annotations

import asyncio
import base64
import itertools
import json
from dataclasses import dataclass
from typing import Any

import httpx
import websockets
import websockets.asyncio.client


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class CDPTarget:
    id: str
    title: str = ""
    url: str = ""
    type: str = "page"
    web_socket_debugger_url: str = ""


# ---------------------------------------------------------------------------
# CDP client
# ---------------------------------------------------------------------------


class CDPError(Exception):
    """Raised when a CDP command returns an error response."""


class CDP:
    """Manages browser-level and page-level CDP connections."""

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 9222,
        timeout: int = 15,
        verbose: bool = False,
    ) -> None:
        self.host = host
        self.port = port
        self.timeout = timeout
        self.verbose = verbose

        self._id_counter = itertools.count(1)

        self._http_base = f"http://{host}:{port}"

        # Browser-level
        self._browser_ws: websockets.asyncio.client.ClientConnection | None = None
        self._pending: dict[int, asyncio.Future[dict[str, Any]]] = {}

        # Page-level
        self._target_ws: websockets.asyncio.client.ClientConnection | None = None
        self._target_pending: dict[int, asyncio.Future[dict[str, Any]]] = {}
        self._target_events: dict[str, list[asyncio.Queue[dict[str, Any]]]] = {}

        # Background tasks
        self._browser_task: asyncio.Task[None] | None = None
        self._target_task: asyncio.Task[None] | None = None

        # Emitted when the page-level WebSocket disconnects
        self.disconnected = asyncio.Event()

    # ------------------------------------------------------------------
    # HTTP helpers
    # ------------------------------------------------------------------

    async def _http_get(self, path: str) -> Any:
        async with httpx.AsyncClient(timeout=httpx.Timeout(self.timeout)) as client:
            resp = await client.get(f"{self._http_base}{path}")
            resp.raise_for_status()
            return resp.json()

    async def _http_put(self, path: str, **json_data: Any) -> Any:
        async with httpx.AsyncClient(timeout=httpx.Timeout(self.timeout)) as client:
            resp = await client.put(f"{self._http_base}{path}", json=json_data)
            resp.raise_for_status()
            return resp.json()

    # ------------------------------------------------------------------
    # Connection management
    # ------------------------------------------------------------------

    async def connect(self) -> None:
        """Establish browser-level WebSocket connection."""
        await self._wait_for_browser()

        version = await self.version()
        ws_url = version.get("webSocketDebuggerUrl", "")
        if not ws_url:
            raise CDPError("no WebSocket URL in version response")

        self._browser_ws = await websockets.asyncio.client.connect(
            ws_url,
            max_size=32 * 1024 * 1024,
            write_limit=32 * 1024 * 1024,
        )
        self._browser_task = asyncio.create_task(self._browser_recv_loop())

    async def close(self) -> None:
        if self._target_ws is not None:
            await self._target_ws.close()
        if self._browser_ws is not None:
            await self._browser_ws.close()

    async def close_browser(self) -> None:
        if self._browser_ws is not None:
            await self._browser_ws.close()
            self._browser_ws = None

    # ------------------------------------------------------------------
    # Browser-level commands
    # ------------------------------------------------------------------

    async def version(self) -> dict[str, Any]:
        return await self._http_get("/json/version")

    async def list_targets(self) -> list[CDPTarget]:
        raw = await self._http_get("/json/list")
        return [
            CDPTarget(
                id=t["id"],
                title=t.get("title", ""),
                url=t.get("url", ""),
                type=t.get("type", "page"),
                web_socket_debugger_url=t.get("webSocketDebuggerUrl", ""),
            )
            for t in raw
        ]

    async def new_tab(self, url: str = "") -> CDPTarget:
        path = "/json/new"
        if url:
            path += f"?{url}"
        raw = await self._http_put(path)
        return CDPTarget(
            id=raw["id"],
            title=raw.get("title", ""),
            url=raw.get("url", ""),
            type=raw.get("type", "page"),
            web_socket_debugger_url=raw.get("webSocketDebuggerUrl", ""),
        )

    # ------------------------------------------------------------------
    # Page-level connection
    # ------------------------------------------------------------------

    async def attach_to_target(self, target_id: str) -> None:
        """Open a page-level WebSocket to a specific tab."""
        targets = await self.list_targets()
        ws_url = ""
        for t in targets:
            if t.id == target_id:
                ws_url = t.web_socket_debugger_url
                break

        if not ws_url:
            raise CDPError(f"target {target_id!r} not found or has no WS URL")

        self._target_ws = await websockets.asyncio.client.connect(
            ws_url,
            max_size=32 * 1024 * 1024,
            write_limit=32 * 1024 * 1024,
        )
        self._target_task = asyncio.create_task(self._target_recv_loop())

    # ------------------------------------------------------------------
    # Page-level commands
    # ------------------------------------------------------------------

    async def navigate_to(self, url: str) -> dict[str, Any]:
        return await self._target_send("Page.navigate", {"url": url})

    async def enable_network(self) -> dict[str, Any]:
        return await self._target_send("Network.enable", {})

    async def enable_fetch(self) -> asyncio.Queue[dict[str, Any]]:
        """Enable Fetch domain and return an event queue.

        Subscribe to Fetch.requestPaused events first, then enable
        Fetch with patterns covering all HTTP/HTTPS requests and responses.
        """
        queue: asyncio.Queue[dict[str, Any]] = asyncio.Queue(maxsize=200)
        if "Fetch.requestPaused" not in self._target_events:
            self._target_events["Fetch.requestPaused"] = []
        self._target_events["Fetch.requestPaused"].append(queue)

        patterns = [
            {"urlPattern": "http://*/*", "requestStage": "Request"},
            {"urlPattern": "https://*/*", "requestStage": "Request"},
            {"urlPattern": "http://*/*", "requestStage": "Response"},
            {"urlPattern": "https://*/*", "requestStage": "Response"},
        ]
        result = await self._target_send("Fetch.enable", {"patterns": patterns})
        return queue

    async def get_response_body(self, request_id: str) -> dict[str, Any]:
        return await self._target_send(
            "Fetch.getResponseBody", {"requestId": request_id}
        )

    async def continue_request(
        self,
        request_id: str,
        *,
        url: str | None = None,
        method: str | None = None,
        post_data: str | None = None,
        headers: list[dict[str, str]] | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"requestId": request_id}
        if url is not None:
            params["url"] = url
        if method is not None:
            params["method"] = method
        if post_data is not None:
            params["postData"] = post_data
        if headers is not None:
            params["headers"] = headers
        return await self._target_send("Fetch.continueRequest", params)

    async def continue_response(
        self,
        request_id: str,
        response_headers: list[dict[str, str]] | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"requestId": request_id}
        if response_headers is not None:
            params["responseHeaders"] = response_headers
        return await self._target_send("Fetch.continueResponse", params)

    async def fulfill_request(
        self,
        request_id: str,
        response_code: int,
        *,
        response_headers: list[dict[str, str]] | None = None,
        body: str | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {
            "requestId": request_id,
            "responseCode": response_code,
        }
        if response_headers is not None:
            params["responseHeaders"] = response_headers
        if body is not None:
            params["body"] = base64.b64encode(body.encode("utf-8")).decode()
        return await self._target_send("Fetch.fulfillRequest", params)

    async def fail_request(
        self, request_id: str, error_reason: str = "Failed"
    ) -> dict[str, Any]:
        return await self._target_send(
            "Fetch.failRequest",
            {"requestId": request_id, "errorReason": error_reason},
        )

    # ------------------------------------------------------------------
    # Internal: JSON-RPC send / recv
    # ------------------------------------------------------------------

    async def _target_send(self, method: str, params: dict[str, Any]) -> dict[str, Any]:
        if self._target_ws is None:
            raise CDPError("target not attached")
        msg_id = next(self._id_counter)
        payload = json.dumps({"id": msg_id, "method": method, "params": params})

        future: asyncio.Future[dict[str, Any]] = asyncio.get_event_loop().create_future()
        self._target_pending[msg_id] = future

        await self._target_ws.send(payload)

        try:
            return await asyncio.wait_for(future, timeout=self.timeout)
        except asyncio.TimeoutError:
            self._target_pending.pop(msg_id, None)
            raise CDPError(f"CDP command {method!r} timed out")
        finally:
            self._target_pending.pop(msg_id, None)

    async def _browser_send(self, method: str, params: dict[str, Any]) -> dict[str, Any]:
        if self._browser_ws is None:
            raise CDPError("browser not connected")
        msg_id = next(self._id_counter)
        payload = json.dumps({"id": msg_id, "method": method, "params": params})

        future: asyncio.Future[dict[str, Any]] = asyncio.get_event_loop().create_future()
        self._pending[msg_id] = future

        await self._browser_ws.send(payload)

        try:
            return await asyncio.wait_for(future, timeout=self.timeout)
        except asyncio.TimeoutError:
            self._pending.pop(msg_id, None)
            raise CDPError(f"CDP command {method!r} timed out")
        finally:
            self._pending.pop(msg_id, None)

    async def _browser_recv_loop(self) -> None:
        assert self._browser_ws is not None
        try:
            async for raw in self._browser_ws:
                msg: dict[str, Any] = json.loads(raw)
                msg_id = msg.get("id")
                if msg_id is not None and msg_id in self._pending:
                    future = self._pending.pop(msg_id)
                    if "error" in msg:
                        future.set_exception(
                            CDPError(f"CDP error: {msg['error']}")
                        )
                    else:
                        future.set_result(msg.get("result", {}))
        except websockets.exceptions.ConnectionClosed:
            pass

    async def _target_recv_loop(self) -> None:
        assert self._target_ws is not None
        try:
            async for raw in self._target_ws:
                msg: dict[str, Any] = json.loads(raw)
                msg_id = msg.get("id")

                # Response to a command
                if msg_id is not None and msg_id in self._target_pending:
                    future = self._target_pending.pop(msg_id)
                    if "error" in msg:
                        future.set_exception(
                            CDPError(f"CDP error: {msg['error']}")
                        )
                    else:
                        future.set_result(msg.get("result", {}))
                    continue

                # Event notification
                method = msg.get("method", "")
                if method and method in self._target_events:
                    params = msg.get("params", {})
                    for queue in self._target_events[method]:
                        try:
                            queue.put_nowait(params)
                        except asyncio.QueueFull:
                            pass
        except websockets.exceptions.ConnectionClosed:
            self.disconnected.set()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    async def _wait_for_browser(self, retries: int = 30, delay: float = 0.5) -> None:
        for _ in range(retries):
            try:
                await self.version()
                return
            except Exception:
                await asyncio.sleep(delay)
        raise CDPError(
            f"browser not ready after {retries * delay:.0f}s at "
            f"http://{self.host}:{self.port}"
        )
