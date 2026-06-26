"""
ClawLink Relay Server — Message router for coordinating OpenClaw agent sessions.

All data is in-memory only — nothing is written to disk. The server shuts down
cleanly with Ctrl-C and leaves no persistent state.

When --token is set, every request must include the Authorization header:
  Authorization: Bearer <token>
This prevents unintended parties from joining your relay.

Usage:
  python server.py                           # localhost only, no auth
  python server.py --host 0.0.0.0 --token X  # LAN access with auth token
  python server.py --port 8080               # Custom port
  python server.py --no-mdns                 # Disable LAN auto-discovery
"""

import argparse
import asyncio
import json
import time
import uuid
import socket
import threading
from datetime import datetime, timezone
from typing import Dict, Optional

try:
    from aiohttp import web
    HAS_AIOHTTP = True
except ImportError:
    HAS_AIOHTTP = False

try:
    from zeroconf import ServiceInfo, Zeroconf
    HAS_ZEROCONF = True
except ImportError:
    HAS_ZEROCONF = False


# ── Auth Middleware ─────────────────────────────────────────────────────────

SHARED_TOKEN: Optional[str] = None  # Set by --token argument


@web.middleware
async def auth_middleware(request, handler):
    """Require Bearer token when SHARED_TOKEN is configured."""
    if SHARED_TOKEN is None:
        return await handler(request)

    # WebSocket upgrade passes token as query param (?token=X) or header
    token = None
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        token = auth_header[7:]
    elif "token" in request.rel_url.query:
        token = request.rel_url.query["token"]

    if token != SHARED_TOKEN:
        return web.json_response(
            {"error": "Unauthorized. Provide Authorization: Bearer <token>"},
            status=401
        )

    return await handler(request)


# ── Agent Registry ──────────────────────────────────────────────────────────

class AgentRegistry:
    """In-memory registry of connected agents. No disk writes."""

    def __init__(self):
        self.agents: Dict[str, dict] = {}
        self.message_queues: Dict[str, list] = {}
        self.broadcast_log: list = []
        self.ws_connections: Dict[str, web.WebSocketResponse] = {}
        self.file_store: Dict[str, dict] = {}

    def register(self, agent_id: str, name: str, capabilities: list,
                 machine: str = "", description: str = "") -> dict:
        agent = {
            "agent_id": agent_id,
            "name": name,
            "capabilities": capabilities,
            "machine": machine,
            "description": description,
            "registered_at": datetime.now(timezone.utc).isoformat(),
            "last_heartbeat": time.time(),
            "status": "online"
        }
        self.agents[agent_id] = agent
        if agent_id not in self.message_queues:
            self.message_queues[agent_id] = []
        return agent

    def heartbeat(self, agent_id: str) -> bool:
        if agent_id in self.agents:
            self.agents[agent_id]["last_heartbeat"] = time.time()
            self.agents[agent_id]["status"] = "online"
            return True
        return False

    def deregister(self, agent_id: str):
        self.agents.pop(agent_id, None)
        self.message_queues.pop(agent_id, None)
        self.ws_connections.pop(agent_id, None)

    def get_online_agents(self, stale_seconds: float = 120.0) -> list:
        now = time.time()
        online = []
        for aid, agent in self.agents.items():
            if now - agent["last_heartbeat"] < stale_seconds:
                agent["status"] = "online"
                online.append(agent)
            else:
                agent["status"] = "stale"
        return online

    def enqueue_message(self, to_agent: str, message: dict):
        if to_agent not in self.message_queues:
            self.message_queues[to_agent] = []
        message["queued_at"] = datetime.now(timezone.utc).isoformat()
        self.message_queues[to_agent].append(message)

    def poll_messages(self, agent_id: str) -> list:
        msgs = self.message_queues.get(agent_id, [])
        self.message_queues[agent_id] = []
        return msgs


registry = AgentRegistry()


# ── HTTP REST API ───────────────────────────────────────────────────────────

async def handle_register(request):
    data = await request.json()
    agent_id = data.get("agent_id", str(uuid.uuid4())[:8])
    name = data.get("name", f"agent-{agent_id[:4]}")
    capabilities = data.get("capabilities", [])
    machine = data.get("machine", request.remote or "unknown")
    description = data.get("description", "")

    agent = registry.register(agent_id, name, capabilities, machine, description)

    join_msg = {
        "type": "agent_joined",
        "agent": agent,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    await broadcast_to_websockets(join_msg, exclude=agent_id)

    return web.json_response({
        "status": "registered",
        "agent": agent,
        "server_time": datetime.now(timezone.utc).isoformat()
    })


async def handle_discover(request):
    agents = registry.get_online_agents()
    return web.json_response({
        "agents": agents,
        "count": len(agents),
        "server_time": datetime.now(timezone.utc).isoformat()
    })


async def handle_heartbeat(request):
    data = await request.json()
    agent_id = data.get("agent_id")
    if not agent_id:
        return web.json_response({"error": "agent_id required"}, status=400)
    ok = registry.heartbeat(agent_id)
    return web.json_response({"status": "ok" if ok else "unknown_agent"})


async def handle_delegate(request):
    data = await request.json()
    from_agent = data.get("from_agent")
    to_agent = data.get("to_agent")
    task = data.get("task")
    context = data.get("context", {})
    priority = data.get("priority", "normal")

    if not all([from_agent, to_agent, task]):
        return web.json_response(
            {"error": "from_agent, to_agent, and task are required"}, status=400
        )

    message = {
        "type": "task_delegation",
        "message_id": str(uuid.uuid4())[:12],
        "from_agent": from_agent,
        "to_agent": to_agent,
        "task": task,
        "context": context,
        "priority": priority,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    ws = registry.ws_connections.get(to_agent)
    if ws and not ws.closed:
        await ws.send_json(message)
        delivery = "websocket"
    else:
        registry.enqueue_message(to_agent, message)
        delivery = "queued"

    return web.json_response({
        "status": "delegated",
        "delivery": delivery,
        "message_id": message["message_id"]
    })


async def handle_broadcast(request):
    data = await request.json()
    from_agent = data.get("from_agent")
    content = data.get("content")
    topic = data.get("topic", "general")
    tags = data.get("tags", [])

    if not all([from_agent, content]):
        return web.json_response(
            {"error": "from_agent and content required"}, status=400
        )

    message = {
        "type": "knowledge_broadcast",
        "message_id": str(uuid.uuid4())[:12],
        "from_agent": from_agent,
        "content": content,
        "topic": topic,
        "tags": tags,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    registry.broadcast_log.append(message)
    if len(registry.broadcast_log) > 200:
        registry.broadcast_log = registry.broadcast_log[-200:]

    await broadcast_to_websockets(message, exclude=from_agent)

    for aid in registry.agents:
        if aid != from_agent:
            registry.enqueue_message(aid, message)

    return web.json_response({
        "status": "broadcast_sent",
        "message_id": message["message_id"],
        "recipients": len(registry.agents) - 1
    })


async def handle_poll(request):
    agent_id = request.match_info["agent_id"]
    registry.heartbeat(agent_id)
    messages = registry.poll_messages(agent_id)
    return web.json_response({
        "messages": messages,
        "count": len(messages)
    })


async def handle_respond(request):
    data = await request.json()
    from_agent = data.get("from_agent")
    to_agent = data.get("to_agent")
    message_id = data.get("message_id")
    result = data.get("result")
    status = data.get("status", "completed")

    message = {
        "type": "task_response",
        "message_id": message_id,
        "response_id": str(uuid.uuid4())[:12],
        "from_agent": from_agent,
        "to_agent": to_agent,
        "result": result,
        "status": status,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    ws = registry.ws_connections.get(to_agent)
    if ws and not ws.closed:
        await ws.send_json(message)
        delivery = "websocket"
    else:
        registry.enqueue_message(to_agent, message)
        delivery = "queued"

    return web.json_response({"status": "response_sent", "delivery": delivery})


async def handle_file_put(request):
    data = await request.json()
    file_key = data.get("file_key")
    content = data.get("content")
    agent_id = data.get("agent_id")
    file_type = data.get("file_type", "text")

    if not all([file_key, content, agent_id]):
        return web.json_response(
            {"error": "file_key, content, and agent_id required"}, status=400
        )

    version = registry.file_store.get(file_key, {}).get("version", 0) + 1

    registry.file_store[file_key] = {
        "file_key": file_key,
        "content": content,
        "file_type": file_type,
        "last_editor": agent_id,
        "version": version,
        "updated_at": datetime.now(timezone.utc).isoformat()
    }

    notify = {
        "type": "file_updated",
        "file_key": file_key,
        "version": version,
        "last_editor": agent_id,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    await broadcast_to_websockets(notify, exclude=agent_id)
    for aid in registry.agents:
        if aid != agent_id:
            registry.enqueue_message(aid, notify)

    return web.json_response({"status": "saved", "version": version})


async def handle_file_get(request):
    file_key = request.match_info["file_key"]
    file_data = registry.file_store.get(file_key)
    if not file_data:
        return web.json_response({"error": "file not found"}, status=404)
    return web.json_response(file_data)


async def handle_file_list(request):
    files = [
        {k: v for k, v in f.items() if k != "content"}
        for f in registry.file_store.values()
    ]
    return web.json_response({"files": files, "count": len(files)})


async def handle_websocket(request):
    agent_id = request.match_info["agent_id"]
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    registry.ws_connections[agent_id] = ws
    registry.heartbeat(agent_id)

    print(f"[ClawLink] WebSocket connected: {agent_id}")

    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                data = json.loads(msg.data)
                msg_type = data.get("type")

                if msg_type == "heartbeat":
                    registry.heartbeat(agent_id)
                elif msg_type == "delegate":
                    data["from_agent"] = agent_id
                    to_agent = data.get("to_agent")
                    target_ws = registry.ws_connections.get(to_agent)
                    if target_ws and not target_ws.closed:
                        await target_ws.send_json(data)
                    else:
                        registry.enqueue_message(to_agent, data)
                elif msg_type == "broadcast":
                    data["from_agent"] = agent_id
                    data["timestamp"] = datetime.now(timezone.utc).isoformat()
                    await broadcast_to_websockets(data, exclude=agent_id)
                    for aid in registry.agents:
                        if aid != agent_id:
                            registry.enqueue_message(aid, data)

            elif msg.type == web.WSMsgType.ERROR:
                print(f"[ClawLink] WS error for {agent_id}: {ws.exception()}")
    finally:
        registry.ws_connections.pop(agent_id, None)
        print(f"[ClawLink] WebSocket disconnected: {agent_id}")

    return ws


async def broadcast_to_websockets(message: dict, exclude: str = ""):
    for aid, ws in list(registry.ws_connections.items()):
        if aid != exclude and not ws.closed:
            try:
                await ws.send_json(message)
            except Exception:
                registry.ws_connections.pop(aid, None)


async def handle_info(request):
    return web.json_response({
        "service": "ClawLink Relay",
        "version": "1.0.1",
        "auth_required": SHARED_TOKEN is not None,
        "agents_online": len(registry.get_online_agents()),
        "total_broadcasts": len(registry.broadcast_log),
        "shared_files": len(registry.file_store),
        "note": "All data is in-memory only. No disk writes. Stops cleanly with Ctrl-C.",
        "endpoints": {
            "register": "POST /register",
            "discover": "GET /discover",
            "heartbeat": "POST /heartbeat",
            "delegate": "POST /delegate",
            "broadcast": "POST /broadcast",
            "respond": "POST /respond",
            "poll": "GET /poll/<agent_id>",
            "files_put": "POST /files",
            "files_get": "GET /files/<file_key>",
            "files_list": "GET /files",
            "websocket": "GET /ws/<agent_id>"
        },
        "server_time": datetime.now(timezone.utc).isoformat()
    })


# ── mDNS/Zeroconf Broadcast ────────────────────────────────────────────────

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def start_mdns(port: int) -> Optional['Zeroconf']:
    if not HAS_ZEROCONF:
        print("[ClawLink] zeroconf not installed — skipping mDNS broadcast")
        return None

    local_ip = get_local_ip()
    hostname = socket.gethostname()

    info = ServiceInfo(
        "_clawlink._tcp.local.",
        f"ClawLink Relay ({hostname})._clawlink._tcp.local.",
        addresses=[socket.inet_aton(local_ip)],
        port=port,
        properties={
            "version": "1.0.1",
            "hostname": hostname,
            "auth": "yes" if SHARED_TOKEN else "no",
        },
        server=f"{hostname}.local.",
    )

    zc = Zeroconf()
    zc.register_service(info)
    print(f"[ClawLink] mDNS broadcasting on {local_ip}:{port}")
    return zc


# ── Main ────────────────────────────────────────────────────────────────────

def create_app():
    app = web.Application(middlewares=[auth_middleware])
    app.router.add_get("/", handle_info)
    app.router.add_post("/register", handle_register)
    app.router.add_get("/discover", handle_discover)
    app.router.add_post("/heartbeat", handle_heartbeat)
    app.router.add_post("/delegate", handle_delegate)
    app.router.add_post("/broadcast", handle_broadcast)
    app.router.add_post("/respond", handle_respond)
    app.router.add_get("/poll/{agent_id}", handle_poll)
    app.router.add_post("/files", handle_file_put)
    app.router.add_get("/files", handle_file_list)
    app.router.add_get("/files/{file_key}", handle_file_get)
    app.router.add_get("/ws/{agent_id}", handle_websocket)
    return app


def main():
    global SHARED_TOKEN

    if not HAS_AIOHTTP:
        print("ERROR: aiohttp is required. Install with: pip install --user aiohttp")
        return

    parser = argparse.ArgumentParser(description="ClawLink Relay Server")
    parser.add_argument("--host", default="127.0.0.1",
                        help="Bind address (default: 127.0.0.1 localhost only; use 0.0.0.0 for LAN)")
    parser.add_argument("--port", type=int, default=9077, help="Port (default: 9077)")
    parser.add_argument("--no-mdns", action="store_true", help="Disable mDNS broadcast")
    parser.add_argument("--token", default=None,
                        help="Shared auth token. Required when --host 0.0.0.0 is used.")
    args = parser.parse_args()

    # Warn if opening to network without auth
    if args.host == "0.0.0.0" and not args.token:
        print("WARNING: Binding to all interfaces without --token.")
        print("         Any machine on the network can connect.")
        print("         Use --token YOUR_SECRET to require authentication.")
        print()

    SHARED_TOKEN = args.token

    zc = None
    if not args.no_mdns and args.host != "127.0.0.1":
        zc = start_mdns(args.port)

    local_ip = get_local_ip() if args.host == "0.0.0.0" else "localhost"
    auth_note = f"token required" if SHARED_TOKEN else "no auth (localhost only)"

    print(f"""
╔══════════════════════════════════════════════════════╗
║              🔗 ClawLink Relay Server                ║
╠══════════════════════════════════════════════════════╣
║  HTTP API:    http://{local_ip}:{args.port:<5}                  ║
║  WebSocket:   ws://{local_ip}:{args.port:<5}/ws/<agent_id>     ║
║  Auth:        {auth_note:<38} ║
║  Storage:     in-memory only (no disk writes)        ║
║  mDNS:        {"ACTIVE" if zc else "DISABLED":<46} ║
╠══════════════════════════════════════════════════════╣
║  Connect agents with: python3 client.py register     ║
╚══════════════════════════════════════════════════════╝
""")

    app = create_app()

    try:
        web.run_app(app, host=args.host, port=args.port, print=lambda _: None)
    except KeyboardInterrupt:
        pass
    finally:
        if zc:
            zc.unregister_all_services()
            zc.close()
        print("[ClawLink] Server stopped. All in-memory data cleared.")


if __name__ == "__main__":
    main()
