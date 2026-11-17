#!/usr/bin/env python3
"""Stream live Hyperliquid trades from Hydromancer's WebSocket.

  Requires websockets (pinned in requirements.txt).
  export HYDROMANCER_API_KEY=...
  python stream_trades.py BTC ETH            # prints trades; Ctrl+C to stop

The WebSocket only accepts the key as the `token` query parameter, so this
script never prints the connection URL and masks `token=` in everything it prints.
"""
import asyncio
import json
import os
import re
import sys

import websockets

URL = "wss://api.hydromancer.xyz/ws?token={key}"


def redact(text):
    return re.sub(r"token=[^&\s'\"]+", "token=***", text)


async def main(coins, max_messages=None):
    key = os.environ.get("HYDROMANCER_API_KEY")
    if not key:
        sys.exit("Set HYDROMANCER_API_KEY first (https://docs.hydromancer.xyz/readme/get-api-keys)")
    # The server sends a JSON {"type": "ping"} every 60 s; reply with a pong or it drops the connection.
    async with websockets.connect(URL.format(key=key), max_size=None,
                                  user_agent_header="hydromancer-skill/0.1") as ws:
        await ws.send(json.dumps({
            "method": "subscribe",
            "requestId": "trades-1",
            "subscription": {"type": "trades", "coins": coins},
        }))
        seen = 0
        async for raw in ws:
            msg = json.loads(raw)
            if msg.get("type") == "ping":
                await ws.send(json.dumps({"type": "pong"}))
                continue
            kind = msg.get("type")
            if kind in ("connected", "subscriptionUpdate"):
                print("control:", redact(json.dumps(msg)), file=sys.stderr)
                if kind == "subscriptionUpdate" and msg.get("failed"):
                    sys.exit(f"subscription failed: {redact(json.dumps(msg))}")
                continue
            if kind == "error":
                sys.exit(f"server error: {redact(json.dumps(msg))}")
            if kind != "trades":
                continue  # ignore other message types (the protocol adds new ones over time)
            print(redact(json.dumps(msg)))
            seen += 1
            if max_messages and seen >= max_messages:
                break


if __name__ == "__main__":
    try:
        asyncio.run(main(sys.argv[1:] or ["BTC"]))
    except KeyboardInterrupt:
        pass
    except Exception as exc:  # keep the key out of tracebacks and logs
        sys.exit(f"stream error: {type(exc).__name__}: {redact(str(exc))}")
