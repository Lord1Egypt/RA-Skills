---
name: photo-webcam
description: List and snapshot retrieval for webcams (especially foto-webcam.eu). Use this skill when the user types “webcam <number>”, wants to manage a webcam favorites list, or needs a current snapshot JPG from a foto-webcam.eu webcam sent to chat.
---

# Photo-Webcam Snapshots

Goal: Fetch a current image from a saved favorites list (number -> webcam page) and send it to the user.

## Data source (favorites)

Default file in the workspace:
- `docs/webcams/favorites-muenchen.json`

Format:
- `items[].id` (int)
- `items[].name` (string)
- `items[].page` (URL of the webcam page)
- optional `items[].image` (direct image URL)

## Typical user commands

- webcam 1
- webcam 3+4+5
- liste
- liste webcams
- fuege <name> <url> hinzu

## Workflow: webcam N -> send image

1) Load favorites list from docs/webcams/favorites-muenchen.json.
2) Find entry with id equal to N.
3) Fetch snapshot:
   - If image is set: load that URL directly
   - Otherwise: derive current 1200 jpg from page URL
4) Save image to /tmp/webcamN.jpg
5) Send image via openclaw CLI:
   openclaw message send --channel telegram --target <CHAT_ID> --message “Webcam N Name” --media /tmp/webcamN.jpg

## Workflow: webcam 3+4+5 -> multiple images

Maximum 6 images per request; ask first if more are requested.

Run a separate openclaw call for each ID — never bundle multiple images into a single command or response.

Example for “webcam 1+3”:

  python3 ... --id 1 --out /tmp/webcam1.jpg
  -> read name from script output
  openclaw message send --channel telegram --target <CHAT_ID> --message “Webcam 1 <name>” --media /tmp/webcam1.jpg

  python3 ... --id 3 --out /tmp/webcam3.jpg
  -> read name from script output
  openclaw message send --channel telegram --target <CHAT_ID> --message “Webcam 3 <name>” --media /tmp/webcam3.jpg

Each openclaw command runs separately. The caption for each image comes exclusively from the script output (field “name”) of the respective call.

## Workflow: liste -> send favorites list

Send a plain text list:
Webcam 1 Name
Webcam 2 Name
etc.

No formatting, plain text only.

## Resolving the image URL (foto-webcam.eu)

For a webcam page like:
- `https://www.foto-webcam.eu/webcam/zugspitze/`

there is usually a direct “current” image at:
- `https://www.foto-webcam.eu/webcam/zugspitze/current/1200.jpg`

In practice: fetch the HTML with a browser User-Agent and search for a link matching `.../current/<digits>.jpg`.

## Script

Use the script:
- `skills/public/foto-webcam/scripts/foto_webcam_snapshot.py`

Examples:

- Snapshot via favorites ID:
  - `python3 skills/public/foto-webcam/scripts/foto_webcam_snapshot.py --favorites docs/webcams/favorites-muenchen.json --id 4 --out /tmp/webcam4.jpg`

- Snapshot via URL:
  - `python3 skills/public/foto-webcam/scripts/foto_webcam_snapshot.py --url https://www.foto-webcam.eu/webcam/zugspitze/ --out /tmp/zugspitze.jpg`

## Maintenance / adding webcams

- Add a new webcam: append to `favorites-muenchen.json` (new `id`, `name`, `page`).
- If a source is unreliable, set `image` to a direct JPG link.

Important: chat responses must be plain text only (no Markdown). For audio, use clean speech only (no special characters or formatting).

---

> Eine deutsche Version dieser Skill-Beschreibung ist weiter unten zu finden.

---

# Foto-Webcam Schnappschüsse (Deutsch)

Ziel: Ein aktuelles Bild aus einer gespeicherten Favoritenliste (Nummer → Webcam-Seite) abrufen und an den Benutzer senden.

## Datenquelle (Favoriten)

Standarddatei im Workspace:
- `docs/webcams/favorites-muenchen.json`

Format:
- `items[].id` (int)
- `items[].name` (string)
- `items[].page` (URL der Webcam-Seite)
- optional `items[].image` (direkte Bild-URL)

## Typische Benutzerbefehle

- webcam 1
- webcam 3+4+5
- liste
- liste webcams
- fuege <name> <url> hinzu

## Ablauf: webcam N -> Bild senden

1) Favoritenliste aus docs/webcams/favorites-muenchen.json laden.
2) Eintrag mit der entsprechenden ID finden.
3) Schnappschuss abrufen:
   - Falls `image` gesetzt ist: diese URL direkt laden
   - Andernfalls: aktuelles 1200-JPG aus der Seiten-URL ableiten
4) Bild unter /tmp/webcamN.jpg speichern
5) Bild per openclaw CLI senden:
   openclaw message send --channel telegram --target <CHAT_ID> --message "Webcam N Name" --media /tmp/webcamN.jpg

## Ablauf: webcam 3+4+5 -> mehrere Bilder

Maximal 6 Bilder pro Anfrage; bei mehr zuerst nachfragen.

Für jede ID einen separaten openclaw-Aufruf ausführen — niemals mehrere Bilder in einem einzigen Befehl oder einer Antwort bündeln.

Beispiel für „webcam 1+3":

  python3 ... --id 1 --out /tmp/webcam1.jpg
  -> Name aus Script-Ausgabe lesen
  openclaw message send --channel telegram --target <CHAT_ID> --message "Webcam 1 <name>" --media /tmp/webcam1.jpg

  python3 ... --id 3 --out /tmp/webcam3.jpg
  -> Name aus Script-Ausgabe lesen
  openclaw message send --channel telegram --target <CHAT_ID> --message "Webcam 3 <name>" --media /tmp/webcam3.jpg

Jeder openclaw-Befehl läuft separat. Die Bildunterschrift kommt ausschließlich aus der Script-Ausgabe (Feld „name") des jeweiligen Aufrufs.

## Ablauf: liste -> Favoritenliste senden

Einfache Textliste senden:
Webcam 1 Name
Webcam 2 Name
usw.

Keine Formatierung, nur reiner Text.

## Bild-URL auflösen (foto-webcam.eu)

Für eine Webcam-Seite wie:
- `https://www.foto-webcam.eu/webcam/zugspitze/`

gibt es normalerweise ein aktuelles Bild unter:
- `https://www.foto-webcam.eu/webcam/zugspitze/current/1200.jpg`

In der Praxis: HTML mit Browser-User-Agent abrufen und nach einem Link suchen, der auf `.../current/<Ziffern>.jpg` passt.

## Script

Das Script verwenden:
- `skills/public/foto-webcam/scripts/foto_webcam_snapshot.py`

Beispiele:

- Schnappschuss per Favoriten-ID:
  - `python3 skills/public/foto-webcam/scripts/foto_webcam_snapshot.py --favorites docs/webcams/favorites-muenchen.json --id 4 --out /tmp/webcam4.jpg`

- Schnappschuss per URL:
  - `python3 skills/public/foto-webcam/scripts/foto_webcam_snapshot.py --url https://www.foto-webcam.eu/webcam/zugspitze/ --out /tmp/zugspitze.jpg`

## Pflege / Webcams hinzufügen

- Neue Webcam hinzufügen: Eintrag in `favorites-muenchen.json` ergänzen (neue `id`, `name`, `page`).
- Bei unzuverlässiger Quelle: `image` auf eine direkte JPG-URL setzen.

Wichtig: Chat-Antworten nur als reiner Text (kein Markdown). Für Sprachausgabe: sauberer Text ohne Sonderzeichen oder Formatierung.
