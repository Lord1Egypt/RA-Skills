#!/usr/bin/env bash
set -euo pipefail
# load env if present
source "$(dirname "$0")/_env_loader.sh"

SESSION=${1:-debug}
OUTDIR=${OUT_DIR:-out}
mkdir -p "$OUTDIR"
WS_PORT=${2:-${REMOTE_DEBUG_PORT:-9222}}
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# Simple node snippet to get cookies via CDP
if command -v node >/dev/null 2>&1; then
  NODE_PATH="$SKILL_DIR/node_modules" node -e "
    const [,,wsPort,outDir] = process.argv;
    (async()=>{
      try {
        const {chromium}=require('playwright');
        const browser=await chromium.connectOverCDP('http://127.0.0.1:'+wsPort);
        const contexts=browser.contexts();
        const context=contexts.length?contexts[0]:await browser.newContext();
        const cookies=await context.cookies();
        require('fs').writeFileSync(outDir+'/devtools_cookies.json',JSON.stringify(cookies,null,2));
        console.log('cookies saved');
        await browser.close();
        process.exit(0);
      } catch (e) {
        console.error('Playwright cookie export failed:', e.message);
        process.exit(1);
      }
    })()
  " "$WS_PORT" "$OUTDIR" || true
else
  echo "Node not found. Cannot export cookies via CDP."
  exit 1
fi
