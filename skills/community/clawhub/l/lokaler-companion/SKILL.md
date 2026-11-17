---
name: lokaler-companion
description: >
  Baut einen "Companion" — eine lokal laufende Beobachtungs-Anwendung: kleiner
  Server auf 127.0.0.1, Doppelklick-Starter, installierbare PWA, optionale
  Browser-Erweiterung, Meldung beim Zustandswechsel, Dauerbetrieb im Container.
  Nutze diesen Skill, sobald jemand etwas dauerhaft im Auge behalten und
  benachrichtigt werden will — Livestreams, Kanäle, Feeds, Preise,
  Build-Zustände, Serververfügbarkeit, Ordner, Warteschlangen. Auch wenn die
  Anfrage nur nach einem Teil klingt: "sag mir Bescheid wenn X online geht",
  "kleines Tool das im Hintergrund läuft", "Statusseite für Y", "als App
  installierbar", "soll dauerhaft laufen", "auch nach Neustart", "als
  Docker-Container". Besonders wichtig bei einer einzelnen HTML-Datei, die
  fremde Daten abruft: ob das trägt, hängt an einer CORS-Freigabe, die man
  vorher prüfen muss — sonst bleibt die Datei beim Nutzer leer.
---

# Lokaler Companion

Ein Companion ist eine kleine Anwendung, die auf dem Rechner des Nutzers läuft,
etwas im Turnus beobachtet und sich meldet, wenn sich etwas ändert. Er gehört
dem Nutzer: keine Cloud, keine Anmeldung, kein Konto, nichts verlässt den
Rechner außer den Abrufen der beobachteten Quelle.

Dieser Skill beschreibt das Muster und bringt die Werkzeuge mit, die man sonst
jedes Mal neu schreibt.

## Warum es diesen Skill gibt

Die naheliegende Lösung ist *eine* HTML-Datei, die der Nutzer doppelklickt.
Manchmal geht das — meistens nicht, und der Unterschied hängt an einer einzigen
Frage, die man **vor** dem Bauen klären muss.

Eine über `file://` geöffnete Seite hat die Herkunft `null`. Sie darf einen
fremden Server nur dann abrufen, wenn dieser von sich aus
`Access-Control-Allow-Origin: *` mitschickt. Das tun öffentliche
Browser-Schnittstellen oft; gewöhnliche Webseiten so gut wie nie. Und an fremden
Servern lässt sich diese Kopfzeile nicht nachrüsten.

**Die Entscheidung: jede Quelle einmal anfragen.**

```bash
curl -sI "<adresse>" | grep -i access-control-allow-origin
```

- Kommt bei **jeder** Quelle `*` zurück → eine einzelne Datei genügt, und sie ist
  die freundlichste Lösung. Kein Server, kein Starter, kein Python.
- Kommt bei **einer** Quelle nichts → die Datei wird beim Nutzer leer bleiben,
  mit `TypeError: Failed to fetch`. Dann braucht es den lokalen Server.

Wer diese Frage überspringt, liefert etwas ab, das beim Entwickeln funktioniert
(dort läuft ein Server) und beim Nutzer nicht.

| Herkunft | darf abrufen |
|---|---|
| `file://` | nur Ziele mit `Access-Control-Allow-Origin: *` |
| `http://127.0.0.1:<port>` | den eigenen Server frei; fremde wie oben — aber der eigene Server darf für die Seite abrufen, ohne dass der Browser dazwischensteht |
| `chrome-extension://…` | alles, was in `host_permissions` steht |

Die letzte Zeile ist der eigentliche Grund für die Architektur: **Ein lokaler
Server holt die Daten selbst** — serverseitig gibt es kein CORS — und reicht sie
der Oberfläche unter derselben Herkunft weiter. Damit ist jede Quelle erreichbar,
nicht nur die höflichen.

## Die vier Teile

```
companion/
├── server.py          Rückgrat: beobachtet im Turnus, liefert JSON + Oberfläche
├── web/               Oberfläche, ausgeliefert vom Server (nicht per Doppelklick!)
│   ├── index.html
│   ├── manifest.webmanifest   ─┐ machen die Oberfläche
│   ├── sw.js                   │ zur installierbaren App
│   └── icons/                 ─┘
├── Start.cmd          Doppelklick: startet unsichtbar, wartet, öffnet Fenster
└── extension/         optional: Meldung ohne offenen Tab
```

Nicht jedes Projekt braucht alle vier. Die Reihenfolge unten ist so gewählt,
dass nach jedem Schritt etwas Vorzeigbares da ist.

## Reihenfolge

### 1. Erst der Server, dann alles andere

Der Server ist der einzige Teil, ohne den nichts geht. Baue ihn zuerst, mit
Bordmitteln (`http.server`, `urllib`, `json`) — jede Abhängigkeit ist eine
Fehlerquelle beim Nutzer, die du nicht siehst.

Zwei Aufgaben, sauber getrennt:

- **Beobachten**: ein Hintergrundfaden fragt die Quelle alle *n* Sekunden ab,
  schreibt den Verlauf auf die Platte und löst bei Wechseln eine Meldung aus.
- **Ausliefern**: JSON unter `/api/…`, die Oberfläche unter `/`.

Beides in einem Prozess, weil der Nutzer nur eine Sache starten soll.

**CORS nicht vergessen.** Sobald die Oberfläche auch von woanders kommen kann
(installierte App, Erweiterung, Artefakt), braucht jede Antwort:

```python
self.send_header("Access-Control-Allow-Origin", "*")
self.send_header("Access-Control-Allow-Headers", "Content-Type")
self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")

def do_OPTIONS(self):          # Vorabanfrage des Browsers
    self._send(204, b"", "text/plain")
```

Das ist unbedenklich: der Server hört nur auf `127.0.0.1` und ist von außen
nicht erreichbar.

### 2. Die echten Antwortstrukturen ermitteln — nicht raten

Bevor du die Oberfläche schreibst, lass den Server laufen und sieh dir an, was
er **tatsächlich** zurückgibt. Feldnamen zu raten ist der häufigste Grund für
eine Oberfläche, die überall `undefined` anzeigt.

```bash
python scripts/probe_api.py http://127.0.0.1:8765 /api/status /api/live/all /api/events
```

Das Skript ruft jeden Endpunkt auf und druckt die Struktur mit echten
Beispielwerten. Schreibe die Oberfläche gegen **diese** Ausgabe.

### 3. Oberfläche — und was passiert, wenn der Server fehlt

Zwei Regeln, die sich in der Praxis bewährt haben:

**Entkoppeln, was ohne Abruf funktioniert.** Ein eingebetteter `<iframe>`, ein
Link, ein gespeicherter Wert brauchen kein `fetch()`. Baue sie ein, *bevor* du
den Status holst, nicht danach. Sonst reißt ein fehlender Server die halbe
Seite mit, die auch ohne ihn nützlich wäre.

```javascript
mount(name);        // läuft immer
fetchStatus(name);  // darf scheitern, ohne den Rest zu beschädigen
```

**Fehler erklären, nicht nur melden.** „Failed to fetch" hilft niemandem. Sag,
was fehlt und was zu tun ist:

> Unter `http://127.0.0.1:8765` antwortet nichts. Ohne laufenden Monitor gibt es
> keinen Status und keine Meldung. Starten: Doppelklick auf `Start.cmd`.

### 4. Zustandswechsel erkennen und melden

Das ist der eigentliche Zweck. Der Kern ist unspektakulär, aber es gibt drei
Stellen, an denen es schiefgeht:

```python
neu = pruefen(ziel)
alt = zustand.get(ziel)

if alt is not None and neu != alt:        # ① nicht beim ersten Lauf melden
    melden("wechsel", ziel, neu)
if neu is not None:                        # ② unbekannt ≠ Wechsel
    zustand[ziel] = neu
    speichern(zustand)                     # ③ überlebt den Neustart
```

- ① Ohne die `alt is not None`-Prüfung meldet der erste Durchlauf nach jedem
  Start alles — der Nutzer schaltet die Meldungen nach zwei Tagen ab.
- ② Ein fehlgeschlagener Abruf ist **kein** Wechsel auf „offline". Halte
  `None` (unbekannt) von `False` (nachweislich offline) getrennt.
- ③ Ohne Speichern ist nach jedem Neustart wieder Zustand ①.

**Immer drei Wege gleichzeitig bedienen**, denn jeder einzelne fällt irgendwann aus:

| Weg | wofür | fällt aus wenn |
|---|---|---|
| Ereignisprotokoll (`data/events.json`) | Verlauf, Oberfläche, Nachschlagen | nie — das ist der Anker |
| System-/Browser-Meldung | der Nutzer bekommt es sofort mit | Meldungen sind abgeschaltet |
| Webhook (POST) | Weiterleitung nach Discord, Slack, Matrix | keine Adresse eingetragen |

Das Protokoll ist der Anker: Auch wenn keine Meldung durchkam, steht der Wechsel
mit Zeitstempel in der Datei, und die Oberfläche kann ihn zeigen.

### 5. Der Starter

Ein Nutzer, der eine Kommandozeile öffnen muss, benutzt das Werkzeug nicht.
`scripts/starter/` enthält eine fertige Vorlage; sechs Dinge machen den
Unterschied zwischen „geht" und „geht nicht":

1. **Laufzeit suchen und beim Fehlen helfen** — `py -3`, dann `python`. Fehlt
   sie, nenne den Downloadlink *und* den Haken „Add python.exe to PATH". Ohne
   diesen Haken scheitert die Installation still.
2. **Nicht doppelt starten** — erst den Port anfragen. Antwortet er, nur das
   Fenster öffnen.
3. **Auf den Port warten, nicht auf die Uhr** — `sleep 3` ist geraten. Frage in
   einer Schleife bis zu 20 Sekunden lang `/api/status` an und mache erst weiter,
   wenn wirklich geantwortet wird.
4. **Unsichtbar starten, Ausgabe in eine Datei** — kein Konsolenfenster, das
   herumsteht. Prozessnummer nach `data/companion.pid`, Ausgabe nach
   `data/companion.log`.
5. **Beim Scheitern die letzten Protokollzeilen zeigen** und auf eine
   Fehlersuch-Variante mit sichtbarem Fenster verweisen. Ein Fenster, das
   aufgeht und sofort wieder zu ist, ist die schlimmste aller Rückmeldungen.
6. **Als eigenes Fenster öffnen** — `msedge --app=<url>` bzw.
   `chrome --app=<url>`. Ohne Adressleiste wirkt es wie ein Programm, nicht wie
   eine Webseite.

Lege drei Dateien nebeneinander: **Start**, **beenden**, **Fehlersuche**.

### 6. Dauerbetrieb: Container statt Starter

Der Starter löst „einfach zu bedienen", nicht „läuft weiter, wenn niemand
hinsieht". Sobald jemand „soll immer laufen", „auch nach Neustart" oder „im
Hintergrund" sagt, gehört der Companion in einen Container.

```yaml
ports:    ["127.0.0.1:8765:8765"]   # nicht "8765:8765" — sonst im ganzen Netz offen
volumes:  ["companion-data:/app/data"]
restart:  unless-stopped
```

Drei Dinge, die dabei regelmäßig schiefgehen:

- **`--host 0.0.0.0` im Container.** Bindet der Dienst an `127.0.0.1`, meint er
  das Loopback *des Containers* und ist von außen nicht erreichbar — auch nicht
  über die Portweiterleitung. Nach außen dicht macht die linke Seite der
  Portangabe, nicht die Bindung im Programm.
- **Keine Systemmeldung mehr.** Ein Linux-Container kann keine Windows- oder
  macOS-Meldung erzeugen; ein `notify.command` scheitert dort still. Es bleiben
  Ereignisprotokoll, Webhook und die Meldung der geöffneten App. Trage den
  Systembefehl dann gar nicht erst ein.
- **`restart` reicht nicht.** Es greift nur, wenn der Docker-Dienst selbst
  startet. Bei Docker Desktop ist das ein Haken in den Einstellungen — ohne ihn
  läuft nach dem Neustart nichts, und niemand weiß warum.

Einzelheiten, compose-Datei und Prüfliste: `references/docker.md`.

### 7. Als App installierbar machen (PWA)

`127.0.0.1` gilt als sichere Herkunft — die Installation funktioniert also ohne
Zertifikat. Damit der Browser sie anbietet, müssen fünf Dinge stimmen; an zwei
davon scheitert es fast immer:

```bash
python scripts/pwa_kit.py web/ --name "Mein Companion" --theme "#2481cc"
```

Das Skript erzeugt Manifest, Service Worker und Symbole (192, 512, maskierbar)
und trägt die Verweise in `index.html` ein. Was es sonst zu beachten gibt:

- **MIME-Typen** — hier scheitert es am häufigsten, und der Browser sagt nicht,
  warum. Ein Manifest wird nur als `application/manifest+json` akzeptiert, ein
  Service Worker nur als `text/javascript`. Ein Server, der alles als
  `text/plain` ausliefert, verhindert die Installation lautlos.
- **Zwischenspeicher-Regel** — die Hülle darf gecacht werden, `/api/…` **nie**.
  Ein zwischengespeicherter Livestatus ist schlimmer als gar keiner: Er sieht
  richtig aus und ist falsch.
- **Eigener Installationsknopf** — Browser blenden ihren eigenen erst spät und
  versteckt ein. Auf `beforeinstallprompt` hören und einen sichtbaren Knopf
  anbieten.

Einzelheiten und Prüfliste: `references/pwa.md`.

### 8. Erweiterung (optional, aber der einzige Weg zu „ohne offenen Tab")

Eine PWA meldet nur, solange sie läuft. Eine Erweiterung mit `chrome.alarms`
prüft auch bei geschlossenem Browserfenster weiter und braucht dank
`host_permissions` **keinen laufenden Server**.

Baue sie als *ladefertigen Ordner* mit `manifest.json` an der Wurzel — nicht als
Beschreibung, wie man einen bauen könnte. „Ordner in `chrome://extensions`
laden" ist nur dann eine Anleitung, wenn der Ordner existiert.

Aufbau, Berechtigungen und die CSP-Zeile für eingebettete Rahmen:
`references/erweiterung.md`.

## Keine Beispieldaten festverdrahten

Beim Entwickeln braucht man ein konkretes Beispiel — ein Konto, eine URL, eine
Kennung. Es darf nur nicht im Ergebnis landen. Ein Werkzeug mit dem Testkonto
des Entwicklers im Code ist für den Nutzer wertlos und wirkt unfertig.

- Überall ein **Eingabefeld**; gespeichert wird nur, was der Nutzer eingetippt hat.
- In Beispielen, Vorlagen, README und Kommentaren steht ein neutraler
  Platzhalter (`creator`, `beispiel`, `<name>`).
- Eingaben großzügig annehmen: `name`, `@name` und die volle URL sollen alle gehen.

Vor der Übergabe prüfen — das ist schnell und fängt genau den Fehler, den man
selbst übersieht:

```bash
python scripts/check_no_hardcode.py . --forbid <testname>
```

## Abnahme

Diese Liste ist aus echten Fehlschlägen entstanden. Jeder Punkt stand schon
einmal für „beim Entwickler ging es".

- [ ] Server startet mit Bordmitteln, ohne Installation von Paketen
- [ ] Jede Antwort trägt die CORS-Kopfzeilen, `OPTIONS` wird beantwortet
- [ ] Oberfläche gegen die **gemessenen** Antwortstrukturen geschrieben
- [ ] Ohne Server zeigt die Oberfläche trotzdem, was ohne Abruf geht
- [ ] Fehlermeldung nennt Ursache **und** nächsten Schritt
- [ ] Erster Durchlauf nach dem Start meldet nichts
- [ ] Fehlgeschlagener Abruf wird nicht als „offline" gewertet
- [ ] Zustand überlebt den Neustart
- [ ] Wechsel steht im Ereignisprotokoll, auch wenn keine Meldung ankam
- [ ] Starter findet die Laufzeit oder erklärt genau, was fehlt
- [ ] Starter wartet auf den Port, nicht auf die Uhr
- [ ] Zweiter Doppelklick startet nichts doppelt
- [ ] Manifest kommt als `application/manifest+json`, `sw.js` als `text/javascript`
- [ ] `/api/` wird nicht zwischengespeichert
- [ ] Im Container: `--host 0.0.0.0`, Port nur an `127.0.0.1` veröffentlicht
- [ ] Im Container: Verlauf im benannten Volume, `TZ` gesetzt, kein Systembefehl
- [ ] Erweiterung ist ein ladefertiger Ordner mit `manifest.json` an der Wurzel
- [ ] Kein Testname im Ergebnis (`check_no_hardcode.py` ist grün)

## Grenzen

Beobachte nur, was öffentlich abrufbar ist. Anmeldeschranken, Zugriffssperren
und Wartezeiten sind Zugangskontrollen — sie zu umgehen ist nicht Teil dieses
Musters, auch nicht mit guter Begründung. Wo es offizielle Einbettungen oder
Schnittstellen gibt, nimm die: Sie sind stabiler und bleiben erlaubt.

Halte den Turnus höflich. Sekundentakt bringt selten mehr Information und
handelt eine Sperre ein; ein bis fünf Minuten reichen fast immer.

## Werkzeuge in diesem Skill

| Datei | Zweck |
|---|---|
| `scripts/probe_api.py` | Endpunkte abfragen und die echte JSON-Struktur drucken |
| `scripts/pwa_kit.py` | Manifest, Service Worker, Symbole erzeugen und HTML verknüpfen |
| `scripts/check_no_hardcode.py` | Ergebnis nach Testnamen und Beispieldaten durchsuchen |
| `scripts/starter/` | Starter-Vorlage (Windows `.ps1` + `.cmd`, macOS/Linux `.sh`) |
| `references/docker.md` | Dauerbetrieb im Container, Volumes, Fallen bei der Einhängung |
| `references/pwa.md` | Installierbarkeit, MIME-Typen, Zwischenspeicher-Regeln |
| `references/starter.md` | Starter je Betriebssystem, Fehlerbilder |
| `references/erweiterung.md` | Manifest V3, Berechtigungen, Meldungen, CSP |
| `references/fallstricke.md` | Die Fehler, die dieses Muster geformt haben |
