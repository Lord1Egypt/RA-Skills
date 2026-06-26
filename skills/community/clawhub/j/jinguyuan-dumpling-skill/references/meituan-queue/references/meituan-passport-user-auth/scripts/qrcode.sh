#!/usr/bin/env bash
# QR code generator for auth link (Node.js implementation)
# Usage: bash qrcode.sh <url> [client_id]
# Output on success (image): QRCODE_IMAGE:<png_file_path>
# Output on success (text):  QRCODE_TEXT:<terminal half-block qr code>
# Output on failure:         QRCODE_SKIP
set -euo pipefail

URL="${1:-}"
CLIENT_ID="${2:-}"

if [ -z "$URL" ]; then
  echo "QRCODE_SKIP"
  exit 0
fi

# 确定输出文件路径：统一存放在 scripts/ 目录；有 client_id 时按其命名（覆盖），否则使用随机名称（用完即删）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd)"
RAND_FILE=0
if [ -n "$CLIENT_ID" ]; then
  IMGFILE="$SCRIPT_DIR/qrcode_${CLIENT_ID}.png"
  TXTFILE="$SCRIPT_DIR/qrcode_${CLIENT_ID}.txt"
else
  RAND=$(LC_ALL=C tr -dc 'a-z0-9' < /dev/urandom 2>/dev/null | head -c8; true)
  IMGFILE="$SCRIPT_DIR/qrcode_${RAND}.png"
  TXTFILE="$SCRIPT_DIR/qrcode_${RAND}.txt"
  RAND_FILE=1
fi

# 随机文件退出时自动清理
cleanup() {
  if [ "$RAND_FILE" = "1" ]; then
    rm -f "$IMGFILE" "$TXTFILE"
  fi
}
trap cleanup EXIT

if ! command -v node &>/dev/null; then
  echo "QRCODE_SKIP"
  exit 0
fi

NODE_GLOBAL_MODULES=""
if command -v npm &>/dev/null; then
  NODE_GLOBAL_MODULES="$(npm root -g 2>/dev/null)"
fi

if [ -z "$NODE_GLOBAL_MODULES" ]; then
  echo "QRCODE_SKIP"
  exit 0
fi

# 检查 qrcode 模块是否可用，若未安装则自动安装
if ! NODE_PATH="$NODE_GLOBAL_MODULES" node -e "require('qrcode')" 2>/dev/null; then
  echo "[qrcode.sh] qrcode 模块未安装，正在自动安装..." >&2
  if ! npm install -g qrcode 2>&1 >&2; then
    echo "QRCODE_SKIP"
    exit 0
  fi
  # 重新获取全局模块路径（防止路径变化）
  NODE_GLOBAL_MODULES="$(npm root -g 2>/dev/null)"
  # 再次验证是否安装成功
  if ! NODE_PATH="$NODE_GLOBAL_MODULES" node -e "require('qrcode')" 2>/dev/null; then
    echo "QRCODE_SKIP"
    exit 0
  fi
fi

# 优先尝试生成 PNG 图片（无行间距，可直接扫码）
RESULT=$(NODE_PATH="$NODE_GLOBAL_MODULES" node -e "
const qr = require('qrcode');
const file = process.argv[1];
const url = process.argv[2];
qr.toFile(file, url, {
  type: 'png',
  width: 300,
  margin: 2,
  errorCorrectionLevel: 'M'
}, (err) => {
  if (!err) { process.stdout.write('QRCODE_IMAGE:' + file); }
  else { process.stdout.write('QRCODE_SKIP'); }
});
" -- "$IMGFILE" "$URL" 2>/dev/null)

if [ "$RESULT" = "QRCODE_IMAGE:$IMGFILE" ]; then
  echo "$RESULT"
  exit 0
fi

# 降级：生成字符二维码（按 client_id 维度覆盖写入 TXTFILE）
NODE_PATH="$NODE_GLOBAL_MODULES" node -e "
const qr = require('qrcode');
const fs = require('fs');
const url = process.argv[1];
const file = process.argv[2];
qr.toString(url, {type:'terminal', small:true, errorCorrectionLevel:'M'}, (err, str) => {
  if (!err) { fs.writeFileSync(file, str, 'utf8'); }
});
" -- "$URL" "$TXTFILE" 2>/dev/null

if [ -f "$TXTFILE" ] && [ -s "$TXTFILE" ]; then
  printf "QRCODE_TEXT:%s" "$(cat "$TXTFILE")"
  exit 0
fi

echo "QRCODE_SKIP"
