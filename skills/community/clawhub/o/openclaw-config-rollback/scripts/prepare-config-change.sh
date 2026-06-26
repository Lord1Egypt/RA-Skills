#!/bin/bash

# 配置修改准备脚本
# 用法：./prepare-config-change.sh "修改描述" "验证事项 1,验证事项 2,..."

CONFIG=~/.openclaw/openclaw.json
BACKUP_DIR=~/.openclaw/backups
STATE_FILE=~/.openclaw/.config-modified-state
VERIFICATION_FILE=~/.openclaw/workspace/docs/PENDING_VERIFICATION.md
LOG=/tmp/openclaw-config-change.log

description="$1"
verification_items="$2"

if [ -z "$description" ]; then
    echo "❌ 用法：$0 \"修改描述\" \"验证事项 1,验证事项 2,...\""
    exit 1
fi

# 1. 创建备份目录
mkdir -p $BACKUP_DIR

# 2. 备份当前配置
timestamp=$(date +%Y%m%d-%H%M%S)
backup_file=$BACKUP_DIR/openclaw-${timestamp}.json
cp $CONFIG $backup_file
echo "$(date): 已备份配置到 $backup_file" >> $LOG

# 3. 记录状态文件（用于超时回滚）
current_time=$(date +%s)
echo "$current_time" > $STATE_FILE
echo "$backup_file" >> $STATE_FILE
echo "$(date): 已记录状态文件" >> $LOG

# 4. 更新待验证事项文件
cat >> $VERIFICATION_FILE << EOF

## $(date +%Y-%m-%d) $(date +%H:%M) - $description

**修改内容：**
- 文件：\`~/.openclaw/openclaw.json\`
- 备份：\`$backup_file\`

**验证事项：**
EOF

if [ -n "$verification_items" ]; then
    IFS=',' read -ra ITEMS <<< "$verification_items"
    for item in "${ITEMS[@]}"; do
        echo "- [ ] $item" >> $VERIFICATION_FILE
    done
else
    echo "- [ ] （待补充）" >> $VERIFICATION_FILE
fi

cat >> $VERIFICATION_FILE << EOF

**回滚截止时间：** $(date -v+5M +%Y-%m-%d\ %H:%M)（修改后 5 分钟）

**状态：** pending

---

EOF

echo "$(date): 已更新待验证事项文件" >> $LOG

# 5. 输出信息
echo "✅ 配置修改准备完成"
echo ""
echo "备份文件：$backup_file"
echo "回滚截止时间：$(date -v+5M +%Y-%m-%d\ %H:%M)"
echo ""
echo "现在可以修改配置了。修改完成后请执行："
echo "  openclaw gateway restart"
echo ""
echo "如果 5 分钟内没有重启，会自动回滚。"
