#!/usr/bin/env python3
"""takeout_download.py — Download aller Takeout-Teile via aria2c mit CDP-Cookie-Refresh.

- Parst aus EINER gerippten (oder manuell angegebenen) usercontent-URL: JOB, USER, TS
- Konstruiert daraus alle N Teil-URLs (Muster ist fuer alle Teile identisch)
- VOR jedem Teil: frische Cookies via CDP Storage.getCookies aus dem Browser
  (startet den Browser selbst neu, falls geschlossen)
- NACH jedem Teil: PK-Magic + Mindestgroesse; HTML-Muell wird geloescht und retryt
- Resume via .aria2-Kontrolldateien; Drossel per --limit
Log: <dir>/takeout_download.log
"""
import argparse
import asyncio
import json
import os
import re
import subprocess
import sys
import time
import urllib.request

import websockets

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36")
CDP = "http://127.0.0.1:9222"


def log(msg_file, m):
    line = f"[{time.strftime('%H:%M:%S')}] {m}"
    print(line, flush=True)
    msg_file.write(line + "\n")


def parse_url(url):
    """Zieht TS, JOB und USER aus einer gerippten usercontent-URL (Doku-Hilfe)."""
    m = re.search(r"takeout-(\d{8}T\d{6}Z)-1-001\.zip\?j=([\w-]+)&i=0&user=(\d+)", url)
    if not m:
        raise SystemExit(
            "URL entspricht nicht dem Muster (takeout-<TS>-1-001.zip?j=...&i=0&user=...).\n"
            "Erst mit discover_url.py eine echte finale URL beschaffen.")
    return m.groups()


def ensure_browser(browser_app, linux_cmd=None):
    try:
        urllib.request.urlopen(CDP + "/json/version", timeout=5)
        return True
    except Exception:
        pass
    print(f"Browser nicht erreichbar — starte neu ...", flush=True)
    if sys.platform == "darwin":
        subprocess.run(["open", "-a", browser_app, "--args",
                        "--remote-debugging-port=9222",
                        "--no-first-run", "--no-default-browser-check"])
    else:
        subprocess.run(linux_cmd or "chromium --remote-debugging-port=9222 --no-first-run",
                       shell=True)
    for _ in range(10):
        time.sleep(3)
        try:
            urllib.request.urlopen(CDP + "/json/version", timeout=5)
            time.sleep(5)
            return True
        except Exception:
            continue
    return False


async def _all_cookies(bws, domains_filter=None):
    async with websockets.connect(bws, max_size=10 * 1024 * 1024) as ws:
        await ws.send(json.dumps({"id": 1, "method": "Storage.getCookies", "params": {}}))
        while True:
            r = json.loads(await ws.recv())
            if r.get("id") == 1:
                cookies = r["result"]["cookies"]
                if domains_filter:
                    cookies = [c for c in cookies
                               if any(c["domain"].endswith(d) for d in domains_filter)]
                return cookies


def refresh_cookies(jar_path):
    version = json.loads(urllib.request.urlopen(CDP + "/json/version", timeout=10).read())
    # Minimierung: NUR Google-Cookies. Fuer den Download noetig sind google.com-
    # Subdomains (takeout, accounts, usercontent). Alles andere (Banken, Shops,
    # andere Dienste) verlaesst den Browser nicht.
    GOOGLE = [".google.com", ".googleusercontent.com", ".youtube.com"]
    cookies = asyncio.run(_all_cookies(version["webSocketDebuggerUrl"], GOOGLE))
    fd = os.open(jar_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        f.write("# Netscape HTTP Cookie File\n")
        f.write("# Minimized jar: google.com domains only. Delete after use.\n")
        for c in cookies:
            dom = c["domain"]
            flag = "TRUE" if dom.startswith(".") else "FALSE"
            exp = int(c["expires"]) if c.get("expires", -1) and c["expires"] > 0 else 2147483647
            f.write(f"{dom}\t{flag}\t{c.get('path', '/')}\t"
                    f"{'TRUE' if c.get('secure') else 'FALSE'}\t{exp}\t{c['name']}\t{c['value']}\n")
    return len(cookies)


def is_zip(path):
    try:
        with open(path, "rb") as f:
            return f.read(4) == b"PK\x03\x04"
    except Exception:
        return False


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("--job", required=True, help="Takeout-Job-ID")
    ap.add_argument("--user", required=True, help="numerische User-ID aus der gerippten URL")
    ap.add_argument("--ts", required=True, help="Timestamp-Stamm, z.B. 20260827T130928Z")
    ap.add_argument("--total", type=int, default=18, help="Anzahl Teile")
    ap.add_argument("--dir", required=True, help="Zielordner")
    ap.add_argument("--limit", default="5M", help="aria2 max-overall-download-limit")
    ap.add_argument("--jar", default="/tmp/takeout_cookies_all.netscape")
    ap.add_argument("--browser", default="Comet", help="Browser-App-Name (macOS open -a)")
    ap.add_argument("--linux-browser-cmd", default=None,
                    help="Linux: Startbefehl statt 'open -a' (z.B. 'google-chrome "
                         "--remote-debugging-port=9222')")
    args = ap.parse_args()

    global CDP
    CDP = "http://127.0.0.1:9222"
    os.makedirs(args.dir, exist_ok=True)
    logf = open(os.path.join(args.dir, "takeout_download.log"), "a", buffering=1)
    log(logf, f"=== Runner gestartet: {args.total} Teile, Limit {args.limit} ===")

    for i in range(args.total):
        fname = f"takeout-{args.ts}-1-{i + 1:03d}.zip"
        target = os.path.join(args.dir, fname)
        if os.path.exists(target) and is_zip(target) and not os.path.exists(target + ".aria2"):
            log(logf, f"Teil {i + 1}/{args.total}: bereits fertig — skip")
            continue
        url = ("https://takeout-download.usercontent.google.com/download/"
               f"takeout-{args.ts}-1-{i + 1:03d}.zip?j={args.job}&i={i}"
               f"&user={args.user}&authuser=0")
        ok = False
        for attempt in range(1, 4):
            try:
                if not ensure_browser(args.browser, args.linux_browser_cmd):
                    log(logf, "Browser nicht startbar — Abbruch")
                    return
                n = refresh_cookies(args.jar)
                log(logf, f"Teil {i + 1}/{args.total} (Versuch {attempt}): {n} Cookies, Start")
            except Exception as e:
                log(logf, f"FEHLER beim Cookie-Refresh: {e} — Abbruch")
                return
            cmd = ["aria2c",
                   f"--load-cookies={args.jar}",
                   f"--user-agent={UA}",
                   "--referer=https://takeout.google.com/",
                   f"--dir={args.dir}",
                   f"--out={fname}",
                   url,
                   "--continue=true", "--file-allocation=none",
                   "--split=4", "--max-connection-per-server=4", "--min-split-size=10M",
                   "--max-tries=2", "--retry-wait=15", "--timeout=60",
                   f"--max-overall-download-limit={args.limit}",
                   "--summary-interval=60", "--console-log-level=notice"]
            with open(os.path.join(args.dir, "aria2c_part.log"), "a") as al:
                subprocess.run(cmd, stdout=al, stderr=subprocess.STDOUT)
            if os.path.exists(target) and is_zip(target) and os.path.getsize(target) > 5e9:
                log(logf, f"Teil {i + 1}/{args.total} FERTIG: "
                          f"{os.path.getsize(target) / 1e9:.2f} GB (echtes ZIP)")
                ok = True
                break
            if os.path.exists(target) and not is_zip(target):
                os.remove(target)
                log(logf, f"  HTML statt ZIP — Retry (Versuch {attempt})")
            time.sleep(5)
        if not ok:
            log(logf, f"Teil {i + 1}/{args.total} nach 3 Versuchen nicht gelungen — Abbruch. "
                      f"Falls weiterhin HTML: Browser Google-Session pruefen, dann neu starten.")
            return
    log(logf, f"=== ALLE {args.total} TEILE FERTIG ===")


if __name__ == "__main__":
    main()