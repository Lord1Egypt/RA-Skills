"""
ClawLink Client — CLI + library for OpenClaw agents to join the ClawLink network.

Pass --token (or set CLAWLINK_TOKEN env var) to match the relay server's token.

Usage:
  python client.py --relay http://HOST:9077 --token SECRET register --name "researcher" --caps "search,summarize"
  python client.py discover
  python client.py delegate --to <agent_id> --task "Find recent papers on X"
  python client.py broadcast --topic "finding" --content "Result: ..."
  python client.py poll
  python client.py respond --to <agent_id> --msg-id <id> --result "Done"
  python client.py file-put --key "report.md" --file ./report.md
  python client.py file-get --key "report.md"
  python client.py file-list
  python client.py scan         # mDNS scan for relay servers on LAN
"""

import argparse
import json
import os
import sys
import time
import socket
from typing import Optional

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    from zeroconf import ServiceBrowser, Zeroconf, ServiceStateChange
    HAS_ZEROCONF = True
except ImportError:
    HAS_ZEROCONF = False


# ── State file for persistent agent identity ────────────────────────────────

STATE_DIR = os.path.expanduser("~/.clawlink")
STATE_FILE = os.path.join(STATE_DIR, "agent_state.json")


def load_state() -> dict:
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}


def save_state(state: dict):
    os.makedirs(STATE_DIR, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


# ── mDNS Scanner ────────────────────────────────────────────────────────────

def scan_for_relays(timeout: float = 5.0) -> list:
    """Scan LAN for ClawLink relay servers via mDNS."""
    if not HAS_ZEROCONF:
        print("zeroconf not installed. Install with: pip install --user zeroconf")
        return []

    found = []

    class Listener:
        def add_service(self, zc, type_, name):
            info = zc.get_service_info(type_, name)
            if info:
                addresses = [socket.inet_ntoa(a) for a in info.addresses]
                for addr in addresses:
                    url = f"http://{addr}:{info.port}"
                    props = {
                        k.decode() if isinstance(k, bytes) else k:
                        v.decode() if isinstance(v, bytes) else v
                        for k, v in info.properties.items()
                    }
                    found.append({
                        "name": name,
                        "url": url,
                        "host": addr,
                        "port": info.port,
                        "properties": props
                    })

        def remove_service(self, zc, type_, name):
            pass

        def update_service(self, zc, type_, name):
            pass

    zc = Zeroconf()
    listener = Listener()
    browser = ServiceBrowser(zc, "_clawlink._tcp.local.", listener)

    print(f"Scanning for ClawLink relays on LAN ({timeout}s)...")
    time.sleep(timeout)
    zc.close()

    return found


# ── Client Library ──────────────────────────────────────────────────────────

class ClawLinkClient:
    """Python client for interacting with a ClawLink relay server."""

    def __init__(self, relay_url: str = None, token: str = None):
        if not HAS_REQUESTS:
            raise RuntimeError("requests library required: pip install --user requests")

        if relay_url:
            self.relay_url = relay_url.rstrip("/")
        else:
            self.relay_url = self._auto_discover()

        # Token from arg, env var, or saved state
        self.token = (
            token
            or os.environ.get("CLAWLINK_TOKEN")
        )

        self.agent_id = None
        self.agent_name = None

        state = load_state()
        if state.get("relay_url") == self.relay_url:
            self.agent_id = state.get("agent_id")
            self.agent_name = state.get("agent_name")

    def _auto_discover(self) -> str:
        relays = scan_for_relays(timeout=3.0) if HAS_ZEROCONF else []
        if relays:
            url = relays[0]["url"]
            print(f"Auto-discovered relay: {url}")
            return url
        return "http://localhost:9077"

    def _headers(self) -> dict:
        h = {"Content-Type": "application/json"}
        if self.token:
            h["Authorization"] = f"Bearer {self.token}"
        return h

    def _post(self, endpoint: str, data: dict) -> dict:
        resp = requests.post(
            f"{self.relay_url}/{endpoint}",
            json=data,
            headers=self._headers(),
            timeout=10
        )
        resp.raise_for_status()
        return resp.json()

    def _get(self, endpoint: str) -> dict:
        resp = requests.get(
            f"{self.relay_url}/{endpoint}",
            headers=self._headers(),
            timeout=10
        )
        resp.raise_for_status()
        return resp.json()

    def register(self, name: str, capabilities: list = None,
                 description: str = "") -> dict:
        import uuid
        agent_id = str(uuid.uuid4())[:8]
        result = self._post("register", {
            "agent_id": agent_id,
            "name": name,
            "capabilities": capabilities or [],
            "machine": socket.gethostname(),
            "description": description
        })
        self.agent_id = result["agent"]["agent_id"]
        self.agent_name = name

        save_state({
            "relay_url": self.relay_url,
            "agent_id": self.agent_id,
            "agent_name": self.agent_name
        })

        return result

    def discover(self) -> list:
        return self._get("discover").get("agents", [])

    def heartbeat(self) -> dict:
        return self._post("heartbeat", {"agent_id": self.agent_id})

    def delegate(self, to_agent: str, task: str, context: dict = None,
                 priority: str = "normal") -> dict:
        return self._post("delegate", {
            "from_agent": self.agent_id,
            "to_agent": to_agent,
            "task": task,
            "context": context or {},
            "priority": priority
        })

    def broadcast(self, content: str, topic: str = "general",
                  tags: list = None) -> dict:
        return self._post("broadcast", {
            "from_agent": self.agent_id,
            "content": content,
            "topic": topic,
            "tags": tags or []
        })

    def poll(self) -> list:
        return self._get(f"poll/{self.agent_id}").get("messages", [])

    def respond(self, to_agent: str, message_id: str, result: str,
                status: str = "completed") -> dict:
        return self._post("respond", {
            "from_agent": self.agent_id,
            "to_agent": to_agent,
            "message_id": message_id,
            "result": result,
            "status": status
        })

    def file_put(self, file_key: str, content: str,
                 file_type: str = "text") -> dict:
        return self._post("files", {
            "file_key": file_key,
            "content": content,
            "agent_id": self.agent_id,
            "file_type": file_type
        })

    def file_get(self, file_key: str) -> dict:
        return self._get(f"files/{file_key}")

    def file_list(self) -> list:
        return self._get("files").get("files", [])

    def info(self) -> dict:
        return self._get("")


# ── CLI Interface ───────────────────────────────────────────────────────────

def cli():
    parser = argparse.ArgumentParser(
        description="ClawLink Client — Connect your OpenClaw agent to the mesh"
    )
    parser.add_argument("--relay", default=None,
                        help="Relay server URL (default: auto-discover or localhost:9077)")
    parser.add_argument("--token", default=None,
                        help="Auth token (or set CLAWLINK_TOKEN env var)")

    sub = parser.add_subparsers(dest="command")

    reg = sub.add_parser("register", help="Join the ClawLink network")
    reg.add_argument("--name", required=True)
    reg.add_argument("--caps", default="")
    reg.add_argument("--description", default="")

    sub.add_parser("discover", help="List online agents")
    sub.add_parser("heartbeat", help="Send heartbeat")

    dlg = sub.add_parser("delegate", help="Delegate a task to another agent")
    dlg.add_argument("--to", required=True)
    dlg.add_argument("--task", required=True)
    dlg.add_argument("--context", default="{}")
    dlg.add_argument("--priority", default="normal", choices=["low", "normal", "high", "urgent"])

    bcast = sub.add_parser("broadcast", help="Broadcast knowledge")
    bcast.add_argument("--content", required=True)
    bcast.add_argument("--topic", default="general")
    bcast.add_argument("--tags", default="")

    sub.add_parser("poll", help="Poll for incoming messages")

    rsp = sub.add_parser("respond", help="Respond to a delegated task")
    rsp.add_argument("--to", required=True)
    rsp.add_argument("--msg-id", required=True)
    rsp.add_argument("--result", required=True)
    rsp.add_argument("--status", default="completed")

    fp = sub.add_parser("file-put", help="Create/update a shared file")
    fp.add_argument("--key", required=True)
    fp.add_argument("--file", required=True)
    fp.add_argument("--type", default="text")

    fg = sub.add_parser("file-get", help="Retrieve a shared file")
    fg.add_argument("--key", required=True)
    fg.add_argument("--output", default=None)

    sub.add_parser("file-list", help="List shared files")
    sub.add_parser("scan", help="Scan LAN for ClawLink relays via mDNS")
    sub.add_parser("info", help="Get relay server info")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == "scan":
        relays = scan_for_relays()
        if relays:
            print(f"\nFound {len(relays)} relay(s):")
            for r in relays:
                auth = r["properties"].get("auth", "unknown")
                print(f"  {r['url']}  ({r['name']})  auth={auth}")
        else:
            print("No relays found on LAN.")
        return

    client = ClawLinkClient(args.relay, args.token)

    if args.command == "register":
        caps = [c.strip() for c in args.caps.split(",") if c.strip()]
        result = client.register(args.name, caps, args.description)
        print(json.dumps(result, indent=2))

    elif args.command == "discover":
        agents = client.discover()
        if agents:
            print(f"\n{'Name':<20} {'ID':<10} {'Capabilities':<30} {'Machine':<15} {'Status'}")
            print("─" * 90)
            for a in agents:
                caps = ", ".join(a.get("capabilities", []))
                print(f"{a['name']:<20} {a['agent_id']:<10} {caps:<30} {a.get('machine',''):<15} {a['status']}")
        else:
            print("No agents online.")

    elif args.command == "heartbeat":
        print(json.dumps(client.heartbeat(), indent=2))

    elif args.command == "delegate":
        ctx = json.loads(args.context) if args.context != "{}" else {}
        print(json.dumps(client.delegate(args.to, args.task, ctx, args.priority), indent=2))

    elif args.command == "broadcast":
        tags = [t.strip() for t in args.tags.split(",") if t.strip()]
        print(json.dumps(client.broadcast(args.content, args.topic, tags), indent=2))

    elif args.command == "poll":
        messages = client.poll()
        if messages:
            for m in messages:
                print(f"\n[{m.get('type', 'unknown')}] from {m.get('from_agent', '?')}")
                if m.get("task"):
                    print(f"  Task: {m['task']}")
                if m.get("content"):
                    print(f"  Content: {m['content']}")
                if m.get("result"):
                    print(f"  Result: {m['result']}")
        else:
            print("No new messages.")

    elif args.command == "respond":
        print(json.dumps(client.respond(args.to, args.msg_id, args.result, args.status), indent=2))

    elif args.command == "file-put":
        with open(args.file, "r") as f:
            content = f.read()
        print(json.dumps(client.file_put(args.key, content, args.type), indent=2))

    elif args.command == "file-get":
        data = client.file_get(args.key)
        if args.output:
            with open(args.output, "w") as f:
                f.write(data.get("content", ""))
            print(f"Saved to {args.output}")
        else:
            print(data.get("content", ""))

    elif args.command == "file-list":
        files = client.file_list()
        if files:
            print(f"\n{'Key':<30} {'Version':<10} {'Editor':<15} {'Updated'}")
            print("─" * 75)
            for f in files:
                print(f"{f['file_key']:<30} v{f['version']:<9} {f.get('last_editor',''):<15} {f.get('updated_at','')[:19]}")
        else:
            print("No shared files.")

    elif args.command == "info":
        print(json.dumps(client.info(), indent=2))


if __name__ == "__main__":
    cli()
