#!/usr/bin/env bash
# Install a custom theme folder into iA Presenter's Themes directory (macOS).
# Usage: install_theme.sh THEME_DIR [--force]      install/replace
#        install_theme.sh --list                   list installed custom + built-in themes
set -euo pipefail
BASE="$HOME/Library/Containers/net.ia.presenter/Data/Library/Application Support/iA Presenter"
THEMES="$BASE/Themes"

list_themes() {
  python3 - "$BASE" <<'PY'
import json, os, re, sys
base = sys.argv[1]
def lenient(path):
    txt = open(path, encoding="utf-8").read()
    try:
        return json.loads(txt)
    except Exception:
        return json.loads(re.sub(r",(\s*[}\]])", r"\1", txt))
for label, sub in (("custom", "Themes"), ("built-in", ".Themes")):
    d = os.path.join(base, sub)
    if not os.path.isdir(d):
        continue
    print(f"{label} ({d}):")
    for name in sorted(os.listdir(d)):
        tj = os.path.join(d, name, "template.json")
        if not os.path.isfile(tj):
            continue
        try:
            t = lenient(tj)
            presets = [p.get("Name") for p in lenient(os.path.join(d, name, "presets.json")).get("Presets", [])] if os.path.isfile(os.path.join(d, name, "presets.json")) else []
            print(f'  {t.get("Name",name):16} template id: "{str(t.get("Name",name)).lower()}"   presets: {", ".join(map(str,presets)) or "-"}   css: {t.get("Css")}')
        except Exception as e:
            print(f"  {name}: unreadable ({e})")
PY
}

if [ "${1:-}" = "--list" ]; then list_themes; exit 0; fi
SRC="${1:?usage: install_theme.sh THEME_DIR [--force] | --list}"
FORCE="${2:-}"
[ -d "$SRC" ] || { echo "error: $SRC is not a directory" >&2; exit 1; }
[ -f "$SRC/template.json" ] || { echo "error: $SRC/template.json missing" >&2; exit 1; }
[ -f "$SRC/presets.json" ] || { echo "error: $SRC/presets.json missing" >&2; exit 1; }

NAME=$(python3 - "$SRC" <<'PY'
import json, os, re, sys
src = sys.argv[1]
def load(p):
    txt = open(p, encoding="utf-8").read()
    try:
        return json.loads(txt)
    except Exception as e:
        try:
            json.loads(re.sub(r",(\s*[}\]])", r"\1", txt)); print(f"warning: {os.path.basename(p)} has trailing commas (works, but write strict JSON)", file=sys.stderr); return json.loads(re.sub(r",(\s*[}\]])", r"\1", txt))
        except Exception:
            sys.exit(f"error: {p} is not valid JSON: {e}")
t = load(os.path.join(src, "template.json")); p = load(os.path.join(src, "presets.json"))
for k in ("Name", "Css"):
    if not t.get(k): sys.exit(f"error: template.json lacks {k}")
if not os.path.isfile(os.path.join(src, t["Css"])): sys.exit(f'error: CSS file "{t["Css"]}" named in template.json not found')
presets = p.get("Presets") or []
if not presets: sys.exit("error: presets.json has no Presets")
for pr in presets:
    for k in ("DarkBodyTextColor", "LightBodyTextColor", "DarkBackgroundColor", "LightBackgroundColor", "Appearance"):
        if k not in pr: print(f'warning: preset "{pr.get("Name")}" lacks {k}', file=sys.stderr)
    if pr.get("Appearance") not in ("light", "dark"): print(f'warning: preset "{pr.get("Name")}" Appearance should be "light" or "dark"', file=sys.stderr)
print(t["Name"])
PY
)
DEST="$THEMES/$NAME"
mkdir -p "$THEMES"
if [ -d "$DEST" ] && [ "$FORCE" != "--force" ]; then
  echo "error: $DEST exists (use --force to replace)" >&2; exit 1
fi
rm -rf "$DEST"
cp -R "$SRC" "$DEST"
find "$DEST" -name ".DS_Store" -delete
echo "installed: $DEST"
echo "template id for info.json: \"$(printf '%s' "$NAME" | tr '[:upper:]' '[:lower:]')\""
if pgrep -xq "iA Presenter"; then
  echo "iA Presenter is running – quit and relaunch it once so the new theme appears (edits to a theme in use hot-reload afterwards)."
else
  echo "launch iA Presenter and pick the theme in Design → Theme."
fi
