#!/bin/bash
# Usage: contacts-search.sh <name>
# Searches contacts by name in memory/contacts/contacts.d/

CONTACTS_DIR="$(dirname "$0")/../memory/contacts/contacts.d"

if [ -z "$1" ]; then
    echo "Usage: $0 <name>"
    exit 1
fi

find "$CONTACTS_DIR" -name "*.yaml" -exec grep -l "name:" {} \; | while read f; do
    if grep -q "name:.*$1" "$f"; then
        echo "=== $(basename "$f" .yaml) ==="
        cat "$f"
        echo ""
    fi
done
