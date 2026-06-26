#!/bin/bash
# Search Polymarket markets and return JSON
# Usage: ./search.sh "bitcoin" 10

QUERY="${1:-bitcoin}"
LIMIT="${2:-5}"

polymarket -o json markets search "$QUERY" --limit "$LIMIT"
