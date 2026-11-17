#!/usr/bin/env bash
# scripts/contacts-write.sh
# Read, update, create, and delete Microsoft Graph contacts.
#
# Subcommands:
#   get    --contact-id <id>   [--format json|summary|raw]
#   update --contact-id <id>   [--display-name ...] [--given-name ...] ... [--apply]
#   create --display-name ...   [--given-name ...] [--surname ...] [--email ...] ... [--apply]
#   delete --contact-id <id>   [--apply]
#
# Safety rules (same as calendar-write.sh):
#   1. Dry-run by default; --apply required for real writes.
#   2. Delete always shows the contact first, then asks for "YES" confirmation.
#   3. Update shows current values and proposed changes before applying.
#   4. Never logs tokens.

set -Eeuo pipefail
IFS=$' \t\n'

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
# shellcheck source=./_lib.sh
. "$SCRIPT_DIR/_lib.sh"



usage() {
    cat >&2 <<'USAGE'
Usage: contacts-write.sh <subcommand> [options]

Subcommands:
  get    --contact-id <id>   [--format json|summary|raw]
  update --contact-id <id>   [--display-name ...] [--given-name ...] [--surname ...]
                             [--email ...] [--phone ...] [--company ...] [--job-title ...]
                             [--notes ...] [--apply]
  create --display-name ...  [--given-name ...] [--surname ...] [--email ...]
                             [--phone ...] [--company ...] [--job-title ...] [--notes ...]
                             [--apply]
  delete --contact-id <id>   [--apply]

Options:
  --contact-id <id>    Contact ID (for get/update/delete)
  --display-name       Full display name
  --given-name         First name
  --surname            Last name
  --email              Primary email address (replaces existing email array)
  --phone              Mobile phone number
  --company            Company name
  --job-title          Job title
  --notes              Personal notes
  --format summary|json|raw   Output format (default: summary)
  --apply              Actually execute the write (default: dry-run)
  -h, --help           Show this help

Safety:
  - update/create default to dry-run (prints JSON payload, no network call)
  - delete always shows the contact first and asks for confirmation
  - pass --apply to execute; for delete you must also type YES at the prompt

Examples:
  # View a contact (dry)
  contacts-write.sh get --contact-id "AAMk..."

  # Update a contact (dry-run, see payload)
  contacts-write.sh update --contact-id "AAMk..." --email "new@example.com" --phone "13812345678"

  # Actually update
  contacts-write.sh update --contact-id "AAMk..." --email "new@example.com" --apply

  # Create a new contact
  contacts-write.sh create --display-name "Zhang San" --email "zhang@example.com" --phone "13912345678" --apply

  # Delete a contact (always requires --apply + YES confirmation)
  contacts-write.sh delete --contact-id "AAMk..." --apply
USAGE
}

# ---- Common helpers --------------------------------------------------------

# Check token has Contacts.Read or Contacts.ReadWrite (for read/get)
_check_contacts_read_scope() {
    if [[ ! -f "$OUTLOOK_CONTACTS_TOKENS" ]]; then
        die "no tokens file; run scripts/setup-device-code.sh first"
    fi
    local scope
    scope=$(jq -r '.scope // ""' "$OUTLOOK_CONTACTS_TOKENS" 2>/dev/null || echo "")
    if [[ "$scope" != *"Contacts.Read"* && "$scope" != *"Contacts.ReadWrite"* ]]; then
        die "token scope missing Contacts.Read (or Contacts.ReadWrite). Re-run setup-device-code.sh with --force."
    fi
}

# Check token has Contacts.ReadWrite (for create/update/delete)
_check_contacts_write_scope() {
    if [[ ! -f "$OUTLOOK_CONTACTS_TOKENS" ]]; then
        die "no tokens file; run scripts/setup-device-code.sh first"
    fi
    local scope
    scope=$(jq -r '.scope // ""' "$OUTLOOK_CONTACTS_TOKENS" 2>/dev/null || echo "")
    if [[ "$scope" != *"Contacts.ReadWrite"* ]]; then
        die "token scope missing Contacts.ReadWrite. Re-run setup-device-code.sh with --force."
    fi
}

# Format a single contact object for summary
print_contact_summary() {
    local json="$1"
    printf '%s' "$json" | jq -r '
        def em:  if (.emailAddresses | type) == "array" then ([.emailAddresses[] | select(.address != null)] | .[0].address // "-") else "-" end;
        def ph:  .mobilePhone // ((.businessPhones | if type == "array" then .[0] else null end)) // ((.homePhones | if type == "array" then .[0] else null end)) // "-";
        def bp:  if (.businessPhones | type) == "array" then .businessPhones | join(", ") else "-" end;
        def hp:  if (.homePhones | type) == "array" then .homePhones | join(", ") else "-" end;
        def id:  .id // "-";
        "ID:         \(.id)",
        "Name:       \(.displayName // "-")",
        "Given:      \(.givenName // "-")",
        "Surname:    \(.surname // "-")",
        "Email:      \(em)",
        "Mobile:     \(.mobilePhone // "-")",
        "Business:   \(bp)",
        "Home:       \(hp)",
        "Company:    \(.companyName // "-")",
        "Job Title:  \(.jobTitle // "-")",
        "Notes:      \(.personalNotes // "-")"
    ' >&2
}

# Build a JSON contact body from the provided fields
build_contact_body() {
    local dn="${1:-}" gn="${2:-}" sn="${3:-}" email="${4:-}" phone="${5:-}" company="${6:-}" jobTitle="${7:-}" notes="${8:-}"

    # Start with empty object
    local jq_filter='{}'
    local -a jq_args=()

    if [[ -n "$dn" ]]; then
        jq_filter+=' | .displayName=$dn'
        jq_args+=(--arg dn "$dn")
    fi
    if [[ -n "$gn" ]]; then
        jq_filter+=' | .givenName=$gn'
        jq_args+=(--arg gn "$gn")
    fi
    if [[ -n "$sn" ]]; then
        jq_filter+=' | .surname=$sn'
        jq_args+=(--arg sn "$sn")
    fi
    if [[ -n "$email" ]]; then
        jq_filter+=' | .emailAddresses=[{name: $emailName, address: $emailAddr}]'
        jq_args+=(--arg emailName "$dn" --arg emailAddr "$email")
    fi
    if [[ -n "$phone" ]]; then
        jq_filter+=' | .mobilePhone=$phone'
        jq_args+=(--arg phone "$phone")
    fi
    if [[ -n "$company" ]]; then
        jq_filter+=' | .companyName=$company'
        jq_args+=(--arg company "$company")
    fi
    if [[ -n "$jobTitle" ]]; then
        jq_filter+=' | .jobTitle=$jobTitle'
        jq_args+=(--arg jobTitle "$jobTitle")
    fi
    if [[ -n "$notes" ]]; then
        jq_filter+=' | .personalNotes=$notes'
        jq_args+=(--arg notes "$notes")
    fi

    # Remove null/empty fields
    jq_filter+=' | with_entries(select(.value != null and .value != "" and .value != []))'

    jq -n "${jq_args[@]}" "$jq_filter"
}

# ---- Subcommands -----------------------------------------------------------

cmd_get() {
    local contact_id="" format="summary"
    while (( $# > 0 )); do
        case "$1" in
            --contact-id) contact_id="$2"; shift 2 ;;
            --format)     format="$2"; shift 2 ;;
            -h|--help)    usage; exit 0 ;;
            *)            die "unknown option: $1" ;;
        esac
    done
    [[ -n "$contact_id" ]] || die "--contact-id is required"

    load_config || die "config missing"
    load_tokens || die "tokens missing"
    ensure_fresh_token
    _check_contacts_read_scope

    local url="${OUTLOOK_CONTACTS_GRAPH_BASE}/me/contacts/$contact_id"
    log_info "GET $url"
    local resp
    resp=$(graph_request GET "$url")

    case "$format" in
        raw)  echo "$resp" | jq -c . ;;
        json) echo "$resp" | jq . ;;
        summary) print_contact_summary "$resp" ;;
        *) die "unknown format: $format" ;;
    esac
}

cmd_update() {
    local contact_id="" display_name="" given_name="" surname="" email="" phone="" company="" job_title="" notes="" apply=0 yes=0
    while (( $# > 0 )); do
        case "$1" in
            --contact-id)   contact_id="$2"; shift 2 ;;
            --display-name) display_name="$2"; shift 2 ;;
            --given-name)   given_name="$2"; shift 2 ;;
            --surname)      surname="$2"; shift 2 ;;
            --email)        email="$2"; shift 2 ;;
            --phone)        phone="$2"; shift 2 ;;
            --company)      company="$2"; shift 2 ;;
            --job-title)    job_title="$2"; shift 2 ;;
            --notes)        notes="$2"; shift 2 ;;
            --apply)        apply=1; shift ;;
            --yes)          yes=1; shift ;;
            -h|--help)      usage; exit 0 ;;
            *)              die "unknown option: $1" ;;
        esac
    done
    [[ -n "$contact_id" ]] || die "--contact-id is required"

    # At least one field to change
    if [[ -z "$display_name" && -z "$given_name" && -z "$surname" && -z "$email" && -z "$phone" && -z "$company" && -z "$job_title" && -z "$notes" ]]; then
        die "at least one field to update is required (--display-name, --email, --phone, etc.)"
    fi

    load_config || die "config missing"
    load_tokens || die "tokens missing"
    ensure_fresh_token
    _check_contacts_write_scope

    # 1. Fetch current state
    local url="${OUTLOOK_CONTACTS_GRAPH_BASE}/me/contacts/$contact_id"
    log_info "GET $url (fetch current state)"
    local current
    current=$(graph_request GET "$url")

    echo "--- Current contact ---" >&2
    print_contact_summary "$current" >&2
    echo "" >&2

    # 2. Build the PATCH body
    local body
    body=$(build_contact_body "$display_name" "$given_name" "$surname" "$email" "$phone" "$company" "$job_title" "$notes")

    echo "--- Proposed changes ---" >&2
    echo "$body" | jq . >&2
    echo "" >&2

    # 3. Dry-run or apply (with confirmation)
    if ! require_apply_and_confirm "$apply" "$yes" "UPDATE contact $contact_id"; then
        exit 0
    fi

    echo "Applying PATCH to $url ..." >&2
    local resp
    resp=$(graph_request PATCH "$url" "$body")
    echo "--- Updated contact ---" >&2
    print_contact_summary "$resp" >&2
}

cmd_create() {
    local display_name="" given_name="" surname="" email="" phone="" company="" job_title="" notes="" apply=0 yes=0
    while (( $# > 0 )); do
        case "$1" in
            --display-name) display_name="$2"; shift 2 ;;
            --given-name)   given_name="$2"; shift 2 ;;
            --surname)      surname="$2"; shift 2 ;;
            --email)        email="$2"; shift 2 ;;
            --phone)        phone="$2"; shift 2 ;;
            --company)      company="$2"; shift 2 ;;
            --job-title)    job_title="$2"; shift 2 ;;
            --notes)        notes="$2"; shift 2 ;;
            --apply)        apply=1; shift ;;
            --yes)          yes=1; shift ;;
            -h|--help)      usage; exit 0 ;;
            *)              die "unknown option: $1" ;;
        esac
    done
    [[ -n "$display_name" ]] || die "--display-name is required for create"

    load_config || die "config missing"
    load_tokens || die "tokens missing"
    ensure_fresh_token
    _check_contacts_write_scope

    local body
    body=$(build_contact_body "$display_name" "$given_name" "$surname" "$email" "$phone" "$company" "$job_title" "$notes")

    echo "--- Proposed new contact ---" >&2
    echo "$body" | jq . >&2
    echo "" >&2

    if ! require_apply_and_confirm "$apply" "$yes" "CREATE contact '$display_name'"; then
        exit 0
    fi

    local url="${OUTLOOK_CONTACTS_GRAPH_BASE}/me/contacts"
    echo "POST $url ..." >&2
    local resp
    resp=$(graph_request POST "$url" "$body")
    echo "--- Created contact ---" >&2
    print_contact_summary "$resp" >&2
}

cmd_delete() {
    local contact_id="" apply=0 yes=0
    while (( $# > 0 )); do
        case "$1" in
            --contact-id) contact_id="$2"; shift 2 ;;
            --apply)      apply=1; shift ;;
            --yes)        yes=1; shift ;;
            -h|--help)    usage; exit 0 ;;
            *)            die "unknown option: $1" ;;
        esac
    done
    [[ -n "$contact_id" ]] || die "--contact-id is required"

    load_config || die "config missing"
    load_tokens || die "tokens missing"
    ensure_fresh_token
    _check_contacts_write_scope

    local url="${OUTLOOK_CONTACTS_GRAPH_BASE}/me/contacts/$contact_id"
    log_info "GET $url (fetching before delete)"
    local current
    current=$(graph_request GET "$url")

    echo "--- Contact to be deleted ---" >&2
    print_contact_summary "$current" >&2
    echo "" >&2

    if ! require_apply_and_confirm "$apply" "$yes" "DELETE contact $contact_id"; then
        exit 0
    fi

    graph_request DELETE "$url" >/dev/null
    log_info "contact deleted ($contact_id)"
}

# ---- Dispatch --------------------------------------------------------------

SUBCMD="${1:-}"
shift || true

case "$SUBCMD" in
    -h|--help|"")   usage; exit 0 ;;
    get)             cmd_get "$@" ;;
    update)          cmd_update "$@" ;;
    create)          cmd_create "$@" ;;
    delete)          cmd_delete "$@" ;;
    *)               die "unknown subcommand: $SUBCMD" ;;
esac
