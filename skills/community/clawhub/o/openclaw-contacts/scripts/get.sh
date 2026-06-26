#!/bin/bash
# Usage: contacts-get.sh <contact_id>
# Shows full contact details

CONTACTS_DIR="$(dirname "$0")/../memory/contacts/contacts.d"

if [ -z "$1" ]; then
    echo "Usage: $0 <contact_id>"
    exit 1
fi

if [ -f "$CONTACTS_DIR/$1.yaml" ]; then
    cat "$CONTACTS_DIR/$1.yaml"
else
    echo "Contact not found: $1"
    exit 1
fi
