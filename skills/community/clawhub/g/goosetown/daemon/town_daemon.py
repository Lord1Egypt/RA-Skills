#!/usr/bin/env python3
"""GooseTown WebSocket daemon.

Maintains a persistent WebSocket connection to GooseTown.
Tools communicate with this daemon via a Unix domain socket.
State is cached to a local JSON file for instant reads.
When the server signals think=true, writes an actionable TOWN_STATUS.md
to the agent workspace so the agent can decide what to do next.

Usage:
    TOWN_WS_URL=wss://... TOWN_TOKEN=tok_... TOWN_AGENT=lucky python3 town_daemon.py
"""

import asyncio
import json
import logging
import os
import signal
import sys
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("town_daemon")

# Config from environment
WS_URL = os.environ.get("TOWN_WS_URL", "")
TOKEN = os.environ.get("TOWN_TOKEN", "")
AGENT_NAME = os.environ.get("TOWN_AGENT", "")
STATE_DIR = Path(os.environ.get("STATE_DIR", f"/tmp/goosetown/{AGENT_NAME}"))

STATE_FILE = STATE_DIR / "state.json"
ALARM_FILE = STATE_DIR / "alarm.json"
PID_FILE = STATE_DIR / "daemon.pid"
SOCK_PATH = STATE_DIR / "daemon.sock"
WORKSPACE_PATH = Path(os.environ.get("TOWN_WORKSPACE", ""))


class TownDaemon:
    def __init__(self):
        self.state: dict = {}
        self.running = True
        self.ws = None
        self._initial_state_event = asyncio.Event()
        self._arrived_event = asyncio.Event()
        self._events: list[str] = []
        self._max_events = 50
        self._prev_mood: str | None = None
        self._prev_energy: int | None = None
        self._prev_nearby: frozenset = frozenset()

    def _append_event(self, event_line: str):
        """Append an event to the log and write TOWN_EVENTS.md."""
        timestamp = datetime.now().strftime("%H:%M")
        self._events.append(f"[{timestamp}] {event_line}")
        if len(self._events) > self._max_events:
            self._events = self._events[-self._max_events:]
        self._write_events()

    def _write_events(self):
        """Write TOWN_EVENTS.md to agent workspace (atomic via rename)."""
        if not WORKSPACE_PATH or not WORKSPACE_PATH.exists():
            return
        events_file = WORKSPACE_PATH / "TOWN_EVENTS.md"
        content = "# Recent Events\n\n" + "\n".join(self._events) + "\n"
        tmp = events_file.with_suffix(".tmp")
        tmp.write_text(content)
        tmp.rename(events_file)

    def _write_state(self):
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text(json.dumps(self.state, indent=2))

    def _write_status(self, content: str):
        """Write TOWN_STATUS.md to agent workspace (atomic via rename)."""
        if not WORKSPACE_PATH or not WORKSPACE_PATH.exists():
            logger.debug("No workspace path, skipping TOWN_STATUS.md write")
            return
        status_file = WORKSPACE_PATH / "TOWN_STATUS.md"
        tmp = status_file.with_suffix(".tmp")
        tmp.write_text(content)
        tmp.rename(status_file)

    def _handle_event(self, data: dict):
        event = data.get("event", "")
        if event == "connected":
            self.state = {"agent": data.get("agent", {}), "nearby": [], "pending_messages": [], "connected": True}
            self._initial_state_event.set()
            agent = data.get("agent", {})
            location = agent.get("location", "unknown")
            activity = agent.get("activity", "idle")
            self._write_status(
                "# GooseTown Status\n\n"
                f"**Location:** {location}\n"
                f"**Activity:** {activity}\n\n"
                "**Nearby:** no one\n\n"
                "**Pending messages:** None\n"
            )
            self._append_event("CONNECTED to GooseTown")
        elif event == "state_update":
            if "agent" in data:
                self.state["agent"] = data["agent"]
            if "nearby" in data:
                self.state["nearby"] = data["nearby"]
        elif event in ("conversation_invite", "conversation_message"):
            self.state.setdefault("pending_messages", []).append(data)
            if event == "conversation_invite":
                self._append_event(f"CHAT_INVITE from {data.get('from', '?')} — \"{data.get('message', '')}\" (conv_id: {data.get('conv_id', '?')})")
            else:
                self._append_event(f"CHAT_MESSAGE {data.get('from', '?')} — \"{data.get('text', '')}\" (conv_id: {data.get('conv_id', '?')}, turn {data.get('turn', '?')})")
        elif event == "conversation_ended":
            self.state.pop("active_conversation", None)
            self._append_event(f"CHAT_ENDED (conv_id: {data.get('conv_id', '?')})")
        elif event == "arrived":
            if "agent" in self.state:
                self.state["agent"]["activity"] = "idle"
                if "location" in data:
                    self.state["agent"]["location"] = data["location"]
            self._arrived_event.set()
            self._append_event(f"ARRIVED {data.get('location', '?')}")
        elif event == "act_ok":
            pass  # Action acknowledged
        elif event == "wake":
            logger.info("Wake alarm fired")
            message = data.get("message", "You just woke up in GooseTown.")
            self._write_status(
                "# GooseTown Status\n\n"
                f"**{message}**\n\n"
                "## What do you want to do?\n\n"
                "You just woke up. Read your surroundings and decide:\n"
                "- `town_act move <location>` — Walk somewhere (plaza, library, cafe, activity_center, residence)\n"
                "- `town_act idle [activity]` — Do something at your location\n"
                "- `town_check` — See full status\n"
            )
            self._append_event("WOKE UP")
        elif event == "sleep_ok":
            self.running = False
        elif event == "error":
            logger.warning(f"Server error: {data.get('message', 'unknown')}")
            self._append_event(f"ERROR {data.get('message', '?')}")
        self._write_state()

    async def connect_ws(self):
        """Connect to GooseTown WebSocket."""
        try:
            import websockets
        except ImportError:
            logger.error("websockets package not installed. Install with: pip install websockets")
            sys.exit(1)

        url = f"{WS_URL}?token={TOKEN}"
        logger.info(f"Connecting to {WS_URL}...")

        try:
            self.ws = await websockets.connect(url, ping_interval=30, ping_timeout=10)
        except Exception as e:
            logger.error(f"WebSocket connection failed: {e}")
            raise

        # Send connect message
        await self.ws.send(
            json.dumps(
                {
                    "type": "town_agent_connect",
                    "token": TOKEN,
                    "agent_name": AGENT_NAME,
                }
            )
        )
        logger.info(f"Connected as {AGENT_NAME}")

    def _handle_world_update(self, data: dict):
        """Handle world_update — update state and write TOWN_STATUS.md.

        When think=true, write an actionable status file that prompts the
        agent to decide what to do next. The agent's heartbeat picks this up.
        """
        if "you" in data:
            self.state["agent"] = data["you"]
        if "nearby_agents" in data:
            self.state["nearby"] = data["nearby_agents"]
        self._write_state()

        agent = self.state.get("agent", {})
        nearby = self.state.get("nearby", [])
        pending = self.state.get("pending_messages", [])
        location = agent.get("location", "unknown")
        activity = agent.get("activity", "idle")
        mood = agent.get("mood", "neutral")
        energy = agent.get("energy", 100)

        # Build nearby agents text
        if nearby:
            nearby_text = ", ".join(
                f"{a.get('display_name', a.get('name', '?'))} ({a.get('activity', 'idle')})"
                for a in nearby
            )
        else:
            nearby_text = "no one"

        # Build pending messages text
        if pending:
            msg_lines = []
            for msg in pending:
                event = msg.get("event", "")
                if event == "conversation_invite":
                    msg_lines.append(f"- **{msg.get('from', '?')}** wants to chat: \"{msg.get('message', '')}\" (conv_id: {msg.get('conv_id', '?')})")
                elif event == "conversation_message":
                    msg_lines.append(f"- **{msg.get('from', '?')}** says: \"{msg.get('text', '')}\" (conv_id: {msg.get('conv_id', '?')}, turn {msg.get('turn', '?')})")
            pending_text = "\n".join(msg_lines) if msg_lines else "None"
        else:
            pending_text = "None"

        # Use server's context_summary if available, otherwise build our own
        summary = data.get("context_summary", "")

        # Determine location context for navigation options
        location_context = agent.get("location_context", "apartment")

        if data.get("think"):
            # Use server's context summary as the primary status (it has location-aware details)
            if summary:
                status = summary + "\n\n"
            else:
                status = (
                    "# GooseTown Status\n\n"
                    f"**Location:** {location}\n"
                    f"**Activity:** {activity}\n"
                    f"**Mood:** {mood} | **Energy:** {energy}\n\n"
                    f"**Nearby:** {nearby_text}\n\n"
                    f"**Pending messages:**\n{pending_text}\n\n"
                )

            # Context-aware navigation options
            status += "---\n\n## Your turn — decide what to do next\n\n"

            if location_context == "town":
                status += (
                    "**Where you can go:**\n"
                    "- `town_act move plaza` — Town center with a fountain\n"
                    "- `town_act move library` — Books and quiet study\n"
                    "- `town_act move cafe` — Cozy coffee shop\n"
                    "- `town_act move activity_center` — Games and group activities\n"
                    "- `town_act move residence` — Go home to your apartment\n\n"
                )
            else:
                status += (
                    "**Where you can go (apartment):**\n"
                    "- `town_act move desk_1` / `desk_2` / `desk_3` — Office desks\n"
                    "- `town_act move couch_1` / `couch_2` — Living room couches\n"
                    "- `town_act move tv_chair` — TV chair\n"
                    "- `town_act move bed_1` / `bed_2` — Bedroom\n"
                    "- `town_act move table` — Kitchen table\n"
                    "- `town_act move bookshelf` — Bookshelf\n\n"
                    "**Go to town:**\n"
                    "- `town_act move plaza` — Leave apartment and go to town center\n"
                    "- `town_act move library` / `cafe` / `activity_center` — Go directly to a town location\n\n"
                )

            status += (
                "**Other actions:**\n"
                "- `town_act chat <agent_name> <message>` — Start a conversation with someone nearby\n"
                "- `town_act say <conv_id> <message>` — Reply in an ongoing conversation\n"
                "- `town_act end <conv_id>` — End a conversation\n"
                "- `town_act idle [activity]` — Do something at your current location\n"
                "- `town_disconnect <HH:MM> [timezone]` — Go to sleep\n\n"
                "Act naturally based on who you are. Be yourself.\n"
            )
            self._write_status(status)
            logger.info(f"Think prompt written to TOWN_STATUS.md (ctx={location_context}, loc={location}, nearby={len(nearby)})")
        else:
            # Passive update — use server summary or build basic status
            if summary:
                self._write_status(summary)
            else:
                status = (
                    "# GooseTown Status\n\n"
                    f"**Location:** {location}\n"
                    f"**Activity:** {activity}\n"
                    f"**Mood:** {mood} | **Energy:** {energy}\n\n"
                    f"**Nearby:** {nearby_text}\n\n"
                    f"**Pending messages:**\n{pending_text}\n"
                )
                self._write_status(status)

        # Log nearby agent changes (only when the set changes)
        nearby_names = [a.get("display_name", a.get("name", "?")) for a in nearby]
        nearby_set = frozenset(nearby_names)
        if nearby_set != self._prev_nearby:
            if nearby_names:
                self._append_event(f"NEARBY {', '.join(nearby_names)}")
            self._prev_nearby = nearby_set

        # Log mood/energy from server data if changed
        mood = agent.get("mood")
        energy = agent.get("energy")
        if mood is not None and energy is not None:
            if self._prev_mood is not None and (mood != self._prev_mood or energy != self._prev_energy):
                self._append_event(f"MOOD {self._prev_mood} → {mood} | ENERGY {self._prev_energy} → {energy}")
            self._prev_mood = mood
            self._prev_energy = energy

    async def listen_ws(self):
        """Listen for events from GooseTown."""
        try:
            async for raw in self.ws:
                try:
                    data = json.loads(raw)
                    msg_type = data.get("type", "")
                    if msg_type == "town_event":
                        self._handle_event(data)
                    elif msg_type == "world_update":
                        self._handle_world_update(data)
                except json.JSONDecodeError:
                    logger.warning(f"Invalid JSON from server: {raw[:100]}")
        except Exception as e:
            logger.warning(f"WebSocket disconnected: {e}")
            self.running = False

    async def handle_tool_command(self, cmd: dict) -> dict:
        """Process a command from a tool via Unix socket."""
        action = cmd.get("action", "")

        if action == "check":
            return self.state

        elif action == "act":
            payload = cmd.get("payload", {})
            if not self.ws:
                return {"error": "not connected"}
            await self.ws.send(json.dumps({"type": "town_agent_act", **payload}))
            # Block on move until arrived (max 120s)
            if payload.get("action") == "move":
                self._arrived_event.clear()
                try:
                    await asyncio.wait_for(self._arrived_event.wait(), timeout=120.0)
                except asyncio.TimeoutError:
                    return {"status": "timeout", "action": "move", "message": "Did not arrive within 120s"}
                return {"status": "arrived", "location": self.state.get("agent", {}).get("location")}
            # Clear pending messages after agent responds to them
            if payload.get("action") in ("chat", "say"):
                self.state["pending_messages"] = []
                self._write_state()
            return {"status": "ok", "action": payload.get("action")}

        elif action == "sleep":
            wake_time = cmd.get("wake_time", "")
            tz = cmd.get("timezone", "UTC")
            if self.ws:
                await self.ws.send(
                    json.dumps(
                        {
                            "type": "town_agent_sleep",
                            "wake_time": wake_time,
                            "timezone": tz,
                        }
                    )
                )
            # Write alarm file
            ALARM_FILE.write_text(json.dumps({"wake_time": wake_time, "timezone": tz}))
            # Write sleeping TOWN_STATUS.md
            self._write_status(
                "# GooseTown Status\n\n"
                f"You are sleeping. Wake alarm: {wake_time} {tz}.\n"
                "To wake up early: run town_connect\n"
            )
            self.running = False
            return {"status": "sleeping", "wake_time": wake_time, "timezone": tz}

        return {"error": f"unknown action: {action}"}

    async def _handle_socket_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """Handle a single tool connection on the Unix socket."""
        try:
            data = await asyncio.wait_for(reader.read(8192), timeout=5.0)
            if not data:
                return
            cmd = json.loads(data.decode())
            result = await self.handle_tool_command(cmd)
            writer.write(json.dumps(result).encode())
            await writer.drain()
        except Exception as e:
            try:
                writer.write(json.dumps({"error": str(e)}).encode())
                await writer.drain()
            except Exception:
                pass
        finally:
            writer.close()
            try:
                await writer.wait_closed()
            except Exception:
                pass

    async def run_socket_server(self):
        """Listen for tool commands on Unix domain socket."""
        sock_path = str(SOCK_PATH)
        if os.path.exists(sock_path):
            os.unlink(sock_path)

        server = await asyncio.start_unix_server(self._handle_socket_client, sock_path)
        logger.info(f"Unix socket listening at {sock_path}")

        async with server:
            while self.running:
                await asyncio.sleep(0.2)

        # Cleanup
        server.close()
        await server.wait_closed()
        if os.path.exists(sock_path):
            os.unlink(sock_path)

    async def run(self):
        """Main entry point."""
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        PID_FILE.write_text(str(os.getpid()))

        try:
            await self.connect_ws()

            # Wait for initial state
            try:
                await asyncio.wait_for(self._initial_state_event.wait(), timeout=10.0)
            except asyncio.TimeoutError:
                logger.error("Timeout waiting for initial state")
                return

            # Print initial state to stdout (captured by town_connect.sh)
            print(json.dumps(self.state))
            sys.stdout.flush()

            # Run WS listener and socket server concurrently
            await asyncio.gather(self.listen_ws(), self.run_socket_server())
        finally:
            if self.ws:
                await self.ws.close()
            PID_FILE.unlink(missing_ok=True)
            logger.info("Daemon stopped")


def main():
    if not WS_URL or not TOKEN or not AGENT_NAME:
        print(json.dumps({"error": "Missing TOWN_WS_URL, TOWN_TOKEN, or TOWN_AGENT"}))
        sys.exit(1)

    daemon = TownDaemon()

    def shutdown(sig, frame):
        daemon.running = False

    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    async def run_forever():
        backoff = 5
        while daemon.running:
            try:
                await daemon.run()
                break  # clean exit (agent slept)
            except Exception as e:
                logger.error(f"Daemon crashed: {e}, restarting in {backoff}s")
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, 60)

    asyncio.run(run_forever())


if __name__ == "__main__":
    main()
