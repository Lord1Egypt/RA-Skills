#!/usr/bin/env bash
# Dry-run every submission body in a batch file against POST /submissions/validate/
# WITHOUT creating anything, then pre-flight every pointer/affordance URL for 3xx
# redirects. Cheap insurance before a real submit pass: it catches payload-shape
# and natural-key errors up front, and the single highest-yield populator trap —
# a cited URL that `curl -L` follows but the pipeline fetcher (which does not
# follow redirects) sees as a 404.
#
# Usage:
#   OAG_TOKEN=oag_... ./oag-validate-batch.sh org-with-product.batch.json
#
# The batch file is a JSON array of submission bodies (see org-with-product.batch.json).
# Exits non-zero if any body fails validation or any URL redirects. Set
# OAG_PREFLIGHT=0 to skip the redirect check (offline validation).
set -euo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=./oag-common.sh
. "$here/oag-common.sh"

batch_file="${1:?usage: oag-validate-batch.sh BATCH_FILE.json}"
oag_require_token

count="$(jq 'length' "$batch_file")"
echo "Validating $count submission(s) from $batch_file against $OAG_BASE_URL"

failures=0
unresolved=0
for i in $(seq 0 $((count - 1))); do
  body="$(jq -c ".[$i]" "$batch_file")"
  label="$(printf '%s' "$body" | jq -r '.model + " " + (.payload.slug // .object_id // "?")')"

  oag_api POST /api/v1/submissions/validate/ "$body"
  resp="$OAG_LAST_BODY"
  if [ "${OAG_LAST_STATUS:-}" = "200" ] && [ "$(printf '%s' "$resp" | jq -r '.valid')" = "true" ]; then
    echo "  [$i] OK       $label"
  elif [ "${OAG_LAST_STATUS:-}" != "200" ] && [ "${OAG_LAST_STATUS:-}" != "400" ] && [ "${OAG_LAST_STATUS:-}" != "422" ]; then
    unresolved=$((unresolved + 1))
    echo "  [$i] UNRESOLVED  $label -> HTTP ${OAG_LAST_STATUS:-?}: $(oag_error_detail)"
  else
    failures=$((failures + 1))
    # A payload-shape / natural-key failure — the whole point of the dry-run — comes
    # back as { "errors": { "<field path>": [msg, …] } } on the public API; conflicts
    # as .conflict_type; other coded errors as .detail. Render whichever is present.
    detail="$(oag_error_detail)"
    echo "  [$i] INVALID  $label -> HTTP ${OAG_LAST_STATUS:-?}: $detail"
  fi
  [ "$i" -lt "$((count - 1))" ] && oag_pace
done

if [ "$unresolved" -gt 0 ]; then
  echo "$unresolved/$count unresolved; validation could not complete. Retry validation before submitting." >&2
  exit 1
fi
if [ "$failures" -gt 0 ]; then
  echo "$failures/$count invalid. Fix the payloads before submitting." >&2
  exit 1
fi
echo "All $count valid."

# Payloads are well-formed; now check that the URLs they cite survive the
# pipeline fetcher, which (unlike `curl -L`) does not follow redirects.
oag_preflight_urls "$batch_file"
if [ "${OAG_PREFLIGHT_REDIRECTS:-0}" -gt 0 ]; then
  exit 1
fi
