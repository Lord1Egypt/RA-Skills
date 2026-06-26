#!/usr/bin/env bash
# OpenClaw Bootstrap - 最小化最佳实践初始化
# 幂等设计：可安全重复执行

set -euo pipefail

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
ASSETS="$SKILL_DIR/assets"

ok()   { echo "✅ $1"; }
skip() { echo "⏭  $1 (exists)"; }

echo ""
echo "🦞 OpenClaw Bootstrap v1.0"
echo "=========================="

# --- 1. 目录 ---
mkdir -p "$WORKSPACE"/{memory,.learnings}
mkdir -p "$HOME/.openclaw/hooks"

# --- 2. 工作区文件（不覆盖） ---
for f in AGENTS.md SOUL.md USER.md MEMORY.md HEARTBEAT.md BOOT.md; do
    [ -f "$WORKSPACE/$f" ] && skip "$f" || { cp "$ASSETS/$f" "$WORKSPACE/$f"; ok "$f"; }
done

# --- 3. .learnings ---
for f in LEARNINGS.md ERRORS.md FEATURE_REQUESTS.md; do
    [ -f "$WORKSPACE/.learnings/$f" ] && skip ".learnings/$f" || { cp "$ASSETS/learnings/$f" "$WORKSPACE/.learnings/$f"; ok ".learnings/$f"; }
done

# --- 4. clawhub + self-improving-agent ---
if ! command -v clawhub &>/dev/null; then
    echo "📦 Installing clawhub CLI..."
    npm i -g clawhub 2>/dev/null && ok "clawhub" || echo "⚠️  npm i -g clawhub failed"
else
    ok "clawhub (exists)"
fi

if [ ! -d "$WORKSPACE/skills/self-improving-agent" ]; then
    echo "📦 Installing self-improving-agent..."
    clawhub install self-improving-agent --workdir "$WORKSPACE" 2>/dev/null && ok "self-improving-agent" || echo "⚠️  Run: clawhub login && clawhub install self-improving-agent"
else
    skip "self-improving-agent"
fi

# --- 5. Hook ---
if [ -d "$WORKSPACE/skills/self-improving-agent/hooks/openclaw" ] && [ ! -d "$HOME/.openclaw/hooks/self-improvement" ]; then
    cp -r "$WORKSPACE/skills/self-improving-agent/hooks/openclaw" "$HOME/.openclaw/hooks/self-improvement"
    openclaw hooks enable self-improvement 2>/dev/null && ok "self-improvement hook" || echo "⚠️  Hook enable failed"
else
    skip "self-improvement hook"
fi

# --- 6. Cron ---
CRONS=$(openclaw cron list --json 2>/dev/null | python3 -c "import sys,json; print(' '.join(j['name'] for j in json.load(sys.stdin).get('jobs',[])))" 2>/dev/null || echo "")

add_cron() {
    local name="$1" cron="$2" timeout="$3" msg="$4"
    echo "$CRONS" | grep -q "$name" && skip "cron: $name" || {
        openclaw cron add --name "$name" --cron "$cron" --tz "Asia/Shanghai" --timeout-seconds "$timeout" --message "$msg" 2>/dev/null && ok "cron: $name" || echo "⚠️  cron: $name failed"
    }
}

add_cron "weekly-self-reflection" "0 22 * * 0" 600 \
"每周自省：
1. 读取 memory/ 本周日志
2. 更新 MEMORY.md
3. 写报告到 memory/reflection-本周.md
4. 回复 NO_REPLY"

add_cron "monthly-learnings-review" "0 21 1 * *" 600 \
"月度学习回顾：
1. 扫描 .learnings/ 中 pending 高优先级条目
2. promote 到 AGENTS.md 或 MEMORY.md
3. 写报告到 memory/learnings-review-本月.md
4. 回复 NO_REPLY"

echo ""
echo "🎉 Done! Next steps:"
echo "   1. Edit USER.md — fill in your info"
echo "   2. Edit MEMORY.md — add preferences"
echo "   3. clawhub login — if not logged in"
echo ""
