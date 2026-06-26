#!/bin/bash
# ── JARVIS UI 安裝 ──
# 用法: ./setup.sh

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
DIM='\033[2m'
NC='\033[0m'

echo -e "${CYAN}🦾 JARVIS UI Setup${NC}"
echo ""

# 檢查依賴
echo "Checking dependencies..."
command -v node >/dev/null 2>&1 || { echo -e "${RED}❌ Node.js required (v20+)${NC}"; exit 1; }
command -v npm >/dev/null 2>&1 || { echo -e "${RED}❌ npm required${NC}"; exit 1; }

# npm install
echo "Installing dependencies..."
npm install --production

# 如果沒有預 build 的 dist/，就 build
if [ ! -d "dist" ]; then
  echo "Building static files..."
  npm install  # 需要 devDependencies
  npm run build
fi

# 自動偵測 Gateway Token
if [ ! -f ".env" ] || ! grep -q "GATEWAY_TOKEN" .env 2>/dev/null; then
  echo ""
  echo "Detecting Gateway token..."
  
  OPENCLAW_CONFIG="${HOME}/.openclaw/openclaw.json"
  TOKEN=""
  
  if [ -f "$OPENCLAW_CONFIG" ]; then
    # 嘗試用 node 解析 JSON（跨平台，不依賴 jq）
    TOKEN=$(node -e "try{console.log(JSON.parse(require('fs').readFileSync('$OPENCLAW_CONFIG','utf8')).gateway?.token||'')}catch{}" 2>/dev/null)
  fi
  
  if [ -n "$TOKEN" ]; then
    echo "GATEWAY_TOKEN=$TOKEN" > .env
    echo -e "${GREEN}✅ Gateway token auto-detected and saved to .env${NC}"
  else
    echo -e "${CYAN}⚠️  Could not auto-detect Gateway token.${NC}"
    echo -e "   Set it manually: ${DIM}echo \"GATEWAY_TOKEN=your_token\" > .env${NC}"
    echo -e "   Find it in: ${DIM}~/.openclaw/openclaw.json → gateway.token${NC}"
  fi
fi

echo ""
echo -e "${GREEN}✅ Installation complete!${NC}"
echo ""

# edge-tts 檢查
if ! python3 -m edge_tts --version >/dev/null 2>&1; then
  echo -e "${CYAN}📢 TTS setup (optional):${NC}"
  echo -e "     ${DIM}pip install edge-tts${NC}"
  echo ""
fi

echo -e "${CYAN}Next steps:${NC}"
echo ""
echo "  1. Start the server:"
echo -e "     ${DIM}node --env-file=.env server/index.js${NC}"
echo ""
echo "  2. Open in browser:"
echo -e "     ${DIM}http://localhost:9999${NC}"
echo ""
echo "  3. (Optional) Customize your agent:"
echo -e "     ${DIM}cp config.json config.local.json${NC}"
echo -e "     ${DIM}# Edit config.local.json — change name, emoji, port, etc.${NC}"
echo ""
echo -e "${DIM}For production (auto-restart): npm i -g pm2 && pm2 start server/index.js --name jarvis --node-args=\"--env-file=.env\"${NC}"
echo ""
echo -e "${CYAN}🦾 Enjoy your JARVIS!${NC}"
echo ""
echo -e "${DIM}⚠️  Remote access? Add to ~/.openclaw/openclaw.json:${NC}"
echo -e "${DIM}   { \"gateway\": { \"controlUi\": { \"allowInsecureAuth\": true } } }${NC}"
