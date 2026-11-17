# Installierbare Oberfläche (PWA)

Ziel: Der Nutzer soll den Companion im Startmenü haben, nicht als Lesezeichen.

`scripts/pwa_kit.py` erledigt den mechanischen Teil. Dieses Dokument erklärt,
was dahintersteckt und wo es klemmt.

## Die fünf Bedingungen

Ein Browser bietet „Installieren" erst an, wenn alle fünf erfüllt sind. Er sagt
nicht, welche fehlt — deshalb der Reihe nach prüfen.

| # | Bedingung | typischer Fehler |
|---|---|---|
| 1 | sichere Herkunft | erfüllt: `127.0.0.1` und `localhost` gelten als sicher, kein Zertifikat nötig |
| 2 | Manifest verknüpft und ladbar | `<link rel="manifest">` fehlt, oder der Server liefert 404 |
| 3 | Manifest mit `name`, `icons` (192 **und** 512), `start_url`, `display` | nur ein Symbol, oder `display: browser` |
| 4 | Service Worker angemeldet mit `fetch`-Behandlung | Worker ohne `fetch`-Ereignis zählt nicht |
| 5 | richtige MIME-Typen | **häufigster Grund**, siehe unten |

## MIME-Typen

Einfache Server liefern unbekannte Endungen als `text/plain` aus. Damit wird
das Manifest ignoriert und der Service Worker abgelehnt — beides stillschweigend.

```python
TYPES = {
    ".html":        "text/html; charset=utf-8",
    ".js":          "text/javascript; charset=utf-8",
    ".css":         "text/css; charset=utf-8",
    ".json":        "application/json; charset=utf-8",
    ".webmanifest": "application/manifest+json; charset=utf-8",
    ".png":         "image/png",
    ".svg":         "image/svg+xml",
}
```

Nachprüfen ohne Browser:

```bash
curl -s -o /dev/null -w "%{content_type}\n" http://127.0.0.1:8765/manifest.webmanifest
curl -s -o /dev/null -w "%{content_type}\n" http://127.0.0.1:8765/sw.js
```

## Der Service Worker

Eine einzige Regel entscheidet über Nutzen oder Schaden:

> Die Hülle darf zwischengespeichert werden. `/api/…` niemals.

Ein zwischengespeicherter Livestatus sieht richtig aus und ist falsch — das ist
schlimmer als eine ehrliche Fehlermeldung.

```javascript
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET' || url.origin !== location.origin) return;
  if (url.pathname.startsWith('/api/')) return;      // immer frisch

  e.respondWith(                                      // Netz zuerst, Speicher als Rückfall
    fetch(e.request).then(r => {
      const copy = r.clone();
      caches.open(CACHE).then(c => c.put(e.request, copy)).catch(() => {});
      return r;
    }).catch(() => caches.match(e.request).then(r => r || caches.match('/')))
  );
});
```

„Netz zuerst" statt „Speicher zuerst", weil die Oberfläche sich noch ändert und
ein hartnäckig alter Stand schwer zu erklären ist.

**Beim Entwickeln:** Der Worker überlebt Neuladen. Wenn Änderungen nicht
ankommen — *Application → Service Workers → Update on reload*, oder
`CACHE`-Namen hochzählen.

## Installationsknopf

Browser blenden ihren eigenen Knopf spät und versteckt ein; viele Nutzer finden
ihn nie. Einen sichtbaren anbieten:

```html
<button id="installBtn" hidden>Als App installieren</button>
```

```javascript
let deferredPrompt = null;
window.addEventListener('beforeinstallprompt', e => {
  e.preventDefault();                 // ohne das erscheint gar nichts
  deferredPrompt = e;
  const b = document.getElementById('installBtn');
  if (b) { b.hidden = false; b.onclick = async () => {
    b.hidden = true; deferredPrompt.prompt();
    await deferredPrompt.userChoice; deferredPrompt = null;
  }; }
});
window.addEventListener('appinstalled', () => {
  const b = document.getElementById('installBtn'); if (b) b.hidden = true;
});
```

`beforeinstallprompt` gibt es nur in Chrome und Edge. Safari installiert über
*Teilen → Zum Home-Bildschirm*, Firefox auf dem Rechner gar nicht — der Knopf
bleibt dort einfach verborgen, was in Ordnung ist.

## Symbole

192 und 512 Pixel sind Pflicht. Dazu ein maskierbares mit `purpose: maskable`
und rund 12 % Rand, sonst schneidet Android in die Zeichnung.

`pwa_kit.py` erzeugt alle drei rechnerisch, ohne Bildbibliothek.

## Meldungen aus der App heraus

Der Service Worker kann Meldungen zeigen, auch wenn das Fenster im Hintergrund
ist. Die Seite schickt sie hinüber:

```javascript
await Notification.requestPermission();               // einmalig, nach einem Klick
const reg = await navigator.serviceWorker.ready;
reg.active.postMessage({ type: 'notify', title: '…', body: '…', url: '/' });
```

Die Erlaubnis muss aus einer Nutzerhandlung heraus erfragt werden — ungefragt
beim Laden lehnen Browser ab. Ohne offenes Fenster meldet sich nur eine
Erweiterung; siehe `erweiterung.md`.

## Auf Android

Es gibt **keine APK**. Eine PWA hat keine Installationsdatei, die man
verschicken oder seitlich aufspielen könnte — sie wird aus dem Browser
installiert. Wer nach „der App-Datei" fragt, hat ein anderes Modell im Kopf;
das gehört richtiggestellt, bevor jemand nach einem Build sucht, den es nicht
gibt.

Der Ablauf: Adresse in Chrome öffnen → Menü → *App installieren*. Danach liegt
sie mit eigenem Symbol im App-Drawer und startet ohne Adressleiste.

Zwei Voraussetzungen, die auf dem Telefon strenger wirken als am Rechner:

- **HTTPS ist Pflicht.** `localhost` gilt nur auf dem Gerät selbst als sicher.
  Ein Telefon erreicht den Rechner über eine andere Adresse, und `http://…`
  bedeutet dort: kein Service Worker, keine Installation, keine Meldungen.
  Über ein VPN wie Tailscale liefert `tailscale serve --bg <port>` ein echtes
  Zertifikat und damit `https://<host>.<tailnet>.ts.net`.
- **Meldungen brauchen eine Nutzerhandlung.** `Notification.requestPermission()`
  muss aus einem Klick heraus laufen. Ein sichtbarer Knopf in der Oberfläche
  ist dafür der einzige verlässliche Weg.

Wenn wirklich eine echte `.apk` gefordert ist, geht das über eine Trusted Web
Activity (Bubblewrap) — braucht aber Java, Android-SDK, einen Signierschlüssel
und eine `assetlinks.json` auf dem Server. Für den Eigengebrauch lohnt der
Aufwand fast nie.

## Prüfliste

- [ ] `curl` liefert `application/manifest+json` für das Manifest
- [ ] `curl` liefert `text/javascript` für `sw.js`
- [ ] Manifest hat 192er **und** 512er Symbol
- [ ] `display: "standalone"`, `start_url` liegt in `scope`
- [ ] Worker behandelt `fetch` und lässt `/api/` durch
- [ ] Eigener Installationsknopf vorhanden
- [ ] *Application → Manifest* zeigt keine Warnung
