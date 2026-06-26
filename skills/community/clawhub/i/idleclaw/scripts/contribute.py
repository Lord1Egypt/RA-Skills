"""IdleClaw Contribute — Share your idle Ollama inference with the community."""

import asyncio
import json
import logging
import os
import random
import sys
import time
import uuid

from ollama import AsyncClient
import websockets

from config import get_server_url

logging.basicConfig(level=logging.INFO, format="%(asctime)s [idleclaw] %(message)s")
logger = logging.getLogger("contribute")

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
HEARTBEAT_INTERVAL = 15
BASE_DELAY = 1
MAX_DELAY = 60

ALLOWED_PARAMS = {"model", "messages", "stream", "think", "keep_alive", "options", "tools", "format"}
MAX_MESSAGES = 50
MAX_CONTENT_CHARS = 10_000


def validate_params(params: dict, registered_models: list[str]) -> dict:
    """Validate ollama_params: whitelist keys, check model, enforce limits."""
    sanitized = {k: v for k, v in params.items() if k in ALLOWED_PARAMS}
    model = sanitized.get("model")
    if not model or model not in registered_models:
        raise ValueError(f"Model not registered: {model}")
    messages = sanitized.get("messages", [])
    if len(messages) > MAX_MESSAGES:
        raise ValueError(f"Too many messages: {len(messages)}")
    for msg in messages:
        content = msg.get("content", "")
        if isinstance(content, str) and len(content) > MAX_CONTENT_CHARS:
            raise ValueError(f"Message too long: {len(content)} chars")
    return sanitized

_health_cache: dict[str, float | bool] = {"healthy": True, "checked_at": 0.0}
HEALTH_CACHE_TTL = 5  # seconds


async def check_health() -> bool:
    """Check if Ollama is reachable. Caches result for HEALTH_CACHE_TTL seconds."""
    now = time.monotonic()
    if now - _health_cache["checked_at"] < HEALTH_CACHE_TTL:
        return bool(_health_cache["healthy"])
    try:
        client = AsyncClient(host=OLLAMA_HOST)
        await client.list()
        _health_cache["healthy"] = True
    except Exception:
        _health_cache["healthy"] = False
    _health_cache["checked_at"] = now
    return bool(_health_cache["healthy"])


async def get_ollama_version() -> str:
    try:
        import httpx
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{OLLAMA_HOST}/api/version")
            return resp.json().get("version", "unknown") if resp.status_code == 200 else "unknown"
    except Exception:
        return "unknown"


async def check_ollama() -> list[dict]:
    try:
        client = AsyncClient(host=OLLAMA_HOST)
        response = await client.list()
        return [{"name": m.model, "size": m.size} for m in response.models]
    except Exception as e:
        print(f"Error: Cannot connect to Ollama at {OLLAMA_HOST} ({e})", file=sys.stderr)
        sys.exit(1)


async def warmup_models(models: list[dict]) -> None:
    client = AsyncClient(host=OLLAMA_HOST)
    for m in models:
        try:
            await client.chat(model=m["name"], messages=[{"role": "user", "content": "hi"}], keep_alive=-1)
            logger.info("Warmed up model: %s", m["name"])
        except Exception as e:
            logger.warning("Failed to warm up %s: %s", m["name"], e)


async def stream_inference(params: dict):
    """Stream Ollama response chunks as dicts. Node is a relay — no local tool execution."""
    client = AsyncClient(host=OLLAMA_HOST)
    stream = await client.chat(**params)
    async for chunk in stream:
        message = chunk.get("message", {})
        msg_dict: dict = {}
        for key in ("role", "content", "thinking", "tool_calls"):
            val = message.get(key) if isinstance(message, dict) else getattr(message, key, None)
            if val is not None and val != "" and val != []:
                if key == "tool_calls" and isinstance(val, list):
                    val = [tc.model_dump() if hasattr(tc, "model_dump") else tc for tc in val]
                msg_dict[key] = val
        msg_dict.setdefault("role", "assistant")
        msg_dict.setdefault("content", "")
        yield {"message": msg_dict, "done": chunk.get("done", False)}


async def run_node(server_url: str, models: list[dict], ollama_version: str) -> None:
    """Connect to server, register, and handle inference requests."""
    node_id = str(uuid.uuid4())
    ws_url = server_url.replace("https://", "wss://").replace("http://", "ws://") + "/ws/node"

    logger.info("Connecting to %s", ws_url)
    ws = await websockets.connect(ws_url)

    # Register
    await ws.send(json.dumps({
        "type": "register",
        "node_id": node_id,
        "models": models,
        "max_concurrent": 2,
        "ollama_version": ollama_version,
    }))
    raw = await ws.recv()
    msg = json.loads(raw)
    if msg.get("type") != "registered":
        raise RuntimeError(f"Registration failed: {msg}")

    model_names = [m["name"] for m in models]
    logger.info("Registered as node %s", node_id)
    logger.info("Sharing models: %s", ", ".join(model_names))
    logger.info("Waiting for inference requests... (Ctrl+C to stop)")

    active_requests = 0
    inference_tasks: dict[str, asyncio.Task] = {}

    async def heartbeat():
        nonlocal active_requests
        while True:
            await asyncio.sleep(HEARTBEAT_INTERVAL)
            await ws.send(json.dumps({
                "type": "heartbeat",
                "node_id": node_id,
                "active_requests": active_requests,
                "available": True,
            }))

    async def handle_inference(req: dict):
        nonlocal active_requests
        request_id = req["request_id"]
        ollama_params = req["ollama_params"]

        try:
            ollama_params = validate_params(ollama_params, model_names)
        except ValueError as e:
            logger.warning("Invalid request %s: %s", request_id[:8], e)
            await ws.send(json.dumps({
                "type": "inference_error",
                "request_id": request_id,
                "error": "invalid_request",
            }))
            return

        if not await check_health():
            logger.warning("Ollama unavailable for request %s", request_id[:8])
            await ws.send(json.dumps({
                "type": "inference_error",
                "request_id": request_id,
                "error": "ollama_unavailable",
            }))
            return

        active_requests += 1
        logger.info("Inference request %s for %s", request_id[:8], ollama_params.get("model", "?"))
        try:
            async for chunk in stream_inference(ollama_params):
                await ws.send(json.dumps({
                    "type": "inference_chunk",
                    "request_id": request_id,
                    "chunk": {
                        "message": chunk.get("message", {}),
                        "done": chunk.get("done", False),
                    },
                }))
            logger.info("Inference complete: %s", request_id[:8])
        except asyncio.CancelledError:
            logger.info("Inference cancelled: %s", request_id[:8])
        except Exception:
            logger.exception("Inference error for %s", request_id[:8])
            try:
                await ws.send(json.dumps({
                    "type": "inference_error",
                    "request_id": request_id,
                    "error": "ollama_error",
                }))
            except Exception:
                pass
        finally:
            active_requests = max(0, active_requests - 1)

    async def listen():
        async for raw in ws:
            msg = json.loads(raw)
            if msg.get("type") == "inference_request":
                request_id = msg["request_id"]
                task = asyncio.create_task(handle_inference(msg))
                inference_tasks[request_id] = task
                task.add_done_callback(lambda _, rid=request_id: inference_tasks.pop(rid, None))
            elif msg.get("type") == "cancel_request":
                request_id = msg.get("request_id")
                task = inference_tasks.get(request_id)
                if task and not task.done():
                    task.cancel()
                    logger.info("Cancelled inference: %s", request_id)

    await asyncio.gather(listen(), heartbeat())


async def main():
    server_url = get_server_url()

    print(f"IdleClaw Contribute | Server: {server_url} | Ollama: {OLLAMA_HOST}")

    models = await check_ollama()
    if not models:
        print("Error: No models found. Pull a model first: ollama pull llama3.2:3b", file=sys.stderr)
        sys.exit(1)

    for m in models:
        print(f"  - {m['name']} ({m['size'] / (1024**3):.1f} GB)")

    # Detect Ollama version
    ollama_version = await get_ollama_version()
    logger.info("Ollama version: %s", ollama_version)

    # Pre-load models into memory
    logger.info("Warming up models...")
    await warmup_models(models)

    # Connect with reconnection
    attempt = 0
    while True:
        try:
            await run_node(server_url, models, ollama_version)
            attempt = 0
        except websockets.exceptions.InvalidURI:
            print(f"Error: Invalid server URL: {server_url}. Check IDLECLAW_SERVER.", file=sys.stderr)
            sys.exit(1)
        except (ConnectionRefusedError, OSError, Exception) as e:
            logger.warning("Connection lost: %s", e)

        delay = min(BASE_DELAY * (2 ** attempt), MAX_DELAY) + random.uniform(0, 1)
        logger.info("Reconnecting in %.1fs...", delay)
        await asyncio.sleep(delay)
        attempt += 1


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped.")
