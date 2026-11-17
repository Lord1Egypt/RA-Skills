#!/usr/bin/env python3
"""Aus einem web/-Ordner eine installierbare App machen.

Erzeugt Manifest, Service Worker und Symbole und traegt die Verweise in die
HTML-Datei ein. Keine Abhaengigkeiten — die Symbole entstehen als PNG direkt
aus zlib und struct.

    python pwa_kit.py web/ --name "Mein Companion" --theme "#2481cc"

Danach muss der Server die Dateien noch mit den richtigen MIME-Typen
ausliefern; das Skript druckt am Ende, welche das sind. Ein Manifest als
text/plain wird stillschweigend ignoriert — das ist der haeufigste Grund,
warum der Browser die Installation nicht anbietet.
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import re
import struct
import sys
import zlib

# --------------------------------------------------------------- Symbole ---

def _png(path: pathlib.Path, size: int, rgb: tuple[int, int, int], pad: float = 0.0) -> None:
    """Abgerundetes Quadrat mit Sendewellen-Zeichen. Rein rechnerisch, ohne Schrift."""
    w = h = size
    inset = size * pad
    span = size - 2 * inset
    radius = span * 0.22
    rows: list[list[tuple[int, int, int, int]]] = [[(0, 0, 0, 0)] * w for _ in range(h)]

    def in_rounded(x: float, y: float) -> float:
        """1.0 innen, 0.0 aussen, dazwischen weiche Kante."""
        lx, ly = x - inset, y - inset
        dx = max(radius - lx, 0.0, lx - (span - radius))
        dy = max(radius - ly, 0.0, ly - (span - radius))
        if lx < 0 or ly < 0 or lx > span or ly > span:
            return 0.0
        d = math.hypot(dx, dy)
        if d <= radius - 1.0:
            return 1.0
        if d >= radius:
            return 0.0
        return radius - d

    # Grundflaeche
    for y in range(h):
        for x in range(w):
            a = in_rounded(x + 0.5, y + 0.5)
            if a > 0:
                rows[y][x] = (*rgb, int(255 * min(1.0, a)))

    # Sendewellen: Punkt unten links, drei Boegen nach oben rechts
    ox, oy = inset + span * 0.30, inset + span * 0.72
    dot = span * 0.058
    bands = [(span * 0.20, span * 0.045), (span * 0.34, span * 0.045), (span * 0.48, span * 0.045)]
    for y in range(h):
        for x in range(w):
            if rows[y][x][3] == 0:
                continue
            px, py = x + 0.5 - ox, y + 0.5 - oy
            d = math.hypot(px, py)
            hit = d <= dot
            if not hit and px > 0 and py < 0:            # nur der Quadrant oben rechts
                ang = math.degrees(math.atan2(-py, px))
                if 12 <= ang <= 78:
                    hit = any(abs(d - r) <= t / 2 for r, t in bands)
            if hit:
                rows[y][x] = (255, 255, 255, rows[y][x][3])

    raw = b"".join(
        b"\x00" + b"".join(struct.pack("4B", *rows[y][x]) for x in range(w))
        for y in range(h)
    )

    def chunk(tag: bytes, data: bytes) -> bytes:
        body = tag + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)

    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )


def _rgb(value: str) -> tuple[int, int, int]:
    v = value.lstrip("#")
    if len(v) == 3:
        v = "".join(c * 2 for c in v)
    if len(v) != 6:
        raise ValueError(f"Farbe muss #rrggbb sein, nicht {value!r}")
    return tuple(int(v[i:i + 2], 16) for i in (0, 2, 4))     # type: ignore[return-value]


# ------------------------------------------------------------- Bausteine ---

SW = """\
/* Service Worker. Grundregel: die Huelle darf aus dem Zwischenspeicher kommen,
 * damit die App auch ohne laufenden Server startet und etwas Sinnvolles zeigt.
 * Alles unter /api/ kommt IMMER frisch — ein zwischengespeicherter Livestatus
 * sieht richtig aus und ist falsch, das ist schlimmer als gar keiner. */

const CACHE = '__CACHE__';
const SHELL = __SHELL__;

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE)
      .then(c => c.addAll(SHELL))
      .catch(() => {})            // eine fehlende Datei darf die Installation nicht kippen
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET' || url.origin !== location.origin) return;
  if (url.pathname.startsWith('/api/')) return;      // niemals zwischenspeichern

  e.respondWith(
    fetch(e.request)
      .then(r => {
        const copy = r.clone();
        caches.open(CACHE).then(c => c.put(e.request, copy)).catch(() => {});
        return r;
      })
      .catch(() => caches.match(e.request).then(r => r || caches.match('/')))
  );
});

/* Meldung beim Zustandswechsel: die Seite schickt sie herueber, der Worker
   zeigt sie an — so erscheint sie auch, wenn das Fenster im Hintergrund ist. */
self.addEventListener('message', e => {
  const d = e.data;
  if (!d || d.type !== 'notify') return;
  self.registration.showNotification(d.title || 'Hinweis', {
    body: d.body || '',
    icon: '/icons/app-192.png',
    badge: '/icons/app-192.png',
    tag: d.tag || 'companion',
    data: { url: d.url || '/' }
  });
});

self.addEventListener('notificationclick', e => {
  e.notification.close();
  const target = (e.notification.data && e.notification.data.url) || '/';
  e.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true }).then(list => {
      for (const c of list) if ('focus' in c) return c.focus();
      return clients.openWindow(target);
    })
  );
});
"""

HEAD = """\
  <link rel="manifest" href="/manifest.webmanifest">
  <meta name="theme-color" content="__THEME__">
  <link rel="icon" href="/icons/app-192.png">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-title" content="__SHORT__">
  <link rel="apple-touch-icon" href="/icons/app-192.png">
</head>"""

TAIL = """\
<script>
/* Service Worker anmelden. Laeuft nur ueber 127.0.0.1 oder https — beides
   gilt als sichere Herkunft, ein Zertifikat ist also nicht noetig. */
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js').catch(() => {});
  });
}
/* Eigener Installationsknopf: Browser blenden ihren eigenen spaet und
   versteckt ein, viele Nutzer finden ihn nie. */
let deferredPrompt = null;
window.addEventListener('beforeinstallprompt', e => {
  e.preventDefault();
  deferredPrompt = e;
  const b = document.getElementById('installBtn');
  if (b) {
    b.hidden = false;
    b.onclick = async () => {
      b.hidden = true;
      deferredPrompt.prompt();
      await deferredPrompt.userChoice;
      deferredPrompt = null;
    };
  }
});
window.addEventListener('appinstalled', () => {
  const b = document.getElementById('installBtn');
  if (b) b.hidden = true;
});
</script>
</body>"""


def main() -> int:
    ap = argparse.ArgumentParser(description="web/-Ordner zur installierbaren App machen")
    ap.add_argument("webdir", help="Ordner mit index.html")
    ap.add_argument("--name", required=True, help="voller Name der App")
    ap.add_argument("--short", default=None, help="Kurzname fuers Symbol (Standard: erstes Wort)")
    ap.add_argument("--theme", default="#2481cc", help="Themenfarbe #rrggbb")
    ap.add_argument("--description", default="", help="Beschreibung im Manifest")
    ap.add_argument("--html", default="index.html", help="einzubindende HTML-Datei")
    args = ap.parse_args()

    web = pathlib.Path(args.webdir)
    if not web.is_dir():
        print(f"Kein Ordner: {web}", file=sys.stderr)
        return 1
    html = web / args.html
    if not html.is_file():
        print(f"Fehlt: {html}", file=sys.stderr)
        return 1

    short = args.short or args.name.split()[0]
    rgb = _rgb(args.theme)

    # --- Symbole ---
    icons = web / "icons"
    icons.mkdir(exist_ok=True)
    _png(icons / "app-192.png", 192, rgb)
    _png(icons / "app-512.png", 512, rgb)
    _png(icons / "app-maskable.png", 512, rgb, pad=0.12)   # Rand, damit Android nicht beschneidet
    print("  Symbole   : icons/app-192.png, app-512.png, app-maskable.png")

    # --- Manifest ---
    manifest = {
        "id": "/",
        "name": args.name,
        "short_name": short,
        "description": args.description or args.name,
        "start_url": "/",
        "scope": "/",
        "display": "standalone",
        "display_override": ["window-controls-overlay", "standalone"],
        "orientation": "any",
        "background_color": "#ffffff",
        "theme_color": args.theme,
        "lang": "de",
        "categories": ["utilities", "productivity"],
        "icons": [
            {"src": "/icons/app-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "/icons/app-512.png", "sizes": "512x512", "type": "image/png"},
            {"src": "/icons/app-maskable.png", "sizes": "512x512",
             "type": "image/png", "purpose": "maskable"},
        ],
    }
    (web / "manifest.webmanifest").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("  Manifest  : manifest.webmanifest")

    # --- Service Worker ---
    shell = json.dumps(["/", "/manifest.webmanifest",
                        "/icons/app-192.png", "/icons/app-512.png"], indent=2)
    (web / "sw.js").write_text(
        SW.replace("__CACHE__", re.sub(r"[^a-z0-9]+", "-", short.lower()).strip("-") + "-v1")
          .replace("__SHELL__", shell),
        encoding="utf-8")
    print("  Worker    : sw.js")

    # --- HTML verknuepfen ---
    src = html.read_text(encoding="utf-8")
    changed = False
    if "manifest.webmanifest" not in src and "</head>" in src:
        src = src.replace("</head>",
                          HEAD.replace("__THEME__", args.theme).replace("__SHORT__", short), 1)
        changed = True
    if "serviceWorker" not in src and "</body>" in src:
        src = src.replace("</body>", TAIL, 1)
        changed = True
    if changed:
        html.write_text(src, encoding="utf-8")
        print(f"  HTML      : {args.html} verknuepft")
    else:
        print(f"  HTML      : {args.html} war schon verknuepft")

    print("""
  Noch zu tun im Server — ohne die richtigen MIME-Typen lehnt der Browser
  die Installation ab, ohne zu sagen warum:

      ".webmanifest": "application/manifest+json; charset=utf-8"
      ".js":          "text/javascript; charset=utf-8"
      ".png":         "image/png"

  Und einen Knopf mit  id="installBtn" hidden  in die Oberflaeche setzen.""")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
