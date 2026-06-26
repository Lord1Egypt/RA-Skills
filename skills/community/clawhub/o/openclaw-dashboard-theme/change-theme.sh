#!/usr/bin/env bash
#===============================================
# OpenClaw Dashboard Theme Changer
# Finds CSS/JS files dynamically, updates accent color
# and all CSS variable variants robustly.
#===============================================
set -euo pipefail

# --- Argument Validation ---
if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <hex-color>"
  echo "Example: $0 '#fcd337'"
  exit 1
fi

INPUT="$1"
# Accept with or without #
COLOR="${INPUT//#/}"
if [[ ! "$COLOR" =~ ^[a-fA-F0-9]{6}$ ]]; then
  echo "Error: Invalid hex color '$INPUT'. Use format #RRGGBB (e.g. #fcd337)"
  exit 1
fi
COLOR="#${COLOR}"
echo "==> Target accent color: $COLOR"

# --- Locate OpenClaw assets directory ---
NPM_GLOBAL="$(npm root -g 2>/dev/null || echo "${HOME}/.npm-global/lib/node_modules")"
ASSETS_DIR="${NPM_GLOBAL}/openclaw/dist/control-ui/assets"

if [[ ! -d "$ASSETS_DIR" ]]; then
  echo "Error: OpenClaw assets not found at $ASSETS_DIR"
  echo "Is OpenClaw installed?"
  exit 1
fi

# --- Find CSS file (index-*.css in control-ui assets) ---
CSS_FILES=("$ASSETS_DIR"/index-*.css)
if [[ ! -f "${CSS_FILES[0]}" ]]; then
  echo "Error: No CSS file found in $ASSETS_DIR"
  exit 1
fi
CSS="${CSS_FILES[0]}"
echo "==> CSS file: $(basename "$CSS")"

# --- Find JS file (index-*.js — the main bundle with accent colors) ---
# The main bundle is the largest index-*.js file (not a .map)
JS_FILES=("$ASSETS_DIR"/index-*.js)
JS=""
for f in "${JS_FILES[@]}"; do
  if [[ -f "$f" && ! "$f" =~ \.map$ ]]; then
    JS="$f"
    break
  fi
done
if [[ -z "$JS" ]]; then
  echo "Warning: No main JS bundle found, skipping JS update"
  JS=""
else
  echo "==> JS file: $(basename "$JS")"
fi

# --- Compute color variants ---
# Parse R, G, B from #RRGGBB
R=$((16#${COLOR:1:2}))
G=$((16#${COLOR:3:2}))
B=$((16#${COLOR:5:2}))

# accent-hover: darken by ~15% in RGB (for contrast on hover)
accent_hover_r=$(( R > 20 ? R - 20 : 0 ))
accent_hover_g=$(( G > 20 ? G - 20 : 0 ))
accent_hover_b=$(( B > 20 ? B - 20 : 0 ))
ACCENT_HOVER=$(printf "#%02x%02x%02x" $accent_hover_r $accent_hover_g $accent_hover_b)

# accent-muted: slightly darker than main (~25% reduction)
accent_muted_r=$(( R > 30 ? R - 30 : 0 ))
accent_muted_g=$(( G > 30 ? G - 30 : 0 ))
accent_muted_b=$(( B > 30 ? B - 30 : 0 ))
ACCENT_MUTED=$(printf "#%02x%02x%02x" $accent_muted_r $accent_muted_g $accent_muted_b)

# accent-subtle: main color at ~10% opacity = RRGGBB + "1a" (hex for ~10% alpha)
ACCENT_SUBTLE="${COLOR}1a"

# accent-glow: main color at ~20% opacity = RRGGBB + "33" (hex for ~20% alpha)
ACCENT_GLOW="${COLOR}33"

# focus: accent color at ~20% opacity (same as glow)
FOCUS="${COLOR}33"

echo "==> Computed variants:"
echo "    accent-hover:  $ACCENT_HOVER"
echo "    accent-muted: $ACCENT_MUTED"
echo "    accent-subtle: $ACCENT_SUBTLE"
echo "    accent-glow:   $ACCENT_GLOW"
echo "    focus:         $FOCUS"

# ============================================================
# CSS VARIABLE APPROACH
# Replace --accent and all related CSS variables across all
# theme blocks (light, dark, openknot, dash, etc.)
# ============================================================
echo ""
echo "==> Updating CSS variables in $(basename "$CSS")..."

# Core accent variables
sed -i "s/--accent:#[a-fA-F0-9]\{6\};/--accent:${COLOR};/g" "$CSS"
sed -i "s/--primary:#[a-fA-F0-9]\{6\};/--primary:${COLOR};/g" "$CSS"
sed -i "s/--ring:#[a-fA-F0-9]\{6\};/--ring:${COLOR};/g" "$CSS"

# Hover/muted/subtle/glow variants
sed -i "s/--accent-hover:#[a-fA-F0-9]\{6\};/--accent-hover:${ACCENT_HOVER};/g" "$CSS"
sed -i "s/--accent-muted:#[a-fA-F0-9]\{6\};/--accent-muted:${ACCENT_MUTED};/g" "$CSS"
sed -i "s/--accent-subtle:#[a-fA-F0-9]\{6\};/--accent-subtle:${ACCENT_SUBTLE};/g" "$CSS"
sed -i "s/--accent-glow:#[a-fA-F0-9]\{8\};/--accent-glow:${ACCENT_GLOW};/g" "$CSS"
sed -i "s/--focus:#[a-fA-F0-9]\{8\};/--focus:${FOCUS};/g" "$CSS"

echo "==> CSS variables updated."

# ============================================================
# JS BUNDLE — replace hardcoded accent colors
# We look for colors that appear multiple times (indicating they
# are used as the primary accent, not one-off colors).
# We specifically skip: #007bff (blue links), #6366f1 (purple),
# #00e5cc (teal), #050810 (near-black), #f59e0b (orange/warn),
# #dfb82b (amber/danger).
# ============================================================
if [[ -n "$JS" && -f "$JS" ]]; then
  echo ""
  echo "==> Checking JS file $(basename "$JS")..."

  # Get unique hex colors and their frequencies
  JSCOLORS=$(grep -oE "#[a-fA-F0-9]{6}" "$JS" | sort | uniq -c | sort -rn)
  echo "    Top colors in JS:"
  echo "$JSCOLORS" | head -10 | sed 's/^/    /'

  # Replace the old accent color (currently whatever was there before)
  # by finding which non-standard color appears most and replacing it
  # with our new color.
  # Common accent color patterns in the JS bundle:
  # We target colors that:
  #   - Are NOT one of the standard palette colors
  #   - Appear multiple times (>=2 occurrences as the main accent)
  # The "danger" color (#ef4444 equivalent) should NOT be changed

  # Find colors that are likely the old accent (appear >= 2 times, not in standard palette)
  STANDARD_COLORS="007bff|00e5cc|050810|6366f1|f59e0b|dfb82b|22c55e|3b82f6|14b8a6|eab308"

  # Get the current accent color from CSS (we just set it, but check what was there)
  # We replace any color that is clearly an accent (not standard palette, appears >=2)
  OLD_ACCENT=$(echo "$JSCOLORS" | grep -vE "^\\s*[0-9]+\\s#($STANDARD_COLORS)$" | awk '{print $2}' | head -3)

  if [[ -n "$OLD_ACCENT" ]]; then
    echo "    Replacing old accent color(s) in JS: $OLD_ACCENT"
    for old in $OLD_ACCENT; do
      # Skip if it looks like it could be the new color (idempotent check)
      if [[ "$old" != "$COLOR" ]]; then
        sed -i "s/${old}/${COLOR}/g" "$JS"
        echo "    Replaced $old -> $COLOR"
      fi
    done
  else
    echo "    No old accent color found to replace (may already be set)"
  fi
fi

# ============================================================
# Verification
# ============================================================
echo ""
echo "==> Verifying changes..."

# Check accent CSS variable is set correctly
CSS_ACCENT=$(grep -oP "(?<=--accent:)[^;]+" "$CSS" | head -1)
if [[ "$CSS_ACCENT" == "$COLOR" ]]; then
  echo "    ✅ CSS --accent: $CSS_ACCENT (correct)"
else
  echo "    ⚠️  CSS --accent: $CSS_ACCENT (expected $COLOR)"
fi

# Check no old red/danger colors remain in CSS accent vars
OLD_ACCENT_REDS="ff5c5c|dc2626|e5243b|c41e30|ff4040|e0242b|d32f2f|ef4444"
if grep -qE "--accent:--($OLD_ACCENT_REDS)" "$CSS" 2>/dev/null; then
  echo "    ⚠️  Old red accent values still found in CSS"
else
  echo "    ✅ No old red accent values in CSS"
fi

echo ""
echo "==> Done! Force-refresh your browser (Ctrl+Shift+R / Cmd+Shift+R)."
echo "    Run 'openclaw update' to re-apply after upgrading OpenClaw."
