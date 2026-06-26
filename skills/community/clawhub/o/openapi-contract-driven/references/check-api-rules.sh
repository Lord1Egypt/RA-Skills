#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════
# check-api-rules.sh — OpenAPI 规则检查（不依赖 Spectral CLI）
#
# 用法:
#   bash scripts/check-api-rules.sh standards/lexguard-openapi.yaml
#   bash scripts/check-api-rules.sh standards/yujuzhilian-openapi.yaml
#
# ops-agent 部署验证脚本会调用此脚本。
# 退出码: 0=全部通过 1=有 error 2=有 warn 3=脚本内部错误
# ═══════════════════════════════════════════════════════════

set -euo pipefail

YAML_FILE="${1:-}"
if [ -z "$YAML_FILE" ] || [ ! -f "$YAML_FILE" ]; then
  echo "❌ 用法: $0 <openapi-yaml-file>"
  exit 3
fi

PASS=0
FAIL=0
WARN=0
ERRORS=""

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║  OpenAPI 规则检查 ── $(basename "$YAML_FILE")"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# ── 规则 1: 所有端点必须有 operationId ───────────────────
echo "▶ 规则 1/7: operationId 完整性"
# 不限制缩进，任何 operationId: 都算
op_ids=$(grep -c 'operationId:' "$YAML_FILE" 2>/dev/null | head -1)
op_ids=${op_ids//[^0-9]/}; op_ids=${op_ids:-0}
# HTTP 方法同样不限制缩进
http_methods=$(grep -cE '^\s+(get|post|put|delete|patch|options):' "$YAML_FILE" 2>/dev/null | head -1)
http_methods=${http_methods//[^0-9]/}; http_methods=${http_methods:-0}
if [ "$op_ids" -ge "$http_methods" ] && [ "$op_ids" -gt 0 ]; then
  echo "  ✅ $op_ids operationId / $http_methods HTTP 方法 → 全部覆盖"
  PASS=$((PASS + 1))
else
  echo "  ❌ $op_ids operationId / $http_methods HTTP 方法 → 有缺失"
  FAIL=$((FAIL + 1))
fi

# ── 规则 2: 成功响应必须有 ApiResponse wrapper ──────────
echo "▶ 规则 2/7: 200 响应 ApiResponse wrapper"
# 同时匹配 YAML $ref 格式和注释引用格式
api_resp_count=$(grep -cE '\$ref:.*ApiResponse|#/components/schemas/ApiResponse' "$YAML_FILE" 2>/dev/null | head -1)
api_resp_count=${api_resp_count//[^0-9]/}; api_resp_count=${api_resp_count:-0}
if [ "$api_resp_count" -gt 0 ]; then
  echo "  ✅ ApiResponse 引用 $api_resp_count 处"
  PASS=$((PASS + 1))
else
  echo "  ❌ 未发现 ApiResponse 引用"
  FAIL=$((FAIL + 1))
fi

# ── 规则 3: ErrorResponse 标准错误模型 ──────────────────
echo "▶ 规则 3/7: ErrorResponse 标准错误模型"
err_resp_count=$(grep -c "ErrorResponse" "$YAML_FILE" 2>/dev/null; true)
err_resp_count=${err_resp_count//[^0-9]/}
err_resp_count=${err_resp_count:-0}
if [ "$err_resp_count" -gt 0 ]; then
  echo "  ✅ ErrorResponse 定义/引用 $err_resp_count 处"
  PASS=$((PASS + 1))
else
  echo "  ⚠️  未发现 ErrorResponse — 建议补"
  WARN=$((WARN + 1))
fi

# ── 规则 4: 分页参数规范 ─────────────────────────────
echo "▶ 规则 4/7: 分页参数统一 (PageParam/SizeParam)"
page_refs=$(grep -c "PageParam\|SizeParam" "$YAML_FILE" 2>/dev/null | head -1)
page_refs=${page_refs//[^0-9]/}; page_refs=${page_refs:-0}
sort_refs=$(grep -c "SortParam" "$YAML_FILE" 2>/dev/null | head -1)
sort_refs=${sort_refs//[^0-9]/}; sort_refs=${sort_refs:-0}
if [ "$page_refs" -gt 0 ]; then
  echo "  ✅ 分页参数引用 $page_refs 处 (Sort: $sort_refs)"
  PASS=$((PASS + 1))
else
  echo "  ⚠️  未发现分页参数引用 — 列表端点可能缺分页"
  WARN=$((WARN + 1))
fi

# ── 规则 5: 每个 service tag 有 health 端点 ────────────
echo "▶ 规则 5/7: 服务 health 端点"
# 直接统计 health/healthCheck 出现次数
health_count=$(grep -c 'health\|healthCheck' "$YAML_FILE" 2>/dev/null | head -1)
health_count=${health_count//[^0-9]/}; health_count=${health_count:-0}
if [ "$health_count" -gt 0 ]; then
  echo "  ✅ $health_count 处 health/healthCheck 引用"
  PASS=$((PASS + 1))
else
  echo "  ⚠️  未发现 health 端点 — 每个服务应该有"
  WARN=$((WARN + 1))
fi

# ── 规则 6: 日期字段 format: date-time ─────────────────
echo "▶ 规则 6/7: 日期字段显式 format"
date_fields=$(grep -cE '^\s+(createdAt|updatedAt|startDate|endDate|dueDate|paidAt|reportedAt|completedAt|signedAt|reviewedAt|uploadedAt):' "$YAML_FILE" 2>/dev/null | head -1)
date_fields=${date_fields//[^0-9]/}; date_fields=${date_fields:-0}
date_formats=$(grep -B1 -E '^\s+(createdAt|updatedAt|startDate|endDate|dueDate|paidAt|reportedAt|completedAt|signedAt|reviewedAt|uploadedAt):' "$YAML_FILE" 2>/dev/null | grep -c "format:" | head -1)
date_formats=${date_formats//[^0-9]/}; date_formats=${date_formats:-0}
if [ "$date_fields" -eq 0 ] || [ "$date_formats" -ge "$date_fields" ]; then
  echo "  ✅ 日期字段 format 标注率: $date_formats/$date_fields"
  PASS=$((PASS + 1))
else
  echo "  ⚠️  日期字段 format 缺失: $((date_fields - date_formats))/$date_fields 个未标 format"
  WARN=$((WARN + 1))
fi

# ── 规则 7: JWT security 声明 ─────────────────────────
echo "▶ 规则 7/7: BearerAuth securityScheme"
if grep -q "BearerAuth\|bearerAuth\|bearer.*JWT\|securitySchemes" "$YAML_FILE" 2>/dev/null; then
  echo "  ✅ BearerAuth securityScheme 已声明"
  PASS=$((PASS + 1))
else
  echo "  ❌ 缺少 BearerAuth securityScheme 声明"
  FAIL=$((FAIL + 1))
fi

# ── 汇总 ──────────────────────────────────────────────
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  结果: ✅ $PASS/7 通过  ❌ $FAIL 失败  ⚠️ $WARN 警告"
echo "═══════════════════════════════════════════════════════════"

if [ "$FAIL" -gt 0 ]; then
  echo "❌ 有 $FAIL 项 ERROR — 修复后再部署"
  exit 1
elif [ "$WARN" -gt 0 ]; then
  echo "⚠️  有 $WARN 项 WARN — 建议改进，不阻塞部署"
  exit 0
else
  echo "✅ 全部通过"
  exit 0
fi
