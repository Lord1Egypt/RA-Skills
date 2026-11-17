# assets/

> English: `tessdata/` holds optional Tesseract language models for use without root.
> The published package ships none; install them via your package manager
> (`tesseract-ocr-<lang>`) or `bash scripts/install.sh --portable`.

`tessdata/` ist der Ablageort für Tesseract-Sprachmodelle ohne Root-Rechte.
**Das veröffentlichte Paket enthält hier keine Modelle** (`.clawhubignore`).
Die Modelle kommen aus dem signierten Paketmanager der Distribution:

```bash
sudo apt install tesseract-ocr tesseract-ocr-deu   # Debian/Ubuntu, osd und eng kommen mit
bash scripts/install.sh --portable --lang "deu eng"     # ohne root: Modelle hierher
```

`scripts/install.sh --portable` lädt die Pakete `tesseract-ocr-<lang>` mit
`apt-get download` aus dem Distributions-Repository und legt nur die
`.traineddata`-Dateien hier ab. Dabei wird nichts installiert und kein fremder
Code ausgeführt.

`scripts/ocr.sh` bindet Modelle aus diesem Ordner nur ein, wenn das System sie
nicht selbst mitbringt. Dafür legt es im privaten Temp-Verzeichnis ein
Merge-Verzeichnis aus Symlinks an. Systemmodelle bleiben unverändert.

`osd.traineddata` braucht man nur für `--psm 0/1`. Fehlt es, bricht `ocr.sh`
mit Exit 2 und dem Hinweis `apt install tesseract-ocr-osd` ab.

Eigene, zusätzlich trainierte `.traineddata`-Dateien können ebenfalls hier liegen.
Es sind reine Daten, keine ausführbaren Dateien.
