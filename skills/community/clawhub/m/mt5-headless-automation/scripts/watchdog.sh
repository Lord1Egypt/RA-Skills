#!/bin/bash
# Heartbeat-tjek: hvis HB-fil er ældre end 90 sek → genstart MT5 + re-attach EA
EA="${1:-DRT-Axe}"
MT5="/home/openclaw/.wine-mt5/drive_c/Program Files/MetaTrader 5"
export DISPLAY="${DISPLAY:-:99}"
HB="$MT5/MQL5/Files/${EA}_HB.txt"
[ ! -f "$HB" ] && { echo "HB mangler — genstarter"; pkill -f "terminal64.exe"; wine "$MT5/terminal64.exe" & sleep 25; bash "$(dirname "$0")/attach_ea.sh" "$EA"; exit; }
AGE=$(( $(date +%s) - $(stat -c %Y "$HB") ))
if [ "$AGE" -gt 90 ]; then
  echo "HB forældet ($AGE s) — genstarter MT5 + re-attach"
  pkill -f "terminal64.exe"; sleep 3
  wine "$MT5/terminal64.exe" & sleep 25
  bash "$(dirname "$0")/attach_ea.sh" "$EA"
else
  echo "OK — HB $AGE s gammel"
fi
