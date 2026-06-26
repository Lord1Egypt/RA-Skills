#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${GMAIL_BRIDGE_URL:-http://127.0.0.1:8787}"
SECRET="${BRIDGE_SECRET:-}"   # optional; if your bridge enforces x-bridge-secret

hdrs=()
if [[ -n "${SECRET}" ]]; then
  hdrs=(-H "x-bridge-secret: ${SECRET}")
fi

cmd="${1:-}"
shift || true

usage() {
  cat >&2 <<'USAGE'
Usage:
  run.sh recent [max]                    # list latest emails (subject/from/date/snippet)
  run.sh unread [max]                    # list unread emails
  run.sh search "<gmail query>" [max]    # search gmail (e.g. 'from:amazon invoice')
  run.sh get <messageId> [format]        # get one message (default: metadata; formats: metadata|full|raw)

  run.sh drive-search "<drive query>" [pageSize]
    # Example: run.sh drive-search "name contains 'FutureReady'" 10

  run.sh drive-file <fileId>

  run.sh sheets-get <spreadsheetId> "<range>"
    # Example: run.sh sheets-get 1AbC... "Sheet1!A1:D20"

  run.sh sheets-set <spreadsheetId> "<range>" '<jsonValues>'
    # jsonValues example: '[[\"A1\",\"B1\"],[\"A2\",\"B2\"]]'

  run.sh cal-events [maxResults] [timeMinISO] [timeMaxISO] [calendarId]
    # Example: run.sh cal-events 10 2026-02-01T00:00:00Z 2026-03-01T00:00:00Z primary

  run.sh cal-create "<summary>" <startISO> <endISO> [calendarId] [location] [description]
USAGE
}

jq_pretty='jq -C .'

case "${cmd}" in
  recent)
    max="${1:-10}"
    curl -sS "${hdrs[@]}" "${BASE_URL}/gmail/recent?max=${max}" | eval "${jq_pretty}"
    ;;
  unread)
    max="${1:-10}"
    curl -sS "${hdrs[@]}" "${BASE_URL}/gmail/unread?max=${max}" | eval "${jq_pretty}"
    ;;
  search)
    q="${1:-}"
    max="${2:-10}"
    if [[ -z "${q}" ]]; then usage; exit 2; fi
    # URL-encode query using jq
    q_enc="$(printf '%s' "${q}" | jq -sRr @uri)"
    curl -sS "${hdrs[@]}" "${BASE_URL}/gmail/recent?max=${max}&q=${q_enc}" | eval "${jq_pretty}"
    ;;
  get)
    id="${1:-}"
    format="${2:-metadata}"
    if [[ -z "${id}" ]]; then usage; exit 2; fi
    curl -sS "${hdrs[@]}" "${BASE_URL}/gmail/get/${id}?format=${format}" | eval "${jq_pretty}"
    ;;
  drive-search)
    q="${1:-}"
    pageSize="${2:-10}"
    if [[ -z "${q}" ]]; then usage; exit 2; fi
    q_enc="$(printf '%s' "${q}" | jq -sRr @uri)"
    curl -sS "${hdrs[@]}" "${BASE_URL}/drive/search?q=${q_enc}&pageSize=${pageSize}" | eval "${jq_pretty}"
    ;;
  drive-file)
    fileId="${1:-}"
    if [[ -z "${fileId}" ]]; then usage; exit 2; fi
    curl -sS "${hdrs[@]}" "${BASE_URL}/drive/file/${fileId}" | eval "${jq_pretty}"
    ;;
  sheets-get)
    spreadsheetId="${1:-}"
    range="${2:-}"
    if [[ -z "${spreadsheetId}" || -z "${range}" ]]; then usage; exit 2; fi
    range_enc="$(printf '%s' "${range}" | jq -sRr @uri)"
    curl -sS "${hdrs[@]}" "${BASE_URL}/sheets/get?spreadsheetId=${spreadsheetId}&range=${range_enc}" | eval "${jq_pretty}"
    ;;
  sheets-set)
    spreadsheetId="${1:-}"
    range="${2:-}"
    values_json="${3:-}"
    if [[ -z "${spreadsheetId}" || -z "${range}" || -z "${values_json}" ]]; then usage; exit 2; fi
    curl -sS "${hdrs[@]}" -X POST "${BASE_URL}/sheets/set" \
      -H "Content-Type: application/json" \
      -d "{\"spreadsheetId\":\"${spreadsheetId}\",\"range\":\"${range}\",\"values\":${values_json},\"valueInputOption\":\"USER_ENTERED\"}" \
      | eval "${jq_pretty}"
    ;;
  cal-events)
    maxResults="${1:-10}"
    timeMin="${2:-}"
    timeMax="${3:-}"
    calendarId="${4:-primary}"

    qs="maxResults=${maxResults}&calendarId=$(printf '%s' "${calendarId}" | jq -sRr @uri)"
    if [[ -n "${timeMin}" ]]; then qs="${qs}&timeMin=$(printf '%s' "${timeMin}" | jq -sRr @uri)"; fi
    if [[ -n "${timeMax}" ]]; then qs="${qs}&timeMax=$(printf '%s' "${timeMax}" | jq -sRr @uri)"; fi

    curl -sS "${hdrs[@]}" "${BASE_URL}/calendar/events?${qs}" | eval "${jq_pretty}"
    ;;
  cal-create)
    summary="${1:-}"
    startISO="${2:-}"
    endISO="${3:-}"
    calendarId="${4:-primary}"
    location="${5:-}"
    description="${6:-}"

    if [[ -z "${summary}" || -z "${startISO}" || -z "${endISO}" ]]; then usage; exit 2; fi

    curl -sS "${hdrs[@]}" -X POST "${BASE_URL}/calendar/create" \
      -H "Content-Type: application/json" \
      -d "$(jq -nc \
        --arg summary "${summary}" \
        --arg startISO "${startISO}" \
        --arg endISO "${endISO}" \
        --arg calendarId "${calendarId}" \
        --arg location "${location}" \
        --arg description "${description}" \
        '{summary:$summary,startISO:$startISO,endISO:$endISO,calendarId:$calendarId,location:$location,description:$description}')" \
      | eval "${jq_pretty}"
    ;;
  ""|-h|--help|help)
    usage
    ;;
  *)
    echo "Unknown command: ${cmd}" >&2
    usage
    exit 2
    ;;
esac
