#!/usr/bin/env bash
# scripts/contacts-read.sh
# Read Microsoft Graph personal contacts from the signed-in user's Outlook.com / M365 account.
#
# Subcommands:
#   list   [--filter <odata>] [--limit N] [--offset N] [--format summary|json|simple|raw]
#   search <query> [--limit N] [--format summary|json|simple|raw]
#
# Standalone auth: uses ~/.outlook-contacts/ config & tokens managed by this skill.
# Requires Contacts.Read scope in the access token.

set -Eeuo pipefail
IFS=$' \t\n'

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
# shellcheck source=./_lib.sh
. "$SCRIPT_DIR/_lib.sh"



usage() {
    cat >&2 <<'USAGE'
Usage: contacts-read.sh <subcommand> [options]

Subcommands:
  list                       List all contacts (paginated: max 200 per page).
  search <query>             Search contacts by displayName / emailAddress.
                             Uses Microsoft Graph $search (keyword search).

Options:
  --filter <odata>           OData $filter expression (list subcommand only).
                             e.g. "jobTitle eq 'Professor'"
                             e.g. "startswith(givenName,'X')"
  --limit N                  Max contacts to return.          [default: 50]
  --offset N                 Skip N contacts for pagination.  [default: 0]
  --format summary|json|simple|raw  Output format.            [default: summary]
                             summary  - compact table: name, email, phone, company
                             json     - pretty-printed full Graph JSON
                             simple   - one line per contact: "name <email>"
                             raw      - single-line JSON array

  -h, --help                 Show this help.

Examples:
  contacts-read.sh list --format summary
  contacts-read.sh search "Wang" --format simple
  contacts-read.sh list --filter "companyName eq 'Microsoft'" --format json
USAGE
}

SUBCMD="${1:-list}"
shift || true

case "$SUBCMD" in
    -h|--help|"") usage; exit 0 ;;
    list|search) : ;;
    *) die "unknown subcommand: $SUBCMD  (try list or search)" ;;
esac

# ---- Parse shared options --------------------------------------------------
FORMAT="summary"
LIMIT=50
OFFSET=0
FILTER=""
QUERY=""

while (( $# > 0 )); do
    case "$1" in
        --format)
            FORMAT="${2:-summary}"
            shift 2
            ;;
        --limit)
            LIMIT="$2"
            [[ "$LIMIT" =~ ^[0-9]+$ ]] && (( LIMIT >= 1 )) || die "--limit must be a positive integer"
            shift 2
            ;;
        --offset)
            OFFSET="$2"
            [[ "$OFFSET" =~ ^[0-9]+$ ]] && (( OFFSET >= 0 )) || die "--offset must be a non-negative integer"
            shift 2
            ;;
        --filter)
            FILTER="$2"
            shift 2
            ;;
        -h|--help)
            usage; exit 0
            ;;
        --)
            shift
            QUERY="$*"
            break
            ;;
        *)
            # positional: search query or unknown
            if [[ "$SUBCMD" == "search" && -z "$QUERY" ]]; then
                QUERY="$1"
            else
                die "unknown option: $1"
            fi
            shift
            ;;
    esac
done

if [[ "$SUBCMD" == "search" && -z "$QUERY" ]]; then
    die "search subcommand requires a query string"
fi

case "$FORMAT" in
    summary|json|simple|raw) : ;;
    *) die "unknown format: $FORMAT (expected summary|json|simple|raw)" ;;
esac

# ---- Auth check ------------------------------------------------------------
load_config  || die "config missing; run scripts/setup-device-code.sh first"
load_tokens  || die "tokens missing; run scripts/setup-device-code.sh first"
ensure_fresh_token

# Verify the token has Contacts.Read scope
_check_contacts_scope() {
    if [[ ! -f "$OUTLOOK_CONTACTS_TOKENS" ]]; then
        die "no tokens file; run scripts/setup-device-code.sh first"
    fi
    local scope
    scope=$(jq -r '.scope // ""' "$OUTLOOK_CONTACTS_TOKENS" 2>/dev/null || echo "")
    if [[ "$scope" != *"Contacts.Read"* && "$scope" != *"Contacts.ReadWrite"* ]]; then
        cat >&2 <<EOF
[error] token scope does not include the contacts permission (Contacts.ReadWrite).
        Current scopes: $scope

        This skill has its own contacts-scoped login. Re-run the local setup
        to refresh scopes:

          cd ~/.openclaw/skills/outlook-contacts
          ./scripts/setup-device-code.sh --client-id \$CLIENT_ID --tenant-id common --force

EOF
        exit 1
    fi
    return 0
}
_check_contacts_scope

# ---- Query helpers ---------------------------------------------------------

# Build the Graph URL with query params
build_contacts_url() {
    local base="${OUTLOOK_CONTACTS_GRAPH_BASE}/me/contacts"
    local -a params=()

    # Select reasonable fields to limit response size
    params+=("\$select=id,displayName,givenName,surname,emailAddresses,businessPhones,homePhones,mobilePhone,companyName,jobTitle,personalNotes,createdDateTime,lastModifiedDateTime")

    if [[ "$SUBCMD" == "search" && -n "$QUERY" ]]; then
        # URL-encode the search query
        local encoded
        encoded=$(python3 -c "import sys,urllib.parse; print(urllib.parse.quote(sys.argv[1]))" "$QUERY" 2>/dev/null || printf '%s' "$QUERY")
        params+=("\$search=\"$encoded\"")
    fi

    if [[ -n "$FILTER" ]]; then
        local encoded_filter
        encoded_filter=$(python3 -c "import sys,urllib.parse; print(urllib.parse.quote(sys.argv[1]))" "$FILTER" 2>/dev/null || printf '%s' "$FILTER")
        params+=("\$filter=$encoded_filter")
    fi

    # Default ordering by displayName
    if [[ "$SUBCMD" != "search" ]]; then
        params+=("\$orderby=displayName")
    fi

    params+=("\$top=$LIMIT")
    if (( OFFSET > 0 )); then
        params+=("\$skip=$OFFSET")
    fi

    local qs
    qs=$(printf '&%s' "${params[@]}")
    printf '%s?%s' "$base" "${qs:1}"
}

# ---- Formatters ------------------------------------------------------------

# Extract primary email from emailAddresses array
_extract_primary_email() {
    jq -r '
        if (.emailAddresses | type) == "array" then
            ([.emailAddresses[] | select(.address != null)] | .[0].address // "-")
        else
            "-"
        end
    '
}

# Extract primary phone: mobilePhone > businessPhones[0] > homePhones[0]
_extract_phone() {
    jq -r '
        .mobilePhone //
        ((.businessPhones | if type == "array" then .[0] else null end)) //
        ((.homePhones | if type == "array" then .[0] else null end)) //
        "-"
    '
}

# ---- Main logic ------------------------------------------------------------

URL=$(build_contacts_url)
log_info "GET $URL"

RESP=$(graph_request GET "$URL")

# Check if response has .value array
if ! echo "$RESP" | jq -e '.value' >/dev/null 2>&1; then
    die "Graph response missing .value array: $(echo "$RESP" | head -c 300)"
fi

TOTAL=$(echo "$RESP" | jq '.value | length')
NEXT_LINK=$(echo "$RESP" | jq -r '.["@odata.nextLink"] // empty')

case "$FORMAT" in
    raw)
        echo "$RESP" | jq -c '.value'
        [[ -n "$NEXT_LINK" ]] && log_info "next page: $NEXT_LINK (use --offset to paginate)" >&2 || true
        ;;
    json)
        echo "$RESP" | jq '.'
        [[ -n "$NEXT_LINK" ]] && log_info "next page: $NEXT_LINK (use --offset to paginate)" >&2 || true
        ;;
    summary)
        if (( TOTAL == 0 )); then
            echo "(no contacts found)" >&2
            exit 0
        fi

        # Header
        printf '%-20s  %-28s  %-16s  %-15s  %-15s\n' "NAME" "EMAIL" "PHONE" "COMPANY" "TITLE" >&2
        printf '%.0s-' {1..100} >&2
        echo >&2
        printf '\n' >&2

        # Rows
        echo "$RESP" | jq -c '.value[]' | while read -r contact; do
            name=$(echo "$contact" | jq -r '.displayName // "?"')
            email=$(echo "$contact" | _extract_primary_email)
            phone=$(echo "$contact" | _extract_phone)
            company=$(echo "$contact" | jq -r '.companyName // "-"')
            title=$(echo "$contact" | jq -r '.jobTitle // "-"')
            printf '%-20s  %-28s  %-16s  %-15s  %-15s\n' \
                "${name:0:19}" "${email:0:27}" "${phone:0:15}" "${company:0:14}" "${title:0:14}"
        done

        echo >&2
        echo "Total: $TOTAL contacts" >&2
        [[ -n "$NEXT_LINK" ]] && log_info "more results available (use --offset to paginate)" >&2 || true
        ;;
    simple)
        if (( TOTAL == 0 )); then
            echo "(no contacts found)"
            exit 0
        fi
        echo "$RESP" | jq -r '
            .value[] |
            def em: if (.emailAddresses | type) == "array" then ([.emailAddresses[] | select(.address != null)] | .[0].address // "") else "" end;
            def ph: .mobilePhone // ((.businessPhones | if type == "array" then .[0] else null end)) // ((.homePhones | if type == "array" then .[0] else null end)) // "";
            if em != "" then
                (if ph != "" then "\(.displayName // "?") <\(em)> 📞\(ph)" else "\(.displayName // "?") <\(em)>" end)
            else
                "\(.displayName // "?")"
            end
        '
        [[ -n "$NEXT_LINK" ]] && log_info "more results available (use --offset to paginate)" >&2 || true
        ;;
esac
