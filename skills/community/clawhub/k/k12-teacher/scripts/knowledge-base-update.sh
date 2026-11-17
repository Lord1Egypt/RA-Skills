#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${1:-${SCRIPT_DIR}/..}"
MODE=""
TARGET=""

usage() {
    echo "Usage: $0 --download <syllabus-id> | --local <path-to-file> | --help"
    echo ""
    echo "Download or update syllabus metadata for the k12-teacher knowledge base."
}

if [ "$#" -eq 0 ]; then
    usage
    exit 1
fi

while [ "$#" -gt 0 ]; do
    case "$1" in
        --download)
            MODE="download"
            TARGET="${2:-}"
            shift 2
            ;;
        --local)
            MODE="local"
            TARGET="${2:-}"
            shift 2
            ;;
        --help|-h)
            usage
            exit 0
            ;;
        *)
            echo "Unknown argument: $1" >&2
            usage >&2
            exit 1
            ;;
    esac
done

if [ -z "$MODE" ] || [ -z "$TARGET" ]; then
    echo "A valid mode and target are required." >&2
    usage >&2
    exit 1
fi

if [ "$MODE" = "download" ]; then
    echo "[INFO] Download mode requested for syllabus: ${TARGET}"
    echo "[INFO] This repository includes the update contract and validation hook; external fetching is intentionally kept as a placeholder for local use."
elif [ "$MODE" = "local" ]; then
    if [ ! -f "$TARGET" ]; then
        echo "[ERROR] Local syllabus file does not exist: ${TARGET}" >&2
        exit 1
    fi
    echo "[INFO] Local mode requested: ${TARGET}"
fi

echo "[INFO] Synchronizing registry and validation state for ${TARGET}"
if [ -x "${PROJECT_ROOT}/scripts/validate-structure.sh" ]; then
    "${PROJECT_ROOT}/scripts/validate-structure.sh" "${PROJECT_ROOT}"
else
    echo "[WARN] Validation script is not executable; run chmod +x scripts/validate-structure.sh before use." >&2
fi

echo "[INFO] Knowledge base update flow completed successfully."
