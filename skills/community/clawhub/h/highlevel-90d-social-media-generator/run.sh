#!/usr/bin/env bash
# 90-day social calendar pipeline. ONE command per client.
#
# MODE A - HighLevel connected (needs HIGHLEVEL_ACCESS_TOKEN in .env or env):
#   ./run.sh --email client@email.com [--count 45] [--start-date YYYY-MM-DD]
#
# MODE B - No HighLevel needed (client details given directly):
#   ./run.sh --details "Company Name|website.com|City|ST|Business Category|Company description"
#   ./run.sh --client-json path/to/client.json
#
# Both modes produce the SAME output: output/<slug>-social-90d.csv
# (HighLevel Social Planner import format) + -posts.json for the image step.
#
# Optional flags:
#   --count N            number of posts (default 45)
#   --start-date DATE    first post date (default today)
#   --no-images          skip the image step entirely
#   --llm-key KEY        LLM API key (else DEEPSEEK_API_KEY/OPENAI_API_KEY env)
#   --image-base-url URL public URL prefix for images (else imageUrls stay empty)
#   --gemini-key KEY | --fal-key KEY | --kling-ak KEY --kling-sk KEY
set -euo pipefail
cd "$(dirname "$0")"

EMAIL=""
DETAILS=""
CLIENT_JSON=""
COUNT=45
START_DATE="$(date +%F)"
NO_IMAGES=0
LLM_KEY=""
LLM_MODEL=""
LLM_BASE=""
IMAGE_BASE_URL=""
GEMINI_KEY=""
FAL_KEY=""
KLING_AK=""
KLING_SK=""
SSH_HOST=""
SSH_USER=""
SSH_KEY=""
SSH_REMOTE_DIR="public_html/social"
FTP_HOST=""
FTP_USER=""
FTP_PASS=""
FTP_REMOTE_DIR="public_html/social"
PUBLIC_URL_BASE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --email) EMAIL="$2"; shift 2 ;;
    --details) DETAILS="$2"; shift 2 ;;
    --client-json) CLIENT_JSON="$2"; shift 2 ;;
    --count) COUNT="$2"; shift 2 ;;
    --start-date) START_DATE="$2"; shift 2 ;;
    --no-images) NO_IMAGES=1; shift ;;
    --llm-key) LLM_KEY="$2"; shift 2 ;;
    --llm-model) LLM_MODEL="$2"; shift 2 ;;
    --llm-base) LLM_BASE="$2"; shift 2 ;;
    --image-base-url) IMAGE_BASE_URL="$2"; shift 2 ;;
    --gemini-key) GEMINI_KEY="$2"; shift 2 ;;
    --fal-key) FAL_KEY="$2"; shift 2 ;;
    --kling-ak) KLING_AK="$2"; shift 2 ;;
    --kling-sk) KLING_SK="$2"; shift 2 ;;
    --ssh-host) SSH_HOST="$2"; shift 2 ;;
    --ssh-user) SSH_USER="$2"; shift 2 ;;
    --ssh-key) SSH_KEY="$2"; shift 2 ;;
    --ssh-remote-dir) SSH_REMOTE_DIR="$2"; shift 2 ;;
    --ftp-host) FTP_HOST="$2"; shift 2 ;;
    --ftp-user) FTP_USER="$2"; shift 2 ;;
    --ftp-pass) FTP_PASS="$2"; shift 2 ;;
    --ftp-remote-dir) FTP_REMOTE_DIR="$2"; shift 2 ;;
    --public-url-base) PUBLIC_URL_BASE="$2"; shift 2 ;;
    *) echo "unknown arg: $1"; exit 2 ;;
  esac
done

if [[ -z "$EMAIL" && -z "$DETAILS" && -z "$CLIENT_JSON" ]]; then
  echo "usage: ./run.sh --email x@y.com | --details \"Company|site|City|ST|Category|Desc\" | --client-json file.json"
  echo "       (no mode given = interactive: you'll be asked for each client detail one at a time)"
fi

mkdir -p data output

# ---- 1. Client details ----
if [[ -n "$EMAIL" ]]; then
  echo "==> 1/5 fetching client from HighLevel: $EMAIL"
  python3 scripts/fetch_client.py --email "$EMAIL" --json-out "data/client.json"
elif [[ -n "$DETAILS" ]]; then
  echo "==> 1/5 using client details (no HighLevel connection)"
  python3 scripts/fetch_client.py --details "$DETAILS" --json-out "data/client.json"
elif [[ -n "$CLIENT_JSON" ]]; then
  echo "==> 1/5 loading client JSON: $CLIENT_JSON"
  python3 scripts/fetch_client.py --client-json "$CLIENT_JSON" --json-out "data/client.json"
else
  echo "==> 1/5 interactive: asking for client details one at a time (no HighLevel connection)"
  python3 scripts/fetch_client.py --interactive --json-out "data/client.json"
fi

DOMAIN=$(python3 -c "import json;print((json.load(open('data/client.json')).get('website') or '').replace('https://','').replace('http://','').rstrip('/'))")
echo "    domain: $DOMAIN"

# ---- 2. Sitemap ----
SITEMAP="https://${DOMAIN}/sitemap.xml"
echo "==> 2/5 fetching sitemap: $SITEMAP"
python3 scripts/fetch_sitemap.py "$SITEMAP" --out "data/sitemap.txt"

# ---- 3. Posts ----
echo "==> 3/5 generating $COUNT posts (every other day, 9am, from $START_DATE)"
LLM_ARGS=()
[[ -n "$LLM_KEY" ]] && LLM_ARGS+=(--llm-key "$LLM_KEY")
[[ -n "$LLM_MODEL" ]] && LLM_ARGS+=(--llm-model "$LLM_MODEL")
[[ -n "$LLM_BASE" ]] && LLM_ARGS+=(--llm-base "$LLM_BASE")
python3 scripts/generate_posts.py --client-json data/client.json \
  --sitemap-file data/sitemap.txt \
  --start-date "$START_DATE" --count "$COUNT" \
  --out "output/$(basename "$DOMAIN")-social-90d.csv" "${LLM_ARGS[@]}"

# ---- 4. Images (optional) ----
if [[ "$NO_IMAGES" == "1" ]]; then
  echo "==> 4/5 skipped (--no-images)"
else
  echo "==> 4/5 generating images (local, no upload)"
  IMG_ARGS=(--posts-json "output/$(basename "$DOMAIN")-social-90d-posts.json"
            --csv "output/$(basename "$DOMAIN")-social-90d.csv"
            --client-json data/client.json
            --outdir "output/$(basename "$DOMAIN")-images")
  [[ -n "$LLM_KEY" ]] && IMG_ARGS+=(--llm-key "$LLM_KEY")
  [[ -n "$LLM_MODEL" ]] && IMG_ARGS+=(--llm-model "$LLM_MODEL")
  [[ -n "$LLM_BASE" ]] && IMG_ARGS+=(--llm-base "$LLM_BASE")
  [[ -n "$IMAGE_BASE_URL" ]] && IMG_ARGS+=(--image-base-url "$IMAGE_BASE_URL")
  [[ -n "$GEMINI_KEY" ]] && IMG_ARGS+=(--gemini-key "$GEMINI_KEY")
  [[ -n "$FAL_KEY" ]] && IMG_ARGS+=(--fal-key "$FAL_KEY")
  [[ -n "$KLING_AK" ]] && IMG_ARGS+=(--kling-ak "$KLING_AK")
  [[ -n "$KLING_SK" ]] && IMG_ARGS+=(--kling-sk "$KLING_SK")
  [[ -n "$SSH_HOST" ]] && IMG_ARGS+=(--ssh-host "$SSH_HOST" --ssh-user "$SSH_USER" --ssh-key "$SSH_KEY" --ssh-remote-dir "$SSH_REMOTE_DIR")
  [[ -n "$FTP_HOST" ]] && IMG_ARGS+=(--ftp-host "$FTP_HOST" --ftp-user "$FTP_USER" --ftp-pass "$FTP_PASS" --ftp-remote-dir "$FTP_REMOTE_DIR")
  [[ -n "$PUBLIC_URL_BASE" ]] && IMG_ARGS+=(--public-url-base "$PUBLIC_URL_BASE")
  python3 scripts/generate_images.py "${IMG_ARGS[@]}" || echo "    (image step failed, CSV still valid)"
fi

# ---- 5. Done ----
echo "==> 5/5 DONE: output/$(basename "$DOMAIN")-social-90d.csv"
echo "    Import it into the client's HighLevel Social Planner."
