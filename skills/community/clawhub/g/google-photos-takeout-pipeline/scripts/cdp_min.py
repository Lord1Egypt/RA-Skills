#!/usr/bin/env python3
"""cdp_min.py — minimal Chrome DevTools Protocol client for local debugging (port 9222).

Usage:
  python3 cdp_min.py tabs                 # list page tabs
  python3 cdp_min.py open <url>           # open URL in new tab (PUT /json/new)

As a library (sys.path.insert the dir, then `from cdp_min import eval_js, connect_tab, send`):
  await eval_js(tab_id, "document.title")
  async with await connect_tab(tab_id) as ws:
      await send(ws, "Input.dispatchMouseEvent", {...})
"""
import json, asyncio, sys, urllib.request, urllib.parse
import websockets

DEBUG_HOST = "http://127.0.0.1:9222"

def http_json(path, method="GET"):
    req = urllib.request.Request(DEBUG_HOST + path, method=method)
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read().decode())

def list_tabs():
    return [t for t in http_json("/json") if t.get("type") == "page"]

def new_tab(url):
    return http_json("/json/new?" + urllib.parse.quote(url, safe=""), method="PUT")

def close_tab(tab_id):
    try:
        urllib.request.urlopen(f"http://127.0.0.1:9222/json/close/{tab_id}", timeout=10).read()
    except Exception:
        pass

async def send(ws, method, params=None, timeout=30):
    msg_id = send._id = getattr(send, "_id", 0) + 1
    await ws.send(json.dumps({"id": msg_id, "method": method, "params": params or {}}))
    while True:
        raw = await asyncio.wait_for(ws.recv(), timeout)
        data = json.loads(raw)
        if data.get("id") == msg_id:
            if "error" in data:
                raise RuntimeError(f"{method}: {data['error']}")
            return data.get("result", {})

async def connect_tab(tab_id):
    tabs = http_json("/json")
    for t in tabs:
        if t["id"] == tab_id:
            return websockets.connect(t["webSocketDebuggerUrl"], max_size=50 * 1024 * 1024)
    raise RuntimeError(f"tab {tab_id} not found")

async def eval_js(tab_id, expr, await_promise=False):
    async with await connect_tab(tab_id) as ws:
        res = await send(ws, "Runtime.evaluate", {
            "expression": expr, "returnByValue": True,
            "awaitPromise": await_promise, "timeout": 20000})
        return res.get("result", {}).get("value")

async def real_click(tab_id, needle):
    """Trusted CDP mouse click on the innermost visible element containing needle."""
    import json as _json
    pos_raw = await eval_js(tab_id, """(() => {
      const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      let n;
      while ((n = w.nextNode())) {
        if (n.textContent.trim().startsWith('%s')) {
          let el = n.parentElement;
          while (el) {
            const r = el.getBoundingClientRect();
            if (r.width > 0 && r.height > 0 && r.width < 600)
              return JSON.stringify({x: r.x + r.width/2, y: r.y + r.height/2});
            el = el.parentElement;
          }
        }
      }
      return null;
    })()""" % needle)
    if not pos_raw:
        return "not found"
    p = _json.loads(pos_raw)
    async with await connect_tab(tab_id) as ws:
        await send(ws, "Input.dispatchMouseEvent", {"type": "mouseMoved", "x": p["x"], "y": p["y"]})
        await asyncio.sleep(0.3)
        await send(ws, "Input.dispatchMouseEvent", {"type": "mousePressed", "x": p["x"], "y": p["y"], "button": "left", "clickCount": 1})
        await asyncio.sleep(0.15)
        await send(ws, "Input.dispatchMouseEvent", {"type": "mouseReleased", "x": p["x"], "y": p["y"], "button": "left", "clickCount": 1})
    return f"clicked ({p['x']:.0f},{p['y']:.0f})"

async def get_cookie_header(tab_id, urls=("https://takeout.google.com", "https://accounts.google.com")):
    async with await connect_tab(tab_id) as ws:
        res = await send(ws, "Network.getCookies", {"urls": list(urls)})
    return "; ".join(f"{c['name']}={c['value']}" for c in res["cookies"])

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "tabs"
    if cmd == "tabs":
        for t in http_json("/json"):
            if t.get("type") == "page":
                print(t["id"], "|", t["url"][:110])
    elif cmd == "open":
        print(asyncio.run(new_tab(sys.argv[2]))["id"])