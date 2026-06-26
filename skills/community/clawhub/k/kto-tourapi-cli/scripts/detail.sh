#!/usr/bin/env bash
# detail.sh — One-shot fetch of all detail endpoints for a single contentId.
#
# Fans out to:
#   - detailCommon2 (always)
#   - detailIntro2  (if --content-type-id passed)
#   - detailInfo2   (if --content-type-id passed; e.g. rooms for stays, days for courses)
#   - detailImage2  (if --include-images)
#
# Usage:
#   detail.sh --content-id 126508 [--content-type-id 12] [--include-images]
#
# Output: a single compact JSON object on stdout, with sub-keys:
#   { contentId, common, intro?, info?, images? }
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "$here/_common.sh"

cid="" cti="" include_images="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --content-id)       cid="$2";      shift 2;;
    --content-type-id)  cti="$2";      shift 2;;
    --include-images)   include_images="true"; shift;;
    -h|--help)
      sed -n '2,17p' "$0" | sed 's/^# \{0,1\}//'
      exit 0;;
    *) echo "error: unknown flag '$1'" >&2; exit 64;;
  esac
done

[[ -z "$cid" ]] && { echo "error: --content-id is required." >&2; exit 64; }
[[ -n "$cti" ]] && valid_content_type "$cti"

require_bin curl jq

# --- common (always) ---
common_raw=$(tourapi_get "detailCommon2" "contentId=$cid")
common=$(echo "$common_raw" | jq -c '
  .response.body.items.item as $it
  | if   $it == null then null
    elif ($it | type) == "array"  then $it[0]
    else $it
    end
')

intro="null"; info_arr="[]"; images_arr="[]"

if [[ -n "$cti" ]]; then
  intro_raw=$(tourapi_get "detailIntro2" "contentId=$cid" "contentTypeId=$cti")
  intro=$(echo "$intro_raw" | jq -c '
    .response.body.items.item as $it
    | if   $it == null then null
      elif ($it | type) == "array"  then $it[0]
      else $it
      end
  ')

  info_raw=$(tourapi_get "detailInfo2" "contentId=$cid" "contentTypeId=$cti")
  info_arr=$(echo "$info_raw" | jq -c '
    .response.body.items.item as $it
    | if   $it == null then []
      elif ($it | type) == "array"  then $it
      else [$it]
      end
  ')
fi

if [[ "$include_images" == "true" ]]; then
  img_raw=$(tourapi_get "detailImage2" "contentId=$cid" "imageYN=Y" "subImageYN=Y")
  images_arr=$(echo "$img_raw" | jq -c '
    .response.body.items.item as $it
    | if   $it == null then []
      elif ($it | type) == "array"  then $it
      else [$it]
      end
  ')
fi

jq -nc \
  --arg cid "$cid" \
  --argjson common "$common" \
  --argjson intro "$intro" \
  --argjson info "$info_arr" \
  --argjson images "$images_arr" \
  '{contentId:$cid, common:$common, intro:$intro, info:$info, images:$images}'
