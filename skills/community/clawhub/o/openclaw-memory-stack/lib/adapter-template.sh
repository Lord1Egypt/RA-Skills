#!/usr/bin/env bash
# OpenClaw Memory Stack — Adapter Template
# This is the canonical adapter implementation skeleton.
# All 8 wrappers MUST copy this parsing logic into their adapter() function.
#
# Usage in wrapper.sh:
#   source "$(dirname "$0")/../../lib/contracts.sh"
#   # (contracts.sh already sources platform.sh)
#
#   adapter() {
#     # === Canonical argument parser (copy from adapter-template.sh) ===
#     local query="" hint=""
#     while [ $# -gt 0 ]; do
#       case "$1" in
#         --hint) hint="$2"; shift 2 ;;
#         *)      query="$1"; shift ;;
#       esac
#     done
#
#     if [ -z "$query" ]; then
#       contract_error "" "BACKEND_NAME" "BACKEND_ERROR" "No query provided"
#       return 1
#     fi
#
#     local start_ms
#     start_ms=$(now_ms)
#
#     # === Backend-specific search logic here ===
#     # Use $hint to optimize:
#     #   exact   → prefer exact/BM25 search
#     #   semantic → prefer vector/semantic search
#     #   relationship → prefer graph traversal
#     #   timeline → prefer time-sorted results
#     #   decision → prefer decision/causal chain search
#     #   grep    → prefer pattern matching
#     #   ""      → use default/hybrid strategy
#
#     # ... perform search, collect results ...
#
#     local end_ms duration_ms
#     end_ms=$(now_ms)
#     duration_ms=$(( end_ms - start_ms ))
#
#     # === Build contract response ===
#     # contract_success "$query" "BACKEND_NAME" "$results_json" "$count" "$duration_ms" "$normalized_relevance"
#     # contract_empty "$query" "BACKEND_NAME" "$duration_ms"
#     # contract_error "$query" "BACKEND_NAME" "ERROR_CODE" "error message"
#   }
#
#   # === Dispatch (bottom of wrapper.sh) ===
#   case "$1" in
#     --adapter) shift; adapter "$@" ;;
#     *)         cmd_"${1//-/_}" "${@:2}" ;;
#   esac

# This file is documentation/reference only. It is NOT sourced by wrappers.
# Wrappers source lib/contracts.sh (which sources lib/platform.sh).
