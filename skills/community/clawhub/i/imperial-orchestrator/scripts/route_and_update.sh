#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATE_FILE="${STATE_FILE:-$ROOT/.imperial_state.json}"
BENCHMARK_FILE="${BENCHMARK_FILE:-$ROOT/.imperial_benchmark.json}"
AUDIT_FILE="${AUDIT_FILE:-$ROOT/.imperial_audit.json}"
SESSION_DIR="${SESSION_DIR:-$ROOT/.imperial_sessions}"
OPENCLAW_CONFIG="${OPENCLAW_CONFIG:-$HOME/.openclaw/openclaw.json}"

usage() {
  cat <<'EOF'
🏯 Imperial Orchestrator · 统一入口

用法:
  imperial <command> [options]

命令:
  ── 完整自动化 ──
  run       'task text'          全自动: 路由→执行→审核→反馈 (推荐)
  run       'task' --strict      严格模式: 审核不过自动重试
  run       'task' --session id  多轮对话模式
  run       'task' --json        JSON 格式输出

  ── 分步操作 ──
  route     'task text'          只路由，不执行
  exec      routing.json         执行路由结果 JSON
  full      'task text'          验证→路由（旧版兼容）

  ── 模型管理 ──
  validate                       探活所有模型
  benchmark [category]           跑基准测试
  leaderboard                    查看排行榜

  ── 监控统计 ──
  stats                          累计成本/token/调用统计
  audit     [N]                  最近 N 条审计日志 (默认 20)

环境变量:
  STATE_FILE       状态文件路径
  BENCHMARK_FILE   基准测试文件路径
  AUDIT_FILE       审计日志文件路径
  SESSION_DIR      会话存储目录
  OPENCLAW_CONFIG  openclaw.json 路径
EOF
  exit 1
}

CMD="${1:-}"
shift || true

case "$CMD" in
  run)
    TASK="${1:-}"
    shift || true
    [[ -z "$TASK" ]] && { echo "❌ 需要任务文本" >&2; exit 1; }
    # 确保 state 存在
    python3 "$ROOT/scripts/health_check.py" \
      --openclaw-config "$OPENCLAW_CONFIG" \
      --write-state "$STATE_FILE" >/dev/null 2>&1 || true
    python3 "$ROOT/scripts/orchestrator.py" \
      --task "$TASK" \
      --openclaw-config "$OPENCLAW_CONFIG" \
      --state-file "$STATE_FILE" \
      --benchmark-file "$BENCHMARK_FILE" \
      --audit-file "$AUDIT_FILE" \
      --session-dir "$SESSION_DIR" \
      "$@"
    ;;

  route)
    TASK="${1:-}"
    [[ -z "$TASK" ]] && { echo "❌ 需要任务文本" >&2; exit 1; }
    python3 "$ROOT/scripts/health_check.py" \
      --openclaw-config "$OPENCLAW_CONFIG" \
      --write-state "$STATE_FILE" >/dev/null 2>&1 || true
    python3 "$ROOT/scripts/router.py" \
      --task "$TASK" \
      --openclaw-config "$OPENCLAW_CONFIG" \
      --state-file "$STATE_FILE" \
      --benchmark-file "$BENCHMARK_FILE"
    ;;

  exec)
    ROUTING_JSON="${1:-}"
    [[ -z "$ROUTING_JSON" ]] && { echo "❌ 需要路由结果 JSON 文件" >&2; exit 1; }
    python3 "$ROOT/scripts/executor.py" \
      --routing-json "$ROUTING_JSON" \
      --openclaw-config "$OPENCLAW_CONFIG" \
      --state-file "$STATE_FILE" \
      --audit-file "$AUDIT_FILE"
    ;;

  validate)
    python3 "$ROOT/scripts/health_check.py" \
      --openclaw-config "$OPENCLAW_CONFIG" \
      --write-state "$STATE_FILE" --summary
    echo ""
    python3 "$ROOT/scripts/model_validator.py" \
      --openclaw-config "$OPENCLAW_CONFIG" \
      --state-file "$STATE_FILE" \
      "$@"
    ;;

  benchmark)
    CATEGORY="${1:-}"
    python3 "$ROOT/scripts/health_check.py" \
      --openclaw-config "$OPENCLAW_CONFIG" \
      --write-state "$STATE_FILE" >/dev/null 2>&1 || true
    EXTRA_ARGS=()
    [[ -n "$CATEGORY" ]] && EXTRA_ARGS+=(--category "$CATEGORY")
    python3 "$ROOT/scripts/benchmark.py" \
      --openclaw-config "$OPENCLAW_CONFIG" \
      --state-file "$STATE_FILE" \
      --benchmark-file "$BENCHMARK_FILE" \
      "${EXTRA_ARGS[@]}"
    ;;

  leaderboard)
    python3 "$ROOT/scripts/benchmark.py" \
      --benchmark-file "$BENCHMARK_FILE" \
      --leaderboard
    ;;

  stats)
    python3 "$ROOT/scripts/orchestrator.py" \
      --audit-file "$AUDIT_FILE" \
      --stats
    ;;

  audit)
    N="${1:-20}"
    python3 "$ROOT/scripts/orchestrator.py" \
      --audit-file "$AUDIT_FILE" \
      --audit-tail "$N"
    ;;

  full)
    # 旧版兼容: validate → route
    TASK="${1:-}"
    [[ -z "$TASK" ]] && { echo "❌ 需要任务文本" >&2; exit 1; }
    python3 "$ROOT/scripts/health_check.py" \
      --openclaw-config "$OPENCLAW_CONFIG" \
      --write-state "$STATE_FILE" >/dev/null 2>&1 || true
    python3 "$ROOT/scripts/model_validator.py" \
      --openclaw-config "$OPENCLAW_CONFIG" \
      --state-file "$STATE_FILE" 2>/dev/null || true
    python3 "$ROOT/scripts/router.py" \
      --task "$TASK" \
      --openclaw-config "$OPENCLAW_CONFIG" \
      --state-file "$STATE_FILE" \
      --benchmark-file "$BENCHMARK_FILE"
    ;;

  *)
    usage
    ;;
esac
