#!/usr/bin/env bash
#
# sm-ocr-scanner - Selbsttest
#
# Erzeugt synthetische Testdaten in einem Temp-Verzeichnis und prueft
# Funktion, Fehlerbehandlung und Exit-Codes von scripts/ocr.sh.
# Veraendert nichts ausserhalb des Temp-Verzeichnisses.
#
if [ -z "${BASH_VERSINFO:-}" ] || [ "${BASH_VERSINFO[0]}" -lt 4 ] || \
   { [ "${BASH_VERSINFO[0]}" -eq 4 ] && [ "${BASH_VERSINFO[1]}" -lt 4 ]; }; then
  echo "sm-ocr-scanner: bash >= 4.4 erforderlich (gefunden: ${BASH_VERSION:-unbekannt})" >&2
  exit 2
fi
set -uo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
readonly SCRIPT_DIR
readonly OCR="$SCRIPT_DIR/ocr.sh"
# Aufruf ueber bash: Pakete von ClawHub kommen ohne Ausfuehrungsrechte an
ocr() { bash "$OCR" "$@"; }
PATH="$HOME/.local/bin:$PATH"; export PATH

PASS=0; FAIL=0; SKIP=0
TD="$(mktemp -d "${TMPDIR:-/tmp}/sm-ocr-selftest-XXXXXX")"
# Aufraeumen nur des eigenen mktemp-Verzeichnisses, ohne Symlinks zu folgen
cleanup_td() {
  [[ "$TD" == */sm-ocr-selftest-* && -d "$TD" && ! -L "$TD" ]] || return 0
  find -P "$TD" -depth -delete 2>/dev/null || true
}
trap cleanup_td EXIT

green() { printf '\033[32m%s\033[0m' "$1"; }
red()   { printf '\033[31m%s\033[0m' "$1"; }
yellow(){ printf '\033[33m%s\033[0m' "$1"; }

check() {   # check <name> <erwarteter-exitcode> <cmd...>
  local name="$1" want="$2"; shift 2
  local out rc
  out="$("$@" 2>&1)"; rc=$?
  if [[ "$rc" == "$want" ]]; then
    printf '  %s %s\n' "$(green '[PASS]')" "$name"; ((PASS++))
  else
    printf '  %s %s (Exit %s, erwartet %s)\n' "$(red '[FAIL]')" "$name" "$rc" "$want"
    printf '%s\n' "$out" | sed 's/^/         /' | head -5
    ((FAIL++))
  fi
}

check_out() {  # check_out <name> <regex> <cmd...>
  local name="$1" re="$2"; shift 2
  local out
  out="$("$@" 2>/dev/null)"
  # Here-String statt Pipe: grep -q + pipefail kann sonst per SIGPIPE falsch scheitern
  if grep -qE -- "$re" <<<"$out"; then
    printf '  %s %s\n' "$(green '[PASS]')" "$name"; ((PASS++))
  else
    printf '  %s %s (Muster "%s" nicht gefunden)\n' "$(red '[FAIL]')" "$name" "$re"
    printf '%s\n' "$out" | sed 's/^/         /' | head -5
    ((FAIL++))
  fi
}

check_any() {  # wie check_out, wertet aber STDOUT und STDERR aus
  local name="$1" re="$2"; shift 2
  local out
  out="$("$@" 2>&1)"
  if grep -qE -- "$re" <<<"$out"; then
    printf '  %s %s\n' "$(green '[PASS]')" "$name"; ((PASS++))
  else
    printf '  %s %s (Muster "%s" nicht gefunden)\n' "$(red '[FAIL]')" "$name" "$re"
    printf '%s\n' "$out" | sed 's/^/         /' | head -5
    ((FAIL++))
  fi
}

skipped() { printf '  %s %s\n' "$(yellow '[SKIP]')" "$1"; ((SKIP++)); }

printf '\n\033[1msm-ocr-scanner - Selbsttest\033[0m\n'
printf 'Skript: %s\n' "$OCR"
[[ -r "$OCR" ]] || { printf '%s ocr.sh nicht lesbar\n' "$(red '[ABBRUCH]')"; exit 1; }

# --- Testdaten erzeugen -----------------------------------------------------
# Bild und PDF werden getrennt erzeugt: faellt eine Variante aus (z. B. Pillow
# ohne JPEG-Support), bleiben die uebrigen Tests trotzdem lauffaehig.
HAVE_IMG=0
make_png_pil() {
  python3 - "$TD" <<'PY' >/dev/null 2>&1
import sys, glob
from PIL import Image, ImageDraw, ImageFont
td = sys.argv[1]
c = glob.glob('/usr/share/fonts/**/DejaVuSans.ttf', recursive=True) \
  + glob.glob('/usr/share/fonts/**/*.ttf', recursive=True)
f = ImageFont.truetype(c[0], 40) if c else ImageFont.load_default()
img = Image.new('L', (1000, 200), 255)
d = ImageDraw.Draw(img)
d.text((30, 40),  "Rechnung ueber Pruefgebuehren", font=f, fill=0)
d.text((30, 110), "Betrag 1234 EUR", font=f, fill=0)
img.save(td + '/test.png')
PY
}
make_png_im() {
  convert -size 1000x200 xc:white -pointsize 40 -fill black \
    -annotate +30+80 "Rechnung ueber Pruefgebuehren" \
    -annotate +30+150 "Betrag 1234 EUR" "$TD/test.png" >/dev/null 2>&1
}
make_pdf_pil() {
  python3 - "$TD" <<'PY' >/dev/null 2>&1
import sys
from PIL import Image
td = sys.argv[1]
im = Image.open(td + '/test.png').convert('RGB')
im.save(td + '/scan.pdf', save_all=True, append_images=[im], resolution=300.0)
im.save(td + '/one.pdf', resolution=300.0)
PY
}
make_pdf_img2pdf() {
  img2pdf -o "$TD/scan.pdf" "$TD/test.png" "$TD/test.png" >/dev/null 2>&1 \
    && img2pdf -o "$TD/one.pdf" "$TD/test.png" >/dev/null 2>&1
}
make_pdf_im() {
  convert "$TD/test.png" "$TD/test.png" "$TD/scan.pdf" >/dev/null 2>&1 \
    && convert "$TD/test.png" "$TD/one.pdf" >/dev/null 2>&1
}

command -v python3 >/dev/null 2>&1 && make_png_pil
[[ -s "$TD/test.png" ]] || { command -v convert >/dev/null 2>&1 && make_png_im; }
[[ -s "$TD/test.png" ]] && HAVE_IMG=1

if [[ $HAVE_IMG -eq 1 ]]; then
  make_pdf_pil || true
  [[ -s "$TD/scan.pdf" ]] || { command -v img2pdf >/dev/null 2>&1 && make_pdf_img2pdf; } || true
  [[ -s "$TD/scan.pdf" ]] || { command -v convert  >/dev/null 2>&1 && make_pdf_im; }    || true
fi

printf 'Testdaten: %s\n\n' "$TD"

# --- 1. Basis ---------------------------------------------------------------
printf '\033[1m1. Grundfunktionen\033[0m\n'
check     "--version"                0 ocr -V
check     "--help"                   0 ocr -h
check     "--check"                  0 ocr --check
check     "Aufruf ohne Argumente"    1 ocr

# --- 2. Parameterpruefung ---------------------------------------------------
printf '\n\033[1m2. Parameterpruefung\033[0m\n'
check     "unbekannte Option"        1 ocr --gibtsnicht x.png
check     "DPI ausserhalb Bereich"   1 ocr --dpi 9999 x.png
check     "PSM ausserhalb Bereich"   1 ocr --psm 99 x.png
check     "OEM ausserhalb Bereich"   1 ocr --oem 9 x.png
check     "ungueltiges Format"       1 ocr -f xml x.png
# Injection-Versuch mit harmloser Kanarie: Wuerde --lang je ausgewertet,
# entstuende die Datei. Pruefung: Exit 1 UND keine Kanarie.
check     "Shell-Injection in --lang abgewiesen" 1 ocr -l "eng;touch $TD/kanarie" x.png
check     "Kommandosubstitution in --lang"   1 ocr -l "eng\$(touch $TD/kanarie)" x.png
if [[ ! -e "$TD/kanarie" ]]; then
  printf '  %s Injection nicht ausgefuehrt (keine Kanarie)\n' "$(green '[PASS]')"; ((PASS++))
else
  printf '  %s Injection wurde ausgefuehrt (Kanarie vorhanden)\n' "$(red '[FAIL]')"; ((FAIL++))
fi
check     "--format pdf ohne --out"  1 ocr -f pdf x.png
check     "fehlende Datei"           1 ocr -l eng "$TD/gibtsnicht.png"
check     "DPI mit fuehrender Null"  1 ocr --dpi 0300 x.png
check     "--max-pages 0"            1 ocr --max-pages 0 x.png
check     "--timeout keine Zahl"     1 ocr --timeout 5m x.png
check     "Verzeichnis als --out"    1 ocr -l eng -o "$TD" x.png

# --- 3. OCR -----------------------------------------------------------------
printf '\n\033[1m3. OCR-Funktion\033[0m\n'
if [[ $HAVE_IMG -eq 1 ]]; then
  check_out "Bild -> Text"           'Rechnung'  ocr -l eng "$TD/test.png"
  check_out "TSV-Ausgabe"            'conf'      ocr -l eng -f tsv "$TD/test.png"
  check     "Ausgabe in Datei"       0           ocr -l eng -o "$TD/out.txt" "$TD/test.png"
  check     "Overwrite-Schutz"       1           ocr -l eng -o "$TD/out.txt" "$TD/test.png"
  check     "--overwrite erlaubt"    0           ocr -l eng -o "$TD/out.txt" --overwrite "$TD/test.png"
  if [[ -f "$TD/out.txt" ]]; then
    if [[ "$(stat -c '%a' "$TD/out.txt" 2>/dev/null)" == "600" ]]; then
      printf '  %s Ausgabedatei mit Modus 600\n' "$(green '[PASS]')"; ((PASS++))
    else
      printf '  %s Ausgabedatei nicht 600 (ist %s)\n' "$(red '[FAIL]')" "$(stat -c '%a' "$TD/out.txt")"; ((FAIL++))
    fi
  fi
  cp "$TD/test.png" "$TD/datei mit leerzeichen.png"
  check_out "Dateiname mit Leerzeichen" 'Rechnung' ocr -l eng "$TD/datei mit leerzeichen.png"
  cp "$TD/test.png" "$TD/-fuehrender-bindestrich.png"
  check_out "Dateiname mit fuehrendem -" 'Rechnung' ocr -l eng -- "$TD/-fuehrender-bindestrich.png"
  printf 'kein Bild\n' > "$TD/text.txt"
  check     "nicht unterstuetzter Typ" 1 ocr -l eng "$TD/text.txt"
  printf '<?xml version="1.0"?>\n<svg width="10" height="10"></svg>\n' > "$TD/vektor.svg"
  check     "SVG wird abgelehnt (nur Rasterformate)" 1 ocr -l eng "$TD/vektor.svg"
  # Symlink als Ausgabeziel: ohne --overwrite weder schreiben noch dem Link folgen
  ln -s "$TD/link-ziel.txt" "$TD/link.txt"
  check     "Symlink als --out abgewiesen" 1 ocr -l eng -o "$TD/link.txt" "$TD/test.png"
  if [[ ! -e "$TD/link-ziel.txt" ]]; then
    printf '  %s Symlink-Ziel unberuehrt\n' "$(green '[PASS]')"; ((PASS++))
  else
    printf '  %s Symlink-Ziel wurde beschrieben\n' "$(red '[FAIL]')"; ((FAIL++))
  fi
  # Bild -> durchsuchbares PDF: exakt der angegebene Name, Modus 600
  check     "Bild -> PDF unter exaktem Namen" 0 ocr -l eng -f pdf -o "$TD/bild-ocr" "$TD/test.png"
  if [[ -f "$TD/bild-ocr" && "$(stat -c '%a' "$TD/bild-ocr" 2>/dev/null)" == "600" ]]; then
    printf '  %s PDF-Ausgabe vorhanden, Modus 600\n' "$(green '[PASS]')"; ((PASS++))
  else
    printf '  %s PDF-Ausgabe fehlt oder Modus nicht 600\n' "$(red '[FAIL]')"; ((FAIL++))
  fi
else
  skipped "Bildtests (weder Pillow noch ImageMagick verfuegbar)"
fi

# --- 4. Deutsch -------------------------------------------------------------
printf '\n\033[1m4. Deutsches Sprachmodell\033[0m\n'
CHECK_OUT="$(ocr --check 2>/dev/null)"
if [[ $HAVE_IMG -eq 1 ]] && grep -qE '^(Systemmodelle|Bundle-Modelle):.*\bdeu\b' <<<"$CHECK_OUT"; then
  check_out "OCR mit -l deu"         'Rechnung'  ocr -l deu "$TD/test.png"
else
  skipped "deu nicht verfuegbar (scripts/install.sh ausfuehren)"
fi

# --- 5. PDF -----------------------------------------------------------------
printf '\n\033[1m5. PDF-Verarbeitung\033[0m\n'
if [[ -f "$TD/scan.pdf" ]] && command -v pdftoppm >/dev/null 2>&1; then
  check_out "gescanntes PDF -> Text"      'Seite 1'  ocr -l eng "$TD/scan.pdf"
  check_out "mehrseitig (Seite 2)"        'Seite 2'  ocr -l eng "$TD/scan.pdf"
  check     "PDF -> durchsuchbares PDF"   0          ocr -l eng -f pdf -o "$TD/ocr.pdf" "$TD/scan.pdf"
  if [[ "$(stat -c '%a' "$TD/ocr.pdf" 2>/dev/null)" == "600" ]]; then
    printf '  %s durchsuchbares PDF mit Modus 600\n' "$(green '[PASS]')"; ((PASS++))
  else
    printf '  %s durchsuchbares PDF nicht 600\n' "$(red '[FAIL]')"; ((FAIL++))
  fi
  check_any "Hinweis auf temporaere Seitenbilder" 'HINWEIS' ocr -l eng "$TD/scan.pdf"
  out_q="$(ocr -l eng -q "$TD/scan.pdf" 2>&1 >/dev/null)"
  if ! grep -q 'HINWEIS' <<<"$out_q"; then
    printf '  %s --quiet unterdrueckt den Hinweis\n' "$(green '[PASS]')"; ((PASS++))
  else
    printf '  %s --quiet unterdrueckt den Hinweis nicht\n' "$(red '[FAIL]')"; ((FAIL++))
  fi
  if command -v pdfinfo >/dev/null 2>&1; then
    check   "Seitengrenze --max-pages 1 bei 2 Seiten" 1 ocr -l eng --max-pages 1 "$TD/scan.pdf"
  else
    skipped "Seitengrenze (pdfinfo fehlt)"
  fi
  # Regression 1.1.0: Seitenbilder des ersten PDF duerfen nicht ins zweite geraten
  if [[ -f "$TD/one.pdf" ]]; then
    n="$(ocr -l eng -q "$TD/scan.pdf" "$TD/one.pdf" 2>/dev/null | grep -c -- '^--- Seite ')"
    if [[ "$n" == "3" ]]; then
      printf '  %s Stapel 2+1 Seiten ergibt 3 Seiten\n' "$(green '[PASS]')"; ((PASS++))
    else
      printf '  %s Stapel 2+1 Seiten ergibt %s Seiten (Vermischung)\n' "$(red '[FAIL]')" "$n"; ((FAIL++))
    fi
  else
    skipped "Stapel-Regression (one.pdf fehlt)"
  fi
  if command -v pdftotext >/dev/null 2>&1 && [[ -f "$TD/ocr.pdf" ]]; then
    if [[ "$(pdftotext "$TD/ocr.pdf" - 2>/dev/null)" == *Rechnung* ]]; then
      printf '  %s Textlayer im erzeugten PDF\n' "$(green '[PASS]')"; ((PASS++))
    else
      printf '  %s Textlayer im erzeugten PDF fehlt\n' "$(red '[FAIL]')"; ((FAIL++))
    fi
    check_any "Textlayer wird erkannt" 'Textlayer' \
      env OCR_TEXTLAYER_MIN=40 bash "$OCR" -l eng -v "$TD/ocr.pdf"
    check_any "--force-ocr erzwingt Rasterung" 'Seite 1' \
      env OCR_TEXTLAYER_MIN=40 bash "$OCR" -l eng --force-ocr "$TD/ocr.pdf"
  fi
else
  skipped "PDF-Tests (poppler-utils oder Testdaten fehlen)"
fi

# --- 6. Installer (nur Probelaeufe, veraendert nichts) ------------------------
printf '\n\033[1m6. Installer (dry-run)\033[0m\n'
INST="$SCRIPT_DIR/install.sh"
TESSDATA_BEFORE=0; [[ -e "${SCRIPT_DIR%/*}/assets/tessdata" ]] && TESSDATA_BEFORE=1
check "install.sh --help"                         0 bash "$INST" --help
check "install.sh unbekannte Option"              1 bash "$INST" --gibtsnicht
check "install.sh ungueltiger Sprachcode"         1 bash "$INST" --dry-run --lang 'de;x'
check "dry-run portabel"                          0 bash "$INST" --dry-run --portable
check "dry-run portabel --no-ocrmypdf (Exit 0)"   0 bash "$INST" --dry-run --portable --no-ocrmypdf
if [[ $TESSDATA_BEFORE -eq 1 || ! -e "${SCRIPT_DIR%/*}/assets/tessdata" ]]; then
  printf '  %s dry-run legt nichts an\n' "$(green '[PASS]')"; ((PASS++))
else
  printf '  %s dry-run hat assets/tessdata angelegt\n' "$(red '[FAIL]')"; ((FAIL++))
fi
# Verhalten statt Textsuche: ohne root bleibt der Installer immer portabel
if [[ "$(id -u)" -ne 0 ]]; then
  check_out "ohne root: portabler Modus, keine Systeminstallation" 'portabel \(kein root\)' \
    bash "$INST" --dry-run
else
  skipped "Pruefung 'ohne root portabel' (Selbsttest laeuft als root)"
fi

# --- 7. Hygiene -------------------------------------------------------------
printf '\n\033[1m7. Hygiene\033[0m\n'
LEFT="$(find "${TMPDIR:-/tmp}" -maxdepth 1 -type d -name 'sm-ocr-????????' -mmin -5 2>/dev/null | wc -l)"
if [[ "$LEFT" -eq 0 ]]; then
  printf '  %s keine Temp-Reste\n' "$(green '[PASS]')"; ((PASS++))
else
  printf '  %s %s Temp-Verzeichnis(se) nicht aufgeraeumt\n' "$(red '[FAIL]')" "$LEFT"; ((FAIL++))
fi
EXTRA="$(find "${SCRIPT_DIR%/*}" -type f \( -name '*.py' -o -name '*.js' -o -name '*.exe' \) 2>/dev/null)"
if [[ -z "$EXTRA" ]]; then
  printf '  %s keine undeklarierten Hilfsprogramme im Paket\n' "$(green '[PASS]')"; ((PASS++))
else
  printf '  %s undeklarierte Dateien im Paket: %s\n' "$(red '[FAIL]')" "$EXTRA"; ((FAIL++))
fi
if command -v shellcheck >/dev/null 2>&1; then
  check "shellcheck -S warning" 0 shellcheck -S warning "$OCR" "$SCRIPT_DIR/install.sh" "$SCRIPT_DIR/selftest.sh"
else
  skipped "shellcheck nicht installiert"
fi

# --- Ergebnis ---------------------------------------------------------------
printf '\n\033[1mErgebnis:\033[0m %s bestanden, %s fehlgeschlagen, %s uebersprungen\n\n' \
  "$(green "$PASS")" "$( ((FAIL)) && red "$FAIL" || printf '0' )" "$SKIP"
(( FAIL == 0 ))
