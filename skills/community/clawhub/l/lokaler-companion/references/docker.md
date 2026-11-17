# Dauerbetrieb im Container

Der Starter löst „einfach zu bedienen". Er löst nicht „läuft weiter, wenn
niemand hinsieht": Nach einem Neustart, einem Absturz oder einem versehentlich
geschlossenen Fenster ist der Companion weg — und ein Beobachter, der Lücken
hat, ist genau in dem Moment blind, auf den man gewartet hat.

Ein Container schließt diese Lücke. Es lohnt sich, sobald jemand sagt „soll
immer laufen", „auch nach Neustart", „im Hintergrund", „auf dem Server".

## Das Grundgerüst

```dockerfile
FROM python:3.12-slim
ENV TZ=Europe/Berlin PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt      # eigene Schicht: bleibt im Cache
COPY tgmon/ ./tgmon/
COPY web/ ./web/
COPY server.py ./
RUN mkdir -p /app/data

RUN useradd --uid 10001 --create-home --shell /usr/sbin/nologin app \
 && chown -R app:app /app
USER app

EXPOSE 8765
CMD ["python", "server.py", "--host", "0.0.0.0", "--port", "8765", "--no-browser"]
```

**`--host 0.0.0.0` ist Pflicht.** Bindet der Dienst im Container an
`127.0.0.1`, meint er *das Container-eigene* Loopback. Von außen ist er dann
nicht erreichbar — auch nicht über die veröffentlichte Portweiterleitung. Das
ist der Fehler, der am meisten Zeit kostet, weil alles richtig aussieht.

`TZ` nicht vergessen: Sonst stehen im Ereignisprotokoll UTC-Zeiten, die nicht
zu dem passen, was der Nutzer auf seiner Uhr sieht.

## compose

```yaml
services:
  monitor:
    build: .
    container_name: companion
    ports:
      - "127.0.0.1:8765:8765"      # siehe unten — die linke Seite ist wichtig
    volumes:
      - companion-data:/app/data
      - ./config.json:/app/config.json:ro
    environment: { TZ: Europe/Berlin }
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "python", "-c",
             "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8765/api/status', timeout=5).status==200 else 1)"]
      interval: 60s
      start_period: 20s
    security_opt: [ "no-new-privileges:true" ]
    logging:
      driver: json-file
      options: { max-size: "10m", max-file: "3" }

volumes:
  companion-data:
```

Vier Stellen, die zählen:

**`127.0.0.1:8765:8765`, nicht `8765:8765`.** Ohne den Präfix öffnet Docker den
Port auf allen Schnittstellen und trägt dabei eine eigene Regel in die Firewall
ein — der Dienst ist dann im ganzen Netz erreichbar, inklusive VPN. Ein
Beobachter ohne Anmeldung gehört nicht dorthin.

**Benanntes Volume statt Ordner-Einhängung** für `data/`. Der gesammelte
Verlauf überlebt damit jedes `--build`, und unter Windows und macOS ist es
deutlich schneller als eine eingehängte Ordnerfreigabe.

**`restart: unless-stopped`**, nicht `always`. Beides startet nach Neustart und
Absturz — aber `always` startet auch wieder, wenn der Nutzer den Container
absichtlich angehalten hat. Das fühlt sich wie ein Defekt an.

**Healthcheck mit Bordmitteln.** Schlanke Abbilder haben kein `curl`. Ein
Dreizeiler in Python funktioniert überall und braucht keine zusätzliche Schicht.

## Was im Container nicht mehr geht

Das ist der Teil, den man dem Nutzer sagen muss, statt ihn entdecken zu lassen:

| | |
|---|---|
| **Systemmeldung** | Ein Linux-Container kann keine Windows- oder macOS-Meldung erzeugen. Ein `notify.command` mit PowerShell scheitert dort still. |
| **Ersatz** | Ereignisprotokoll (läuft immer), Webhook (Discord, Slack, ntfy, Matrix), und die Meldung der installierten App, solange sie geöffnet ist. |
| **Browser öffnen** | `webbrowser.open()` hat im Container niemanden zum Öffnen. Immer mit `--no-browser` starten. |
| **Lokale Dateien** | Alles außerhalb des Volumes ist nach dem nächsten `--build` weg. |

Trage in die Konfiguration den Systembefehl deshalb gar nicht erst ein, wenn
im Container gestartet wird — ein Weg, der nur scheitern kann, verwirrt beim
Suchen nach der Ursache.

## Zwei Fallen bei der Einhängung

**Eine fehlende Datei wird zum Ordner.** Existiert `config.json` beim ersten
Start nicht, legt Docker beim Einhängen ein *Verzeichnis* mit diesem Namen an.
Danach startet der Container nicht mehr, und die Meldung
(`… is a directory`) klingt nach einem ganz anderen Problem. Der Starter sollte
die Datei vorher aus der Vorlage anlegen.

**Schreibrechte im Volume.** Läuft der Prozess als `app` (UID 10001), muss der
Ordner ihm gehören. Bei einem frischen Volume erbt Docker die Rechte des
Ordners aus dem Abbild — deshalb `mkdir` und `chown` in den Dockerfile, *vor*
dem `USER`-Wechsel.

## Startet es auch nach dem Neustart?

`restart: unless-stopped` greift nur, wenn der Docker-Dienst selbst läuft.

- **Docker Desktop (Windows, macOS)**: Settings → General →
  *Start Docker Desktop when you sign in*. Ohne diesen Haken startet nach der
  Anmeldung gar nichts, und `restart` bleibt wirkungslos.
- **Linux**: `sudo systemctl enable docker` — auf den meisten Systemen ohnehin
  eingeschaltet.

Das ist kein Detail, sondern der Unterschied zwischen „läuft dauerhaft" und
„lief bis zum letzten Neustart". In die Anleitung schreiben.

## Erreichbar von anderen Geräten

Nur, wenn der Nutzer danach fragt — und dann über ein VPN wie Tailscale, nicht
über eine offene Portfreigabe.

Wichtig dabei: **Eine rohe VPN-Adresse über HTTP ist keine sichere Herkunft.**
Unter `http://100.x.x.x:8765` gibt es keinen Service Worker, keine
Installation als App und keine Browser-Meldungen — dieselben Einschränkungen
wie bei `file://`. `tailscale serve --bg 8765` legt ein echtes Zertifikat davor
und liefert `https://<host>.<tailnet>.ts.net`; damit funktioniert die App auch
auf dem Telefon.

Eine öffentliche Freigabe (Funnel, Portweiterleitung) ist für einen Dienst ohne
Anmeldung die falsche Antwort. Wer von außen heranwill, gehört ins VPN.

## Prüfliste

- [ ] `--host 0.0.0.0` im Container, `--no-browser` gesetzt
- [ ] Port bindet an `127.0.0.1:`, nicht an alle Schnittstellen
- [ ] `data/` liegt in einem benannten Volume
- [ ] Eingehängte Konfigurationsdatei existiert vor dem ersten Start
- [ ] `TZ` gesetzt, Zeitstempel stimmen mit der Uhr des Nutzers überein
- [ ] `restart: unless-stopped` **und** der Docker-Dienst startet beim Anmelden
- [ ] Healthcheck ohne `curl`
- [ ] Systembefehl für Meldungen leer; Webhook dokumentiert
- [ ] Protokolle begrenzt (`max-size`), sonst füllt der Poller die Platte
