"""
Aligenie Genie2 Client for OpenClaw agents.

Usage:
    # Register agent on startup
    python genie_client.py --register --agent-id lobster --session-key SESSION_KEY
    
    # Poll for pending requests (blocking)
    python genie_client.py --poll --agent-id lobster --timeout 30
    
    # Send heartbeat
    python genie_client.py --heartbeat --agent-id lobster

Environment:
    ALIGENIE_SERVER   - Base URL (default: http://127.0.0.1:58472)

The server must expose these endpoints:
    POST /genie/register
    POST /genie/heartbeat
    GET  /genie/poll?agentId=X&timeout=N
    POST /genie/result
    POST /genie/webhook
    GET  /genie/agents
"""
import argparse
import os
import sys
import time
import threading
import requests
import json

DEFAULT_SERVER = os.environ.get("ALIGENIE_SERVER", "http://127.0.0.1:58472")


class GenieClient:
    """Agent client for the Aligenie Genie2 server."""

    def __init__(self, server_url: str = None, agent_id: str = None, api_key: str = None):
        self.server_url = server_url or DEFAULT_SERVER
        self.agent_id = agent_id or os.environ.get("ALIGENIE_AGENT_ID", "")
        self.api_key = api_key or os.environ.get("ALIGENIE_API_KEY", "")
        self._session = requests.Session()
        self._session.headers["Content-Type"] = "application/json"
        if self.api_key:
            self._session.headers["X-Api-Key"] = self.api_key

    def _url(self, path: str) -> str:
        return f"{self.server_url.rstrip('/')}{path}"

    def register(self, session_key: str = "", timeout: int = 30) -> dict:
        """Register this agent with the server."""
        r = self._session.post(
            self._url("/genie/register"),
            json={"agentId": self.agent_id, "sessionKey": session_key, "timeout": str(timeout)},
            timeout=10,
        )
        r.raise_for_status()
        return r.json()

    def heartbeat(self) -> dict:
        """Send heartbeat to keep registration alive."""
        r = self._session.post(
            self._url("/genie/heartbeat"),
            json={"agentId": self.agent_id},
            timeout=10,
        )
        r.raise_for_status()
        return r.json()

    def poll(self, timeout: int = 30) -> list:
        """Long-poll for pending requests. Returns list of requests."""
        r = self._session.get(
            self._url("/genie/poll"),
            params={"agentId": self.agent_id, "timeout": str(timeout)},
            timeout=timeout + 15,
        )
        r.raise_for_status()
        data = r.json()
        if data.get("success") and data.get("request"):
            return [data["request"]]
        return []

    def submit_result(self, request_id: str, reply: str) -> dict:
        """Submit processing result."""
        r = self._session.post(
            self._url("/genie/result"),
            json={"requestId": request_id, "reply": reply},
            timeout=10,
        )
        r.raise_for_status()
        return r.json()

    def list_agents(self) -> dict:
        """List registered agents (debug)."""
        r = self._session.get(self._url("/genie/agents"), timeout=10)
        r.raise_for_status()
        return r.json()

    def start_heartbeat_loop(self, interval: int = 60):
        """Run heartbeat in background thread."""
        def loop():
            while True:
                time.sleep(interval)
                try:
                    self.heartbeat()
                except Exception as e:
                    print(f"[Heartbeat] Error: {e}", file=sys.stderr)

        t = threading.Thread(target=loop, daemon=True)
        t.start()
        return t

    def start_polling_loop(self, callback, poll_interval: int = 5):
        """
        Run polling loop in background thread.
        
        callback(request: dict) -> str | None:
            Called when a request arrives.
            Should return the reply text, or None to acknowledge without reply.
        """
        def loop():
            while True:
                try:
                    for req in self.poll(timeout=poll_interval):
                        rid = req.get("requestId", "")
                        utterance = req.get("utterance", "")
                        skill_name = req.get("skillName", "")
                        print(f"[Poll] Got: {utterance[:80]}")
                        try:
                            reply = callback(req)
                            if reply and rid:
                                self.submit_result(rid, reply)
                                print(f"[Poll] Reply sent: {reply[:80]}")
                        except Exception as e:
                            print(f"[Poll] Callback error: {e}", file=sys.stderr)
                            if rid:
                                self.submit_result(rid, f"处理出错: {e}")
                except Exception as e:
                    print(f"[Poll] Error: {e}", file=sys.stderr)
                    time.sleep(poll_interval)

        t = threading.Thread(target=loop, daemon=True)
        t.start()
        return t


# ─── CLI ─────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Aligenie Genie2 Agent Client")
    parser.add_argument("--register", action="store_true", help="Register agent")
    parser.add_argument("--poll", action="store_true", help="Poll once")
    parser.add_argument("--heartbeat", action="store_true", help="Send heartbeat")
    parser.add_argument("--agents", action="store_true", help="List agents")
    parser.add_argument("--agent-id", default=os.environ.get("ALIGENIE_AGENT_ID", ""),
                        help="Agent ID (or set ALIGENIE_AGENT_ID env)")
    parser.add_argument("--session-key", default="", help="Session key")
    parser.add_argument("--timeout", type=int, default=30, help="Poll timeout (seconds)")
    parser.add_argument("--server", default=DEFAULT_SERVER,
                        help="Server URL (or set ALIGENIE_SERVER env)")
    parser.add_argument("--api-key", default=os.environ.get("ALIGENIE_API_KEY", ""),
                        help="API key for server auth (or set ALIGENIE_API_KEY env)")
    parser.add_argument("--reply", default="", help="Reply text for pending poll result")
    args = parser.parse_args()

    client = GenieClient(server_url=args.server, agent_id=args.agent_id, api_key=args.api_key)

    if args.agents:
        print(json.dumps(client.list_agents(), indent=2, ensure_ascii=False))
        return

    if args.register:
        if not client.agent_id:
            print("Error: --agent-id required (or set ALIGENIE_AGENT_ID)", file=sys.stderr)
            sys.exit(1)
        result = client.register(args.session_key, args.timeout)
        print(f"Registered: {result}")
        client.start_heartbeat_loop(interval=60)
        print("Heartbeat loop started (background).")
        return

    if args.heartbeat:
        if not client.agent_id:
            print("Error: --agent-id required", file=sys.stderr)
            sys.exit(1)
        print(json.dumps(client.heartbeat(), indent=2))
        return

    if args.poll:
        if not client.agent_id:
            print("Error: --agent-id required", file=sys.stderr)
            sys.exit(1)
        reqs = client.poll(timeout=args.timeout)
        if reqs:
            req = reqs[0]
            print(f"Request: {json.dumps(req, ensure_ascii=False)}")
            if args.reply:
                result = client.submit_result(req["requestId"], args.reply)
                print(f"Result: {result}")
        else:
            print("No pending requests")
        return


if __name__ == "__main__":
    main()
