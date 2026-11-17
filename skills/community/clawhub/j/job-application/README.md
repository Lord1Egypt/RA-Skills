# Job-Application Skill für OpenClaw

[English documentation](README.en.md)

Der Skill erzeugt aus belegbaren Profildaten einen zugeschnittenen, einseitigen
Lebenslauf, ein Anschreiben und eine Bewerbung im Textformat. Alle mitgelieferten
Personen-, Arbeitgeber- und Bewerbungsdaten sind fiktiv. Der Skill versendet oder
veröffentlicht niemals Bewerbungen.

## Voraussetzungen

- Python 3.10 oder neuer
- `pdflatex` für PDFs
- Das LaTeX-Paket `fontawesome5` für die Kontakt-Symbole im CV
- Poppler (`pdfinfo` und `pdftotext`) für die verbindliche PDF-Qualitätsprüfung
- optional: Bash für `render_application.sh` unter Linux/macOS

Prüfen:

```text
python3 --version
pdflatex --version
pdfinfo -v
pdftotext -v
```

Unter Windows ist `py -3` häufig der Python-Befehl. TeX Live oder MiKTeX sowie
Poppler müssen im `PATH` verfügbar sein. Fehlt Poppler, schlägt die
Qualitätsprüfung bewusst mit einer klaren Fehlermeldung fehl.

## Private Daten updatefest speichern

Echte Profile, Fotos, Signaturen und Bewerbungen liegen außerhalb des installierten Skills:

```text
JOB_APPLICATION_DATA_DIR=/pfad/zu/privaten/job-application-daten
JOB_APPLICATION_PROFILE_DIR=/pfad/zum/privaten/profil
JOB_APPLICATION_OUTPUT_DIR=/pfad/zu/applications
```

Ohne `JOB_APPLICATION_OUTPUT_DIR` werden Bewerbungen unter
`$JOB_APPLICATION_DATA_DIR/applications` abgelegt; ohne `JOB_APPLICATION_DATA_DIR`
wird dafür das plattformübliche Nutzerdatenverzeichnis
`openclaw/job-application` verwendet. Ohne `JOB_APPLICATION_PROFILE_DIR` werden
ausschließlich die fiktiven Beispieldaten verwendet. ClawHub-Updates können den
Skill-Ordner ersetzen; private Daten gehören deshalb nicht dorthin. Vor einer
Veröffentlichung ist die Checkliste in `PUBLISHING.md` verbindlich. Der dort
beschriebene Whitelist-Export ist erforderlich, wenn der installierte Skill in
einem größeren Git-Repository liegt.

Für echte Bewerbungen muss derselbe externe Profilordner für CV und Anschreiben
verwendet werden. Entweder `JOB_APPLICATION_PROFILE_DIR` konfigurieren oder den
Pfad explizit übergeben:

```text
python3 scripts/generate_cover_letter.py --content application_content.json --output cover_letter.tex --profile-dir /pfad/zum/privaten/profil
python3 scripts/render_application.py <bewerbungsordner> --profile-dir /pfad/zum/privaten/profil
```

Der Anschreiben-Generator verweigert bei externen Bewerbungen einen stillen
Fallback auf das fiktive Beispielprofil. Der PDF-Validator prüft zusätzlich
Name, E-Mail, Telefon und Anschrift im Kopf des Anschreibens.

## Öffentliches Beispiel reproduzieren

Der folgende Befehl verwendet ausschließlich die fiktiven, mitgelieferten
Profildaten einschließlich der fiktiven Signatur und schreibt die Ergebnisse
außerhalb des installierten Skills:

```text
python3 scripts/render_example.py --output /tmp/job-application-example
```

Er erzeugt `CV.pdf`, `cover_letter.pdf` und `indeed_text.txt` und führt die
verbindliche PDF-Validierung aus. Zeitstempel in PDFs können zwischen Läufen
abweichen; Inhalt, Vorlage und Prüfresultat sind reproduzierbar.

## V2-Schnelltest

Im Skill-Verzeichnis (Linux/macOS):

```bash
python3 scripts/prepare_application.py --slug 2026-10-example-demo
cp examples/job.json examples/application_content.json applications/2026-10-example-demo/
python3 scripts/generate_cv_selection.py --job applications/2026-10-example-demo/job.json --output applications/2026-10-example-demo/cv_selection.json
python3 scripts/generate_cv.py --selection applications/2026-10-example-demo/cv_selection.json --output applications/2026-10-example-demo/CV.tex
python3 scripts/generate_cover_letter.py --content applications/2026-10-example-demo/application_content.json --output applications/2026-10-example-demo/cover_letter.tex
python3 scripts/generate_plain_text.py --content applications/2026-10-example-demo/application_content.json --output applications/2026-10-example-demo/indeed_text.txt
python3 scripts/render_application.py applications/2026-10-example-demo
```

`render_application.py` ruft den Validator automatisch auf. Er prüft, ob beide
PDFs lesbar sind, der CV exakt eine Seite hat, offene Platzhalter fehlen und der
CV die Seite sinnvoll füllt. Für die gezielte Fehlersuche gibt es ausschließlich
die sichtbare Debug-Option `--skip-validation`.

```text
python3 scripts/validate_application.py <bewerbungsordner>
python3 scripts/validate_application.py <bewerbungsordner> --strict-fill
```

`--min-vertical-fill` (Standard `0.52`) und `--max-vertical-fill` (Standard
`0.98`) sind konfigurierbar. Unterhalb des Minimums wird gewarnt; mit
`--strict-fill` wird abgebrochen. Mehr relevanten, belegten Inhalt auswählen
oder Text präzisieren statt Schriftgröße und Abstände zu patchen.

## Zustellung im Chat

Die erzeugten Dateien liegen zunächst lokal. Ein lokaler Pfad ist kein
anklickbarer Download-Link für Telegram, Slack oder andere Chat-Clients. Wenn
eine Person die Unterlagen ausdrücklich im aktuellen Chat anfordert, muss der
betreuende Agent die bereits validierten `CV.pdf`, `cover_letter.pdf` und bei
Bedarf `indeed_text.txt` als native Dokument-Anhänge senden.

Dabei dürfen ausschließlich die finalen angeforderten Ergebnisdateien
übermittelt werden – niemals Profil-JSON, Quelldateien, Signatur-Assets oder
andere private Zwischenstände. Eine Chat-Zustellung autorisiert weder eine
Einreichung noch eine Weiterleitung an Recruiter.

## CV-Auswahl und Limits

`cv_selection.json` verwendet `schema_version: 2` und speichert die bei der
Erzeugung verwendeten Grenzen. Ohne weitere Optionen gelten weiterhin die
bisherigen Werte: fünf Skills, drei Stationen, zwei Bildungsabschlüsse, ein
Projekt, drei Sprachen und zwei Leistungssätze je Station.

Eigene Grenzen gehören in eine JSON-Datei, beispielsweise:

```json
{
  "limits": {
    "skills": 6,
    "experience": 3,
    "education": 2,
    "projects": 1,
    "languages": 3,
    "achievement_sentences_per_experience": 2
  }
}
```

```text
python3 scripts/generate_cv_selection.py --job job.json --limits limits.json --output cv_selection.json
```

Der Generator prüft unbekannte Profil-IDs, doppelte IDs, negative Grenzen und
Überschreitungen, bevor LaTeX erzeugt wird. V1-Auswahldateien ohne
`schema_version` und `limits` bleiben mit den Standardgrenzen lesbar.

## Bewerbung aus einer Basis ableiten

Eine Basisbewerbung wird nur gelesen, niemals verändert oder in den Skill
kopiert:

```text
python3 scripts/prepare_application.py --slug 2026-10-company-role --base-application /absoluter/pfad/zur/basis
python3 scripts/generate_cv_selection.py --job job.json --base /absoluter/pfad/zur/basis/cv_selection.json --mode adaptive --output cv_selection.json
```

`prepare_application.py` validiert die Basis vor dem Anlegen des neuen Ordners.
`adaptive` ist der Standard: jobrelevante Datensätze gehen vor, bestehende
Auswahlentscheidungen füllen anschließend auf. `--mode strict` behält die
Auswahl der Basis bei. Die neue Auswahldatei enthält `derived_from` mit lokalem
Pfad, Hash und Modus; diese Provenienz wird nie in den CV gerendert.

## Einheitliches Inhaltsmodell und Migration

`application_content.json` ist die einzige V2-Quelle für Anschreiben und
Freitext. Sie enthält `job`, `cover_letter` und `plain_text`; ein vollständiges
fiktives Beispiel liegt unter `examples/application_content.json`. Pflichtfelder,
leere Absätze und unbekannte Template-Tokens führen vor dem Rendern zu einer
konkreten Fehlermeldung.

Die alten Dateien `cover_letter.json` und `indeed_text.json` werden in der
Übergangsphase noch von den jeweiligen Generatoren gelesen. Für die Migration:

```text
python3 scripts/convert_application_content.py --cover-letter cover_letter.json --indeed-text indeed_text.json --job job.json --profile /pfad/zum/master_profile.json --output application_content.json
```

## Tests

```text
python3 -m pytest
```

Die Tests verwenden ausschließlich fiktive Daten. Sie decken Limits,
Basisableitung, Inhaltsmigration, erfolgreiche PDF-Prüfung sowie fehlende PDFs,
mehrseitige CVs, Platzhalter, Überlauf, ungültige Schemas und zu leere CVs ab.
