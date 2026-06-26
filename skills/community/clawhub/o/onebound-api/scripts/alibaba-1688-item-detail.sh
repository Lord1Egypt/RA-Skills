#!/bin/bash
# Usage: alibaba-1688-item-detail.sh <num_iid> [sales_data] [agent]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NUM_IID="${1:?Error: num_iid is required}"
SALES_DATA="${2:-0}"
AGENT="${3:-0}"

bash "${SCRIPT_DIR}/gateway-request.sh" \
  "/v1/1688/item-detail" \
  "1688商品详情" \
  "num_iid=${NUM_IID}" \
  "sales_data=${SALES_DATA}" \
  "agent=${AGENT}"
