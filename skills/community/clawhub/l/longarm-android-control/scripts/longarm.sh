#!/usr/bin/env bash
# Thin curl wrapper for the longarm Android HTTP API.
# Environment: LONGARM_URL is required; LONGARM_TOKEN is optional.
set -euo pipefail

die() { echo "longarm: $*" >&2; exit 1; }

usage() {
  cat <<'EOF'
Commands:
  status
  screen-info
  tap X Y [DURATION_MS]
  long-press X Y [DURATION_MS]
  swipe SX SY EX EY [DURATION_MS]
  pinch X Y START_SPREAD END_SPREAD [ANGLE] [DURATION_MS]
  two-finger-swipe SX SY EX EY [SPREAD] [DURATION_MS]
  rotate X Y RADIUS START_ANGLE END_ANGLE [DURATION_MS]
  screenshot [OUT.png]
  screenshot-grid [OUT.png] [QUERY]
  overlay-show
  overlay-hide
  open-app PACKAGE
  open-url URL
  open-intent JSON
  batch-list
  batch-get ID
  batch-create-file TASK.json
  batch-update-file ID TASK.json
  batch-delete ID
  batch-run ID
  batch-run-file TASK.json
  batch-status
  batch-history
  batch-history-get RUN_ID
  batch-history-delete RUN_ID
  batch-history-clear
  batch-shot RUN_ID SHOT_ID [OUT.png]
  batch-export RUN_ID [OUT.zip]
EOF
}

cmd="${1:-}"
shift || true

case "$cmd" in
  ""|-h|--help|help) usage; exit 0 ;;
esac

[[ -n "${LONGARM_URL:-}" ]] || die "LONGARM_URL is not set (e.g. export LONGARM_URL=http://192.168.1.50:8080)"
BASE="${LONGARM_URL%/}"

AUTH=()
if [[ -n "${LONGARM_TOKEN:-}" ]]; then
  AUTH=(-H "Authorization: Bearer ${LONGARM_TOKEN}")
fi

get() { curl -fsS "${AUTH[@]}" -H "Accept: application/json" "${BASE}$1"; }
download() { curl -fsS "${AUTH[@]}" "${BASE}$1" -o "$2"; }
delete() { curl -fsS "${AUTH[@]}" -X DELETE -H "Accept: application/json" "${BASE}$1"; }
post() { curl -fsS "${AUTH[@]}" -X POST -H "Content-Type: application/json" -H "Accept: application/json" -d "$2" "${BASE}$1"; }
post_file() { curl -fsS "${AUTH[@]}" -X POST -H "Content-Type: application/json" -H "Accept: application/json" --data-binary "@$2" "${BASE}$1"; }
put_file() { curl -fsS "${AUTH[@]}" -X PUT -H "Content-Type: application/json" -H "Accept: application/json" --data-binary "@$2" "${BASE}$1"; }

case "$cmd" in
  status) get /api/status; echo ;;
  screen-info) get /api/screen/info; echo ;;
  tap) [[ $# -ge 2 ]] || die "tap needs: X Y [DURATION_MS]"; post /api/gesture/tap "{\"x\":$1,\"y\":$2,\"duration\":${3:-50}}"; echo ;;
  long-press) [[ $# -ge 2 ]] || die "long-press needs: X Y [DURATION_MS]"; post /api/gesture/long_press "{\"x\":$1,\"y\":$2,\"duration\":${3:-1000}}"; echo ;;
  swipe) [[ $# -ge 4 ]] || die "swipe needs: SX SY EX EY [DURATION_MS]"; post /api/gesture/swipe "{\"startX\":$1,\"startY\":$2,\"endX\":$3,\"endY\":$4,\"duration\":${5:-300}}"; echo ;;
  pinch) [[ $# -ge 4 ]] || die "pinch needs: X Y START_SPREAD END_SPREAD [ANGLE] [DURATION_MS]"; post /api/gesture/pinch "{\"x\":$1,\"y\":$2,\"startSpread\":$3,\"endSpread\":$4,\"angle\":${5:-0},\"duration\":${6:-400}}"; echo ;;
  two-finger-swipe) [[ $# -ge 4 ]] || die "two-finger-swipe needs: SX SY EX EY [SPREAD] [DURATION_MS]"; post /api/gesture/two_finger_swipe "{\"startX\":$1,\"startY\":$2,\"endX\":$3,\"endY\":$4,\"spread\":${5:-200},\"duration\":${6:-400}}"; echo ;;
  rotate) [[ $# -ge 5 ]] || die "rotate needs: X Y RADIUS START_ANGLE END_ANGLE [DURATION_MS]"; post /api/gesture/rotate "{\"x\":$1,\"y\":$2,\"radius\":$3,\"startAngle\":$4,\"endAngle\":$5,\"duration\":${6:-600}}"; echo ;;
  screenshot) out="${1:-longarm-screenshot.png}"; download /api/screenshot "$out"; echo "saved $out" ;;
  screenshot-grid) out="${1:-longarm-screenshot-grid.png}"; query="${2:-gridSize=1cm&gridColor=80FF0000&gridWidth=2&scale=true}"; download "/api/screenshot?${query}" "$out"; echo "saved $out" ;;
  overlay-show) post /api/overlay/show "{}"; echo ;;
  overlay-hide) post /api/overlay/hide "{}"; echo ;;
  open-app) [[ $# -ge 1 ]] || die "open-app needs: PACKAGE"; post /api/app/open "{\"packageName\":\"$1\"}"; echo ;;
  open-url) [[ $# -ge 1 ]] || die "open-url needs: URL"; post /api/intent/open "{\"action\":\"android.intent.action.VIEW\",\"data\":\"$1\"}"; echo ;;
  open-intent) [[ $# -ge 1 ]] || die "open-intent needs: JSON"; post /api/intent/open "$1"; echo ;;
  batch-list) get /api/batch; echo ;;
  batch-get) [[ $# -ge 1 ]] || die "batch-get needs: ID"; get "/api/batch/$1"; echo ;;
  batch-create-file) [[ $# -ge 1 ]] || die "batch-create-file needs: TASK.json"; post_file /api/batch "$1"; echo ;;
  batch-update-file) [[ $# -ge 2 ]] || die "batch-update-file needs: ID TASK.json"; put_file "/api/batch/$1" "$2"; echo ;;
  batch-delete) [[ $# -ge 1 ]] || die "batch-delete needs: ID"; delete "/api/batch/$1"; echo ;;
  batch-run) [[ $# -ge 1 ]] || die "batch-run needs: ID"; post "/api/batch/$1/run" "{}"; echo ;;
  batch-run-file) [[ $# -ge 1 ]] || die "batch-run-file needs: TASK.json"; post_file /api/batch/run "$1"; echo ;;
  batch-status) get /api/batch/status; echo ;;
  batch-history) get /api/batch/history; echo ;;
  batch-history-get) [[ $# -ge 1 ]] || die "batch-history-get needs: RUN_ID"; get "/api/batch/history/$1"; echo ;;
  batch-history-delete) [[ $# -ge 1 ]] || die "batch-history-delete needs: RUN_ID"; delete "/api/batch/history/$1"; echo ;;
  batch-history-clear) delete /api/batch/history; echo ;;
  batch-shot) [[ $# -ge 2 ]] || die "batch-shot needs: RUN_ID SHOT_ID [OUT.png]"; out="${3:-longarm-batch-shot.png}"; download "/api/batch/history/$1/screenshots/$2" "$out"; echo "saved $out" ;;
  batch-export) [[ $# -ge 1 ]] || die "batch-export needs: RUN_ID [OUT.zip]"; out="${2:-longarm-batch-screenshots.zip}"; download "/api/batch/history/$1/export" "$out"; echo "saved $out" ;;
  *) die "unknown command '$cmd' (run: longarm.sh help)" ;;
esac
