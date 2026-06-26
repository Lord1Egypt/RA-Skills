#!/usr/bin/env bash
# lib.sh — Shared helpers for obsidian-wiki scripts
# Source this file: . "$(dirname "$0")/lib.sh"

# Extract YAML frontmatter (between first two --- lines).
# Safety: stops after 200 lines to avoid runaway on malformed files.
# Handles CRLF line endings transparently.
get_frontmatter() {
  awk '/^---\r?$/ { n++; if(n==2) exit; next } n==1 { sub(/\r$/, ""); print } NR>200 { exit }' "$1" 2>/dev/null
}

# Extract a single frontmatter field value.
# Usage: get_field <file> <key>  →  prints the raw value (quotes and trailing whitespace stripped)
# Note: <key> must be a plain alphanumeric/hyphen field name (no regex metacharacters).
get_field() {
  get_frontmatter "$1" | sed -n "/^${2}:/{s/^${2}: *//; s/^[\"']//; s/[\"']\$//; s/[[:space:]]*$//; p; q;}"
}
