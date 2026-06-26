# WebSocket API — Real-Time Streaming

Assumes `MASSIVE_API_KEY` is set. Requires a paid Massive subscription for real-time data.
Delayed (15-minute) streaming is available on free plans.

---

## WebSocket Endpoints

| Feed | URL |
|---|---|
| Stocks (real-time) | `wss://socket.massive.com/stocks` |
| Stocks (15-min delay) | `wss://delayed.socket.massive.com/stocks` |
| Options (real-time) | `wss://socket.massive.com/options` |
| Options (15-min delay) | `wss://delayed.socket.massive.com/options` |
| Futures (real-time) | `wss://socket.massive.com/futures` |
| Indices (real-time) | `wss://socket.massive.com/indices` |
| Forex (real-time) | `wss://socket.massive.com/forex` |
| Crypto (real-time) | `wss://socket.massive.com/crypto` |

**Note:** One concurrent connection per asset class by default.

---

## Python WebSocket Client

```python
import asyncio
import json
import os
import websockets

API_KEY = os.environ["MASSIVE_API_KEY"]

async def stream_stocks():
    uri = "wss://socket.massive.com/stocks"

    async with websockets.connect(uri) as ws:
        # Step 1: Authenticate
        await ws.send(json.dumps({"action": "auth", "params": API_KEY}))
        auth_resp = await ws.recv()
        print("Auth:", auth_resp)

        # Step 2: Subscribe to channels
        await ws.send(json.dumps({
            "action": "subscribe",
            "params": "AM.AAPL,AM.MSFT"   # see channels below
        }))

        # Step 3: Receive messages
        async for message in ws:
            events = json.loads(message)
            for event in events:
                handle_event(event)

def handle_event(event):
    ev_type = event.get("ev")
    if ev_type == "AM":
        print(f"Minute bar: {event['sym']} O:{event['o']} H:{event['h']} L:{event['l']} C:{event['c']} V:{event['v']}")
    elif ev_type == "T":
        print(f"Trade: {event['sym']} @ {event['p']} x {event['s']}")
    elif ev_type == "Q":
        print(f"Quote: {event['sym']} bid:{event['bp']} ask:{event['ap']}")

asyncio.run(stream_stocks())
```

---

## Subscription Channels

### Stocks
| Channel | Format | Description |
|---|---|---|
| `T.{ticker}` | `T.AAPL` | Real-time trades |
| `Q.{ticker}` | `Q.AAPL` | Real-time NBBO quotes |
| `AM.{ticker}` | `AM.AAPL` | Minute aggregate bars |
| `A.{ticker}` | `A.AAPL` | Second aggregate bars |

Use `*` to subscribe to all tickers: `T.*`

### Options
| Channel | Format | Description |
|---|---|---|
| `T.{occ}` | `T.O:AAPL261218C00240000` | Option trades |
| `Q.{occ}` | `Q.O:AAPL261218C00240000` | Option quotes |
| `AM.{occ}` | `AM.O:AAPL261218C00240000` | Option minute bars |

### Futures
| Channel | Format | Description |
|---|---|---|
| `T.{ticker}` | `T.ES1!` | Futures trades |
| `Q.{ticker}` | `Q.ES1!` | Futures quotes |
| `AM.{ticker}` | `AM.ES1!` | Futures minute bars |

### Crypto
| Channel | Format | Description |
|---|---|---|
| `XT.{pair}` | `XT.X:BTCUSD` | Crypto trades |
| `XQ.{pair}` | `XQ.X:BTCUSD` | Crypto quotes |
| `XA.{pair}` | `XA.X:BTCUSD` | Crypto minute bars |

---

## Event Fields Reference

### Minute Bar (ev: "AM")
| Field | Description |
|---|---|
| `sym` | Symbol |
| `o` | Open price |
| `h` | High price |
| `l` | Low price |
| `c` | Close price |
| `v` | Volume |
| `a` | VWAP |
| `s` | Start timestamp (Unix ms) |
| `e` | End timestamp (Unix ms) |

### Trade (ev: "T")
| Field | Description |
|---|---|
| `sym` | Symbol |
| `p` | Price |
| `s` | Size |
| `x` | Exchange ID |
| `t` | Timestamp (Unix ns) |

### Quote (ev: "Q")
| Field | Description |
|---|---|
| `sym` | Symbol |
| `bp` | Bid price |
| `ap` | Ask price |
| `bs` | Bid size |
| `as` | Ask size |
| `t` | Timestamp (Unix ns) |

---

## Unsubscribe

```python
await ws.send(json.dumps({
    "action": "unsubscribe",
    "params": "AM.AAPL"
}))
```

---

## Performance Tips

- Process messages quickly — slow consumption causes server-side buffering and disconnection
- If receiving more data than you can process, reduce the number of subscriptions
- Use a wired connection — avoid WiFi and VPNs to minimize latency
- During high-volume periods, multiple events may arrive in a single JSON array — always iterate the array
