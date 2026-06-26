#!/bin/bash
# 一键回滚工具 - 手动选择备份恢复

CONFIG_FILE="$HOME/.openclaw/openclaw.json"
BACKUP_DIR="$HOME/.openclaw/backups"

echo "=== OpenClaw 一键回滚 ==="
echo ""

# 列出所有备份
echo "可用备份列表:"
echo ""

BACKUPS=($(ls -t "$BACKUP_DIR"/openclaw.json.bak.* 2>/dev/null))

if [ ${#BACKUPS[@]} -eq 0 ]; then
    echo "没有找到备份文件！"
    exit 1
fi

# 显示备份列表
for i in "${!BACKUPS[@]}"; do
    BACKUP="${BACKUPS[$i]}"
    FILENAME=$(basename "$BACKUP")
    DATE=$(echo "$FILENAME" | grep -o '[0-9]\{8\}_[0-9]\{6\}')
    FORMATTED_DATE=$(date -j -f "%Y%m%d_%H%M%S" "$DATE" "+%Y-%m-%d %H:%M:%S" 2>/dev/null || echo "$DATE")
    
    # 验证备份有效性
    if python3 -c "import json; json.load(open('$BACKUP'))" 2>/dev/null; then
        STATUS="✅ 有效"
    else
        STATUS="❌ 损坏"
    fi
    
    echo "[$i] $FORMATTED_DATE - $STATUS"
done

echo ""
echo "[c] 取消"
echo ""
read -p "请选择要恢复的备份编号: " choice

if [ "$choice" == "c" ] || [ "$choice" == "C" ]; then
    echo "已取消"
    exit 0
fi

if ! [[ "$choice" =~ ^[0-9]+$ ]] || [ "$choice" -ge ${#BACKUPS[@]} ]; then
    echo "无效的选择"
    exit 1
fi

SELECTED_BACKUP="${BACKUPS[$choice]}"

echo ""
echo "准备恢复到: $(basename "$SELECTED_BACKUP")"
read -p "确认? (y/n): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 先备份当前配置
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    cp "$CONFIG_FILE" "$BACKUP_DIR/openclaw.json.bak.before_rollback.$TIMESTAMP"
    
    # 恢复备份
    cp "$SELECTED_BACKUP" "$CONFIG_FILE"
    
    echo "已恢复，正在重启 OpenClaw..."
    openclaw gateway restart
    
    sleep 3
    if pgrep -f "openclaw.*gateway" > /dev/null; then
        echo "✅ 恢复成功！OpenClaw 已启动"
    else
        echo "❌ 启动失败，请检查日志"
    fi
else
    echo "已取消"
fi
