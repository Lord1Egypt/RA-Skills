#!/bin/bash

SENDER_ID=$1
CHANNEL=$2
QUIET=0

for arg in "$@"; do
    if [[ "$arg" == "-q" || "$arg" == "--quiet" ]]; then
        QUIET=1
    fi
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/../identities.json"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: identities.json not found. Run /identity-guard init to initialize." >&2
    exit 1
fi

if [ -z "$SENDER_ID" ]; then
    echo "Error: sender_id is required" >&2
    exit 1
fi

has_valid_master() {
    grep -qE '"master_id":\s*"[^"]+"' "$CONFIG_FILE" && \
    ! grep -qE '"master_id":\s*"(YOUR_SENDER_ID_HERE|")"' "$CONFIG_FILE"
}

has_valid_allowlist() {
    awk '
        /"allowlist":/ {
            if ($0 ~ /\[[[:space:]]*"/) { found=1; exit }
            in_allow=1
            next
        }
        in_allow && /]/ { in_allow=0 }
        in_allow && /"/ { found=1; exit }
        END { exit (found ? 0 : 1) }
    ' "$CONFIG_FILE"
}

in_global_allowlist() {
    awk -v sender="$SENDER_ID" '
        /"global_allowlist":/ { in_global=1 }
        in_global && $0 ~ "\"" sender "\"" { found=1; exit }
        in_global && /]/ { in_global=0 }
        END { exit (found ? 0 : 1) }
    ' "$CONFIG_FILE"
}

in_channel_allowlist_or_master() {
    awk -v channel="$CHANNEL" -v sender="$SENDER_ID" '
        $0 ~ "\"" channel "\"" { in_channel=1 }
        in_channel && /"master_id":/ {
            if ($0 ~ "\"" sender "\"") { found=1; exit }
        }
        in_channel && /"allowlist":/ {
            if ($0 ~ "\"" sender "\"") { found=1; exit }
            if ($0 ~ /]/) { in_allowlist=0; in_channel=0; next }
            in_allowlist=1
            next
        }
        in_allowlist && "]" { in_allowlist=0; in_channel=0 }
        in_allowlist && $0 ~ "\"" sender "\"" { found=1; exit }
        END { exit (found ? 0 : 1) }
    ' "$CONFIG_FILE"
}

in_any_channel_allowlist_or_master() {
    awk -v sender="$SENDER_ID" '
        /"channels":/ { in_channels=1 }
        in_channels && /"global_allowlist":/ { in_channels=0 }
        in_channels && /"master_id":/ && $0 ~ "\"" sender "\"" { found=1; exit }
        in_channels && /"allowlist":/ {
            if ($0 ~ "\"" sender "\"") { found=1; exit }
            if ($0 ~ /]/) { in_allowlist=0; next }
            in_allowlist=1
            next
        }
        in_allowlist && /]/ { in_allowlist=0 }
        in_allowlist && $0 ~ "\"" sender "\"" { found=1; exit }
        END { exit (found ? 0 : 1) }
    ' "$CONFIG_FILE"
}

if ! has_valid_master && ! has_valid_allowlist && ! grep -qE '"global_allowlist":\s*\[[^\]]+\]' "$CONFIG_FILE"; then
    exit 1
fi

if [ -n "$CHANNEL" ]; then
    if in_global_allowlist; then
        exit 0
    fi

    in_channel_allowlist_or_master && exit 0
    if [ "$QUIET" -eq 0 ]; then
        echo "Unauthorized" >&2
    fi
    exit 1
fi

if in_global_allowlist; then
    exit 0
fi

in_any_channel_allowlist_or_master && exit 0
if [ "$QUIET" -eq 0 ]; then
    echo "Unauthorized" >&2
fi

exit 1
