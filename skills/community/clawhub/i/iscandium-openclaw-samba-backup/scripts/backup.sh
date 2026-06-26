#!/bin/bash

# OpenClaw Samba 备份脚本
# 使用 cp 将 OpenClaw 数据备份到远程 Samba 共享

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_JSON="$SCRIPT_DIR/../config/default.json"

# 读取配置文件
if [ ! -f "$CONFIG_JSON" ]; then
    echo "错误：配置文件不存在"
    echo "请编辑 config/default.json 填写配置"
    exit 1
fi

# 解析 JSON 配置
target_server_ip=$(grep -o '"target_server_ip"[[:space:]]*:[[:space:]]*"[^"]*"' "$CONFIG_JSON" | cut -d'"' -f4)
target_share_name=$(grep -o '"target_share_name"[[:space:]]*:[[:space:]]*"[^"]*"' "$CONFIG_JSON" | cut -d'"' -f4)
target_share_username=$(grep -o '"target_share_username"[[:space:]]*:[[:space:]]*"[^"]*"' "$CONFIG_JSON" | cut -d'"' -f4)
target_share_password=$(grep -o '"target_share_password"[[:space:]]*:[[:space:]]*"[^"]*"' "$CONFIG_JSON" | cut -d'"' -f4)
source_admin_username=$(grep -o '"source_admin_username"[[:space:]]*:[[:space:]]*"[^"]*"' "$CONFIG_JSON" | cut -d'"' -f4)
source_admin_password=$(grep -o '"source_admin_password"[[:space:]]*:[[:space:]]*"[^"]*"' "$CONFIG_JSON" | cut -d'"' -f4)
max_backups=$(grep -o '"max_backups"[[:space:]]*:[[:space:]]*[0-9]*' "$CONFIG_JSON" | grep -o '[0-9]*' | head -1)
source_dir=$(grep -o '"source_dir"[[:space:]]*:[[:space:]]*"[^"]*"' "$CONFIG_JSON" | cut -d'"' -f4)
target_folder=$(grep -o '"target_folder"[[:space:]]*:[[:space:]]*"[^"]*"' "$CONFIG_JSON" | cut -d'"' -f4)
mount_point=$(grep -o '"mount_point"[[:space:]]*:[[:space:]]*"[^"]*"' "$CONFIG_JSON" | cut -d'"' -f4)
mount_vers=$(grep -o '"vers"[[:space:]]*:[[:space:]]*"[^"]*"' "$CONFIG_JSON" | cut -d'"' -f4)

# 检查必要配置
if [ -z "$target_server_ip" ] || [ -z "$target_share_name" ] || [ -z "$target_share_username" ] || [ -z "$target_share_password" ]; then
    echo "错误：配置文件不完整，请填写所有必填项"
    exit 1
fi

# 设置默认值
max_backups=${max_backups:-7}
mount_point=${mount_point:-"/mnt/iscandium-openclaw-samba-backup"}
mount_vers=${mount_vers:-"2.0"}

# 如果没有提供 source_admin_username，使用当前用户
if [ -z "$source_admin_username" ]; then
    source_admin_username=$(whoami)
fi

# 如果没有设置 source_dir，使用默认路径
if [ -z "$source_dir" ] || [ "$source_dir" = "null" ]; then
    source_dir="/home/$source_admin_username/.openclaw"
fi

# 如果没有设置 target_folder，使用 hostname
if [ -z "$target_folder" ] || [ "$target_folder" = "null" ]; then
    target_folder=$(hostname)
fi

# 获取当前时间
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)

echo "=== OpenClaw 备份开始 ==="
echo "目标服务器: $target_server_ip"
echo "共享文件夹: $target_share_name"
echo "源目录: $source_dir"
echo "目标目录: $target_folder/$TIMESTAMP"
echo "保留备份数: $max_backups"
echo ""

# 检查源目录是否存在
if [ ! -d "$source_dir" ]; then
    echo "错误：源目录不存在: $source_dir"
    exit 1
fi

# 创建挂载点
if [ ! -d "$mount_point" ]; then
    echo "$source_admin_password" | sudo -S mkdir -p "$mount_point"
fi

# 卸载已挂载的共享（如果存在）
echo "$source_admin_password" | sudo -S umount "$mount_point" 2>/dev/null

# 挂载 Samba 共享
echo "正在挂载 Samba 共享..."
echo "$source_admin_password" | sudo -S mount -t cifs "//$target_server_ip/$target_share_name" "$mount_point" \
    -o username="$target_share_username",password="$target_share_password",vers="$mount_vers"

if [ $? -ne 0 ]; then
    echo "错误：挂载失败"
    exit 1
fi

# 创建目标目录
TARGET_DIR="$mount_point/$target_folder/$TIMESTAMP"
echo "$source_admin_password" | sudo -S mkdir -p "$TARGET_DIR"

# 执行 cp 备份
echo "正在同步文件..."
echo "$source_admin_password" | sudo -S cp -R "$source_dir/." "$TARGET_DIR/"

if [ $? -eq 0 ]; then
    echo ""
    echo "=== 备份完成 ==="
else
    echo "错误：备份失败"
    echo "$source_admin_password" | sudo -S umount "$mount_point"
    exit 1
fi

# 清理旧备份
echo ""
echo "正在清理旧备份（保留 $max_backups 个）..."
BACKUP_BASE="$mount_point/$target_folder"

OLD_BACKUPS=$(ls -1r "$BACKUP_BASE" 2>/dev/null | grep -E '^[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}-[0-9]{2}-[0-9]{2}$' | tail -n +$((max_backups + 1)))

if [ -n "$OLD_BACKUPS" ]; then
    for old_backup in $OLD_BACKUPS; do
        echo "删除旧备份: $old_backup"
        echo "$source_admin_password" | sudo -S rm -rf "$BACKUP_BASE/$old_backup" 2>/dev/null || true
    done
else
    echo "没有需要清理的旧备份"
fi

# 卸载共享
echo ""
echo "正在卸载共享..."
echo "$source_admin_password" | sudo -S umount "$mount_point"

echo "完成！"
