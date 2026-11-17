#!/usr/bin/env bash
# Generate an ID-photo delivery package via POST /v1/id-pack: one graded/smoothed
# master, then multiple crop specs, optional upload-optimized files and print sheets.
# Usage: id-pack.sh <input> <output-dir> [specs] [style-id] [smooth-strength] [bg-color] [upload] [print-sheet] [outfit-id] [outfit-long-edge]
#   specs            comma-separated crop spec ids (default: passport_cn)
#   style-id         style id (default: motu_business_neutral)
#   smooth-strength  optional M15 smoothing strength, 0-1 (default: 0/off)
#   bg-color         default | white | blue | red | #RRGGBB (default: default)
#   upload           true/false, also export upload-ready JPG files (default: true)
#   print-sheet      paper id such as 6x4/A4, or empty to skip (default: empty)
set -euo pipefail

BASE="${MCE_API_BASE:-https://mce.motu.art}"
IN="${1:?usage: id-pack.sh <input> <output-dir> [specs] [style-id] [smooth-strength] [bg-color] [upload] [print-sheet]}"
OUT_DIR="${2:?usage: id-pack.sh <input> <output-dir> [specs] [style-id] [smooth-strength] [bg-color] [upload] [print-sheet]}"
SPECS="${3:-passport_cn}"
STYLE="${4:-motu_business_neutral}"
SMOOTH_STRENGTH="${5:-}"
BG_COLOR="${6:-default}"
UPLOAD="${7:-true}"
PRINT_SHEET="${8:-}"
OUTFIT_ID="${9:-}"
OUTFIT_LONG_EDGE="${10:-1536}"

[ -f "$IN" ] || { echo "input not found: $IN" >&2; exit 1; }
mkdir -p "$OUT_DIR"

args=(-sS -A "motu-mce-skill/1.0" -X POST "$BASE/v1/id-pack"
  -F "file=@$IN"
  -F "specs=$SPECS"
  -F "style=$STYLE"
  -F "bg_color=$BG_COLOR"
  -F "upload=$UPLOAD")
[ -n "$SMOOTH_STRENGTH" ] && args+=(-F "smooth_strength=$SMOOTH_STRENGTH")
[ -n "$PRINT_SHEET" ] && args+=(-F "print_sheet=$PRINT_SHEET")
[ -n "$OUTFIT_ID" ] && args+=(-F "outfit_id=$OUTFIT_ID" -F "outfit_long_edge=$OUTFIT_LONG_EDGE")
[ -n "${MCE_API_KEY:-}" ] && args+=(-H "X-API-Key: $MCE_API_KEY")

RESP_FILE="$(mktemp)"
trap 'rm -f "$RESP_FILE"' EXIT
curl "${args[@]}" > "$RESP_FILE"
python3 - "$OUT_DIR" "$RESP_FILE" <<'PYCODE'
import base64, json, pathlib, sys
out_dir = pathlib.Path(sys.argv[1])
resp = pathlib.Path(sys.argv[2])
try:
    d = json.loads(resp.read_text(encoding="utf-8"))
except Exception:
    sys.stderr.write("id-pack failed: non-JSON response from server\n")
    sys.exit(1)
if "detail" in d and "items" not in d:
    sys.stderr.write("id-pack failed: %s\n" % d.get("detail"))
    sys.exit(1)
(out_dir / "single").mkdir(exist_ok=True)
(out_dir / "upload").mkdir(exist_ok=True)
(out_dir / "print").mkdir(exist_ok=True)
if d.get("master_base64"):
    (out_dir / "master.png").write_bytes(base64.b64decode(d["master_base64"]))
for item in d.get("items", []):
    sid = item.get("spec_id", "spec")
    if item.get("image_base64"):
        (out_dir / "single" / f"{sid}.png").write_bytes(base64.b64decode(item["image_base64"]))
    upload = item.get("upload") or {}
    if upload.get("image_base64"):
        ext = ".jpg" if upload.get("format") in ("jpeg", "jpg") else ".png"
        (out_dir / "upload" / f"{sid}_upload{ext}").write_bytes(base64.b64decode(upload["image_base64"]))
for idx, sheet in enumerate(d.get("print_sheets", []), start=1):
    if sheet.get("image_base64"):
        (out_dir / "print" / f"sheet_{idx}.jpg").write_bytes(base64.b64decode(sheet["image_base64"]))
# Remove transient absolute server paths before saving the portable report.
for key in ("master_path", "report_path"):
    d.pop(key, None)
for item in d.get("items", []):
    item.pop("path", None)
    if item.get("upload"):
        item["upload"].pop("path", None)
for sheet in d.get("print_sheets", []):
    sheet.pop("path", None)
(out_dir / "report.json").write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding="utf-8")
print("saved id-pack %s  trace=%s  specs=%s" % (out_dir, d.get("trace_id"), ",".join(i.get("spec_id", "") for i in d.get("items", []))))
for item in d.get("items", []):
    comp = item.get("compliance") or {}
    print("  %s compliance=%s" % (item.get("spec_id"), comp.get("status")))
PYCODE
