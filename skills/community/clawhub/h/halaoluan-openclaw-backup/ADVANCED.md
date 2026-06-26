# OpenClaw Backup - 高级使用指南

## 📚 目录

- [高级配置](#高级配置)
- [自定义备份策略](#自定义备份策略)
- [多地备份方案](#多地备份方案)
- [备份验证与恢复测试](#备份验证与恢复测试)
- [性能优化](#性能优化)
- [安全最佳实践](#安全最佳实践)
- [故障排查深入](#故障排查深入)

---

## 🔧 高级配置

### 自定义备份目录

```bash
# 方式1：环境变量
export OPENCLAW_BACKUP_DIR="$HOME/Backups/OpenClaw"

# 方式2：直接修改脚本
# 编辑 scripts/backup.sh，修改第6行：
BACKUP_ROOT="/path/to/custom/backup/dir"
```

### 排除特定文件

编辑 `scripts/backup.sh`，在 `cp -a` 之前添加：

```bash
# 排除日志文件（节省空间）
find "$STATE_DIR_NEW" -name "*.log" -delete 2>/dev/null || true

# 排除 node_modules（如果存在）
find "$STATE_DIR_NEW" -name "node_modules" -type d -exec rm -rf {} + 2>/dev/null || true

# 排除临时文件
find "$STATE_DIR_NEW" -name "*.tmp" -delete 2>/dev/null || true
```

### 压缩级别优化

修改打包命令，调整压缩级别（1-9，默认6）：

```bash
# 最快速度（压缩率低）
tar -czf --fast "$BACKUP_ROOT/$ARCHIVE_NAME" -C "$TMP_DIR" .

# 最大压缩（速度慢）
tar -czf --best "$BACKUP_ROOT/$ARCHIVE_NAME" -C "$TMP_DIR" .

# 自定义级别（如 -9）
tar --use-compress-program="gzip -9" -cf "$BACKUP_ROOT/$ARCHIVE_NAME" -C "$TMP_DIR" .
```

---

## 🎯 自定义备份策略

### 场景1：仅备份关键数据

创建 `scripts/backup_minimal.sh`：

```bash
#!/bin/bash
set -euo pipefail

BACKUP_ROOT="${OPENCLAW_BACKUP_DIR:-$HOME/Desktop/OpenClaw_Backups}"
DATE_STR="$(date +"%Y-%m-%d_%H-%M-%S")"
TMP_DIR="/tmp/openclaw_minimal_$DATE_STR"
ARCHIVE_NAME="openclaw_minimal_$DATE_STR.tar.gz"

mkdir -p "$BACKUP_ROOT" "$TMP_DIR"

echo "🐈‍⬛ OpenClaw 最小备份（仅关键数据）"

# 仅备份关键文件
mkdir -p "$TMP_DIR/.openclaw"
cp -a "$HOME/.openclaw/config.yaml" "$TMP_DIR/.openclaw/" 2>/dev/null || true
cp -a "$HOME/.openclaw/workspace/MEMORY.md" "$TMP_DIR/.openclaw/" 2>/dev/null || true
cp -a "$HOME/.openclaw/workspace/memory/" "$TMP_DIR/.openclaw/" 2>/dev/null || true

tar -czf "$BACKUP_ROOT/$ARCHIVE_NAME" -C "$TMP_DIR" .
shasum -a 256 "$BACKUP_ROOT/$ARCHIVE_NAME" > "$BACKUP_ROOT/$ARCHIVE_NAME.sha256"
rm -rf "$TMP_DIR"

echo "✅ 最小备份完成！大小: $(du -h "$BACKUP_ROOT/$ARCHIVE_NAME" | cut -f1)"
```

### 场景2：增量备份

使用 `rsync` 实现增量备份：

```bash
#!/bin/bash
# scripts/backup_incremental.sh

BACKUP_ROOT="${OPENCLAW_BACKUP_DIR:-$HOME/Desktop/OpenClaw_Backups}"
DATE_STR="$(date +"%Y-%m-%d_%H-%M-%S")"
CURRENT_BACKUP="$BACKUP_ROOT/incremental/$DATE_STR"
LINK_DEST="$BACKUP_ROOT/incremental/latest"

mkdir -p "$CURRENT_BACKUP"

if [ -d "$LINK_DEST" ]; then
    rsync -a --link-dest="$LINK_DEST" "$HOME/.openclaw/" "$CURRENT_BACKUP/"
else
    rsync -a "$HOME/.openclaw/" "$CURRENT_BACKUP/"
fi

# 更新 latest 链接
rm -f "$LINK_DEST"
ln -s "$CURRENT_BACKUP" "$LINK_DEST"

echo "✅ 增量备份完成: $CURRENT_BACKUP"
```

---

## 🌐 多地备份方案

### 方案1：3-2-1 备份自动化

创建 `scripts/backup_321.sh`：

```bash
#!/bin/bash
# 3-2-1备份策略：3份副本、2种介质、1份异地

set -euo pipefail

echo "🐈‍⬛ 执行 3-2-1 备份策略"

# 1. 本地备份（桌面）
export OPENCLAW_BACKUP_DIR="$HOME/Desktop/OpenClaw_Backups"
bash scripts/backup_encrypted.sh
LOCAL_BACKUP=$(ls -t "$OPENCLAW_BACKUP_DIR"/openclaw_backup_*.tar.gz.enc | head -1)

# 2. 移动硬盘备份（第2种介质）
EXTERNAL_DISK="/Volumes/External/OpenClaw_Backups"
if [ -d "$EXTERNAL_DISK" ]; then
    echo "📀 复制到移动硬盘..."
    cp "$LOCAL_BACKUP" "$EXTERNAL_DISK/"
    cp "$LOCAL_BACKUP.sha256" "$EXTERNAL_DISK/"
else
    echo "⚠️  移动硬盘未连接，跳过"
fi

# 3. 云盘备份（异地）
CLOUD_DIR="$HOME/Library/Mobile Documents/com~apple~CloudDocs/OpenClaw_Backups"
mkdir -p "$CLOUD_DIR"
echo "☁️  复制到 iCloud Drive..."
cp "$LOCAL_BACKUP" "$CLOUD_DIR/"
cp "$LOCAL_BACKUP.sha256" "$CLOUD_DIR/"

echo "✅ 3-2-1 备份完成！"
echo "   本地: $LOCAL_BACKUP"
echo "   移动硬盘: $EXTERNAL_DISK"
echo "   云盘: $CLOUD_DIR"
```

### 方案2：异地服务器备份（rsync over SSH）

```bash
#!/bin/bash
# scripts/backup_remote.sh

REMOTE_USER="your_username"
REMOTE_HOST="backup.example.com"
REMOTE_PATH="/backup/openclaw"

# 创建本地备份
bash scripts/backup_encrypted.sh
LOCAL_BACKUP=$(ls -t ~/Desktop/OpenClaw_Backups/openclaw_backup_*.tar.gz.enc | head -1)

# 上传到远程服务器
echo "📡 上传到远程服务器..."
rsync -avz --progress "$LOCAL_BACKUP" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_PATH/"
rsync -avz --progress "$LOCAL_BACKUP.sha256" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_PATH/"

echo "✅ 远程备份完成"
```

---

## 🔍 备份验证与恢复测试

### 定期验证备份完整性

创建 `scripts/verify_all.sh`：

```bash
#!/bin/bash
# 验证所有备份的完整性

BACKUP_ROOT="${OPENCLAW_BACKUP_DIR:-$HOME/Desktop/OpenClaw_Backups}"
cd "$BACKUP_ROOT"

echo "🔐 验证所有备份..."
TOTAL=0
SUCCESS=0
FAILED=0

for sha_file in *.sha256; do
    TOTAL=$((TOTAL + 1))
    if shasum -c "$sha_file" >/dev/null 2>&1; then
        SUCCESS=$((SUCCESS + 1))
        echo "✓ $sha_file"
    else
        FAILED=$((FAILED + 1))
        echo "✗ $sha_file (损坏！)"
    fi
done

echo ""
echo "📊 验证结果："
echo "   总计: $TOTAL"
echo "   成功: $SUCCESS"
echo "   失败: $FAILED"

if [ $FAILED -gt 0 ]; then
    echo ""
    echo "⚠️  警告：有备份文件已损坏，建议重新备份！"
    exit 1
fi
```

### 恢复演练（不影响当前环境）

```bash
#!/bin/bash
# scripts/test_restore.sh

BACKUP_FILE="$1"
TEST_DIR="/tmp/openclaw_restore_test_$(date +%s)"

if [ -z "$BACKUP_FILE" ]; then
    echo "用法: $0 /path/to/backup.tar.gz"
    exit 1
fi

mkdir -p "$TEST_DIR"

echo "🧪 测试恢复: $BACKUP_FILE"
echo "测试目录: $TEST_DIR"

# 解压到临时目录
tar -xzf "$BACKUP_FILE" -C "$TEST_DIR"

# 验证关键文件
if [ -f "$TEST_DIR/.openclaw/config.yaml" ]; then
    echo "✓ config.yaml 存在"
else
    echo "✗ config.yaml 缺失"
fi

if [ -f "$TEST_DIR/.openclaw/workspace/MEMORY.md" ]; then
    echo "✓ MEMORY.md 存在"
else
    echo "✗ MEMORY.md 缺失"
fi

echo ""
echo "📁 备份内容预览:"
ls -lh "$TEST_DIR/.openclaw/"

echo ""
read -p "清理测试目录？[Y/n] " CONFIRM
if [ "$CONFIRM" != "n" ]; then
    rm -rf "$TEST_DIR"
    echo "✅ 已清理"
fi
```

---

## ⚡ 性能优化

### 1. 并行压缩（多核CPU）

安装 `pigz`（并行gzip）：

```bash
brew install pigz
```

修改备份脚本：

```bash
# 替换
tar -czf "$BACKUP_ROOT/$ARCHIVE_NAME" -C "$TMP_DIR" .

# 为
tar --use-compress-program="pigz -9" -cf "$BACKUP_ROOT/$ARCHIVE_NAME" -C "$TMP_DIR" .
```

**性能提升**：4核CPU可提速 2-3倍

### 2. 排除大文件目录

```bash
# 在 cp -a 之前添加
du -sh "$STATE_DIR_NEW"/* | sort -hr | head -10

# 根据输出，排除大文件
rm -rf "$TMP_DIR/.openclaw/logs"
rm -rf "$TMP_DIR/.openclaw/.npm"
```

### 3. 分片备份（大文件）

```bash
# 每500MB分一片
tar -czf - "$TMP_DIR" | split -b 500M - "$BACKUP_ROOT/$ARCHIVE_NAME.part_"

# 恢复时
cat "$BACKUP_ROOT/$ARCHIVE_NAME.part_"* | tar -xzf -
```

---

## 🔒 安全最佳实践

### 1. 密码管理

**推荐方式**（1Password集成）：

```bash
# 从1Password读取密码
export OPENCLAW_BACKUP_PASSWORD=$(op read "op://Personal/OpenClaw Backup/password")
bash scripts/backup_encrypted.sh
```

### 2. 密钥文件加密（高级）

使用GPG加密：

```bash
# 生成密钥对（一次性）
gpg --gen-key

# 加密备份
gpg --encrypt --recipient your-email@example.com openclaw_backup.tar.gz

# 解密
gpg --decrypt openclaw_backup.tar.gz.gpg > openclaw_backup.tar.gz
```

### 3. 双重加密（极高安全）

```bash
# 第一层：OpenSSL
openssl enc -aes-256-cbc ...

# 第二层：GPG
gpg --encrypt --recipient your-email@example.com backup.tar.gz.enc
```

---

## 🐛 故障排查深入

### 问题1：备份速度慢

**诊断**：
```bash
# 监控IO
iostat -w 1

# 检查CPU
top -o cpu
```

**解决**：
- 使用 SSD 作为临时目录
- 启用并行压缩（pigz）
- 排除不必要的文件

### 问题2：磁盘空间不足

**诊断**：
```bash
df -h
du -sh ~/.openclaw
```

**解决**：
```bash
# 清理旧备份（保留最近5个）
cd ~/Desktop/OpenClaw_Backups
ls -t openclaw_backup_*.tar.gz.enc | tail -n +6 | xargs rm -f
```

### 问题3：cron任务失败

**诊断**：
```bash
# 查看cron日志
tail -f /tmp/openclaw_backup.log

# 手动测试cron环境
env -i HOME=$HOME /bin/bash -c 'crontab -l | grep openclaw'
```

**解决**：
- 使用绝对路径
- 设置 PATH 环境变量
- 检查权限

---

## 📊 备份策略对比

| 策略 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| **完整备份** | 简单、快速恢复 | 占用空间大 | 每周/月备份 |
| **增量备份** | 节省空间 | 恢复复杂 | 每日备份 |
| **最小备份** | 速度快、空间小 | 不完整 | 紧急备份 |
| **3-2-1备份** | 最安全 | 管理复杂 | 生产环境 |

---

## 🔗 相关资源

- [OpenClaw官方文档](https://docs.openclaw.ai)
- [备份最佳实践](https://www.backblaze.com/blog/the-3-2-1-backup-strategy/)
- [OpenSSL手册](https://www.openssl.org/docs/)
- [rsync指南](https://rsync.samba.org/)

---

**需要帮助？** [提交Issue](https://github.com/halaoluan/openclaw-backup/issues)
