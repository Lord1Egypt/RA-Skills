#!/usr/bin/env python3
"""discover_url.py — rippt die finale Download-URL eines (gestarteten) Takeout-Downloads
aus dem chrome://downloads-Tab des Browsers (via CDP).

Voraussetzung: Browser laeuft mit --remote-debugging-port=9222 und es wurde (manuell
oder vom Agenten) mindestens ein Takeout-Teil als Download gestartet.
Gibt die URL auf stdout aus und speichert sie optional in eine Datei.
"""
import argparse
import asyncio
import json
import sys
import urllib.request

import websockets


def http_json(path, method="GET"):
    req = urllib.request.Request("http://127.0.0.1:9222" + path, method=method)
    return json.loads(urllib.request.urlopen(req, timeout=10).read())


def dl_tab_id():
    for t in http_json("/json"):
        if t.get("url", "").startswith("chrome://downloads"):
            return t["id"]
    raise RuntimeError("kein chrome://downloads-Tab offen — erst einen Download starten "
                       "(Takeout-Seite -> Herunterladen bei einem Teil)")


async def rip(url_fragment=None):
    tid = dl_tab_id()
    tabs = http_json("/json")
    wsu = next(t["webSocketDebuggerUrl"] for t in tabs if t["id"] == tid)
    async with websockets.connect(wsu, max_size=10 * 1024 * 1024) as ws:
        expr = """
          (() => {
            const items = [...document.querySelector('downloads-manager')
              .shadowRoot.querySelectorAll('downloads-item')];
            const cands = items
              .filter(i => i.data && /takeout.*\\.zip/i.test(i.data.fileName) && i.data.url)
              .map(i => ({f: i.data.fileName, u: i.data.url, s: i.data.state}));
            return JSON.stringify(cands);
          })()
        """
        await ws.send(json.dumps({"id": 1, "method": "Runtime.evaluate",
                                  "params": {"expression": expr, "returnByValue": True}}))
        while True:
            r = json.loads(await ws.recv())
            if r.get("id") == 1:
                return json.loads(r["result"]["result"]["value"])


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", help="URL in diese Datei schreiben (optional)")
    args = ap.parse_args()

    items = asyncio.run(rip())
    if not items:
        print("Kein Takeout-ZIP-Download in chrome://downloads gefunden.\n"
              "Tipp: auf takeout.google.com/manage bei einem Teil 'Herunterladen' klicken,\n"
              "dieses Skript sofort danach laufen lassen (URL bleibt auch pausiert sichtbar).",
              file=sys.stderr)
        sys.exit(1)
    it = items[0]
    print(it["u"])
    if args.out:
        open(args.out, "w").write(it["u"])
        print(f"# {len(items)} Takeout-Downloads gefunden, URL von {it['f']} -> {args.out}",
              file=sys.stderr)


if __name__ == "__main__":
    main()