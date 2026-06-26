#!/usr/bin/env bash
# Mental Health Booking API client for OpenClaw skill
# Usage: booking-api.sh <command> [args...]
#
# Commands:
#   services                                          - List services, states, insurance carriers
#   availability <service> <state> [carrier] [date] [time_pref] - Search providers
#   book '<json>'                                     - Book an appointment (pass JSON string)
#   book-dry '<json>'                                 - Dry-run booking (validates, doesn't book)

set -euo pipefail

BASE_URL="${BOOKING_API_URL:-https://rx.helloklarity.com}"

command="${1:-}"
shift || true

error() { echo "ERROR: $*" >&2; exit 1; }

case "$command" in
  services)
    curl -sf "${BASE_URL}/api/v1/services" | python3 -m json.tool
    ;;

  availability)
    service="${1:-}" ; shift || true
    state="${1:-}"   ; shift || true
    carrier="${1:-}" ; shift || true
    date="${1:-}"    ; shift || true
    time_pref="${1:-}" ; shift || true

    [ -z "$service" ] && error "Usage: klarity-api.sh availability <service> <state> [carrier] [date] [time_pref]"
    [ -z "$state" ]   && error "Usage: klarity-api.sh availability <service> <state> [carrier] [date] [time_pref]"

    # Build query string
    qs="service=${service}&state=${state}"
    [ -n "$carrier" ]   && qs="${qs}&insurance_carrier=$(python3 -c "import urllib.parse; print(urllib.parse.quote('${carrier}'))")"
    [ -n "$date" ]      && qs="${qs}&date=${date}"
    [ -n "$time_pref" ] && qs="${qs}&time_preference=${time_pref}"

    curl -sf "${BASE_URL}/api/v1/availability?${qs}" | python3 -m json.tool
    ;;

  book|book-dry)
    json="${1:-}"
    [ -z "$json" ] && error "Usage: klarity-api.sh book '<json-payload>'"

    url="${BASE_URL}/api/v1/book"
    [ "$command" = "book-dry" ] && url="${url}?mode=dry_run"

    curl -s -X POST \
      -H "Content-Type: application/json" \
      -d "$json" \
      "$url" | python3 -m json.tool
    ;;

  *)
    echo "Mental Health Booking API — OpenClaw Skill"
    echo ""
    echo "Usage: booking-api.sh <command> [args...]"
    echo ""
    echo "Commands:"
    echo "  services                                            List services, states, carriers"
    echo "  availability <service> <state> [carrier] [date] [time]  Search providers"
    echo "  book '<json>'                                       Book appointment"
    echo "  book-dry '<json>'                                   Dry-run (validate only)"
    echo ""
    echo "Environment:"
    echo "  BOOKING_API_URL    Override base URL (default: https://rx.helloklarity.com)"
    ;;
esac
