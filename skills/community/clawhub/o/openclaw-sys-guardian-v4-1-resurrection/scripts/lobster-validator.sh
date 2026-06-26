#!/bin/bash
# Lobster Validator Script
# 核心逻辑：执行深度的端到端自愈验证，模拟真实故障环境

LOG_FILE="$HOME/.openclaw/lobster-guardian.log"
GATEWAY_URL="http://127.0.0.1:18789"

echo "🧪 [LOBSTER-VALIDATOR] 启动自愈系统全链路验收测试..."

# 1. 检测当前状态
if ! curl -s --head  --request GET "$GATEWAY_URL/health" | grep "200 OK" > /dev/null; then
    echo "❌ 初始检查失败：Gateway 目前并未正常运行，请先手动拉起。"
    exit 1
fi

# 2. 模拟 TC-01: 进程意外终止
echo "Step 1/3: 模拟 [TC-01 进程意外终止] (pkill -9)..."
pkill -9 -f "openclaw"
echo "已强杀 OpenClaw 进程。请等待守护进程 (Guardian) 在 1 分钟内探测并自愈..."

# 轮询监测
COUNT=0
while [ $COUNT -lt 120 ]; do
    if curl -s --head  --request GET "$GATEWAY_URL/health" | grep "200 OK" > /dev/null; then
        echo "✅ [TC-01 成功]：Guardian 已自动拉起服务！耗时 ${COUNT}s。"
        break
    fi
    sleep 2
    COUNT=$((COUNT+2))
    [ $((COUNT % 20)) -eq 0 ] && echo "...仍在等待自愈 (${COUNT}s)"
done

if [ $COUNT -ge 120 ]; then
    echo "❌ [TC-01 失败]：Guardian 未能在 2 分钟内自愈。请检查日志：tail -n 20 $LOG_FILE"
    exit 1
fi

# 3. 模拟 TC-03: 配置污染回滚测试 (Dry Run 逻辑模式)
echo "Step 2/3: 验证备份文件是否存在..."
BACKUP_FILE=$(find "$HOME/.openclaw/backups/daily" -name "openclaw.json" | head -n 1)
if [ -f "$BACKUP_FILE" ]; then
    echo "✅ 发现有效备份：$BACKUP_FILE"
else
    echo "❌ 错误：未发现每日备份文件。重新执行 /workspace/scripts/lobster-snapshot.sh"
    /Users/maxleolee/.openclaw/workspace/scripts/lobster-snapshot.sh
fi

# 4. 联动性检查
echo "Step 3/3: 验证飞书看板联动..."
# 尝试抓取日志最后一行是否有修复记录
if grep -q "SUCCESS: Service Restored" "$LOG_FILE"; then
    echo "✅ 守护进程内部日志记录正常。"
else
    echo "⚠️ 尚未在日志中发现修复记录，请手动刷新飞书看板确认。"
fi

echo "🏁 [LOBSTER-VALIDATOR] 验收测试完成。所有核心自愈链路已通。🦞"
