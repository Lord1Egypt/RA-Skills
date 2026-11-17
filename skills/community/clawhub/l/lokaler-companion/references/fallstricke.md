# Fallstricke

Die Fehler, aus denen dieses Muster entstanden ist. Jeder hat einmal echte
Arbeit gekostet, und die meisten sehen beim Entwickeln nicht so aus wie beim
Nutzer.

## Inhalt

1. [Die Herkunft `null`](#1-die-herkunft-null)
2. [CORS am eigenen Server](#2-cors-am-eigenen-server)
3. [Geratene Feldnamen](#3-geratene-feldnamen)
4. [Alles an einen Abruf hängen](#4-alles-an-einen-abruf-hängen)
5. [Der Beispielname im Ergebnis](#5-der-beispielname-im-ergebnis)
6. [Unbekannt ist nicht offline](#6-unbekannt-ist-nicht-offline)
7. [Der erste Durchlauf meldet alles](#7-der-erste-durchlauf-meldet-alles)
8. [Auf die Uhr warten statt auf den Port](#8-auf-die-uhr-warten-statt-auf-den-port)
9. [Eine Anleitung statt eines Ordners](#9-eine-anleitung-statt-eines-ordners)
10. [Stille MIME-Ablehnung](#10-stille-mime-ablehnung)
11. [Zwischengespeicherter Livestatus](#11-zwischengespeicherter-livestatus)
12. [Dateitypen, die sich nicht öffnen lassen](#12-dateitypen-die-sich-nicht-öffnen-lassen)

---

## 1. Die Herkunft `null`

**Bild:** Die HTML-Datei geht auf, sieht richtig aus, bleibt aber leer.
In der Konsole steht `TypeError: Failed to fetch`.

**Ursache:** Über `file://` geöffnete Seiten haben die Herkunft `null`. Sie
dürfen ein fremdes Ziel nur abrufen, wenn dieses `Access-Control-Allow-Origin: *`
mitschickt. Öffentliche Browser-Schnittstellen tun das häufig, gewöhnliche
Webseiten praktisch nie — und nachrüsten kann man es an fremden Servern nicht.

**Nicht raten, nachsehen:**

```bash
curl -sI "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=eur"
#   access-control-allow-origin: *        → aus einer losen Datei erreichbar

curl -sI "https://t.me/s/telegram"
#   (keine solche Zeile)                  → nicht erreichbar
```

**Warum es einem selbst nicht auffällt:** Beim Entwickeln liegt die Datei unter
`http://localhost/…`, weil dort ohnehin ein Server läuft. Erst beim Nutzer, der
doppelklickt, kippt es.

**Lösung:** Sind alle Quellen freigegeben, ist die lose Datei die freundlichste
Antwort — kein Server, kein Starter, nichts zu installieren. Sonst holt der
lokale Server die Daten (serverseitig gibt es kein CORS) und reicht sie unter
derselben Herkunft weiter. Eine Erweiterung mit `host_permissions` ist der
dritte Weg.

Und unabhängig davon: Was ohne Abruf geht, sollte auch ohne Abruf laufen —
siehe [4](#4-alles-an-einen-abruf-hängen).

## 2. CORS am eigenen Server

**Bild:** Der Server läuft, die eingebaute Oberfläche funktioniert — aber die
installierte App oder die Erweiterung bekommt nichts.

**Ursache:** Sobald die Seite von einer anderen Herkunft kommt, ist es für den
Browser ein fremder Abruf.

```python
self.send_header("Access-Control-Allow-Origin", "*")
self.send_header("Access-Control-Allow-Headers", "Content-Type")
self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")

def do_OPTIONS(self):
    self._send(204, b"", "text/plain")
```

Das `do_OPTIONS` wird gern vergessen: Bei POST mit `Content-Type: application/json`
schickt der Browser erst eine Vorabanfrage. Ohne Antwort darauf gibt es die
eigentliche Anfrage nie.

## 3. Geratene Feldnamen

**Bild:** Die Oberfläche steht, zeigt aber überall `undefined` oder leere Karten.

**Ursache:** Der Client wurde gegen die vermutete Struktur geschrieben. Die
tatsächliche heißt anders — `entries` statt `channels`, `target` statt
`username`, `at` statt `timestamp`.

**Lösung:** Erst messen. `scripts/probe_api.py` druckt Feldnamen mit echten
Werten. Das kostet eine Minute und spart eine Stunde Suche.

## 4. Alles an einen Abruf hängen

**Bild:** Der Server fehlt, und die ganze Seite ist tot — obwohl der eingebettete
Player, die Links und die zuletzt eingegebenen Werte auch ohne ihn gingen.

**Ursache:** Der Aufbau war `Status holen → dann anzeigen`. Scheitert Schritt
eins, passiert nichts mehr.

**Lösung:** Umdrehen. Erst alles einbauen, was keinen Abruf braucht, danach den
Status nachladen und nur diesen Teil als „unbekannt" kennzeichnen.

```javascript
mount(name);        // läuft immer
fetchStatus(name);  // darf scheitern
```

## 5. Der Beispielname im Ergebnis

**Bild:** Der Nutzer öffnet das Werkzeug und sieht das Testkonto des
Entwicklers. Kein Eingabefeld. Das Ding ist für ihn wertlos.

**Ursache:** Zum Entwickeln braucht man ein konkretes Beispiel. Nach dem
fünfzigsten Mal liest man es nicht mehr.

**Lösung:** Eingabefeld überall; in Text, Beispielen und Kommentaren ein
neutraler Platzhalter. Vor der Übergabe prüfen:

```bash
python scripts/check_no_hardcode.py . --forbid <testname> --keep data/
```

## 6. Unbekannt ist nicht offline

**Bild:** Nachts kommt eine „ist offline"-Meldung, obwohl nichts passiert ist.
Morgens „ist wieder da".

**Ursache:** Ein Abruf lief in eine Zeitüberschreitung, und das Ergebnis wurde
als „offline" gewertet.

**Lösung:** Drei Zustände sauber trennen — `True` (nachweislich an),
`False` (nachweislich aus), `None` (kein Ergebnis). Nur Wechsel zwischen
`True` und `False` sind Ereignisse. Zwei bis drei Fehlversuche in Folge, bevor
aus `None` ein `False` wird, glätten Netzhänger.

## 7. Der erste Durchlauf meldet alles

**Bild:** Nach jedem Neustart kommt eine Welle von Meldungen. Der Nutzer stellt
sie ab.

**Ursache:** Beim ersten Durchlauf ist der vorherige Zustand leer, also gilt
jeder Wert als Wechsel.

```python
if alt is not None and neu != alt:      # nicht: if neu != alt
    melden(...)
```

Und der Zustand muss auf die Platte, sonst ist nach jedem Neustart wieder
alles neu.

## 8. Auf die Uhr warten statt auf den Port

**Bild:** Der Starter öffnet den Browser, die Seite zeigt „nicht erreichbar".
Beim Neuladen geht es.

**Ursache:** `sleep 3` ist geraten. Auf einem langsamen Rechner braucht der
Start länger.

**Lösung:** In der Schleife fragen, bis geantwortet wird — bis zu 20 Sekunden,
alle 500 ms. Zusätzlich abbrechen, wenn der Prozess vorzeitig endet, sonst
wartet der Nutzer die vollen 20 Sekunden auf etwas Totes.

## 9. Eine Anleitung statt eines Ordners

**Bild:** „Als Browser-Erweiterung lässt sich keins der Verzeichnisse nutzen."

**Ursache:** Es lag eine `README.md` da, die beschreibt, wie man eine
Erweiterung baut — aber kein Ordner mit `manifest.json`. Chrome erkennt eine
Erweiterung ausschließlich an dieser Datei an der Wurzel.

**Lösung:** Den Ordner wirklich anlegen, mit allen Dateien und Symbolen, und
den vollständigen Pfad nennen, der auszuwählen ist.

## 10. Stille MIME-Ablehnung

**Bild:** Alle PWA-Bedingungen scheinen erfüllt, der Browser bietet die
Installation trotzdem nicht an. Keine Fehlermeldung.

**Ursache:** Der Server liefert `manifest.webmanifest` und `sw.js` als
`text/plain` aus — der übliche Standardwert einfacher Server.

```python
".webmanifest": "application/manifest+json; charset=utf-8"
".js":          "text/javascript; charset=utf-8"
```

Nachsehen unter *Entwicklerwerkzeuge → Application → Manifest*; dort steht,
was fehlt.

## 11. Zwischengespeicherter Livestatus

**Bild:** Die App zeigt „läuft gerade", obwohl längst Schluss ist.

**Ursache:** Der Service Worker hat auch `/api/…` in den Zwischenspeicher
gelegt. Ein falscher Status, der richtig aussieht, ist schlimmer als gar keiner.

**Lösung:** Im `fetch`-Ereignis früh aussteigen:

```javascript
if (url.pathname.startsWith('/api/')) return;   // immer frisch
```

## 12. Dateitypen, die sich nicht öffnen lassen

**Bild:** Mehrere Ergebnisdateien werden übergeben, nur eine lässt sich öffnen.

**Ursache:** Je nach Umgebung wird für manche Dateitypen ein Programm
aufgerufen, das nicht da ist oder nicht startet. HTML dagegen geht fast immer,
weil ein Browser vorhanden ist.

**Lösung:** Wenn etwas ankommen *muss*, als HTML ausliefern — notfalls als eine
Seite mit eingebetteten Dateien und Herunterladen-Knöpfen. Und bei Beschwerden
zuerst fragen, welche Datei sich öffnen ließ: Der Unterschied zeigt sofort, ob
Dateien fehlen oder der Aufruf klemmt.
