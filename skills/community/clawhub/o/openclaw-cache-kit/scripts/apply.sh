#!/bin/bash
# openclaw-cache-kit: 캐싱 최적화 설정 적용 스크립트
# Inspired by: https://slashpage.com/thomasjeong/36nj8v2wq5zqj25ykq9z
#
# 적용 항목:
#   - cacheRetention: "long"
#   - contextPruning.ttl: "1h"
#   - heartbeat.every: "59m"
#   - diagnostics.cacheTrace.enabled: true
#
# 사용법: bash scripts/apply.sh

set -euo pipefail

OPENCLAW_CONFIG="${OPENCLAW_CONFIG:-$HOME/.openclaw/openclaw.json}"
BACKUP_DIR="$HOME/.openclaw/backups"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }
err() { echo "[ERROR] $*" >&2; exit 1; }

# ── 사전 점검 ──────────────────────────────────────────────
command -v openclaw >/dev/null 2>&1 || err "openclaw CLI가 설치되어 있지 않습니다."
command -v python3  >/dev/null 2>&1 || err "python3이 필요합니다."

if [[ ! -f "$OPENCLAW_CONFIG" ]]; then
  err "openclaw.json을 찾을 수 없습니다: $OPENCLAW_CONFIG"
fi

# ── 백업 ──────────────────────────────────────────────────
mkdir -p "$BACKUP_DIR"
BACKUP_FILE="$BACKUP_DIR/openclaw.json.$(date '+%Y%m%d_%H%M%S').bak"
cp "$OPENCLAW_CONFIG" "$BACKUP_FILE"
log "✅ 백업 생성: $BACKUP_FILE"

# ── Python으로 JSON 패치 ──────────────────────────────────
log "🔧 캐싱 최적화 설정 적용 중..."

python3 - "$OPENCLAW_CONFIG" << 'PYEOF'
import json, sys

config_path = sys.argv[1]

with open(config_path, encoding="utf-8") as f:
    config = json.load(f)

def deep_set(d, keys, value):
    for k in keys[:-1]:
        d = d.setdefault(k, {})
    d[keys[-1]] = value

MODEL_KEY = "anthropic/claude-sonnet-4-6"

# 1. agents.defaults.models.<model>.alias = "sonnet"
deep_set(config, ["agents", "defaults", "models", MODEL_KEY, "alias"], "sonnet")

# 2. agents.defaults.models.<model>.params.cacheRetention = "long"
deep_set(config, ["agents", "defaults", "models", MODEL_KEY, "params", "cacheRetention"], "long")

# 3. agents.defaults.contextPruning
deep_set(config, ["agents", "defaults", "contextPruning", "mode"], "cache-ttl")
deep_set(config, ["agents", "defaults", "contextPruning", "ttl"], "1h")
deep_set(config, ["agents", "defaults", "contextPruning", "keepLastAssistants"], 3)

# 4. agents.defaults.heartbeat.every = "59m"
deep_set(config, ["agents", "defaults", "heartbeat", "every"], "59m")

# 5. diagnostics.cacheTrace
deep_set(config, ["diagnostics", "cacheTrace", "enabled"], True)
deep_set(config, ["diagnostics", "cacheTrace", "includeSystem"], True)
deep_set(config, ["diagnostics", "cacheTrace", "includeMessages"], False)
deep_set(config, ["diagnostics", "cacheTrace", "includePrompt"], False)

with open(config_path, "w", encoding="utf-8") as f:
    json.dump(config, f, ensure_ascii=False, indent=2)
    f.write("\n")

agents_defaults = config["agents"]["defaults"]
print("적용 완료:")
print(f"  agents.defaults.models.{MODEL_KEY}.params.cacheRetention = {agents_defaults['models'][MODEL_KEY]['params']['cacheRetention']}")
print(f"  agents.defaults.contextPruning.ttl    = {agents_defaults['contextPruning']['ttl']}")
print(f"  agents.defaults.heartbeat.every       = {agents_defaults['heartbeat']['every']}")
print(f"  diagnostics.cacheTrace.enabled        = {config['diagnostics']['cacheTrace']['enabled']}")
PYEOF

log "✅ openclaw.json 업데이트 완료"

# ── Gateway 재시작 ─────────────────────────────────────────
log "🔄 openclaw gateway 재시작 중..."
openclaw gateway restart 2>&1 || true
log "✅ Gateway 재시작 완료 (또는 비대화형 환경에서는 수동 재시작 필요)"

# ── 결과 확인 ─────────────────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 캐싱 최적화 적용 완료!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "절약 효과 확인:"
echo "  bash scripts/check-savings.sh"
echo ""
echo "백업 위치:"
echo "  $BACKUP_FILE"
echo ""
echo "원복 방법:"
echo "  cp '$BACKUP_FILE' '$OPENCLAW_CONFIG' && openclaw gateway restart"
PYEOF
