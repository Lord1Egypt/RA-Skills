#!/bin/bash
# Usage: contacts-list.sh
# Lists all contact IDs and names

CONTACTS_DIR="$(dirname "$0")/../memory/contacts/contacts.d"

echo "Contact ID | Name"
echo "-----------|------"
for f in "$CONTACTS_DIR"/*.yaml; do
    [ -f "$f" ] || continue
    id=$(basename "$f" .yaml)
    name=$(grep "^name:" "$f" | head -1 | sed 's/name: *//')
    echo "$id | ${name:-?}"
done
