#!/bin/bash
# Usage: taobao-item-detail.sh <num_iid> [is_promotion]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NUM_IID="${1:?Error: num_iid is required}"
IS_PROMOTION="${2:-1}"

bash "${SCRIPT_DIR}/gateway-request.sh" \
  "/v1/taobao/item-detail" \
  "淘宝商品详情" \
  "num_iid=${NUM_IID}" \
  "is_promotion=${IS_PROMOTION}"
