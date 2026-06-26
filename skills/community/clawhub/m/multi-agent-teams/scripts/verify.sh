#!/bin/bash

# multi-agent-teams 验证脚本

set -e

OPENCLAW_DIR="/root/.openclaw"

echo "========================================"
echo "  multi-agent-teams 验证脚本"
echo "========================================"
echo ""

# 1. 验证 JSON 配置
echo "1. 验证 openclaw.json..."
if python3 -c "import json; json.load(open('$OPENCLAW_DIR/openclaw.json'))" 2>/dev/null; then
    echo "   ✅ JSON 有效"
else
    echo "   ❌ JSON 无效"
    exit 1
fi

# 2. 验证 Agent 数量
echo ""
echo "2. 验证 Agent 数量..."
AGENT_COUNT=$(openclaw agents list 2>&1 | grep "^-" | wc -l)
echo "   当前 Agent 数量：$AGENT_COUNT"
if [ "$AGENT_COUNT" -ge 23 ]; then
    echo "   ✅ 符合要求 (>= 23)"
else
    echo "   ⚠️  低于预期 (期望 >= 23)"
fi

# 3. 验证团队领导
echo ""
echo "3. 验证团队领导..."
for team in code stock social flow; do
    if openclaw agents list 2>&1 | grep -q "^- $team "; then
        echo "   ✅ $team-agent 已注册"
    else
        echo "   ❌ $team-agent 未注册"
    fi
done

# 4. 验证团队成员
echo ""
echo "4. 验证团队成员..."
code_members="frontend backend test product algorithm audit"
stock_members="analysis risk portfolio research"
social_members="content scheduling engagement analytics"
flow_members="workflow cron integration monitor"

for member in $code_members; do
    if openclaw agents list 2>&1 | grep -q "^- $member "; then
        echo "   ✅ code/$member 已注册"
    else
        echo "   ⚠️  code/$member 未注册"
    fi
done

# 5. 验证 subagents 配置
echo ""
echo "5. 验证 subagents 配置..."
python3 << 'EOF'
import json

with open('/root/.openclaw/openclaw.json', 'r') as f:
    config = json.load(f)

expected = {
    "code": 6,
    "stock": 4,
    "social": 4,
    "flow": 4
}

for agent in config['agents']['list']:
    if agent['id'] in expected:
        if 'subagents' in agent:
            count = len(agent['subagents']['allowAgents'])
            if count == expected[agent['id']]:
                print(f"   ✅ {agent['id']}: {count} 个成员")
            else:
                print(f"   ⚠️  {agent['id']}: {count} 个成员 (期望 {expected[agent['id']]})")
        else:
            print(f"   ❌ {agent['id']}: 缺少 subagents 配置")
EOF

# 6. 验证目录结构
echo ""
echo "6. 验证目录结构..."
for team in code stock social flow; do
    if [ -d "$OPENCLAW_DIR/agents/teams/$team/workspace" ]; then
        echo "   ✅ teams/$team/workspace"
    else
        echo "   ❌ teams/$team/workspace 缺失"
    fi
done

# 7. 验证 Gateway 状态
echo ""
echo "7. 验证 Gateway 状态..."
if openclaw gateway status 2>&1 | grep -q "running"; then
    echo "   ✅ Gateway 运行中"
else
    echo "   ⚠️  Gateway 未运行"
fi

echo ""
echo "========================================"
echo "  验证完成"
echo "========================================"
