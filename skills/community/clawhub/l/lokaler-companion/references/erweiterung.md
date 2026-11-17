# Browser-Erweiterung (Manifest V3)

Nur eine Erweiterung meldet sich, ohne dass ein Tab offen ist. Und nur sie darf
per `host_permissions` fremde Adressen abrufen — sie braucht deshalb nicht
einmal den laufenden Server.

Wenn dieser Punkt im Projekt vorkommt, gilt vor allem eins: **einen wirklich
ladefertigen Ordner abliefern**, nicht die Beschreibung, wie man einen baut.
Chrome erkennt eine Erweiterung ausschließlich an der `manifest.json` an der
Wurzel des gewählten Ordners.

## Aufbau

```
extension/
├── manifest.json        muss hier liegen, nicht eine Ebene höher
├── popup.html
├── popup.js
├── background.js        Dienst im Hintergrund
├── gemeinsam.js         Logik, die beide brauchen
├── icons/               16, 48, 128
└── INSTALL.md           mit dem vollständigen Pfad zum Auswählen
```

## manifest.json

```json
{
  "manifest_version": 3,
  "name": "Companion",
  "version": "1.0.0",
  "description": "Beobachtet und meldet Zustandswechsel.",
  "permissions": ["storage", "alarms", "notifications"],
  "host_permissions": [
    "https://beispiel.example/*",
    "http://127.0.0.1:8765/*"
  ],
  "background": { "service_worker": "background.js" },
  "action": { "default_popup": "popup.html", "default_icon": { "128": "icons/icon128.png" } },
  "icons": { "16": "icons/icon16.png", "48": "icons/icon48.png", "128": "icons/icon128.png" },
  "content_security_policy": {
    "extension_pages": "script-src 'self'; object-src 'self'; frame-src https://beispiel.example"
  }
}
```

Zwei Stellen, an denen es hakt:

- **`frame-src`** — ohne diese Zeile bleibt jeder eingebettete `<iframe>` leer.
  Die Fehlermeldung steht nur in der Konsole des Popups, das sich beim Klicken
  daneben sofort schließt: Rechtsklick auf das Symbol → *Popup untersuchen*.
- **Kein `'unsafe-inline'`** — MV3 erlaubt es nicht. Jedes `onclick="…"` im
  HTML wird still ignoriert. Ereignisse gehören in die `.js`-Datei.

## Prüfen im Turnus, ohne offenen Tab

`setInterval` überlebt den ruhenden Dienst nicht. `chrome.alarms` schon — der
Browser weckt den Dienst dafür auf.

```javascript
chrome.alarms.create('pruefen', { periodInMinutes: 2 });   // Minimum ist 1
chrome.alarms.onAlarm.addListener(a => { if (a.name === 'pruefen') pruefen(); });
chrome.runtime.onStartup.addListener(pruefen);
chrome.runtime.onInstalled.addListener(pruefen);
```

Der Dienst wird zwischen den Weckrufen beendet. Alles, was den Wechsel
erkennen soll, muss in `chrome.storage.local` liegen — Variablen im Modul sind
beim nächsten Aufruf weg. Genau hier entsteht sonst der Fehler „meldet nach
jedem Aufwachen wieder".

## Meldung nur beim Wechsel

```javascript
const { letzter } = await chrome.storage.local.get('letzter');
const jetzt = await pruefen();
if (jetzt === null) return;                       // unbekannt ist kein Wechsel
await chrome.storage.local.set({ letzter: jetzt });

if (jetzt && letzter === false) {                 // nur echter Wechsel
  chrome.notifications.create('c-' + Date.now(), {
    type: 'basic', iconUrl: 'icons/icon128.png',
    title: 'Zustand geändert', message: '…', priority: 1
  });
}
chrome.action.setBadgeText({ text: jetzt ? 'AN' : '' });
```

Das Kennzeichen am Symbol ist unauffälliger als eine Meldung und wird oft
lieber gesehen — beides anbieten und den Nutzer entscheiden lassen.

Bleiben Meldungen aus, obwohl der Code läuft: In den Windows-Einstellungen
sind Benachrichtigungen für den Browser abgeschaltet. Chrome liefert dann
stillschweigend nicht aus.

## Laden

```
1. chrome://extensions öffnen (Edge: edge://extensions)
2. Entwicklermodus einschalten
3. "Entpackte Erweiterung laden"
4. den Ordner mit der manifest.json auswählen
```

In `INSTALL.md` den **vollständigen Pfad** hinschreiben und dazu, welcher
Ordner gemeint ist. „Manifest-Datei fehlt oder ist nicht lesbar" heißt fast
immer: eine Ebene zu hoch ausgewählt.

## Fehlersuche

| Bild | Ursache |
|---|---|
| „Manifest-Datei fehlt oder ist nicht lesbar" | falscher Ordner gewählt |
| Popup bleibt weiß | Fehler im JavaScript — Rechtsklick → *Popup untersuchen* |
| Dienst reagiert nicht | auf `chrome://extensions` bei *Service Worker* auf *Fehler* |
| Rahmen bleibt leer | `frame-src` fehlt in der CSP |
| Knöpfe tun nichts | `onclick` im HTML — unter MV3 verboten |
| Keine Meldungen | Systemeinstellung des Browsers |

## Verteilen

Für den eigenen Gebrauch reicht der Ordner. Ein ZIP daneben ist bequem zum
Weitergeben — aber der Nutzer muss es **entpacken**; Chrome lädt kein Archiv.
Das gehört in die Anleitung, sonst probiert er es genau einmal.
