#!/bin/bash
# OCR-guided EA-attach (undgå fælde #2 + #5): find EA i Navigator → dobbeltklik → Enter
# Brug: bash attach_ea.sh "DRT-Axe"
EA_NAME="${1:-DRT-Axe}"
export DISPLAY="${DISPLAY:-:99}"
XAUTH=$(ps aux | grep 'Xvfb :99' | grep -v grep | grep -oE '\-auth [^ ]+' | awk '{print $2}' | head -1)
[ -n "$XAUTH" ] && export XAUTHORITY="$XAUTH"

xdotool key ctrl+n; sleep 3
TMPD=$(mktemp -d /tmp/mt5ea.XXXXXX); export TMPD
trap "rm -rf "$TMPD"" EXIT
import -window root "$TMPD/nav.png" 2>/dev/null
python3 - "$EA_NAME" << 'PYEOF'
import csv, subprocess, sys, os
name = sys.argv[1]
# Crop venstre panel + OCR
subprocess.run(["python3","-c","""
from PIL import Image
img = Image.open(os.environ['TMPD'] + '/nav.png')
crop = img.crop((0,0,400,720)).resize((1200,2160), Image.LANCZOS)
crop.save(os.environ['TMPD'] + '/nav_big.png')
"""], check=True)
subprocess.run(["tesseract", os.environ["TMPD"]+"/nav_big.png", os.environ["TMPD"]+"/nav", "tsv", "--psm", "11"], check=True, capture_output=True)
found = None
with open(os.environ['TMPD'] + '/nav.tsv') as f:
    r = csv.reader(f, delimiter='\t'); next(r)
    for row in r:
        if len(row) >= 12 and name.lower() in row[11].strip().lower():
            found = (int(row[6])//3, int(row[7])//3)
            break
if not found:
    print(f"FEJL: {name} ikke fundet i navigator-træet"); sys.exit(1)
print(f"FUNDET: {found}")
# Dobbeltklik + Enter
subprocess.run(["xdotool","mousemove",str(found[0]),str(found[1]),"click","--repeat","2","--delay","150","1"])
import time; time.sleep(3)
subprocess.run(["xdotool","key","Return"])
print(f"✅ {name} attached — tjek log/HB")
PYEOF
