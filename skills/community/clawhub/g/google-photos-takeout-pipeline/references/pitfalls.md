# Pitfalls & Operational Playbook

Alles, was bei der Pipeline schiefgehen kann — komplett aus einer echten
867-GB-Migration (Aug 2026) dokumentiert.

## A. Auth & Cookies

1. **Cookie-Scope ist der häufigste Killer.** Filtern der Cookies auf
   `takeout.google.com` + `accounts.google.com` reicht NICHT. Die finale
   Download-Domain `takeout-download.usercontent.google.com` setzt eigene Cookies.
   Nur `Storage.getCookies` (Browser-Target, ALLE Cookies) liefert ein jar, mit dem
   curl/aria2 ZIPs bekommt. Symptom bei fehlenden Domain-Cookies: 302 → ServiceLogin,
   die Diagnose "TLS-Fingerprinting!" ist fast immer falsch.

2. **Session-Cookies rotieren** (`__Secure-1PSIDTS` etc., ~15–30 min). Ein statisches
   Jar liefert irgendwann mitten im Lauf 1,2 MB HTML-Login-Seiten statt 50-GB-ZIPs.
   Gegenmassnahme: Refresh vor JEDEM Teil, PK-Magic-Check nach JEDEM Teil, HTML
   loeschen und retryen. Ein Komplett-Lauf ueber Nacht ohne Refresh stirbt garantiert
   mittendrin.

3. **Origin-Endpoint-Falle.** `takeout.google.com/takeout/download?j=...&i=...`
   redirectet von CLI IMMER auf `accounts.google.com/v3/signin/challenge/pk` —
   unabhaengig von Cookies. Das ist eine interaktive Identitaetsbestaetigung, kein
   fixbarer Header-Bug. Immer die usercontent-URLs verwenden.

4. **Fraud-Detection-Eskalation (wichtig!).** Wiederholte automatisierte
   Login-Versuche fuehren dazu, dass Google den Account als uebernommen behandelt:
   Passwort-Reset-Mails, gesperrte Alternativ-Methoden, 6h-Verzoegerungen
   ("MARL"-Links). Diese Versuche zaehlen SESSIONS-UEBERGREIFEND. Harte Regel:
   Sobald eine Konto-Wiederherstellungs-Mail kommt → ALLE Login-Automatisierung
   dauerhaft beenden. Der Mensch loggt EINMAL manuell ein (echte Klicks sind
   trusted), danach macht der Agent nur noch Downloads mit frischen Cookies.
   Passwort-Reset via myaccount.google.com invalidiert alte Sessions sauber —
   nuetzlicher Reset vor dem manuellen Login.

5. **Takeout-Links laufen ab** (~7 Tage) und sind auf begrenzte Download-Anzahl
   limitiert. Zeitplan einkalkulieren.

## B. Chromium-Download-Kontrolle (falls Browser-Weg noetig)

- `Browser.cancelDownload` (CDP) und `chrome.send('cancel', [id])` wirken NICHT.
- Tab schliessen stoppt den Download NICHT (laeuft im Hintergrund weiter).
- Zuverlaessig: chrome://downloads-WebUI per Shadow-DOM:
  `downloads-manager` → `downloads-item` → ShadowRoot →
  `cr-icon-button.dropdown-trigger` klicken (oeffnet `cr-action-menu`) →
  Button mit exaktem Text 'Pause'/'Fortsetzen'/'Abbrechen' klicken.
  `i.data.state` ist NUMERISCH (0=laufend, 3=unterbrochen, 5=abgebrochen, 2=fertig).
- **Chromium wirft beim CANCEL die .crdownload-Bytes weg.** Erst umbenennen
  (z.B. `.part`), dann canceln — sonst sind 24 GB weg.
- Die finale URL steht in `it.data.url` des downloads-items — auch bei pausierten
  Downloads noch lesbar. Das ist der Weg zum URL-Muster.

## C. Download-Technik

- aria2c-Parameter (bewaehrt): `--continue=true --split=4
  --max-connection-per-server=4 --min-split-size=10M --max-tries=0 --retry-wait=15
  --timeout=60 --file-allocation=none --max-overall-download-limit=5M`.
- **Drosseln ohne Byteverlust:** `kill -STOP <pid>` (0 bytes/s, verifiziert) und
  `kill -CONT <pid>` (sofortiges Continue). Soft-Variante: Limiter-Flag.
- **`ls`-Groessen luegen:** aria2 schreibt mit 4 Verbindungen verteilt in eine
  vorallozierte Datei — `ls` zeigt fast sofort die Endgroesse. Fortschritt nur aus
  aria2s Summary-Zeilen oder dem `.aria2`-Kontrollfile lesen.
- **Crash-Resilienz:** `.aria2`-Kontrolldateien machen Resume exakt — ein
  Runner-Crash verliert keine Bytes, nur die Ueberwachung. Downloads laufen
  browser-intern (bzw. aria2-prozess-intern) weiter.

## D. SSD / macOS

- **Time Machine kann den Mount reissen.** backupd in einer Retry-Schleife mounted
  das Backup-Volume der GLEICHEN Platte und blockiert diskarbitrationd → alle
  diskutil-Aufrufe hängen, Zombie-Mountpoint (`d--x--x--x` root in /Volumes).
  Reihenfolge: `tmutil stopbackup` → Photos.app beenden + photolibraryd killen →
  physisches Ab-/Anstecken bleibt letzter Fix. Fuer Download-Naechte: TM pausieren
  (Watchdog-Loop, der stopbackup feuert, wenn TM wieder anlaeuft).
- **SSD-Budget:** ZIPs + entpackte Daten = 2x Bibliothek. Sofort-Entpacken mit
  Loeschung nach Verifikation haelt den Verbrauch bei ~1x.

## E. Nach der Migration

- Takeout-EXIF zeigt Upload-Datum, NICHT Aufnahmedatum — die JSON-Sidecars haben die
  echten Daten. gpth/gpto lesen sie und fixen File-Timestamps; danach exiftool:
  `exiftool -overwrite_original -r -if 'not defined DateTimeOriginal' -P
  "-AllDates<FileModifyDate" Archive/`.
- Album-Ordner duplizieren Fotos (Album + Jahresordner) — gpth/gpto dedupen das.
- Google-Bearbeitungen sind eingebrannt (Original+Edit als ein Bild oder als
  separate Datei je nach Export-Einstellung).
- Gesichtserkennung/Orte/Suche baut Apple Photos bei 100k+ Fotos tagelang neu auf —
  normal, nicht kaputt.

## F. Der offizielle Google→iCloud-Transfer (Zero-Bandwidth-Alternative)

`takeout.google.com/takeout/transfer/custom/photos` = Googles Data Portability:
Google Photos wird SERVERSEITIG nach Apple iCloud Photos kopiert (auch OneDrive,
Flickr, SmugMug). Keine lokale Bandbreite, keine ZIPs, landet im Album
"Import from Google". Voraussetzungen: genug iCloud-Speicher (867 GB → 2-TB-Plan),
Advanced Data Protection aus.

Flow (3 manuelle User-Schritte, Rest per CDP klickbar):
1. Schritt 1 "Weiter" → Google-OAuth-Kreis (Passkey! User bestaetigt; ohne
   jobId-Reset springt "Weiter" IMMER wieder in diesen Kreis — normal, nicht kaputt)
2. Schritt 2 "Apple – iCloud-Fotos" → "Weiter" → appleid.apple.com-Login (User)
3. Schritt 3 "Zustimmen und fortfahren" (klickbar) → takeout.google.com/manage
   zeigt "Export läuft…", Mail bei Abschluss. Verknuepfung wird danach automatisch
   geloescht.

Status lebt auf /manage, NICHT in den Tabs — Tabs schliessen schadet nicht.
Der Transfer ist der Komfort-Weg; der ZIP-Download parallel gibt das lokale Backup
mit voller Struktur (beides zusammen schliesst sich nicht aus).