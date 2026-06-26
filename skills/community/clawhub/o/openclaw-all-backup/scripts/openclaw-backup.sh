#!/bin/bash
# openclaw-backup.sh - 备份 .openclaw 目录

# 获取当前时间戳
TIMESTAMP=$(date +"%Y%m%d%H%M%S")

# 源目录
SOURCE_DIR="$HOME/.openclaw"

# 目标目录（~/.openclaw 同级别，即 $HOME）
DEST_DIR="$HOME"

# 新目录名
BACKUP_NAME=".openclaw${TIMESTAMP}"
BACKUP_PATH="${DEST_DIR}/${BACKUP_NAME}"

# 检查源目录是否存在
if [ ! -d "$SOURCE_DIR" ]; then
    echo "错误: 源目录 $SOURCE_DIR 不存在"
    exit 1
fi

# 检查目标是否已存在
if [ -e "$BACKUP_PATH" ]; then
    echo "错误: 目标目录 $BACKUP_PATH 已存在"
    exit 1
fi

# 创建目标目录
mkdir -p "$BACKUP_PATH"

# 拷贝所有文件（包括隐藏文件）
# 使用 rsync 或 cp -a 确保保留权限、隐藏文件等
if command -v rsync &> /dev/null; then
    # 使用 rsync（推荐，保留所有属性）
    rsync -av "$SOURCE_DIR/" "$BACKUP_PATH/"
else
    # 使用 cp -a（保留所有属性，包括隐藏文件）
    # 先拷贝所有非隐藏文件
    cp -a "$SOURCE_DIR"/* "$BACKUP_PATH/" 2>/dev/null || true
    # 再拷贝隐藏文件
    cp -a "$SOURCE_DIR"/.* "$BACKUP_PATH/" 2>/dev/null || true
fi

if [ $? -eq 0 ]; then
    echo "备份完成: $BACKUP_PATH"
    echo "原始目录: $SOURCE_DIR"
    echo "备份大小: $(du -sh "$BACKUP_PATH" | cut -f1)"
    echo "文件数量: $(find "$BACKUP_PATH" -type f | wc -l)"
else
    echo "错误: 备份失败"
    exit 1
fi
