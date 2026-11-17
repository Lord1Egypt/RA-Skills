#!/usr/bin/env bash
#
# sm-ocr-scanner - Installation der Abhaengigkeiten
#
# Modus A (vom Benutzer als root gestartet): Systeminstallation ueber den
#          Paketmanager. Das Skript erhoeht seine Rechte nie selbst; die
#          Erhoehung ist ausschliesslich ein bewusster Schritt des Benutzers.
#          Der Paketmanager fragt vor jeder Installation nach.
# Modus B (ohne root): portable Installation ohne Systemrechte -
#          Sprachmodelle nach assets/tessdata,
#          ocrmypdf via pip --user nur mit --allow-pip.
#
# Idempotent: bereits vorhandene Komponenten werden uebersprungen.
#
# NETZWERK: Dieses Skript ist der einzige Teil des Skills, der das Netz
# benutzt, und nur ueber den Paketmanager der Distribution (signierte
# Repositories). PyPI wird ausschliesslich mit --allow-pip kontaktiert.
# ocr.sh selbst arbeitet vollstaendig offline.
#
if [ -z "${BASH_VERSINFO:-}" ] || [ "${BASH_VERSINFO[0]}" -lt 4 ] || \
   { [ "${BASH_VERSINFO[0]}" -eq 4 ] && [ "${BASH_VERSINFO[1]}" -lt 4 ]; }; then
  echo "sm-ocr-scanner: bash >= 4.4 erforderlich (gefunden: ${BASH_VERSION:-unbekannt})" >&2
  exit 2
fi
set -Eeuo pipefail

readonly SCRIPT_NAME="${0##*/}"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
readonly SCRIPT_DIR
readonly SKILL_DIR="${SCRIPT_DIR%/*}"
readonly BUNDLE_TESSDATA="$SKILL_DIR/assets/tessdata"

LANGS_WANTED="deu eng"
WITH_OCRMYPDF=1
ALLOW_PIP=0
DRY_RUN=0
FORCE_PORTABLE=0

info() { printf '\033[1m==>\033[0m %s\n' "$*"; }
ok()   { printf '    [ok]   %s\n' "$*"; }
skip() { printf '    [skip] %s\n' "$*"; }
warn() { printf '    [WARN] %s\n' "$*" >&2; }
die()  { printf '\033[1;31m[%s] ERROR:\033[0m %s\n' "$SCRIPT_NAME" "$1" >&2; exit "${2:-1}"; }

run() {
  if [[ $DRY_RUN -eq 1 ]]; then printf '    [dry]  %s\n' "$*"; return 0; fi
  "$@"
}

# purge_workdir <verzeichnis> - loescht nur ein eigenes mktemp-Arbeitsverzeichnis,
# folgt keinem Symlink.
purge_workdir() {
  local d="$1"
  [[ "$d" == */sm-ocr-inst-* && -d "$d" && ! -L "$d" ]] || return 0
  find -P "$d" -depth -delete 2>/dev/null || true
}

usage() {
  cat <<'USAGE'
sm-ocr-scanner - Installer

VERWENDUNG
  bash scripts/install.sh [OPTIONEN]

OPTIONEN
  --lang "deu eng"   zu installierende Sprachmodelle (Default: "deu eng")
  --no-ocrmypdf      ocrmypdf nicht installieren (Fallback pdfunite genuegt)
  --portable         Systeminstallation ueberspringen, Sprachmodelle ins
                     Skill-Verzeichnis (kein root noetig)
  --allow-pip        im portablen Modus ocrmypdf von PyPI nach ~/.local laden
                     (ohne diese Option wird PyPI nie kontaktiert)
  --dry-run          nur anzeigen, was getan wuerde
  -h, --help         diese Hilfe

RECHTE
  Das Skript ruft selbst kein sudo auf. Fuer die Systeminstallation startet
  der Benutzer es bewusst als root. Der Paketmanager zeigt dann die Pakete
  und fragt nach Bestaetigung; ohne Terminal bricht die Systeminstallation ab.

BEISPIELE
  sudo bash scripts/install.sh                     # Systeminstallation (fragt nach)
  bash scripts/install.sh --portable               # ohne root, Modelle ins Paket
  bash scripts/install.sh --portable --allow-pip   # zusaetzlich ocrmypdf via PyPI
  bash scripts/install.sh --lang "deu eng fra" --dry-run
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --lang)        [[ $# -ge 2 ]] || die "--lang benoetigt einen Wert"; LANGS_WANTED="$2"; shift 2 ;;
    --no-ocrmypdf) WITH_OCRMYPDF=0; shift ;;
    --portable)    FORCE_PORTABLE=1; shift ;;
    --allow-pip)   ALLOW_PIP=1; shift ;;
    --dry-run)     DRY_RUN=1; shift ;;
    -h|--help)     usage; exit 0 ;;
    *)             die "unbekannte Option: $1" ;;
  esac
done

for l in $LANGS_WANTED; do
  [[ "$l" =~ ^[a-z_]{3,}$ ]] || die "ungueltiger Sprachcode: $l"
done

# ------------------------------------------------------- Rechte ermitteln --
# Kein automatisches Erhoehen: ohne root immer portabel.
IS_ROOT=0; [[ "$(id -u)" -eq 0 ]] && IS_ROOT=1
if [[ $FORCE_PORTABLE -eq 0 && $IS_ROOT -eq 0 ]]; then
  FORCE_PORTABLE=1
  NO_ROOT_HINT=1
else
  NO_ROOT_HINT=0
fi

# --------------------------------------------------- Paketmanager erkennen --
# Bewusst ohne automatische Bestaetigung: der Mensch bestaetigt jede Installation.
PM=""; PM_INSTALL=""; PM_UPDATE=""
detect_pm() {
  if   command -v apt-get >/dev/null 2>&1; then PM=apt;    PM_UPDATE="apt-get update -qq"; PM_INSTALL="apt-get install"
  elif command -v dnf     >/dev/null 2>&1; then PM=dnf;    PM_UPDATE="true";               PM_INSTALL="dnf install"
  elif command -v yum     >/dev/null 2>&1; then PM=yum;    PM_UPDATE="true";               PM_INSTALL="yum install"
  elif command -v zypper  >/dev/null 2>&1; then PM=zypper; PM_UPDATE="true";               PM_INSTALL="zypper install"
  elif command -v pacman  >/dev/null 2>&1; then PM=pacman; PM_UPDATE="true";               PM_INSTALL="pacman -S --needed"
  elif command -v apk     >/dev/null 2>&1; then PM=apk;    PM_UPDATE="true";               PM_INSTALL="apk add --interactive"
  elif command -v brew    >/dev/null 2>&1; then PM=brew;   PM_UPDATE="true";               PM_INSTALL="brew install"
  fi
}
detect_pm

pkg_name() {   # pkg_name <komponente> [sprache]
  case "$PM:$1" in
    apt:tesseract)    echo "tesseract-ocr" ;;
    apt:lang)         echo "tesseract-ocr-$2" ;;
    apt:poppler)      echo "poppler-utils" ;;
    apt:ghostscript)  echo "ghostscript" ;;
    apt:ocrmypdf)     echo "ocrmypdf" ;;
    dnf:tesseract|yum:tesseract|zypper:tesseract) echo "tesseract" ;;
    dnf:lang|yum:lang)     echo "tesseract-langpack-$2" ;;
    zypper:lang)           echo "tesseract-ocr-traineddata-$2" ;;
    dnf:poppler|yum:poppler|zypper:poppler) echo "poppler-utils" ;;
    dnf:ghostscript|yum:ghostscript|zypper:ghostscript) echo "ghostscript" ;;
    dnf:ocrmypdf|yum:ocrmypdf|zypper:ocrmypdf) echo "ocrmypdf" ;;
    pacman:tesseract) echo "tesseract" ;;
    pacman:lang)      echo "tesseract-data-$2" ;;
    pacman:poppler)   echo "poppler" ;;
    pacman:ghostscript) echo "ghostscript" ;;
    pacman:ocrmypdf)  echo "ocrmypdf" ;;
    apk:tesseract)    echo "tesseract-ocr" ;;
    apk:lang)         echo "tesseract-ocr-data-$2" ;;
    apk:poppler)      echo "poppler-utils" ;;
    apk:ghostscript)  echo "ghostscript" ;;
    apk:ocrmypdf)     echo "ocrmypdf" ;;
    brew:tesseract)   echo "tesseract" ;;
    brew:lang)        echo "tesseract-lang" ;;
    brew:poppler)     echo "poppler" ;;
    brew:ghostscript) echo "ghostscript" ;;
    brew:ocrmypdf)    echo "ocrmypdf" ;;
    *)                echo "" ;;
  esac
}

# grep ohne -q liest die Eingabe ganz: kein SIGPIPE-Fehlschlag unter pipefail
have_lang() { tesseract --list-langs 2>/dev/null | tail -n +2 | grep -x -- "$1" >/dev/null; }

# ------------------------------------------------------------- Modus A: root --
install_system() {
  info "Systeminstallation ueber $PM"
  local pkgs=() p
  command -v tesseract >/dev/null 2>&1 || pkgs+=("$(pkg_name tesseract)")
  command -v pdftoppm  >/dev/null 2>&1 || pkgs+=("$(pkg_name poppler)")
  if [[ $WITH_OCRMYPDF -eq 1 ]] && ! command -v ocrmypdf >/dev/null 2>&1; then
    pkgs+=("$(pkg_name ghostscript)" "$(pkg_name ocrmypdf)")
  fi
  for l in $LANGS_WANTED; do
    have_lang "$l" || { p="$(pkg_name lang "$l")"; [[ -n "$p" ]] && pkgs+=("$p"); }
  done
  # Duplikate entfernen, Leereintraege raus
  mapfile -t pkgs < <(printf '%s\n' "${pkgs[@]}" | awk 'NF' | sort -u)
  if (( ${#pkgs[@]} == 0 )); then ok "alle Systempakete bereits vorhanden"; return 0; fi
  info "zu installieren: ${pkgs[*]}"
  if [[ $DRY_RUN -eq 0 && ! -t 0 ]]; then
    die "Systeminstallation braucht eine Bestaetigung am Paketmanager, aber STDIN ist kein Terminal.
       Bitte in einem Terminal ausfuehren, oder ohne root: bash scripts/install.sh --portable" 1
  fi
  # shellcheck disable=SC2086
  run $PM_UPDATE || warn "Paketlisten-Update fehlgeschlagen - fahre fort"
  # shellcheck disable=SC2086
  run $PM_INSTALL "${pkgs[@]}" || die "Paketinstallation abgebrochen oder fehlgeschlagen" 2
  ok "Systempakete installiert"
}

# --------------------------------------------------------- Modus B: portabel --
install_lang_portable() {   # nur apt-basierte Systeme koennen .deb ziehen
  local l="$1"
  have_lang "$l" && { skip "Sprachmodell '$l' bereits im System"; return 0; }
  [[ -r "$BUNDLE_TESSDATA/$l.traineddata" ]] && { skip "Sprachmodell '$l' bereits in assets/tessdata/"; return 0; }

  if command -v apt-get >/dev/null 2>&1; then
    info "lade Sprachmodell '$l' via apt-get download (ohne root)"
    # Probelauf: nichts anlegen, nichts laden
    if [[ $DRY_RUN -eq 1 ]]; then
      printf '    [dry]  apt-get download tesseract-ocr-%s -> %s\n' "$l" "$BUNDLE_TESSDATA"
      return 0
    fi
    mkdir -p "$BUNDLE_TESSDATA"
    local w; w="$(mktemp -d "${TMPDIR:-/tmp}/sm-ocr-inst-XXXXXX")"
    (
      umask 027   # Modell landet mit Modus 640
      cd "$w"
      apt-get download "tesseract-ocr-$l" >/dev/null 2>&1 || exit 1
      for f in ./*.deb; do dpkg-deb -x "$f" ex/; done
      find ex -name "$l.traineddata" -exec cp -f {} "$BUNDLE_TESSDATA/" \;
    ) || { purge_workdir "$w"; warn "Download von tesseract-ocr-$l fehlgeschlagen"; return 1; }
    purge_workdir "$w"
    [[ -r "$BUNDLE_TESSDATA/$l.traineddata" ]] \
      && { ok "Sprachmodell '$l' -> assets/tessdata/"; } \
      || { warn "Sprachmodell '$l' konnte nicht extrahiert werden"; return 1; }
  else
    warn "kein apt-get - Sprachmodell '$l' bitte manuell nach assets/tessdata/ legen"
    warn "  Quelle: Paket tesseract-ocr-$l der Distribution oder das offizielle Projekt tesseract-ocr/tessdata_fast"
    return 1
  fi
}

install_ocrmypdf_portable() {
  command -v ocrmypdf >/dev/null 2>&1 && { skip "ocrmypdf bereits vorhanden"; return 0; }
  command -v gs >/dev/null 2>&1 || {
    warn "ghostscript fehlt - ocrmypdf laesst sich ohne root nicht sinnvoll betreiben"
    warn "  Fallback pdftoppm+pdfunite bleibt aktiv, --format pdf funktioniert weiterhin"
    return 1
  }
  if [[ $ALLOW_PIP -eq 0 ]]; then
    skip "ocrmypdf via PyPI nicht freigegeben (--allow-pip) - Fallback pdfunite bleibt aktiv"
    return 0
  fi
  command -v pip3 >/dev/null 2>&1 || { warn "pip3 fehlt - ocrmypdf uebersprungen"; return 1; }
  info "installiere ocrmypdf via pip --user (Quelle: PyPI, freigegeben per --allow-pip)"
  run pip3 install --user --quiet --disable-pip-version-check ocrmypdf \
    || { warn "pip-Installation fehlgeschlagen - Fallback bleibt aktiv"; return 1; }
  ok "ocrmypdf installiert nach ~/.local/bin"
  case ":$PATH:" in
    *":$HOME/.local/bin:"*) : ;;
    *) warn "$HOME/.local/bin steht nicht in PATH - bitte selbst in die PATH-Variable aufnehmen" ;;
  esac
}

install_portable() {
  info "portable Installation (kein root)"
  if [[ $NO_ROOT_HINT -eq 1 ]]; then
    skip "keine Systeminstallation: Skript laeuft ohne root (fuer Systempakete bewusst als root starten)"
  fi
  command -v tesseract >/dev/null 2>&1 \
    || die "tesseract ist nicht installiert und laesst sich ohne root nicht nachruesten.
       Systeminstallation bewusst als root starten:  sudo bash scripts/install.sh" 2
  command -v pdftoppm >/dev/null 2>&1 \
    || warn "poppler-utils fehlt - PDF-Verarbeitung nicht moeglich (Paket: $(pkg_name poppler))"
  for l in $LANGS_WANTED; do install_lang_portable "$l" || true; done
  # if statt "[[ ]] && ...": sonst liefert die Funktion bei --no-ocrmypdf 1 und
  # set -e beendet das Skript vor der Ergebnispruefung (Fehler bis 1.2.0)
  if [[ $WITH_OCRMYPDF -eq 1 ]]; then install_ocrmypdf_portable || true; fi
}

# ------------------------------------------------------------------ Ablauf --
printf '\n\033[1msm-ocr-scanner - Installation\033[0m\n'
printf 'Skill-Verzeichnis: %s\n' "$SKILL_DIR"
printf 'Paketmanager:      %s\n' "${PM:-<keiner erkannt>}"
printf 'Modus:             %s\n' "$( ((FORCE_PORTABLE)) && echo 'portabel (kein root)' || echo 'System (als root gestartet, Paketmanager fragt nach)' )"
printf 'Netzquellen:       %s\n\n' "$( ((ALLOW_PIP)) && echo 'Paketmanager-Repositories, PyPI' || echo 'nur Paketmanager-Repositories' )"

if [[ $FORCE_PORTABLE -eq 1 ]]; then
  install_portable
else
  [[ -n "$PM" ]] || die "kein unterstuetzter Paketmanager gefunden - bitte --portable verwenden" 2
  install_system
fi

printf '\n'
info "Ergebnis"
if [[ $DRY_RUN -eq 0 ]]; then
  PATH="$HOME/.local/bin:$PATH" bash "$SCRIPT_DIR/ocr.sh" --check || true
  printf '\n'
  info "Selbsttest ausfuehren:  bash scripts/selftest.sh"
else
  skip "dry-run - nichts veraendert"
fi
