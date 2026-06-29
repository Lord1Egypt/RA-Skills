# Print Assistant

Ein Projekt, das Drucken, PDF-Bearbeitung, Office-Bearbeitung und Foto-Bearbeitung über natürlichsprachliche Anweisungen im Chat steuert. Datei reinziehen, in eigenen Worten beschreiben was passieren soll, Claude Code erledigt den Rest – inklusive direktem Druck ohne Rückfrage.

## Grundprinzip

- Der Nutzer beschreibt das gewünschte Ergebnis in eigenen Worten (kein technisches Vokabular nötig).
- Claude Code übersetzt das in konkrete Parameter und führt sie aus.
- **Drucken passiert direkt, ohne Bestätigung**, sobald die Anweisung eindeutig verstanden ist. Bei Unklarheit (z. B. unklare Seitenzahl, fehlendes Papierformat) kurz nachfragen statt zu raten.
- Mehrgeräte-Setup: PC (RTX 2070) und Surface Pro 7, beide Windows. Geräteabhängige Werte (Drucker) liegen in `config/printers.yaml`, gekeyt nach Hostname.

## Tool-Routing

| Aufgabe | Werkzeug |
|---|---|
| PDF: Merge, Split, Rotation, Wasserzeichen, Seitenbereich | `pypdf` / `pikepdf` (`scripts/pdf_tools.py`) |
| PDF: reinen Text ändern | **nicht automatisierbar** – Nutzer auf Acrobat verweisen |
| PDF verkleinern / optimieren | `pdf_tools.compress_pdf()` (pikepdf) |
| Office (Word/Excel/PowerPoint): Inhalte bearbeiten | `python-docx`, `openpyxl`, `python-pptx` (`scripts/office_tools.py`) |
| Office → PDF konvertieren (vor dem Drucken) | LibreOffice headless |
| PDF drucken | SumatraPDF CLI (`scripts/print.py`) |
| Foto/Bild drucken | `scripts/print.py` (Pillow + win32print) |
| Office-Datei drucken | erst → PDF (LibreOffice), dann SumatraPDF |

Faustregel: Python zuerst für strukturelle/mechanische Änderungen. Adobe-Connector für alles Optische/KI-gestützte.

## Adobe CC – Tool-Routing

| Aufgabe | Adobe-Tool |
|---|---|
| Belichtung, Helligkeit, Kontrast korrigieren | `image_adjust_exposure` / `image_adjust_brightness_and_contrast` |
| Weißabgleich / Farbtemperatur | `image_adjust_color_temperature` |
| Highlights & Schatten | `image_adjust_highlights` / `image_adjust_dark_portions` / `image_adjust_light_portions` |
| Sättigung, Vibrance | `image_adjust_vibrance_and_saturation` |
| Einzelne Farbe entsättigen / boosten | `image_adjust_single_color_saturation` |
| HSL (Farbton, Sättigung, Helligkeit) | `image_adjust_hsl` |
| Alles auf einmal (mehrere Anpassungen) | `image_apply_adjustments` |
| Automatische Tonkorrektur | `image_apply_auto_tone` |
| Lightroom-Preset anwenden | `image_apply_preset` (verfügbare Presets: `image_list_presets`) |
| Gerade richten | `image_auto_straighten` |
| Zuschneiden / auf Druckformat bringen | `image_crop_and_resize` / `image_crop_to_bounds` |
| Bild KI-gestützt erweitern (Seitenverhältnis passt nicht) | `image_generative_expand` |
| Hintergrund entfernen (Freistellen) | `image_remove_background` |
| Motiv auswählen | `image_select_subject` |
| Bereich per Text auswählen | `image_select_by_prompt` |
| Bereich generativ auffüllen / ersetzen | `image_fill_area` |
| Foto/Logo vektorisieren (für skalierbaren Druck) | `image_vectorize` |
| Mehrere Fotos einheitlich bearbeiten (gleicher Look) | Skill `adobe-batch-edit-photos` |
| Datei zu PDF konvertieren (Alternative zu LibreOffice) | `document_convert_pdf` |
| CSV + InDesign-Template → personalisierte PDFs | `document_merge_data_layout` |
| Unschärfe (Hintergrund weichzeichnen) | `image_apply_gaussian_blur` / `image_apply_lens_blur` |
| Stileffekte (Körnung, Rauschen, Halftone, Tint) | `image_add_grain` / `image_add_noise` / `image_apply_halftone` / `image_apply_monochromatic_tint` |

### Was Adobe CC nicht kann (direkt sagen, nicht versuchen)
- PDF-Text bearbeiten ✗
- Bild über natürliche Auflösung hinaus hochskalieren ✗
- Hintergrund generativ neu erstellen (nur entfernen) ✗

## Druck-Workflow (SumatraPDF)

1. Eingabedatei identifizieren (Typ per Endung/MIME).
2. Falls Office-Datei: erst mit LibreOffice headless zu PDF konvertieren.
3. Aus der Nutzerbeschreibung Druckparameter ableiten: Papierformat, Ausrichtung, Duplex, Farbe/SW, Skalierung, Seitenbereich, Kopienzahl.
4. Zieldrucker aus `config/printers.yaml` anhand Hostname auflösen (falls Nutzer keinen explizit nennt).
5. SumatraPDF mit `-print-to` + `-print-settings` aufrufen.
6. Kurze Erfolgsmeldung im Chat (kein Vorschau-Zwang, da direkt gedruckt wird).

## Konventionen

- Niemals Platzhalter-Code wie "// Rest wie vorher" – immer vollständige Skripte/Funktionen.
- Sprache: Deutsch oder Englisch. Andere Sprachen automatisch übersetzen.
- Bei Adobe-Connector-Aufrufen: Tool-Limitierungen beachten (kein PDF-Textediting, kein Upscaling, keine generative Hintergrund-Ersetzung) – wenn eine Anfrage das verlangt, das dem Nutzer kurz sagen statt es stillschweigend zu versuchen.
- Geräteerkennung über `socket.gethostname()` in Python, Mapping in `config/printers.yaml`.
- **Vorschau-Workflow**: `preview_pdf()` aufrufen, PNG als `preview.png` in den Projektordner kopieren und dem Nutzer sagen, er soll es im VS Code Explorer anklicken. `Start-Process`/`Invoke-Item` funktionieren nicht (Sandbox). `SendUserFile` und `Read` zeigen keine Bilder inline im VSCode-Chat.

## Einmaliges Setup pro Gerät

```bash
# 1. Python-Abhängigkeiten installieren
pip install -r requirements.txt

# 2. SumatraPDF installieren (für PDF-Druck)
#    https://www.sumatrapdfreader.org/download-free-pdf-viewer

# 3. LibreOffice installieren (für Office→PDF-Konvertierung)
#    https://www.libreoffice.org/download/download/

# 4. Druckernamen eintragen (echte Namen per Befehl ermitteln):
#    wmic printer get name
#    Dann config/printers.yaml editieren – Platzhalter <HOSTNAME-...> durch
#    echten Hostnamen (socket.gethostname()) und <Druckername-...> durch
#    den exakten Windows-Druckernamen ersetzen.

# 5. Adobe MCP-Connector authentifizieren (einmalig pro Gerät):
#    In Claude Code: /mcp  → adobe-creativity → einloggen
```

## Einrichtung auf neuem Gerät

```powershell
git clone https://github.com/nilsgollub/PrintAssist.git
cd PrintAssist
powershell -ExecutionPolicy Bypass -File setup.ps1
# danach: /mcp -> adobe-creativity einloggen (optional)
```

`setup.ps1` erkennt Drucker automatisch und schreibt `config/printers.yaml`.
Die Datei ist gitignored — jedes Gerät hat seine eigene lokale Kopie.

## Mittelfristig: Android-Anbindung via Claude Dispatch

Claude Dispatch (Claude Mobile App → "Claude arbeitet von Ihrem Computer aus") ist die
sauberste Lösung: Datei vom Handy schicken, Druckanweisung in Freitext, Claude führt
die Skripte direkt aus – kein Telegram-Bot, kein extra Setup.

**Voraussetzung:** Ein dauerhaft laufendes Gerät (Homeserver geplant).
Die Skripte (print.py, pdf_tools.py, office_tools.py) sind bereits Dispatch-kompatibel –
kein Umbau nötig, sobald der Server steht.
