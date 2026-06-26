# 配置修改助手

# 用法：
#   source ~/.openclaw/scripts/config-alias.sh
#   config-change "修改描述" "验证事项 1,验证事项 2"

config-change() {
    if [ -z "$1" ]; then
        echo "❌ 用法：config-change \"修改描述\" \"验证事项 1,验证事项 2\""
        echo ""
        echo "示例："
        echo "  config-change \"启用 obsidian 技能\" \"验证技能状态，验证 Gateway 启动\""
        return 1
    fi
    
    echo "🔧 准备修改配置..."
    echo "   描述：$1"
    echo "   验证：${2:-（无）}"
    echo ""
    
    ~/.openclaw/scripts/prepare-config-change.sh "$1" "$2"
    
    echo ""
    echo "📝 现在可以编辑配置了："
    echo "   nano ~/.openclaw/openclaw.json"
    echo "   或 vim ~/.openclaw/openclaw.json"
    echo ""
    echo "⏱️  修改完成后，请在 5 分钟内执行："
    echo "   openclaw gateway restart"
    echo ""
    echo "🔍 回滚截止时间：$(date -v+5M +%Y-%m-%d\ %H:%M)"
}

# 显示当前配置修改状态
config-status() {
    STATE_FILE=~/.openclaw/.config-modified-state
    
    if [ ! -f $STATE_FILE ]; then
        echo "✅ 无待处理的配置修改"
        return 0
    fi
    
    modify_time=$(cat $STATE_FILE | head -1)
    backup_file=$(cat $STATE_FILE | tail -1)
    current_time=$(date +%s)
    elapsed=$((current_time - modify_time))
    remaining=$((300 - elapsed))
    
    echo "⚠️  有待处理的配置修改"
    echo "   已过去：${elapsed}秒"
    echo "   剩余：${remaining}秒"
    echo "   备份：$backup_file"
    
    if [ $remaining -lt 0 ]; then
        echo ""
        echo "🚨 已超时！等待自动回滚..."
    fi
}

echo "✅ 配置修改助手已加载"
echo "   命令：config-change \"描述\" \"验证事项\""
echo "   状态：config-status"
