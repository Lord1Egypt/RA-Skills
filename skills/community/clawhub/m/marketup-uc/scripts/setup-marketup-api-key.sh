#!/usr/bin/env bash

set -euo pipefail

ENV_DIR="${HOME}/.openclaw"
ENV_FILE="${ENV_DIR}/.env"

printf "Enter MARKETUP_API_KEY (leave empty to cancel): "
IFS= read -r MARKETUP_API_KEY_INPUT

if [ -z "${MARKETUP_API_KEY_INPUT}" ]; then
  echo "No API key entered. MARKETUP_API_KEY was not updated."
  exit 1
fi

mkdir -p "${ENV_DIR}"
touch "${ENV_FILE}"

if rg -q '^MARKETUP_API_KEY=' "${ENV_FILE}"; then
  sed -i.bak "s|^MARKETUP_API_KEY=.*$|MARKETUP_API_KEY=${MARKETUP_API_KEY_INPUT}|" "${ENV_FILE}"
  rm -f "${ENV_FILE}.bak"
  echo "MARKETUP_API_KEY has been updated in ${ENV_FILE}."
else
  printf "MARKETUP_API_KEY=%s\n" "${MARKETUP_API_KEY_INPUT}" >> "${ENV_FILE}"
  echo "MARKETUP_API_KEY has been appended to ${ENV_FILE}."
fi

exit 0
