#!/bin/bash
# Wrapper to update ocas-taste. Usage: update.sh [--help]
case "${1:-}" in
  --help|-h)
    echo "Wrapper to update ocas-taste: pulls latest from GitHub source, preserving journals and data."
    echo "Usage: update.sh"
    exit 0 ;;
esac
python3 <hermes-home>/scripts/skill_update.py ocas-taste
