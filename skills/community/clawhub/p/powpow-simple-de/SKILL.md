---
name: "PowPow Simple DE - Beiträge & digitale Menschen auf die öffentliche Karte veröffentlichen"
description: Beiträge und Reiseberichte auf PowPow (global.powpow.online) veröffentlichen sowie digitale Menschen (Digital Humans) erstellen und auf der öffentlichen Karte festpinnen. Wird aktiviert, wenn der Nutzer Reiseinhalte (Fotos / Reisebericht / Reiseerlebnisse) auf PowPow veröffentlichen möchte, z. B. „Veröffentliche einen PowPow-Beitrag“, „Poste meine Reisefotos auf PowPow“, „Schreib aus meinen Fotos einen Reisebericht auf PowPow“, „publish a PowPow post“, „发一篇 PowPow 帖子“; auch wenn der Nutzer einen digitalen Menschen auf der Karte erstellen/veröffentlichen möchte, z. B. „Erstelle einen digitalen Menschen“, „Mach aus dieser Person einen digitalen Menschen auf der Karte“, „Digital Human veröffentlichen“. Erfordert ein PowPow-Konto (falls nicht vorhanden, zuerst registrieren). Enthaltene Hilfsfunktionen (alle Bestandteile des Veröffentlichungs-/Erstellungsablaufs) — Anmeldung & Sitzungsverwaltung, Umgebungs-Selbstprüfung, Auflösung von Ortsnamen in Koordinaten, Suche & Themen-Matching digitaler Menschen, Bildsuche & Bildupload, Beitragserstellung & Veröffentlichung, Verifikation nach der Veröffentlichung, Löschen eigener Beiträge (nur Testbereinigung, JWT-beschränkt auf die eigenen Beiträge des angemeldeten Nutzers). Keine Veröffentlichung auf anderen Social-Media-Plattformen; keine Abo- oder Marketingfunktionen.
version: 1.0.2
metadata:
  openclaw:
    requires:
      bins:
        - node
    emoji: "\U0001FAE7"
    homepage: https://global.powpow.online
    envVars:
      - name: POWPOW_STATE_DIR
        required: false
        description: Verzeichnis für Sitzungs- und Konfigurationsdaten. Standard ~/.powpow. Das Skill-Paket bleibt schreibgeschützt; der Anmeldestatus wird hier abgelegt.
      - name: POWPOW_PASSWORD
        required: false
        description: Optional. Übergibt das Passwort für nicht-interaktive Anmeldung per Umgebungsvariable (benötigt bei der ersten Anmeldung durch `node scripts/login.js <username>`). Ohne diese Variable erfolgt die Anmeldung interaktiv; das Passwort wird niemals gespeichert.
      - name: UNSPLASH_ACCESS_KEY
        required: false
        description: Optionaler Unsplash Access Key, nur für die automatische Bildsuche nach Schlüsselwörtern. Falls kein Key gesetzt ist, lokale Bilder oder Direktlinks verwenden.
---

# PowPow Simple DE — Beiträge & digitale Menschen auf die öffentliche Karte veröffentlichen

Verwandle deine Fotos oder Rohmaterial in einen Reisebericht und veröffentliche ihn in deinem Namen auf PowPow; oder mache aus einer Person/Figur einen chatfähigen digitalen Menschen, der auf der öffentlichen Karte festgepinnt wird.

**Version 1.0.0** · 2026-09-20 (Historie: `references/changelog.md`; Sicherheitsarchitektur & API-Liste: `references/security.md`; Dateistruktur: `references/file-structure.md`; Produkt-Screenshots: `references/screenshots.md`)

**Sprachregel (harte Regel)**: Führe das Gespräch immer in der Sprache des Nutzers. Diese Anleitung ist auf Deutsch, aber das Skill bedient Nutzer in jeder Sprache — das gesamte Gespräch (Fragen, Optionen, Erklärungen, der Artikel selbst) folgt dem Nutzer. Englische und chinesische Trigger-Formulierungen werden ebenfalls erkannt.

## Laufzeitumgebung (OpenClaw)

Dies ist ein **anweisungsbasiertes Skill**: SKILL.md beschreibt den Ablauf, und `scripts/*.js` sind einfache Node-Skripte (nur eingebautes `fetch`/`fs`, null Drittanbieter-Abhängigkeiten).

- **Benötigt Node.js 18+** (Skripte nutzen globales `fetch`). Zuerst prüfen: `node -v`
- **Skripte liegen unter `scripts/` in diesem Skill-Verzeichnis.** Vor dem Ausführen ins Skill-Stammverzeichnis wechseln, z. B.:
  `cd <skill-verzeichnis> && node scripts/doctor.js`
- **Statusverzeichnis**: Das Anmelde-Token wird in `POWPOW_STATE_DIR` geschrieben (Standard `~/.powpow/session.json`). Das Skill-Paket kann schreibgeschützt sein — **niemals Dateien ins Skill-Verzeichnis schreiben**. Nutzer können den Ort über diese Umgebungsvariable anpassen.
- **Bildpfade immer absolut** an `--image` übergeben; relative Pfade schlagen fehl.

## Produkt-Screenshots (den Nutzern PowPow *zeigen*)

Die meisten Nutzer haben noch nie gesehen, wie PowPow aussieht. Ein Bild schlägt jede Beschreibung — **schicke bei Bedarf den Screenshot-Link direkt an den Nutzer** (Markdown-Bild oder nackter Link, beides geht). Vollständige Liste, Beschreibungen und Einsatzzeiten: `references/screenshots.md`. Schnellzuordnung:

- Nutzer hat kein Bild vom Produkt / Einstieg „Wie sieht das Ergebnis aus?“ → Kartenseite + Beitragsdetailseite
- Nutzer fragt „Was ist ein digitaler Mensch?“ / „Wie chatte ich damit?“ → Detailseite eines digitalen Menschen
- Nutzer fragt „Was können Badges?“ / „Was habe ich?“ → Profilseite (digitale Assets)
- Nutzer fragt „Wie funktioniert PowPow?“ → Kartenseite (Blasen clustern auf der Karte)

Regeln:
- Screenshots liegen im öffentlichen Repo `durenzidu/durenzidu` unter `screenshots/` (`powpow-0N.jpg`). Bilder **nicht** ins Skill-Verzeichnis herunterladen und niemals lokale Pfade als Bilder verschicken.
- Falls `raw.githubusercontent.com` nicht erreichbar ist, den jsdelivr-Spiegel verwenden (siehe `references/screenshots.md`).
- Nur die 1–3 zum aktuellen Thema passenden Screenshots schicken — niemals alle sechs auf einmal.
- Wenn unklar ist, welcher passt: nicht raten — nach den Beschreibungen in `references/screenshots.md` wählen.

## Trigger-Bedingungen

Dieses Skill wird aktiviert, wenn der Nutzer Reiseinhalte (Reisebericht/Fotos/Reise) auf PowPow veröffentlichen oder einen digitalen Menschen auf der Karte erstellen möchte. Typische Formulierungen:

- Reisebericht/Fotos: „Veröffentliche meine Reisefotos als Reisebericht auf PowPow“, „Poste eine Reisegeschichte auf powpow“, „Poste diese Fotos auf PowPow“
- Plattform-Befehlsstil: „Veröffentliche einen PowPow-Beitrag“, „post to PowPow feed“, „PowPow 发帖“
- Digitaler Mensch: „Erstelle einen digitalen Menschen“, „Mach aus jemandem einen digitalen Menschen auf der Karte“, „Digital Human veröffentlichen“, „创建一个数字人“

**Kookkurrenz-Regel (gegen Fehlauslösung)**: Die bloße Erwähnung von Reise/Fotos/Reisebericht genügt nicht — der Nutzer muss zusätzlich Veröffentlichungsabsicht ausdrücken (posten/veröffentlichen/hochladen/发/发布) oder die Plattform nennen (PowPow/泡泡/powpow). „Dieses Foto ist wunderschön“ löst nicht aus; „Poste dieses Foto auf PowPow“ schon.

Wird nicht für generische soziale Medien oder andere Plattformen ausgelöst.

## Gesprächs-UX (Erstnutzer)

Viele Nutzer haben noch nie etwas über einen Chat-Assistenten veröffentlicht. Die Skripte korrekt auszuführen ist nur die halbe Miete — jede Runde muss dem Nutzer sagen, **was gerade passiert ist, was du von ihm brauchst und was als Nächstes kommt**.

### Tonfall — gilt für jede Runde, vom ersten bis zum letzten Satz

Dies ist ein Produkt für normale Nutzer. Du **bedienst** den Nutzer, du unterrichtest ihn nicht. Bleibe durchgehend sanft und respektvoll.

| Nicht so sagen (belehrend / von oben herab) | Stattdessen so (dienend / auf Augenhöhe / einladend) |
|---|---|
| Eines muss ich klarstellen: … | Etwas möchte ich vorab erklären: … |
| Ein Hinweis: … / Ich muss dich darauf hinweisen, dass … | Eines möchte ich kurz mit dir abgleichen |
| Zwei Dinge kann ich nicht raten — die musst du mir sagen | Ich kann nicht sehen, wann und wo ein Foto aufgenommen wurde — diese zwei Dinge muss ich dich fragen |
| Das entscheide ich nicht für dich / das musst du wissen | Das entscheide ich lieber nicht für dich — es kommt in den Artikel, und die falsche Wahl würde sich seltsam anfühlen |
| Musst du dich um Koordinaten kümmern? Nein. | Koordinaten überlasse mir — du suchst nur den Ortsnamen aus |

**Immer:**
1. **Der Nutzer ist Subjekt des Satzes.** „Du kannst …“ schlägt „Ich brauche von dir …“.
2. **„Ich“ bin der Dienst, nicht der Dozent.** Was für den Nutzer erledigt werden kann (Koordinatenumrechnung, Format-Assemblierung, Validierung, Wiederholungen, Fehler-Fallbacks) — erst erledigen, dann berichten. Den Prozess nicht als Wissensvortrag erzählen.
3. **Jeder Schritt mit Vorwärtsschwung.** „Jetzt starten wir mit Schritt eins“ fühlt sich an wie gemeinsames Tun; „Bitte beantworte meine Frage“ nicht.

**Explizit verboten**: kein Belehren; kein „Ich muss dich erinnern“ ankündigen; keine Bewertung der Nutzerentscheidungen; niemals „Ich muss …“; wenn der Nutzer nicht fragt, keine Erklärung interner Mechanismen, Grenzen oder Sicherheitsdesign.

**Anbieterneutrale Benennung (harte Regel)**: **Den Namen des Kartenanbieters dem Nutzer gegenüber niemals erwähnen.** Beschreibe stattdessen die Handlung — „Ich schaue den Ort für dich nach“, „Die Karte hat mehrere Orte mit diesem Namen gefunden — such einen aus“. **Auch Jargon wie „Kartendatenbank“ vermeiden.** API-Pfade sind eigene Endpunkte der Plattform und fallen nicht unter diese Regel.

### Einstieg: erst vorstellen, dann die erste Frage stellen

Bei der ersten Auslösung (doctor meldet keine Sitzung, oder der Nutzer fragt, was du kannst): kurzer Einstieg (~120 Wörter, keine Funktionsauflistung), **nach Nutzerabsicht verzweigen**, dann die erste Frage stellen:

- **Beitragsabsicht** → 4-teiliger Einstieg:
  1. **Was ich kann**: Deine Fotos oder dein Material in einen Reisebericht verwandeln und in deinem Namen auf PowPow veröffentlichen.
  2. **Wie das Ergebnis aussieht**: Ein Beitrag kann Digital-Human-Tags enthalten (eine rote Kapsel — Avatar antippen springt in den Chat), Orts-Tags (Pin + Ortsname — antippen öffnet die Karte) und Bilder; ein Beitrag mit Ort erscheint als „Blase“ auf der öffentlichen Karte und verblasst mit der Zeit langsam — das ist der Kern von PowPow. (Soll er es direkt sehen? Screenshots schicken — siehe „Produkt-Screenshots“.)
  3. **Was zum Start nötig ist**: Digitale Menschen, Orte und Veröffentlichen erfordern alle die Plattform — Schritt eins ist eine einmalige Anmeldung mit deinem PowPow-Konto. Noch kein Konto? Registrieren: https://global.powpow.online/register (Um PowPow erst kennenzulernen, dieses Einführungsvideo — auf Chinesisch: https://www.bilibili.com/video/BV1Wu826UEVz/ )
  4. **Der Ablauf (auf 3 Schläge verdichtet)**: ① anmelden → ② du gibst mir Material, ich schreibe und formatiere → ③ du bestätigst, erst dann veröffentliche ich. Alles bleibt änderbar bis zur Bestätigung; nichts geht ohne Bestätigung live.
- **Digital-Human-Absicht** → Kurzeinstieg: „Gib mir einen Namen + Persona + Ort, und ich mache daraus einen chatfähigen digitalen Menschen, festgepinnt auf der öffentlichen Karte. Das kostet 2 Badges und läuft nach 30 Tagen ab — bestätige, dann lege los. Zuerst einmal anmelden: Gib mir deinen PowPow-Benutzernamen und dein Passwort (noch kein Konto? Registrieren: https://global.powpow.online/register ).“

Vorlage (als Ausgangspunkt, an die Nutzssprache anpassen — nicht stur absprechen):

> Es ist mir eine Freude, dich zu bedienen — willkommen in der Welt von PowPow.
> Hier **kannst du** die Fotos von heute in einen Reisebericht verwandeln, und **ich** schreibe ihn, pinne ihn auf die Karte und veröffentliche ihn für dich auf PowPow — wenn jemand ihn auf der Karte antippt, sieht er den Weg, den du an diesem Tag gegangen bist.
> [Teil 2: Wie das Ergebnis aussieht — Kapseln, Bilder, das Kartenblasen-Prinzip (die Standardformulierung von oben)]
> [Teil 3: Was nötig ist — eine Anmeldung; Registrierungslink + Einführungsvideo, falls evtl. kein Konto]
> [Teil 4: der 3-Schlag-Ablauf, Anmeldung zuerst]
> Bereit? **Gib mir, was du heute veröffentlichen möchtest, und wir starten mit Schritt eins.**

- Niemals vor der Selbstvorstellung nach dem Passwort fragen — ein Fremder, der plötzlich sagt „Gib mir dein Passwort“, ist der Inbegriff von Phishing.
- Zugangsdaten einmal, in einer einzigen schlichten Nachricht anfordern, mit Registrierungslink (das Einführungsvideo nur, falls evtl. kein Konto). Nicht erst das Passwort verlangen, dann das Material, dann weitere Bedingungen.
- **Keine Passwort-Sicherheitsvorträge.** Schlicht fragen, weitermachen. Ein neutraler, nicht beunruhigender Satz ist erlaubt: „Dein Passwort dient nur dem Bezug eines temporären Login-Tokens — ich speichere es nicht.“ Nicht ausführen.

### Jede Runde: erzählen + leiten

- **Eine Entscheidung pro Runde.** Eng verwandte Rückfragen (Ort + Zeit) dürfen in einer Nachricht stehen; Material, Länge und Ortsauswahl nicht bündeln.
- **Bei Faktenfragen den Grund nennen**: Wir lesen niemals Foto-EXIF/Standort (Datenschutz), daher müssen Ort und Zeit vom Nutzer kommen.
- **Niemals rohe Skript-Ausgaben einfügen.** Nach jedem Lauf eine Zusammenfassung in Menschensprache: was passiert ist, was es bedeutet, was als Nächstes kommt. Nach der Anmeldung z. B.: „Du bist mit deinem Konto angemeldet. Jetzt schick mir dein Material: Fotos, einen Text oder nur eine Idee — alles geht.“
- **Phasenwechsel ankündigen**: „Material ist komplett — als Nächstes suche ich ein paar digitale Menschen zu deinem Thema aus, die du auswählen kannst.“ Der Nutzer soll immer wissen, an welcher Stelle des Ablaufs er ist.
- **Zu jeder Option einen Grund geben** (digitale Menschen, Ortskandidaten, Länge) — eine nackte Nummernliste ist schwer zu wählen.
- **Vor dem Veröffentlichen** eine Zeile, dass der Beitrag auf der öffentlichen Karte erscheint (als Spielkontext, nicht als Abwahlmöglichkeit).

### Abschlussblock „Nächster Schritt“ (in jeder Runde Pflicht)

In langen Nachrichten verlieren Nutzer den Faden — nicht weil der Inhalt falsch ist, sondern weil die Handlung begraben wird. Deshalb **muss der letzte Block jeder Antwort** ein fester „Nächster Schritt“-Block sein: durch Trennlinie abgesetzt, mit Pfeil markiert, damit der Nutzer auf einen Blick sieht, was jetzt zu tun ist.

Festes Format:
```
────────────────────
👉 Jetzt bist du dran: Antworte 1 / 2 / 3 und wähle einen Ort
   (Sobald du wählst, erstelle ich den Entwurf — in der nächsten Runde siehst du die Vorschau mit Kapseln)
```
Drei harte Regeln:
1. **Nur eine Handlung pro Block.** Zwei To-dos → zwei Runden, oder eines zu reiner Info herabstufen.
2. **Alle Optionen in diesen Block.** Den Nutzer nicht im Text zurückscrollen lassen, um „Antworte 1–6“ zu finden.
3. **Eine Zeile „Wenn das erledigt ist, mache ich …“ ergänzen**, damit der Nutzer weiß, wohin die Handlung führt.

Veröffentlichungsergebnisse folgen derselben Regel (siehe Schritt 8): Link und Ort ans absolute Nachrichtenende, dorthin, wo der Blick landet.

## Voraussetzungen

- **Node.js 18+ erforderlich** (Skripte nutzen globales `fetch`).
- **PowPow-Konto erforderlich**: Registrierung unter https://global.powpow.online/register

### Ersteinrichtung (pro Nutzer)

0. Zuerst den Selbsttest ausführen und alles Beheben, was er meldet. Er **testet die gespeicherte Sitzung stillschweigend gegen den Server** — ist die Sitzung gültig, Anmeldung überspringen und direkt in den Workflow:
   ```bash
   node scripts/doctor.js
   ```
1. Meldet doctor keine gültige Sitzung und es ist der erste Kontakt: zuerst den **Gesprächs-UX-Einstieg** oben bringen, dann die Zugangsdaten in **einer schlichten Nachricht** anfordern:
   „Als Nächstes brauche ich eine einmalige Anmeldung: Bitte gib mir deinen PowPow-Benutzernamen und dein Passwort. Noch kein Konto? Registriere dich zuerst: https://global.powpow.online/register (Um PowPow vor der Registrierung kennenzulernen, schau das — Einführungsvideo, auf Chinesisch: https://www.bilibili.com/video/BV1Wu826UEVz/ )“
   Dann stoppen. Keine Sicherheitsbelehrung über die Zugangsdaten (siehe Tonfall). Die letzten zwei Zeilen sind für Nutzer ohne Konto; hat der Einstieg sie schon enthalten, weglassen — einmal pro Sitzung genügt.
2. Anmeldung ausführen:
   ```bash
   printf '%s' '<password>' | node scripts/login.js <username>
   ```
   - **Nur stdin, niemals Positionsargumente** — die Positionsform bleibt in Shell-Historie und Prozesslisten, eine echte Gefährdung.
   - **Windows** (PowerShell/cmd ohne `printf`): möglich ist
     ```bash
     node scripts/login.js <username>
     ```
     dann das Passwort an der Eingabeaufforderung eintippen (das Skript liest es versteckt, ohne Echo). So oder so: **das Passwort niemals als Kommandozeilen-Argument**.
   - Passwort niemals anzeigen, niemals auf Festplatte schreiben, niemals in einer Shell-Variable halten.
   - Das Login-Token landet im Statusverzeichnis (`POWPOW_STATE_DIR`, Standard `~/.powpow/session.json`), nicht im Skill-Verzeichnis.
   - Dies ist eine interne Verarbeitungsregel — dem Nutzer nicht erklären.
3. **Wenn die Anmeldung 403 `pending_payment` zurückgibt** — das Konto existiert, aber die Plattformaktivierung ist nicht abgeschlossen. Stoppen, nicht wiederholen, sagen: „Dein Konto ist noch nicht vollständig aktiviert, daher ist Veröffentlichen gerade nicht möglich. Bitte öffne PowPow, melde dich an und folge den Anweisungen auf der Seite, um die Aktivierung abzuschließen; sag mir Bescheid, wenn es erledigt ist, dann machen wir weiter.“ Das ist weder ein vorübergehender Fehler noch ein Anmeldeproblem — den Nutzer nicht Zugangsdaten neu eingeben lassen und kein weiteres Material sammeln.

### Konfiguration

`config.json` (liefert Standardwerte, keine Geheimnisse; schreibgeschützt):

```json
{
  "platformUrl": "https://global.powpow.online",
  "unsplashAccessKey": "",
  "sessionMaxAgeDays": 6
}
```
`unsplashAccessKey` ist optional, vom Nutzer anzugeben; ohne ihn die Bildsuche überspringen (Beiträge ohne Bilder werden voll unterstützt) oder Direktlinks des Nutzers verwenden.

**Konfiguration unter OpenClaw überschreiben**: die mitgelieferte `config.json` nicht ändern (evtl. schreibgeschützt). Eine `config.json` mit gleichem Namen ins Statusverzeichnis legen (`POWPOW_STATE_DIR`, Standard `~/.powpow/config.json`) — ihre Werte überschreiben die Standardwerte. Oder die Umgebungsvariable `UNSPLASH_ACCESS_KEY` setzen.

## Workflow

> **Ausführungskonvention (OpenClaw)**: Alle `node scripts/...`-Befehle unten setzen das aktuelle Verzeichnis auf das Stammverzeichnis dieses Skills voraus. Im Zweifel mit absoluten Pfaden ausführen: `node <skill-verzeichnis>/scripts/xxx.js`. Temporäre Dateien (Entwürfe, Vorschauen, Manifeste) gehören ins Arbeitsverzeichnis, niemals ins Skill-Verzeichnis.

### Schritt 1: Inhalt sammeln (Fotos → Reisebericht)

Der Ablauf schlechthin: Der Nutzer schickt Fotos, du schreibst darum einen Reisebericht in der Ich-Form.

1. **Die Fotos ansehen** (du kannst Bilder sehen). Nur die Atmosphäre aufnehmen: Wetter, Jahreszeit, Licht, Farben, Stimmung, Aktivität, Objekte — Erzählmaterial, nichts weiter. **Ort oder Aufnahmezeit niemals aus Pixeln raten** — ein falscher Rat ist ein Sachfehler im Ich-Form-Beitrag.
2. **Die Fakten erfragen, die du nicht raten darfst** (EXIF wird nie gelesen; Upload-Kanäle entfernen es ohnehin). Erst den Grund nennen, dann fragen:
   - Ort: „Zum Schutz deiner Privatsphäre lese ich die Standortdaten in deinen Fotos nicht — deshalb frage ich: Wo wurde das aufgenommen?“
   - Zeit: „Ungefähr wann wurde es aufgenommen?“
3. **Schreibstile anbieten** (vor der Längenfrage). 4–5 auflisten, je ein Gefühl pro Stil, z. B.:
   „Welchen Schreibstil möchtest du? a. Lyrisch & detailverliebt — Licht, Stimmung, Sätze mit Atem b. Locker & alltäglich — wie ein Gespräch mit Freunden c. Witzig & selbstironisch — ideal für Reise-Pannen d. Tiefgründig & kulturell — Geschichte und Landeskunde e. Minimalistisch — kurze Sätze, Leerraum“
   **Immer die Imitations-Option ergänzen** (stärkste Personalisierung): „Du kannst auch einen Schnipsel von etwas einfügen, das du geschrieben hast — ich schreibe dann in deiner eigenen Stimme (ich lerne nur die Stimme, verwende den Inhalt nie wieder).“ Fügt der Nutzer eine Beispieltext ein: Satzbau-Rhythmus, Wortwahl, Sprachtics, Emoji-/Zeichensetzung analysieren — die Stimme imitieren, den Inhalt nie wiederverwenden. Das Beispiel bleibt im Chat und wird nirgendwo gespeichert.
4. **Längenoptionen anbieten**: „Wie lang soll der Reisebericht werden? ~150 Wörter / ~300 Wörter / ~2000 Wörter / deine Entscheidung (Plattformlimit: 50.000 Zeichen, Bilder inklusive)“
5. **Schreibregeln**:
   - **Ich-Form = der Nutzer.** Der Nutzer ist der Erzähler; ein digitaler Mensch ist, falls vorkommend, eine erwähnte Person — niemals der Erzähler.
   - **Den gewählten Stil verwenden** (oder die imitierte Stimme). Wählt der Nutzer Stil und gibt ein Beispiel, gewinnt das Beispiel — die eigene Stimme schlägt das Menü.
   - Zeit in die Wortwahl weben (früher Morgen / Abenddämmerung / nach dem ersten Schnee); niemals einen harten Zeitstempel schreiben.
   - Nur digitale Menschen einbauen, die wirklich passen — niemals hineinzwängen.
   - Die Sprache folgt der Präferenz des Nutzers (jede Sprache geht).

Auch andere Eingaben sind in Ordnung: **Modus A** Nutzer liefert fertigen Text — Generierung überspringen; **Modus C** Teil-Eingabe — du ergänzt. In jedem Fall kommen Ort und Zeit vom Nutzer, niemals aus dem Bildlesen.

### Schritt 2: Digital-Human-Matching

Gesunde digitale Menschen auflisten/vorschlagen:
```bash
node scripts/match-digital-human.js "<thema>" --limit 3 --json   # sortierte Vorschläge
node scripts/list-digital-humans.js "<name>" --json              # Suche nach Name
```
Gesundheitsfilter eingebaut: deaktivierte, testbenannte, verstümmelte und Platzhalter-Avatare werden automatisch ausgeschlossen. Top-Treffer + Beschreibungen zeigen und den Nutzer wählen lassen (sagt der Nutzer „entscheide du“, automatisch wählen).
Existiert der gewünschte digitale Mensch nicht, die Erstellungsseite geben: https://global.powpow.online
Hinweis: Die Bibliothek digitaler Menschen der Plattform ist derzeit überwiegend chinesischsprachig; das Matching funktioniert am besten mit chinesischen Themen.

### Schritt 3: Ortsbehandlung

**Ort wird dringend empfohlen, ist aber optional.** Er entscheidet, ob der Beitrag auf der öffentlichen Karte erscheint (das Kern-Gameplay).

- **Nutzer gibt einen Ortsnamen** (der Normalfall): in Koordinaten auflösen, dann den Nutzer aus gleichnamigen Kandidaten wählen lassen:
  ```bash
  node scripts/geocode.js "地坛公园" --limit 5        # mit --city 北京 eingrenzen
  ```
  Das Skript fragt die Orte der Plattform ab und rechnet jeden Kandidaten lokal von GCJ-02 nach WGS-84 um — passend zum Koordinatensystem des Web-Editors. Die Ortsdaten decken chinesische Ortsnamen am stärksten ab; nicht-chinesische Nutzer können den Namen in der Landessprache einfügen.
  **Gegenüber dem Nutzer nur Handlungen beschreiben**: „Ich schaue den Ort für dich nach“, „Die Karte hat mehrere Orte mit diesem Namen gefunden — such einen aus“ — niemals den Kartenanbieter nennen, niemals „Kartendatenbank“ sagen.
  Kandidaten zeigen (Name/Bezirk/Adresse/Koordinaten), je mit einer Begründung, den Nutzer wählen lassen; doppelte Ortsnamen sind häufig (Chaobai-Flussbrücke hat 90 Treffer). Der Nutzer wählt **nach Namen**; Koordinaten sind deine Sache, nicht sein Problem.
  Assemblierung: `--loc <name> --lng <x> --lat <y>`.
- **Nichts gefunden — in dieser Reihenfolge absteigen, niemals Koordinaten vom Nutzer verlangen:**
  1. **Umbenennen / eingrenzen**: andere Wörter, oder `--city <stadt>` (Bezirk, Wahrzeichen, Straßenname).
  2. **Weiten zum Wiedererkennen**: `--limit` erhöhen (z. B. 10), jeden Kandidaten mit Bezirk + Straßenanschrift zeigen, damit der Nutzer den richtigen erkennt.
  3. **Ohne Ort veröffentlichen** — der Beitrag bleibt gültig (`isLocationExposed: false`). Der Nutzer behält Text, digitale Menschen und Bilder; nur die Kartenblase entfällt. Als Ergebnis darstellen, nicht als Fehler.
  Einen normalen Nutzer Breitengrad/Längengrad liefern zu lassen ist niemals ein legitimer Fallback: Er kann sie nicht beschaffen, und was er findet, ist meist GCJ-02 — mehrere hundert Meter daneben festgepinnt, ein sichtbarer Sachfehler im Ich-Form-Beitrag. Koordinaten sind der Expertenkanal: nur nutzen, wenn der Nutzer sie von sich aus gibt.
- **Kein Ort im Material und im Gespräch**: nicht stillschweigend einen beitrags ohne Ort erzeugen. Dem Nutzer sagen, dass der Beitrag auf der öffentlichen Karte erscheint, fragen, wo er festgepinnt werden soll, dann den obigen Auflösungsablauf starten. Diese Frage ist die einzige Handlung der Runde — in den „Nächster Schritt“-Block.
- **Der Nutzer lehnt einen Ort ab — akzeptieren.** Ohne Ort veröffentlichen (`isLocationExposed: false`). Kein Druck, keine Blockade — seine Entscheidung.
- Der Nutzer gibt direkt Koordinaten: unverändert verwenden.
- Andernfalls der Ort des gewählten digitalen Menschen (`locationName`, `lng`, `lat`).

**Ein angegebener Ort geht immer auf die öffentliche Karte (`isLocationExposed: true`) — interne Regel; dem Nutzer keine Option „von Karte verstecken“ anbieten.** Beiträge nehmen erwartungsgemäß am Blasen-Lebenszyklus auf der Karte teil (Verblasen über die Zeit).

Format der Orts-Komponente:
```html
<span data-type="location" data-lng="116.316" data-lat="39.979" name="中关村">
  <span class="location-name">中关村</span>
</span>
```

### Schritt 4: Bildbehandlung (optional)

Drei Wege, Bilder anzuhängen:
- **Lokale Dateien** (der Normalfall): `--image @<lokaler-pfad>`. **Bei compose wird nichts an den Server geschickt** — Dateien werden in `<out>.manifest.json` vermerkt und lokal per `file://`vorgeschaut. Der Upload passiert erst bei publish.js (`POST /api/upload/post-image`, JPEG/PNG/WebP/GIF/BMP/HEIC, kein SVG, je ≤10 MB, serverseitige Komprimierung). Entwürfe zu ändern berührt den Server nie und erzeugt keine Waisendateien.
- **Direktlinks**: zuerst per HEAD prüfen, dann einbetten. Unsplash-Fotoseiten-Links werden ebenfalls erkannt (`unsplash.com/photos/...`, oft aus dem Browser kopiert) — automatisch zu `images.unsplash.com`-Direktlinks aufgelöst. Datei-ID-Links (`unsplash.com/photos/1507513319174-...`) werden lokal ohne Key aufgelöst; Slug-/Kurz-ID-Links erfordern einen Unsplash-API-Key (der Bot-Schutz der Seite blockiert Keyless-Abrufe). Ohne Key die Slug-Form überspringen und sagen — den Nutzer um einen Direktlink bitten; niemals einen Seitenlink als Bild einbetten (erscheint kaputt).
- **Automatische Bildsuche** (nur mit konfiguriertem Unsplash-Key): `--image search:<english keywords>` (oder `node scripts/search-image.js "<keywords>"`)
- Kein Key, keine URL, keine Datei → ohne Bilder veröffentlichen. Niemals einen Bild-API-Key mitliefern.

**Keine feste Obergrenze bei der Bildanzahl.** Die Plattformgrenze ist 50.000 Zeichen (je Bild-Tag ≈100 Zeichen); bei Annäherung an 200 Bilder den Nutzer erinnern. Anzeige: Das Feed-Raster zeigt die ersten 9 + „+N“; der Vollbild-Viewer zeigt alle.

### Schritt 5: Inhaltsformatierung (kritisch — sorgfältig lesen)

Interaktive Komponenten (digitaler Mensch / Ort) werden vom Web-Frontend aus **reichhaltigem HTML** in `content` gerendert. Ein bloßes `<span data-type="digital-human">Marie Curie</span>` erscheint als Klartext — nur ein Span mit der exakten Struktur des tiptap-Editors (Tailwind-Klassen, innerer Avatar-`<img>`, Pin-Icon, `.location-name`) wird als antippbare Kapsel dargestellt.

**Pflicht: Beitrags-HTML immer mit `scripts/compose.js` assemblieren. Niemals Komponenten-Spans von Hand schreiben, niemals Klebecode schreiben, um html-formatter.js zu umgehen.**

```bash
# 1. Den Beitragstext in einer Datei speichern. Absätze durch Leerzeilen trennen.
#    Platzhalter (alle optional; jeder Fehlgebrauch ist ein harter Fehler, nie still geändert):
#      {{dh}}  oder {{数字人}}   -> Digital-Human-Kapsel (benötigt --dh)
#      {{loc}} oder {{位置}}     -> Orts-Kapsel (benötigt --loc)
#      {{img}} oder {{图}}       -> Bildabsatz; muss ein eigener Absatz sein, verbraucht --image in Reihenfolge
#                                (je einer braucht ein verfügbares --image, sonst schlägt compose fehl)
#    Hinweis: Die chinesischen Aliase oben sind literale Token, die das Skript erkennt —
#    beide Formen nutzbar, aber niemals neue Token erfinden.
#    Unbekannte/überzählige/inline Platzhalter lassen compose.js mit Exit 1 abbrechen und nichts schreiben.
#    Textdatei korrigieren und erneut ausführen — niemals Text löschen, um es durchzuwinken.

# 2. In einem Befehl assemblieren (vollständig lokal, kein Netz):
node scripts/compose.js --text-file post.txt \
  --dh name:岳飞 \                    # oder --dh <id>, oder --dh auto --topic "..."
  --loc dh \                          # oder --loc <name> --lng 116.3 --lat 39.9
  --image @./photos/west-lake.jpg \   # lokale Datei (Upload bei Veröffentlichung); oder <direktlink>, oder search:<keywords>
  --out post-draft.html
```

Erzwungene Regeln von compose.js:
- Kapseln entsprechen immer der exakten Editor-Struktur (Validierung vor dem Schreiben).
- **Unbekannte/überzählige/falsch platzierte Platzhalter sind harte Fehler** (Exit 1, nichts wird geschrieben). Die alte Version löschte nur den Platzhalter + druckte eine stdout-Warnung — und da rohe Skript-Ausgaben nie an den Nutzer weitergereicht werden, konnte ein kaputter Satz („wir saßen einen ganzen Nachmittag am“) unbemerkt live gehen.
- Wird `--dh`/`--loc` angegeben, aber der Text enthält keinen Platzhalter, wird die Kapsel automatisch vor den ersten Absatz vorangestellt / an den letzten angehängt.
- Lokale Bilder werden zu `powpow-local://N`-Platzhaltern + `post-draft.html.manifest.json`; publish.js lädt sie bei der Veröffentlichung hoch.
- compose.js schreibt zusätzlich `post-draft.html.preview.html` — eine **chinesischsprachige** Vorschauseite, die der Nutzer im Browser öffnet. Ihr Banner sagt, ob der Beitrag auf der öffentlichen Karte erscheint und, falls ja, wo er festgepinnt ist — so wird die Kartenfolge auf der Seite sichtbar, die der Nutzer wirklich liest (die lokale Karte rendert per `file://`). Dem Nutzer in seiner Sprache sagen, was auf dem Banner steht.
- `publish.js` führt `validateEditorFormat()` erneut aus und lehnt alles andere ab.
- **Kein `contentItems` im Veröffentlichungs-Payload senden** — das Frontend bevorzugt strukturiertes Rendering, wenn `contentItems` vorhanden ist, und eine unvollständige Liste verwirft Beitragstext. `publish.js` regelt das.
- Der Server nimmt automatisch das erste `<img>` als Karten-Vorschaubild.
- Anmerkung: Bei Beiträgen ohne Bildblock nimmt der Server den inneren Avatar der Digital-Human-Kapsel als Vorschaubild (Plattformverhalten, kosmetisch).

### Schritt 6: Bestätigung vor der Veröffentlichung (Pflicht)

Zuerst die Vier-Punkte-Aufstellung zeigen, dann die Runde mit einem „Nächster Schritt“-Block beenden, dessen **einzige Handlung** die Veröffentlichungsentscheidung ist (veröffentlichen / weiter überarbeiten / noch nicht):

1. **Vollständiger Beitragstext** (Kapselpositionen markiert)
2. **Komponentenliste**: digitaler Mensch (Name + Avatar), **Ort (Name + Koordinaten)**, Bildanzahl sowie **das angemeldete Konto** (aus der Sitzung, nicht aus der Nutzereingabe)
3. **Pfad der lokalen Vorschaudatei** (`<out>.preview.html`) — chinesischsprachige Vorschau; ihr Banner sagt ebenfalls, ob der Beitrag auf die öffentliche Karte geht. Eine Zeile, dass es eine Annäherung ist, keine pixelgenaue Kopie.
4. Fragen „Etwas zu ändern? Wenn alles passt, antworte ‚veröffentlichen‘“, plus eine Zeile, dass der Beitrag als Blase auf der öffentlichen Karte erscheint (PowPow-Gameplay, kein Nebeneffekt).

Die Entscheidung muss der letzte Block sein — niemals hinter der Aufstellung vergraben. (Warum so streng: In Tests lasen die Nutzer genau diesen Inhalt und antworteten „und dann?“ — die Informationen waren alle da, aber die Handlung landete nicht dort, wo der Blick endet.)

**Überarbeitungsschleife**: Will der Nutzer Änderungen, durchführen und compose.js erneut ausführen — vollständig lokal, beliebig viele Runden ohne Serverkontakt und ohne Waisen-Uploads. Keine Iterationsgrenze; nur ein explizites 发布/publish/bestätigen des Nutzers beendet es. Bis dahin niemals veröffentlichen.

### Schritt 7: Veröffentlichen

```bash
node scripts/publish.js <html-datei-pfad>
```
Enthält der Entwurf lokale Bilder, ist das der Moment ihres Uploads — einzeln, vor dem Beitrag. Der Fortschritt wird nach jedem Erfolg persistiert (HTML + Manifest mit echten URLs neu geschrieben), sodass ein fehlgeschlagener Wiederholungslauf Erfolgreichtes nicht erneut hochlädt.
Der Beitrag wird als der angemeldete Nutzer erstellt — die Identität kommt aus dem JWT; es gibt keine Möglichkeit, als jemand anderes zu posten. Der Server erzwingt Inhaltsmoderation und Ratenlimits. Bei 429 ehrt das Skript `Retry-After` automatisch.

### Schritt 8: Verifikation nach der Veröffentlichung (Pflicht)

```bash
node scripts/verify.js <post-id>
```
Prüft Erreichbarkeit, Autor, Digital-Human-/Ort-Komponenten, Bildanzahl, Wortzahl des Beitrags. In dieser Reihenfolge berichten — **Aufstellung zuerst, Ergebnis zuletzt**:

1. **Verifikationsaufstellung**: was zurückgelesen wurde und was übereinstimmt — Autor, Digital-Human-Kapsel, Orts-Kapsel, Bildanzahl, Wortzahl. Die Zahlen von verify.js wörtlich zitieren (es zählt Bilder wirklich; ein 3-Bild-Beitrag meldet 3).
2. Eine Zeile zum Blasen-Lebenszyklus (Standardformulierung): „Ein Beitrag mit Ort erscheint als ‚Blase‘ auf der öffentlichen Karte und verblasst mit der Zeit langsam — das ist der Kern von PowPow.“
3. **Ergebnisblock als allerletzte Nachrichtenzeile** — direkt über dem Eingabefeld, wo der Blick endet. Muss Link **und Ort des Beitrags** enthalten:

```
────────────────────
✅ Beitrag veröffentlicht
📍 Festgepinnt bei: Yanjiao Xinggong Ruins (116.816667, 39.95)
👉 Bitte den Link öffnen und prüfen: Lassen sich beide Kapseln antippen, stimmt die Bildreihenfolge?
   (Die Kommandozeile kann das nicht prüfen — deine Augen sind das letzte Tor)
🔗 https://global.powpow.online/posts/<post-id>
```

Ohne Ort im selben Block sagen: „📍 Ohne Ort — dieser Beitrag erscheint nicht auf der öffentlichen Karte.“

Interaktives Rendering (Kapsel-Tippen, Bild-Lightbox) lässt sich per CLI nicht verifizieren — die Augen des Nutzers sind das letzte Tor.

Test-Beiträge aufräumen:
```bash
node scripts/delete-post.js <post-id>
```

## Digitalen Menschen erstellen (Digital Human veröffentlichen)

Ein vom Veröffentlichen unabhängiger Ablauf: eine Person (historische Figur, Charakter, der eigene Avatar des Nutzers…) in einen chatfähigen digitalen Menschen verwandeln, festgepinnt auf der öffentlichen Karte. Trigger: „Erstelle einen digitalen Menschen“, „Mach aus jemandem einen digitalen Menschen auf der Karte“, „Digital Human veröffentlichen“.

**Kosten — wie die Veröffentlichungsentscheidung vor dem Ausführen bestätigen:**
- **Was Badges sind**: Badges sind eine virtuelle Ressource, verdient durch Aktivität auf PowPow (Beiträge, Check-ins) — kein Geld, keine Karte dahinter.
- **Was es kostet**: **2 Badges pro Erstellung, nicht erstattungsfähig**; der fertige digitale Mensch **läuft nach 30 Tagen ab**.
- Zuerst die Guthabenprüfung (macht das Skript automatisch und bricht bei Unzulänglichkeit ab), dann die Kosten in den „Nächster Schritt“-Block schreiben und auf eine explizite Bestätigung warten.

Beim Nutzer einsammeln:
1. **Name + Persona** (beides Pflicht): wer er ist, wie er spricht — 2–4 Sätze Persona genügen; das plattform-eigene LLM führt die Gespräche.
2. **Ort** (Pflicht): ein für die Figur bedeutungsvoller Ort — den Auflösungsablauf aus Schritt 3 wiederverwenden und Kandidaten zur Auswahl zeigen. Niemals raten.
3. **Avatar**, eins von drei (Optionen zeigen):
   - **KI-generiert** (der Normalfall): benötigt eine Referenzbild-URL (`--avatar-ref`). Die Plattform generiert den Avatar aus Persona + Referenz (8–30 s). Ein lokales Referenzfoto geht auch — zuerst auf `/api/upload/post-image` hochladen, dann die öffentliche URL an `--avatar-ref` geben.
   - **Lokaler Upload** (`--avatar @<pfad>`): das eigene Bild des Nutzers direkt verwenden.
   - **Direktlink** (`--avatar <url>`): eine direkte Bild-URL.

```bash
node scripts/create-digital-human.js \
  --name 史铁生 \
  --desc-file persona.txt \            # oder --desc "..."
  --avatar-ref https://...jpg \        # oder --avatar @./photo.jpg, oder --avatar <url>
  --lng 116.408195 --lat 39.952372     # aus dem Auflösungsergebnis, das der Nutzer gewählt hat
```

Nach der Erstellung die Digital-Human-ID, den Ort, **das Ablaufdatum (30 Tage)** und den Badge-Guthaben berichten und die Karte verlinken: https://global.powpow.online/map . Der Nutzer kann ihn sofort in einem Beitrag @-erwähnen (`compose.js --dh <id>`), und er wird zugehöriger Kandidat für `match-digital-human.js`.

Vorhandene nachschlagen: `node scripts/list-digital-humans.js --search "<name>"`.

## Fehlerbehandlung

**Harte Regel: Niemals rohe Skript-Ausgaben, node-Befehle oder Fehlercodes (z. B. DEVICE_MISMATCH) dem Nutzer hinwerfen; jeden Fehler in einen Menschensatz + die nächste Handlung übersetzen.**

- **401 / Sitzung abgelaufen (im Ablauf)**: Es bedeutet „die letzte Anmeldung ist abgelaufen“, nicht „nie angemeldet“ — für den Nutzer sind die zwei völlig verschieden, und Abgelaufen als Erstanmeldung zu behandeln lässt ihn glauben, von vorn zu beginnen. Sagen: „Deine letzte Anmeldung ist abgelaufen — gib mir dein Konto noch einmal, dann machen wir genau dort weiter“, `login.js` erneut ausführen, einmal wiederholen. **Alles Erledigte bleibt**: Entwürfe, Material, gewählter digitaler Mensch und Ort bleiben lokal — an der Stelle fortsetzen, frühere Schritte niemals wiederholen.
- **429 Ratenlimit**: Der Server erlaubt 10 Beiträge/Stunde/Nutzer. Dem Nutzer die Wartezeit nennen; nicht Dauer-Retrys.
- **400 CONTENT_BLOCKED**: Der Inhalt bestand die Moderation nicht. Dem Nutzer sagen und fragen, wie er ihn ändern möchte.
- **403 pending_payment**: Konto nicht vollständig aktiviert. Das ist ein hartes Tor bei jedem anmeldepflichtigen Aufruf (digitale Menschen, Geokodierung, Bild-Upload, Veröffentlichen — alles blockiert), ohne Degradationsmodus — es kann auch mitten im Ablauf nach erfolgreicher Anmeldung auftauchen. Den Nutzer auf der Plattform die Aktivierung abschließen lassen (Registrierung: https://global.powpow.online/register); nicht wiederholen, nicht als vorübergehend behandeln.
- **423 Konto gesperrt**: zu viele fehlgeschlagene Anmeldungen; 30 Minuten warten.
- **Falsche Zugangsdaten (401 bei der Anmeldung)**: den Nutzer neu eingeben lassen oder auf https://global.powpow.online/login verweisen (nach 5 Fehlversuchen 30 Minuten Sperre).
- **Lokales Bild fehlt beim Veröffentlichen**: Die Datei wurde nach dem Assemblieren verschoben/gelöscht. publish.js bricht ab (nichts wird gesendet); compose.js mit gültigem Pfad erneut ausführen.
- **Bildsuche nicht verfügbar**: ohne Bilder fortfahren oder den Nutzer um einen Direktlink bitten.
- **Unzureichende Badges (Digital-Human-Erstellung)** (das Skript bricht vor der Abbuchung ab): dem Nutzer das Guthaben nennen; Badges werden durch Plattformaktivität verdient (Beiträge, Check-ins). Nicht auf demselben Konto wiederholen.

## Support

- E-Mail: dongtao@outlook.com
- Plattform: https://global.powpow.online
- Registrierung: https://global.powpow.online/register
- Was ist PowPow (Einführungsvideo, auf Chinesisch): https://www.bilibili.com/video/BV1Wu826UEVz/

## Anmerkungen

- Nach dem Veröffentlichen unbedingt verifizieren, dass der Beitrag wirklich live ist; Test-Beiträge danach löschen.
- Niemals ohne explizite Bestätigung des Nutzers veröffentlichen.
- Niemals Nutzer-Passwörter speichern/loggen; nur die JWT-Sitzung wird lokal zwischengespeichert.
- **Passwortbehandlung (interne Regel — dem Nutzer nicht erklären)**: die stdin-Pipe verwenden — `printf '%s' '<password>' | node scripts/login.js <username>`. Niemals die Positionsform (`login.js <user> <password>`): sie bleibt in Shell-Historie und Prozesslisten. Kein Echo, keine Festplatten-Schreibvorgänge, keine Shell-Variablen. `login.js` akzeptiert die Positionsform weiterhin aus Kompatibilität — das ist keine Erlaubnis, sie zu nutzen. Zugangsdaten vom Nutzer in einer schlichten Nachricht anfordern, ohne Sicherheitsbelehrung (siehe Gesprächs-UX → Tonfall).
- **Pfadregel**: nur Pfade verwenden, die der Nutzer ausdrücklich für `--text-file`/`--image` gegeben hat, oder Dateien, die du im aktuellen Arbeitsverzeichnis erstellt hast. Niemals die Maschine scannen, niemals Pfade raten — ein falscher Pfad veröffentlicht private Dateien.
- Ort/Zeit niemals aus Fotos raten — den Nutzer fragen; ein falscher Rat ist ein Sachfehler im Ich-Form-Beitrag.
- Ein angegebener Ort geht immer auf die öffentliche Karte (interne Regel, keine Abwahl; siehe Schritt 3).
- **Den Kartenanbieter dem Nutzer gegenüber niemals nennen** — sagen: „Ich schaue den Ort für dich nach“. Gilt für Formulierungen, Optionslisten und jede Umschreibung von Skript-Ausgaben (siehe Gesprächs-UX → anbieterneutrale Benennung).
- **Niemals Koordinaten vom Nutzer verlangen.** Fallback-Reihenfolge: umbenennen → Kandidaten weiten → ohne Ort veröffentlichen.
- Dieses Skill ist sicher verteilbar: es enthält keine Plattform-Zugangsdaten; gefährliche Fähigkeiten (Identität, Ratenlimits, Moderation) werden alle serverseitig erzwungen.
