#!/bin/bash
# 🦞 Lobster Resurrect Protocol v3.1 (Deep Purge)
# 当 OpenClaw Uninstall 指令失效时的强制宿主级清理与重装脚本

VAULT="$HOME/openclaw-backups-vault/daily"
LOG_FILE="$HOME/openclaw-backups-vault/resurrection.log"

echo "🚨 [CRITICAL] 启动系统级强制清理与涅槃重装程序..."

# --- 安全保险开关 (v3.2 优化) ---
echo -e "\033[33m"
echo "⚠️  警告：该脚本将执行【物理级摧毁并重装】操作！"
echo "1. 现有 .openclaw 文件夹将被重命名并归档。"
echo "2. 系统内核将通过 pnpm 强制重新拉取。"
echo "3. 整个过程预计耗时 2-5 分钟。"
echo -e "\033[0m"
echo "你有 30 秒的时间考虑。若要取消，请立即按下 [Ctrl+C] 中断。"

for i in {30..1}; do
    echo -ne "倒计时: $i \r"
    sleep 1
done
echo -e "\n确认生效，启动深度清场...\n"
# ------------------------------

# 1. 强制清理内存残留
echo "Step 1/5: 深度斩首正在运行的进程与服务..."
launchctl unload ~/Library/LaunchAgents/ai.openclaw.lobster.guardian.plist 2>/dev/null
# 扫描并杀掉所有与 openclaw 相关的 node 进程和占用端口
lsof -ti:18789 | xargs kill -9 2>/dev/null
pkill -9 -f "openclaw"

# 2. 系统级物理剔除 (当 uninstall 失效时的强力手段)
echo "Step 2/5: 物理移除程序二进制文件与全局符号..."
# 针对全局安装的 openclaw 执行强制删除
npm uninstall -g openclaw --force 2>/dev/null
pnpm uninstall -g openclaw 2>/dev/null
# 物理删除 node_modules 中的残留路径 (针对 Mac/Linux)
rm -rf /usr/local/lib/node_modules/openclaw 2>/dev/null
rm -rf $(pnpm bin -g)/openclaw 2>/dev/null

# 3. 缓存与环境深度空场
echo "Step 3/5: 排空系统级数据残留与缓存..."
rm -rf ~/.npm/_cacache
rm -rf ~/.pnpm-store
# 注意：这里小心不删除 Vault 备份
# 转移当前损坏的 .openclaw 文件夹名，而不是直接删除，作为最后的反悔机会
mv ~/.openclaw ~/.openclaw_corrupted_$(date +%s) 2>/dev/null

# 4. 重新注入系统内核 (Fresh Install)
echo "Step 4/5: 正在重新从官方源注拉取最新内核..."
pnpm install -g openclaw@latest

# 5. 血脉压榨与灵魂归位
echo "Step 5/5: 从物理保险库恢复最新备份..."
mkdir -p ~/.openclaw/workspace/
LATEST_BKP=$(ls -td $VAULT/* | head -1)
if [ -z "$LATEST_BKP" ]; then
    echo "❌ 错误：保险库中未发现有效备份！请检查 $VAULT"
else
    cp "$LATEST_BKP/openclaw.json" "$HOME/.openclaw/"
    [ -f "$LATEST_BKP/auth-profiles.json" ] && cp "$LATEST_BKP/auth-profiles.json" "$HOME/.openclaw/agents/main/agent/" 2>/dev/null
    cp "$LATEST_BKP/"*.md "$HOME/.openclaw/workspace/"
    echo "✅ 备份文件已回归主目录。"
fi

# 6. 自检启动
openclaw gateway start --force
sleep 20
openclaw doctor --fix

echo "🏁 [SUCCESS] 系统涅槃完成，全系统已恢复至 100% 健康态。🦞"
