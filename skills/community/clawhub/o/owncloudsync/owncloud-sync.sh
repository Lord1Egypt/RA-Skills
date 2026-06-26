#!/usr/bin/env zsh
# ==============================================================================
# Script:       owncloud-sync.sh
# Generated on: 2026-03-01
#
# Description:  Queries Google Drive for recently modified files, compares them
#               against the OwnCloud file inventory, and emails a sync report
#               highlighting MISSING or NEED UPDATE entries.
# ==============================================================================

# ==============================================================================
# PARAMETERS
# ==============================================================================

CONFIG_FILE="$(dirname "$0")/owncloud.json"

if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "FATAL: Configuration file not found: $CONFIG_FILE" >&2
    exit 1
fi

# Load OwnCloud connection parameters from JSON config via jq
ALLFILES_URL=$(jq -r '.ALLFILES_URL // empty' "$CONFIG_FILE")
ALLFILES_USER=$(jq -r '.ALLFILES_USER // empty' "$CONFIG_FILE")
ALLFILES_PASS=$(jq -r '.ALLFILES_PASS // empty' "$CONFIG_FILE")
GOG_ACCOUNT=$(jq -r '.GOG_ACCOUNT // empty' "$CONFIG_FILE")
EMAIL_RECIPIENT=$(jq -r '.EMAIL_RECIPIENT // empty' "$CONFIG_FILE")
PERIOD_DAYS=$(jq -r '.PERIOD_DAYS // empty' "$CONFIG_FILE")

if [[ -z "$ALLFILES_URL" || -z "$ALLFILES_USER" || -z "$ALLFILES_PASS" ]]; then
    echo "FATAL: ALLFILES_URL, ALLFILES_USER, or ALLFILES_PASS missing/empty in $CONFIG_FILE" >&2
    exit 1
fi

if [[ -z "$GOG_ACCOUNT" || -z "$EMAIL_RECIPIENT" || -z "$PERIOD_DAYS" ]]; then
    echo "FATAL: GOG_ACCOUNT, EMAIL_RECIPIENT, or PERIOD_DAYS missing/empty in $CONFIG_FILE" >&2
    exit 1
fi

# ---------------------------------------------------------------------------
# Validate ALLFILES_URL against a strict allowlist before use: must be HTTPS,
# must not contain credentials, redirects, or path traversal sequences.
# This limits the blast radius of a compromised owncloud.json by ensuring
# the URL cannot be silently redirected to an arbitrary external server.
# ---------------------------------------------------------------------------
if [[ ! "$ALLFILES_URL" =~ ^https://[a-zA-Z0-9._-]+(:[0-9]+)?(/[a-zA-Z0-9/_.-]*)?$ ]]; then
    echo "FATAL: ALLFILES_URL does not match expected format (HTTPS only, no credentials): '$ALLFILES_URL'" >&2
    exit 1
fi

export GOG_ACCOUNT

# Compute START_DATE: PERIOD_DAYS days before today
if [[ "$(uname)" == "Darwin" ]]; then
    START_DATE=$(date -v-${PERIOD_DAYS}d +%Y-%m-%d)
else
    START_DATE=$(date -d "${PERIOD_DAYS} days ago" +%Y-%m-%d)
fi

# Could be used to narrow scope
# GOOGLE_DRIVE_QUERY="after:${START_DATE} -type:image"

GOOGLE_DRIVE_QUERY="after:${START_DATE}"

# ==============================================================================
# TEMPORARY FILES & CLEANUP
# ==============================================================================
WORK_DIR=$(mktemp -d "${TMPDIR:-/tmp}/owncloud_sync.XXXXXX")
REPORT_FILE="${WORK_DIR}/report.txt"
GD_RAW_FILE="${WORK_DIR}/gdrive_raw.txt"
OC_RAW_FILE="${WORK_DIR}/owncloud_raw.txt"

cleanup() {
    rm -rf "$WORK_DIR"
}
trap cleanup EXIT INT TERM

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

# --------------------------------------------------------------------------
# date_to_epoch: Convert a date string to epoch seconds for comparison.
#   Handles: "YYYY-MM-DD HH:MM", "YYYY-MM-DD HH:MM:SS",
#            "YYYY-MM-DDTHH:MM:SSZ", "YYYY-MM-DDTHH:MM:SS.nnn+00:00"
# --------------------------------------------------------------------------
date_to_epoch() {
    local dt="$1"

    # Nettoyage agressif
    dt="${dt//T/ }"
    dt="${dt//Z/}"
    dt="${dt%%+*}"
    dt="${dt%%.*}"          # enlève millisecondes

    # Si on a exactement YYYY-MM-DD HH:MM → on ajoute :00
    if [[ $dt =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}\ [0-9]{2}:[0-9]{2}$ ]]; then
        dt="${dt}:00"
    fi

    if [[ "$(uname)" == "Darwin" ]]; then
        date -j -f "%Y-%m-%d %H:%M:%S" "$dt" "+%s" 2>/dev/null || echo "0"
    else
        date -d "$dt" "+%s" 2>/dev/null || echo "0"
    fi
}

# --------------------------------------------------------------------------
# clean_filename: Normalize whitespace in a filename.
#   - Tabs → spaces
#   - Collapse consecutive spaces
#   - Trim leading/trailing whitespace
# --------------------------------------------------------------------------
clean_filename() {
    local name="$1"
    name="${name//$'\t'/ }"                       # tabs → spaces
    name=$(echo "$name" | sed 's/  */ /g')        # collapse spaces
    name="${name## }"                              # trim leading
    name="${name%% }"                              # trim trailing
    echo "$name"
}

# ---------------------------------------------------------------------------
# sed_escape: Sanitize a string for safe interpolation into a sed replacement.
# Escapes characters that carry special meaning in sed's substitution syntax
# (& triggers a back-reference, | and \ break the delimiter or escape chain),
# preventing unintended behavior when variable content is untrusted or
# contains URL-like strings, paths, or arbitrary user input.
# ---------------------------------------------------------------------------
sed_escape() {
    printf '%s' "$1" | sed 's/[&\|]/\\&/g'
}

# ==============================================================================
# TIMING
# ==============================================================================

TIMER_START=$SECONDS
RUN_DATETIME=$(date "+%Y-%m-%d %H:%M:%S %Z")

echo "INFO: =============================================="
echo "INFO: OwnCloud Sync Check — $RUN_DATETIME"
echo "INFO: Period : last $PERIOD_DAYS days (since $START_DATE)"
echo "INFO: Query  : $GOOGLE_DRIVE_QUERY"
echo "INFO: =============================================="

# ==============================================================================
# STEP 1 — Fetch Google Drive file list
# ==============================================================================

echo "INFO: [Step 1/6] Querying Google Drive..."

if ! gog drive search "$GOOGLE_DRIVE_QUERY" > "$GD_RAW_FILE" 2>/dev/null; then
    echo "FATAL: 'gog drive search' failed (exit $?)" >&2
    exit 1
fi

echo "INFO:   → $(wc -l < "$GD_RAW_FILE" | tr -d ' ') raw lines returned"

# ==============================================================================
# STEP 2 — Fetch OwnCloud file list
# ==============================================================================

echo "INFO: [Step 2/6] Fetching OwnCloud file list..."

if ! curl -s -f \
        --proto '=https' \
        --proto-redir '=https' \
        --max-redirs 0 \
        -u "${ALLFILES_USER}:${ALLFILES_PASS}" \
        "${ALLFILES_URL}" \
        > "$OC_RAW_FILE" 2>/dev/null; then
    echo "FATAL: curl to OwnCloud failed (exit $?)" >&2
    exit 1
fi

echo "INFO:   → $(wc -l < "$OC_RAW_FILE" | tr -d ' ') lines returned"

# ==============================================================================
# STEP 3 — Parse OwnCloud file list
#   Format per line:  filename|YYYY-MM-DD HH:MM
#   Example:          Introducing ownCloud.pdf|2022-10-29 22:40
# ==============================================================================

echo "INFO: [Step 3/6] Parsing OwnCloud file list..."

typeset -A oc_dates   # oc_dates[cleaned_filename] = "YYYY-MM-DD HH:MM"

while IFS='|' read -r oc_raw_name oc_raw_date; do
    [[ -z "$oc_raw_name" ]] && continue

    # Trim each field
    oc_raw_name="${oc_raw_name## }"; oc_raw_name="${oc_raw_name%% }"
    oc_raw_date="${oc_raw_date## }"; oc_raw_date="${oc_raw_date%% }"

    oc_clean=$(clean_filename "$oc_raw_name")
    oc_dates["$oc_clean"]="$oc_raw_date"

done < "$OC_RAW_FILE"

echo "INFO:   → ${#oc_dates[@]} files indexed from OwnCloud"

# ==============================================================================
# STEP 4 — Parse Google Drive output
#
#   The 'gog drive search' command returns more than just a name and date.
#   Typical output may look like (tab-separated or fixed-width):
#
#     Id                                Name                       MimeType          ModifiedTime                 Size
#     1BxiMVs0XRA5nFMdKvBdBZjgmUUqpt   facture Q1.pdf             application/pdf   2025-06-15T10:30:00.000Z     123456
#
#   Strategy:
#     A) If tabs are present → split by tab, locate the date column by regex.
#     B) Otherwise → locate the ISO-8601 date via regex, extract the filename
#        from the text preceding it (stripping a leading ID hash).
#
#   In all cases the filename is cleaned (tabs→spaces, collapse, trim).
# ==============================================================================

echo "INFO: [Step 4/6] Parsing Google Drive output..."

typeset -a gd_filenames
typeset -a gd_moddates

IS_FIRST_LINE=true

while IFS= read -r raw_line; do

    # --- Skip the header line ---
    if $IS_FIRST_LINE; then
        IS_FIRST_LINE=false
        # If it looks like a header row, skip it
        if [[ "$raw_line" == *"Name"* || "$raw_line" == *"Id"* \
           || "$raw_line" == *"Modified"* || "$raw_line" == *"Mime"* ]]; then
            continue
        fi
        # Otherwise fall through and parse it as data
    fi

    # Skip blank lines
    [[ -z "${raw_line//[[:space:]]/}" ]] && continue

    gd_name=""
    gd_date=""

    # ------------------------------------------------------------------
    # Strategy A: Tab-separated fields
    # ------------------------------------------------------------------
    if [[ "$raw_line" == *$'\t'* ]]; then

        # Split on literal tab into an array
        local -a tab_fields=("${(@s/	/)raw_line}")

        # Locate the field that looks like an ISO-8601 date
        local date_idx=0
        for (( fi = 1; fi <= ${#tab_fields[@]}; fi++ )); do
            if [[ "${tab_fields[$fi]}" =~ [0-9]{4}-[0-9]{2}-[0-9]{2}[T\ ][0-9]{2}:[0-9]{2} ]]; then
                date_idx=$fi
                break
            fi
        done

        if (( date_idx > 0 )); then
            gd_date="${tab_fields[$date_idx]}"
            # Name is expected in the 2nd field (after the ID)
            if (( ${#tab_fields[@]} >= 2 )); then
                gd_name="${tab_fields[2]}"
            fi
        elif (( ${#tab_fields[@]} >= 2 )); then
            # Fallback: assume field 1 = name, field 2 = date
            gd_name="${tab_fields[1]}"
            gd_date="${tab_fields[2]}"
        fi

    # ------------------------------------------------------------------
    # Strategy B: Locate ISO-8601 date in the line with regex
    # ------------------------------------------------------------------
    elif [[ "$raw_line" =~ ([0-9]{4}-[0-9]{2}-[0-9]{2}[T\ ][0-9]{2}:[0-9]{2}(:[0-9]{2})?(\.[0-9]+)?(Z|[+-][0-9]{2}:?[0-9]{2})?) ]]; then
        gd_date="${match[1]}"

        # Everything before the date is "ID + Name + Type + Size"
        local before_date="${raw_line%%${gd_date}*}"

        # 1. Strip a leading Google Drive file-ID (si présent)
        before_date=$(echo "$before_date" | sed -E 's/^[a-zA-Z0-9_-]{15,}[[:space:]]+//')

        # 2. Strip the SIZE at the end (handles "-", "5 B", "100.2 KB", etc.)
        # On cherche un bloc final qui est soit "-" soit "chiffres + espace optionnel + unité"
        before_date=$(echo "$before_date" | sed -E 's/[[:space:]]+([0-9.]+[[:space:]]*[A-Z]*|-)[[:space:]]*$//')

        # 3. Strip the TYPE / MIME-TYPE (ex: "file", "dir", "application/pdf")
        # Maintenant que la taille est partie, c'est le dernier mot restant avant le nom
        before_date=$(echo "$before_date" | sed -E 's/[[:space:]]+[^[:space:]]+[[:space:]]*$//')

        gd_name="$before_date"
    fi

    # ------------------------------------------------------------------
    # Clean extracted values
    # ------------------------------------------------------------------
    gd_name=$(clean_filename "$gd_name")

    # Normalize date to "YYYY-MM-DD HH:MM" (matches OwnCloud format)
    gd_date="${gd_date//T/ }"
    gd_date="${gd_date//Z/}"
    gd_date="${gd_date%%+*}"       # strip timezone offset
    gd_date="${gd_date%%.*}"       # strip fractional seconds
    gd_date="${gd_date:0:16}"      # keep YYYY-MM-DD HH:MM

    if [[ -n "$gd_name" ]]; then
        gd_filenames+=("$gd_name")
        gd_moddates+=("$gd_date")
    fi

done < "$GD_RAW_FILE"

echo "INFO:   → ${#gd_filenames[@]} files parsed from Google Drive"

# ==============================================================================
# STEP 5 — Compare Google Drive files against OwnCloud & build report
# ==============================================================================

echo "INFO: [Step 5/6] Comparing files and generating report..."

COUNT_OK=0
COUNT_MISSING=0
COUNT_NEEDUPDATE=0

{
    cat <<'BANNER'
================================================================
         O W N C L O U D   S Y N C   R E P O R T
================================================================
BANNER
    echo ""
    echo "  Run date/time     : $RUN_DATETIME"
    echo "  Period            : Last $PERIOD_DAYS days (since $START_DATE)"
    echo "  Google Drive query: gog drive search \"$GOOGLE_DRIVE_QUERY\""
    echo "  OwnCloud endpoint : $ALLFILES_URL"
    echo "  Google Drive files: ${#gd_filenames[@]}"
    echo "  OwnCloud files    : ${#oc_dates[@]}"
    echo ""
    echo "----------------------------------------------------------------"
    printf "  %-55s | %-12s\n" "FILENAME" "STATUS"
    echo "----------------------------------------------------------------"

    for (( i = 1; i <= ${#gd_filenames[@]}; i++ )); do
        fname="${gd_filenames[$i]}"
        fdate="${gd_moddates[$i]}"
        sync_status=""

        # Check presence in OwnCloud ( ${+array[key]} returns 1 if key exists )
        # Remplacer la ligne dans le Step 5 :
        if (( ! ${+oc_dates["$fname"]} )); then
            sync_status="MISSING"
            (( COUNT_MISSING++ ))
        else
            # File exists — compare modification dates
            oc_date_val="${oc_dates["$fname"]}"
            gd_epoch=$(date_to_epoch "$fdate")
            oc_epoch=$(date_to_epoch "$oc_date_val")

            if (( oc_epoch < gd_epoch )); then
                sync_status="NEED UPDATE"
                (( COUNT_NEEDUPDATE++ ))
            else
                sync_status="OK"
                (( COUNT_OK++ ))
            fi
        fi

        printf "  %-55s | %-12s\n" "$fname" "$sync_status"
    done

    echo "----------------------------------------------------------------"
    echo ""
    echo "  SUMMARY"
    echo "  ─────────────────────────"
    echo "    OK          : $COUNT_OK"
    echo "    MISSING     : $COUNT_MISSING"
    echo "    NEED UPDATE : $COUNT_NEEDUPDATE"
    echo "    TOTAL       : ${#gd_filenames[@]}"
    echo ""


} > "$REPORT_FILE"

# Fix the literal $VAR references inside the heredoc-style block
# (We used double-quoted echo so they expanded, but the cat <<'BANNER' is literal)
# Re-do the dynamic header lines properly:
sed -i.bak \
    -e "s|\$RUN_DATETIME|$(sed_escape "${RUN_DATETIME}")|g" \
    -e "s|\$PERIOD_DAYS|$(sed_escape "${PERIOD_DAYS}")|g" \
    -e "s|\$START_DATE|$(sed_escape "${START_DATE}")|g" \
    -e "s|\$GOOGLE_DRIVE_QUERY|$(sed_escape "${GOOGLE_DRIVE_QUERY}")|g" \
    -e "s|\$ALLFILES_URL|$(sed_escape "${ALLFILES_URL}")|g" \
    "$REPORT_FILE" 2>/dev/null
rm -f "${REPORT_FILE}.bak"

# ==============================================================================
# STEP 6 — Append elapsed time & send report
# ==============================================================================

ELAPSED=$((SECONDS - TIMER_START))

{
    echo "----------------------------------------------------------------"
    echo "  Elapsed time      : ${ELAPSED} second(s)"
    echo "  Report finalised  : $(date '+%Y-%m-%d %H:%M:%S %Z')"
    echo "================================================================"
} >> "$REPORT_FILE"

echo "INFO: [Step 6/6] Sending report to $EMAIL_RECIPIENT..."

if gog mail send \
        --to "$EMAIL_RECIPIENT" \
        --subject "OwnCloud Sync Report" \
        --body-file "$REPORT_FILE"; then
    TOTAL_ELAPSED=$((SECONDS - TIMER_START))
    echo "INFO: Report sent successfully."
    echo "INFO: Total elapsed time (including send): ${TOTAL_ELAPSED} second(s)"
else
    echo "ERROR: 'gog mail send' failed (exit $?)" >&2
    # Still show the report on stdout for diagnosis
    echo "--- REPORT CONTENT ---"
    cat "$REPORT_FILE"
    echo "--- END REPORT ---"
    exit 1
fi

echo "INFO: ===== OwnCloud Sync Check Complete ====="
exit 0
