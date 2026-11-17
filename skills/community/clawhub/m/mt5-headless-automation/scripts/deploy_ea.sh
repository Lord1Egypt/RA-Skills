#!/bin/bash
# 1-kommando EA-deploy: kopiér → kompilér → genstart → verificér
# Brug: bash deploy_ea.sh [EA-navn] [workspace-mappe]
EA="${1:-DRT-Axe}"
SRC="${2:-/home/openclaw/.openclaw/workspace/tradevault/ea}"
MT5="/home/openclaw/.wine-mt5/drive_c/Program Files/MetaTrader 5"
export DISPLAY="${DISPLAY:-:99}"

echo "1) Kopiér kildekode → MT5"
cp "$SRC"/*.mq5 "$SRC"/*.mqh "$MT5/MQL5/Experts/" 2>/dev/null

echo "2) Kompilér (MetaEditor)"
wine "$MT5/metaeditor64.exe" /compile:"$MT5/MQL5/Experts/$EA.mq5" /log 2>/dev/null | tail -1
grep -q "0 errors" "$MT5/MQL5/Experts/$EA.log" 2>/dev/null || { echo "KOMPILERINGSFEJL"; exit 1; }

echo "3) Genstart MT5"
pkill -f "terminal64.exe"; sleep 3
wine "$MT5/terminal64.exe" /portable & sleep 20

echo "4) ⚠️ Attach EA'en MANUELT (auto-attach svigter!)"
bash "$(dirname "$0")/attach_ea.sh" "$EA"

echo "5) Verificér"
echo "HB: $(stat -c '%y' "$MT5/MQL5/Files/${EA}_HB.txt" 2>/dev/null | cut -d. -f1)"
echo "ex5: $(md5sum "$MT5/MQL5/Experts/$EA.ex5" | cut -d' ' -f1)"
