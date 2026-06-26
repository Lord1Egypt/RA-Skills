#!/bin/bash
# check_or_suggest_folder.sh
# Usage: check_or_suggest_folder.sh [folder_name]

ROOT="/mnt/jellyfin_media"
FOLDER_NAME="${1:-}"

# ── Sanity check ─────────────────────────────────────────────────────────────
if [[ ! -d "$ROOT" ]]; then
  echo "STATUS: ERROR"
  echo "DETAIL: Root '$ROOT' missing or not mounted."
  exit 1
fi

# ── No name given → list top-level ───────────────────────────────────────────
if [[ -z "$FOLDER_NAME" ]]; then
  echo "STATUS: NO_TARGET_PROVIDED"
  echo "DETAIL: Existing top-level folders:"
  find "$ROOT" -mindepth 1 -maxdepth 1 -type d -printf "  %f\n" | sort
  exit 0
fi

# ── Sanitize ──────────────────────────────────────────────────────────────────
SAFE_NAME=$(echo "$FOLDER_NAME" | sed 's|^\/*||; s|\/*$||; s|\.\.||g')
TARGET="$ROOT/$SAFE_NAME"

# ── Exact match ───────────────────────────────────────────────────────────────
if [[ -d "$TARGET" ]]; then
  echo "STATUS: FOUND_EXACT"
  echo "PATH: $TARGET"
  exit 0
fi

# ── Fuzzy: search leaf name within correct parent dir ────────────────────────
LEAF=$(basename "$SAFE_NAME")
PARENT_REL=$(dirname "$SAFE_NAME")   # e.g. "Shows/Breaking Bad" or "."

if [[ "$PARENT_REL" == "." ]]; then
  SEARCH_DIR="$ROOT"
  MAX_DEPTH=2
else
  SEARCH_DIR="$ROOT/$PARENT_REL"
  MAX_DEPTH=1
fi

if [[ -d "$SEARCH_DIR" ]]; then
  mapfile -t SIMILAR < <(
    find "$SEARCH_DIR" -mindepth 1 -maxdepth "$MAX_DEPTH" -type d \
      -iname "*${LEAF}*" -printf "%P\n" 2>/dev/null | sort
  )
else
  SIMILAR=()
fi

if [[ ${#SIMILAR[@]} -gt 0 ]]; then
  echo "STATUS: FOUND_SIMILAR"
  echo "REQUESTED: $SAFE_NAME"
  echo "DETAIL: Similar folders:"
  for match in "${SIMILAR[@]}"; do
    # %P is relative to SEARCH_DIR; prepend ROOT to get full absolute path
    echo "  $ROOT/$match"
  done
  exit 0
fi

# ── Nothing found → safe to create ───────────────────────────────────────────
echo "STATUS: CLEAN"
echo "PATH: $TARGET"
echo "DETAIL: No match for '$SAFE_NAME'. Safe to create."
exit 0