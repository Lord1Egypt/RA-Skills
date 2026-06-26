---
name: openclaw-backup
slug: halaoluan-openclaw-backup
version: 1.0.0
description: 定期备份 OpenClaw 数据（支持手动/自动/加密备份）。Use when user asks to backup OpenClaw, create backup, save state, protect data, or schedule automatic backups. Triggers: "备份", "backup", "保存数据", "定时备份", "加密备份", "backup to cloud".
---

# OpenClaw 备份 Skill

自动备份 OpenClaw 核心数据，支持加密、定时、云同步。

---

## 使用场景

| 触发词 | 操作 |
|--------|------|
| "备份 OpenClaw" | 立即创建备份 |
| "定时备份" | 配置 cron 自动备份 |
| "加密备份" | 创建密码保护的备份 |
| "备份到云盘" | 备份后同步到云端 |
| "查看备份" | 列出所有备份文件 |

---

## 核心脚本

### 1. 基础备份（无加密）

位置：`scripts/backup.sh`

```bash
#!/bin/bash
set -euo pipefail

# 参数
BACKUP_ROOT="${OPENCLAW_BACKUP_DIR:-$HOME/Desktop/OpenClaw_Backups}"
DATE_STR="$(date +"%Y-%m-%d_%H-%M-%S")"
TMP_DIR="/tmp/openclaw_backup_$DATE_STR"
ARCHIVE_NAME="openclaw_backup_$DATE_STR.tar.gz"

# 数据目录
STATE_DIR_NEW="$HOME/.openclaw"
STATE_DIR_OLD="$HOME/.clawdbot"

mkdir -p "$BACKUP_ROOT"
mkdir -p "$TMP_DIR"

echo "🐈‍⬛ OpenClaw 备份开始..."
echo "备份目标: $BACKUP_ROOT"

FOUND_ANY=0

# 备份 ~/.openclaw
if [ -d "$STATE_DIR_NEW" ]; then
    echo "✓ 发现: $STATE_DIR_NEW"
    cp -a "$STATE_DIR_NEW" "$TMP_DIR/"
    FOUND_ANY=1
fi

# 备份 ~/.clawdbot（旧版兼容）
if [ -d "$STATE_DIR_OLD" ]; then
    echo "✓ 发现: $STATE_DIR_OLD"
    cp -a "$STATE_DIR_OLD" "$TMP_DIR/"
    FOUND_ANY=1
fi

if [ "$FOUND_ANY" -eq 0 ]; then
    echo "❌ 未找到 OpenClaw 数据目录"
    rm -rf "$TMP_DIR"
    exit 1
fi

# 停止网关（可选）
if command -v openclaw >/dev/null 2>&1; then
    echo "⏸  停止 OpenClaw 网关..."
    openclaw gateway stop 2>/dev/null || true
    sleep 2
fi

# 打包
echo "📦 打包中..."
tar -czf "$BACKUP_ROOT/$ARCHIVE_NAME" -C "$TMP_DIR" .

# 生成校验文件
echo "🔐 生成 SHA256 校验..."
shasum -a 256 "$BACKUP_ROOT/$ARCHIVE_NAME" > "$BACKUP_ROOT/$ARCHIVE_NAME.sha256"

# 清理
rm -rf "$TMP_DIR"

# 重启网关
if command -v openclaw >/dev/null 2>&1; then
    echo "▶️  重启 OpenClaw 网关..."
    openclaw gateway start 2>/dev/null || true
fi

echo ""
echo "✅ 备份完成！"
echo "📁 位置: $BACKUP_ROOT/$ARCHIVE_NAME"
echo "🔐 校验: $BACKUP_ROOT/$ARCHIVE_NAME.sha256"
echo ""
echo "建议操作："
echo "1. 复制到移动硬盘"
echo "2. 上传到云盘（建议加密）"
echo "3. 定期验证备份完整性"
```

---

### 2. 加密备份（推荐）

位置：`scripts/backup_encrypted.sh`

```bash
#!/bin/bash
set -euo pipefail

# 参数
BACKUP_ROOT="${OPENCLAW_BACKUP_DIR:-$HOME/Desktop/OpenClaw_Backups}"
DATE_STR="$(date +"%Y-%m-%d_%H-%M-%S")"
TMP_DIR="/tmp/openclaw_backup_$DATE_STR"
ARCHIVE_NAME="openclaw_backup_$DATE_STR.tar.gz"
ENCRYPTED_NAME="openclaw_backup_$DATE_STR.tar.gz.enc"

STATE_DIR_NEW="$HOME/.openclaw"
STATE_DIR_OLD="$HOME/.clawdbot"

mkdir -p "$BACKUP_ROOT"
mkdir -p "$TMP_DIR"

echo "🐈‍⬛ OpenClaw 加密备份开始..."

# 检查密码
if [ -z "${OPENCLAW_BACKUP_PASSWORD:-}" ]; then
    echo "请输入备份密码（至少8位）:"
    read -s BACKUP_PASSWORD
    echo ""
    echo "请再次输入密码:"
    read -s BACKUP_PASSWORD_CONFIRM
    echo ""
    
    if [ "$BACKUP_PASSWORD" != "$BACKUP_PASSWORD_CONFIRM" ]; then
        echo "❌ 密码不匹配"
        exit 1
    fi
    
    if [ ${#BACKUP_PASSWORD} -lt 8 ]; then
        echo "❌ 密码至少8位"
        exit 1
    fi
else
    BACKUP_PASSWORD="$OPENCLAW_BACKUP_PASSWORD"
fi

FOUND_ANY=0

if [ -d "$STATE_DIR_NEW" ]; then
    echo "✓ 发现: $STATE_DIR_NEW"
    cp -a "$STATE_DIR_NEW" "$TMP_DIR/"
    FOUND_ANY=1
fi

if [ -d "$STATE_DIR_OLD" ]; then
    echo "✓ 发现: $STATE_DIR_OLD"
    cp -a "$STATE_DIR_OLD" "$TMP_DIR/"
    FOUND_ANY=1
fi

if [ "$FOUND_ANY" -eq 0 ]; then
    echo "❌ 未找到数据目录"
    rm -rf "$TMP_DIR"
    exit 1
fi

# 停止网关
if command -v openclaw >/dev/null 2>&1; then
    echo "⏸  停止网关..."
    openclaw gateway stop 2>/dev/null || true
    sleep 2
fi

# 打包
echo "📦 打包中..."
tar -czf "/tmp/$ARCHIVE_NAME" -C "$TMP_DIR" .

# 加密（使用 openssl aes-256-cbc）
echo "🔐 加密中..."
openssl enc -aes-256-cbc -salt -pbkdf2 -iter 100000 \
    -in "/tmp/$ARCHIVE_NAME" \
    -out "$BACKUP_ROOT/$ENCRYPTED_NAME" \
    -pass pass:"$BACKUP_PASSWORD"

# 生成校验
shasum -a 256 "$BACKUP_ROOT/$ENCRYPTED_NAME" > "$BACKUP_ROOT/$ENCRYPTED_NAME.sha256"

# 清理
rm -f "/tmp/$ARCHIVE_NAME"
rm -rf "$TMP_DIR"

# 重启网关
if command -v openclaw >/dev/null 2>&1; then
    echo "▶️  重启网关..."
    openclaw gateway start 2>/dev/null || true
fi

echo ""
echo "✅ 加密备份完成！"
echo "📁 位置: $BACKUP_ROOT/$ENCRYPTED_NAME"
echo "🔐 校验: $BACKUP_ROOT/$ENCRYPTED_NAME.sha256"
echo ""
echo "⚠️  请妥善保管密码！丢失密码将无法恢复数据。"
echo ""
echo "解密方法："
echo "openssl enc -aes-256-cbc -d -pbkdf2 -iter 100000 \\"
echo "  -in $ENCRYPTED_NAME \\"
echo "  -out openclaw_backup.tar.gz \\"
echo "  -pass pass:YOUR_PASSWORD"
```

---

### 3. 定时备份配置

位置：`scripts/setup_cron.sh`

```bash
#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKUP_SCRIPT="${OPENCLAW_BACKUP_SCRIPT:-$SCRIPT_DIR/backup_encrypted.sh}"

echo "🐈‍⬛ 配置 OpenClaw 定时备份"
echo ""
echo "选择备份频率："
echo "1. 每天 23:00"
echo "2. 每周日 21:00"
echo "3. 每月1日 20:00"
echo "4. 自定义"
echo ""
read -p "请选择 [1-4]: " CHOICE

case $CHOICE in
    1)
        CRON_EXPR="0 23 * * *"
        DESC="每天 23:00"
        ;;
    2)
        CRON_EXPR="0 21 * * 0"
        DESC="每周日 21:00"
        ;;
    3)
        CRON_EXPR="0 20 1 * *"
        DESC="每月1日 20:00"
        ;;
    4)
        echo "请输入 cron 表达式（如 '0 2 * * *' 代表每天凌晨2点）:"
        read -p "> " CRON_EXPR
        DESC="自定义: $CRON_EXPR"
        ;;
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac

# 检查是否已有任务
if crontab -l 2>/dev/null | grep -q "openclaw.*backup"; then
    echo ""
    echo "⚠️  发现已有 OpenClaw 备份任务，是否覆盖？[y/N]"
    read -p "> " CONFIRM
    if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
        echo "取消操作"
        exit 0
    fi
    
    # 移除旧任务
    crontab -l 2>/dev/null | grep -v "openclaw.*backup" | crontab -
fi

# 添加新任务
(crontab -l 2>/dev/null; echo "$CRON_EXPR $BACKUP_SCRIPT >> /tmp/openclaw_backup.log 2>&1") | crontab -

echo ""
echo "✅ 定时备份已配置"
echo "📅 频率: $DESC"
echo "📜 脚本: $BACKUP_SCRIPT"
echo ""
echo "查看所有定时任务: crontab -l"
echo "查看备份日志: tail -f /tmp/openclaw_backup.log"
```

---

### 4. 列出备份

位置：`scripts/list_backups.sh`

```bash
#!/bin/bash
set -euo pipefail

BACKUP_ROOT="${OPENCLAW_BACKUP_DIR:-$HOME/Desktop/OpenClaw_Backups}"

echo "🐈‍⬛ OpenClaw 备份列表"
echo "位置: $BACKUP_ROOT"
echo ""

if [ ! -d "$BACKUP_ROOT" ]; then
    echo "❌ 备份目录不存在"
    exit 1
fi

cd "$BACKUP_ROOT"

# 统计
TOTAL_FILES=$(ls -1 openclaw_backup_*.tar.gz* 2>/dev/null | grep -v ".sha256" | wc -l | tr -d ' ')
TOTAL_SIZE=$(du -sh . | cut -f1)

echo "📦 共 $TOTAL_FILES 个备份文件，总计 $TOTAL_SIZE"
echo ""

# 列出文件
ls -lht openclaw_backup_*.tar.gz* 2>/dev/null | grep -v ".sha256" | while read -r line; do
    SIZE=$(echo "$line" | awk '{print $5}')
    DATE=$(echo "$line" | awk '{print $6, $7, $8}')
    FILE=$(echo "$line" | awk '{print $9}')
    
    # 检查是否加密
    if [[ "$FILE" == *.enc ]]; then
        ENCRYPTED="🔐 加密"
    else
        ENCRYPTED="📂 未加密"
    fi
    
    # 检查校验文件
    if [ -f "$FILE.sha256" ]; then
        CHECKSUM="✓"
    else
        CHECKSUM="✗"
    fi
    
    echo "[$ENCRYPTED] $FILE"
    echo "  大小: $SIZE | 日期: $DATE | 校验: $CHECKSUM"
    echo ""
done

echo "验证备份完整性："
echo "  shasum -c openclaw_backup_XXXX.tar.gz.sha256"
```

---

## 使用方法

### 方式1：直接调用脚本

```bash
# 普通备份
bash ~/.openclaw/skills/openclaw-backup/scripts/backup.sh

# 加密备份（推荐）
bash ~/.openclaw/skills/openclaw-backup/scripts/backup_encrypted.sh

# 配置定时备份
bash ~/.openclaw/skills/openclaw-backup/scripts/setup_cron.sh

# 查看备份列表
bash ~/.openclaw/skills/openclaw-backup/scripts/list_backups.sh
```

---

### 方式2：通过 OpenClaw 调用

当用户说：
- "备份 OpenClaw" → 执行加密备份
- "定时备份" → 执行 setup_cron.sh
- "查看备份" → 执行 list_backups.sh

---

## 环境变量

可选配置：

```bash
# 备份目录（默认桌面）
export OPENCLAW_BACKUP_DIR="$HOME/Backups/OpenClaw"

# 加密密码（不推荐明文存储）
export OPENCLAW_BACKUP_PASSWORD="your_password"

# 备份脚本路径（用于 cron）
export OPENCLAW_BACKUP_SCRIPT="$HOME/.openclaw/skills/openclaw-backup/scripts/backup_encrypted.sh"
```

---

## 最佳实践

### 1. 3-2-1 备份原则

- 保留 **3** 份副本
- 存在 **2** 种介质（本地 + 移动硬盘/云盘）
- 其中 **1** 份在异地

### 2. 加密备份

备份文件包含敏感数据：
- API Key
- Telegram Bot Token
- 用户记忆
- 对话历史

**强烈建议**使用加密备份（`backup_encrypted.sh`）

### 3. 定期验证

每月验证一次备份完整性：

```bash
cd ~/Desktop/OpenClaw_Backups
shasum -c openclaw_backup_2026-03-13_20-00-00.tar.gz.sha256
```

### 4. 备份触发时机

建议在以下操作后手动备份：
- ✅ 修改配置文件
- ✅ 新增 Skill
- ✅ 更新记忆文件（MEMORY.md）
- ✅ 绑定新渠道
- ✅ 修改 API Key
- ✅ 完成重要对话

---

## 云端同步（可选）

### iCloud Drive

```bash
# 修改备份目录
export OPENCLAW_BACKUP_DIR="$HOME/Library/Mobile Documents/com~apple~CloudDocs/OpenClaw_Backups"
```

### Google Drive / Dropbox

安装对应客户端后：

```bash
export OPENCLAW_BACKUP_DIR="$HOME/Google Drive/OpenClaw_Backups"
# 或
export OPENCLAW_BACKUP_DIR="$HOME/Dropbox/OpenClaw_Backups"
```

---

## 故障排查

### 问题1：cron 任务未执行

**检查**：
```bash
# 查看 cron 任务
crontab -l

# 查看日志
tail -f /tmp/openclaw_backup.log
```

**解决**：确保脚本有执行权限
```bash
chmod +x ~/.openclaw/skills/openclaw-backup/scripts/*.sh
```

---

### 问题2：加密失败

**症状**：`openssl: command not found`

**解决**：macOS 自带 openssl，如果缺失：
```bash
brew install openssl
```

---

### 问题3：备份文件过大

**症状**：备份文件几百MB/GB

**原因**：可能包含日志文件、临时文件

**解决**：编辑 `backup.sh`，添加排除规则：

```bash
# 在 cp -a 之前添加
echo "清理临时文件..."
find "$STATE_DIR_NEW" -name "*.log" -delete 2>/dev/null || true
find "$STATE_DIR_NEW" -name "node_modules" -type d -exec rm -rf {} + 2>/dev/null || true
```

---

## 参考

- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [macOS cron 指南](https://man.openbsd.org/cron.8)
- [OpenSSL 加密指南](https://www.openssl.org/docs/)
