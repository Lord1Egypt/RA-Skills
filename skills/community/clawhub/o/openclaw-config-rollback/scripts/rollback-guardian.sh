#!/bin/bash

# 配置修改回滚守护脚本
# 功能：如果配置修改后 5 分钟内 Gateway 没有成功重启，自动回滚
# 守护进程一直运行，但只在有配置修改时才工作，完成后自动停止

CONFIG=~/.openclaw/openclaw.json
BACKUP_DIR=~/.openclaw/backups
STATE_FILE=~/.openclaw/.config-modified-state
LOG=/tmp/openclaw-rollback-guardian.log
TIMEOUT_SECONDS=300  # 5 分钟

check_gateway_running() {
    openclaw gateway status 2>&1 | grep -q "Runtime: running"
}

rollback() {
    local backup_file=$1
    echo "$(date): 执行回滚到 $backup_file" >> $LOG
    cp $backup_file $CONFIG
    openclaw gateway restart >> $LOG 2>&1
    sleep 5
    if check_gateway_running; then
        echo "$(date): 回滚成功" >> $LOG
        rm -f $STATE_FILE
        return 0
    else
        echo "$(date): 回滚失败" >> $LOG
        return 1
    fi
}

# 主逻辑
if [ ! -f $STATE_FILE ]; then
    # 没有配置修改，直接退出（不写日志，保持安静）
    exit 0
fi

# 有未完成的配置修改，开始工作
modify_time=$(cat $STATE_FILE | head -1)
backup_file=$(cat $STATE_FILE | tail -1)
current_time=$(date +%s)
elapsed=$((current_time - modify_time))

echo "$(date): 检测到配置修改，已过去 ${elapsed}秒" >> $LOG

# 检查 Gateway 是否已经重启成功
if check_gateway_running; then
    # Gateway 运行正常，说明重启成功了
    echo "$(date): Gateway 运行正常，配置修改完成，清除状态文件" >> $LOG
    rm -f $STATE_FILE
    exit 0
fi

# Gateway 未运行，检查是否超时
if [ $elapsed -gt $TIMEOUT_SECONDS ]; then
    # 超时了，执行回滚
    echo "$(date): 配置修改已超时，Gateway 未运行，执行回滚" >> $LOG
    
    if [ -f "$backup_file" ]; then
        rollback $backup_file
    else
        echo "$(date): 备份文件不存在，无法回滚" >> $LOG
        rm -f $STATE_FILE
    fi
else
    remaining=$((TIMEOUT_SECONDS - elapsed))
    echo "$(date): Gateway 未运行，等待重启中（剩余 ${remaining}秒）" >> $LOG
fi
