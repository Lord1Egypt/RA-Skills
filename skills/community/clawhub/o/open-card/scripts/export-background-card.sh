#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   export-background-card.sh <preview_html> <output_png> [width] [height]
# Example:
#   export-background-card.sh /tmp/opencard-preview.html /tmp/opencard-final.png 1200 800

PREVIEW_HTML="${1:?preview html required}"
OUTPUT_PNG="${2:?output png required}"
WIDTH="${3:-1200}"
HEIGHT="${4:-800}"

# -- 依赖检查 ----------------------------------------------------------

if ! command -v node &>/dev/null; then
  echo "Error: node not found." >&2
  echo "  PNG export requires Node.js >= 18." >&2
  echo "  Install: https://nodejs.org/ or via brew/nvm." >&2
  exit 1
fi

if ! command -v npm &>/dev/null; then
  echo "Error: npm not found (usually bundled with Node.js)." >&2
  exit 1
fi

PLAYWRIGHT_PATH="$(node -e "try{console.log(require.resolve('playwright-core'))}catch{}" 2>/dev/null || true)"
if [[ -z "$PLAYWRIGHT_PATH" ]]; then
  PLAYWRIGHT_PATH="$(find "$(npm root -g 2>/dev/null)" -path '*/playwright-core/index.js' 2>/dev/null | head -1 || true)"
fi
if [[ -z "$PLAYWRIGHT_PATH" ]]; then
  echo "Error: playwright-core not found." >&2
  echo "  PNG export requires playwright-core." >&2
  echo "  Install: npm i -g playwright-core" >&2
  exit 1
fi
PLAYWRIGHT_DIR="$(dirname "$PLAYWRIGHT_PATH")"

CHROME_PATH=""
for candidate in \
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  "/Applications/Chromium.app/Contents/MacOS/Chromium" \
  "$(which chromium 2>/dev/null || true)" \
  "$(which google-chrome 2>/dev/null || true)" \
  "$(which google-chrome-stable 2>/dev/null || true)"; do
  if [[ -n "$candidate" && -x "$candidate" ]]; then
    CHROME_PATH="$candidate"
    break
  fi
done
if [[ -z "$CHROME_PATH" ]]; then
  echo "Error: Chrome or Chromium not found." >&2
  echo "  PNG export requires a local Chrome/Chromium installation." >&2
  echo "  Install Chrome: https://www.google.com/chrome/" >&2
  exit 1
fi

# -- Resolve absolute path for file:// URL ----------------------------

PREVIEW_HTML="$(cd "$(dirname "$PREVIEW_HTML")" && pwd)/$(basename "$PREVIEW_HTML")"

# -- 导出 --------------------------------------------------------------

TMP_SCRIPT="$(mktemp /tmp/opencard-export-XXXXXX.js)"
trap 'rm -f "$TMP_SCRIPT"' EXIT

# Pass paths via command-line args (not string interpolation) to avoid injection
cat > "$TMP_SCRIPT" <<'NODE'
const path = require('path');
const { chromium } = require(process.argv[2]);

(async () => {
  const htmlPath = path.resolve(process.argv[3]);
  const out = process.argv[4];
  const width = parseInt(process.argv[5], 10);
  const height = parseInt(process.argv[6], 10);
  const chromePath = process.argv[7];

  const browser = await chromium.launch({ headless: true, executablePath: chromePath });
  const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 2 });
  await page.goto('file://' + encodeURI(htmlPath).replace(/%2F/g, '/'), {
    waitUntil: 'networkidle',
    timeout: 120000,
  });
  // 等待背景图实际渲染完成
  await page.waitForFunction(() => {
    return document.querySelector('.frame') &&
      getComputedStyle(document.querySelector('.frame')).backgroundImage !== 'none';
  }, { timeout: 120000 });
  // 额外等待确保图片完全解码渲染
  await new Promise(r => setTimeout(r, 2000));
  await page.screenshot({ path: out, type: 'png' });
  await browser.close();
})();
NODE

node "$TMP_SCRIPT" "$PLAYWRIGHT_DIR" "$PREVIEW_HTML" "$OUTPUT_PNG" "$WIDTH" "$HEIGHT" "$CHROME_PATH"
echo "$OUTPUT_PNG"
