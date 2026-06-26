#!/bin/bash
# match_variant_options.sh — Fuzzy variant matching for dropdown options
#
# PURPOSE: Helper functions to match non-standard dropdown labels (e.g.
#          "I am not a veteran" vs "No military experience") to the correct
#          option ref in a browser snapshot.
#
# SECURITY: These are pure text-matching functions using grep/sed on snapshot
#           strings passed as arguments. They do NOT access the network, file
#           system, or browser directly.
#
# Usage: source match_variant_options.sh, then call the matching functions below

# Match veteran/military status "No" variants
match_military_no() {
  local snap="$1"
  local ref=$(echo "$snap" | grep -iE '"(I am not a veteran|No military experience|I have no military service|Never served|None)"' | sed 's/.*\[ref=\([^]]*\)\].*/\1/' | head -1)
  if [ -z "$ref" ]; then
    # Fallback: find any option containing "veteran" and a negation keyword
    ref=$(echo "$snap" | grep -i "veteran" | grep -iE "no|not|never" | sed 's/.*\[ref=\([^]]*\)\].*/\1/' | head -1)
  fi
  echo "$ref"
}

# Match sponsorship "No" variants
match_sponsorship_no() {
  local snap="$1"
  local ref=$(echo "$snap" | grep -iE '"(I do not require sponsorship|No sponsorship needed|Will not need sponsorship|I am authorized to work in the US without sponsorship|No)"' | sed 's/.*\[ref=\([^]]*\)\].*/\1/' | head -1)
  if [ -z "$ref" ]; then
    # Fallback: find any option containing "sponsorship" and a negation keyword
    ref=$(echo "$snap" | grep -i "sponsorship" | grep -iE "no|not|don't|won't|without" | sed 's/.*\[ref=\([^]]*\)\].*/\1/' | head -1)
  fi
  echo "$ref"
}

# Match Chinese/Mandarin language option, falls back to "Other"
match_language_chinese() {
  local snap="$1"
  local ref=$(echo "$snap" | grep -iE '"(Chinese|Mandarin|Chinese \(Mandarin\))"' | sed 's/.*\[ref=\([^]]*\)\].*/\1/' | head -1)
  if [ -z "$ref" ]; then
    # Fallback: look for Other language option
    ref=$(echo "$snap" | grep -iE '"(Other|Other language)"' | sed 's/.*\[ref=\([^]]*\)\].*/\1/' | head -1)
  fi
  echo "$ref"
}
