---
name: openclaw-restore
slug: halaoluan-openclaw-restore
version: 1.0.0
description: 一键恢复 OpenClaw 数据（支持加密/未加密备份）。Use when user asks to restore OpenClaw, recover data, restore from backup, or fix broken installation. Triggers: "恢复", "restore", "recover", "恢复备份", "还原数据", "restore backup".
---

# OpenClaw 恢复 Skill

从备份文件一键恢复 OpenClaw 数据，支持加密和未加密备份。

---

## 使用场景

| 触发词 | 操作 |
|--------|------|
| "恢复 OpenClaw" | 从备份恢复数据 |
| "恢复最新备份" | 自动选择最新备份恢复 |
| "恢复加密备份" | 解密并恢复 |
| "列出可恢复的备份" | 显示所有备份 |

---

## 核心脚本

### 1. 恢复脚本（未加密备份）

位置：`scripts/restore.sh`

```bash
#!/bin/bash
set -euo pipefail

if [ $# -lt 1 ]; then
    echo "用法: $0 /path/to/openclaw_backup_xxx.tar.gz"
    exit 1
fi

ARCHIVE="$1"
RESTORE_TMP="/tmp/openclaw_restore_$(date +"%Y-%m-%d_%H-%M-%S")"

if [ ! -f "$ARCHIVE" ]; then
    echo "❌ 备份文件不存在: $ARCHIVE"
    exit 1
fi

# 验证校验文件
if [ -f "$ARCHIVE.sha256" ]; then
    echo "🔐 验证备份完整性..."
    if ! shasum -c "$ARCHIVE.sha256"; then
        echo "❌ 校验失败！备份文件可能已损坏。"
        echo "是否仍要继续？[y/N]"
        read -p "> " CONFIRM
        if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
            exit 1
        fi
    fi
    echo "✓ 校验通过"
fi

mkdir -p "$RESTORE_TMP"

echo "📦 解压备份文件..."
tar -xzf "$ARCHIVE" -C "$RESTORE_TMP"

echo "🐈‍⬛ 开始恢复..."

# 停止OpenClaw
if command -v openclaw >/dev/null 2>&1; then
    echo "⏸  停止 OpenClaw 网关..."
    openclaw gateway stop 2>/dev/null || true
    sleep 2
fi

# 备份当前数据（以防万一）
if [ -d "$HOME/.openclaw" ]; then
    BACKUP_OLD="$HOME/.openclaw.backup.$(date +"%Y%m%d_%H%M%S")"
    echo "💾 备份当前数据到: $BACKUP_OLD"
    mv "$HOME/.openclaw" "$BACKUP_OLD"
fi

# 恢复
if [ -d "$RESTORE_TMP/.openclaw" ]; then
    cp -a "$RESTORE_TMP/.openclaw" "$HOME/"
    echo "✓ 已恢复: ~/.openclaw"
fi

if [ -d "$RESTORE_TMP/.clawdbot" ]; then
    cp -a "$RESTORE_TMP/.clawdbot" "$HOME/"
    echo "✓ 已恢复: ~/.clawdbot"
fi

rm -rf "$RESTORE_TMP"

# 修复检查
if command -v openclaw >/dev/null 2>&1; then
    echo "🔧 执行修复检查..."
    openclaw doctor || true
    echo "▶️  重启 OpenClaw 网关..."
    openclaw gateway restart || true
    sleep 3
    openclaw status || true
fi

echo ""
echo "✅ 恢复完成！"
echo ""
echo "建议立即测试："
echo "1. OpenClaw 是否能正常启动"
echo "2. 记忆是否还在"
echo "3. 渠道登录状态是否保留"
echo "4. API 配置是否正常"
echo ""
if [ -n "${BACKUP_OLD:-}" ]; then
    echo "旧数据已备份到: $BACKUP_OLD"
    echo "确认恢复成功后可删除: rm -rf $BACKUP_OLD"
fi
```

---

### 2. 恢复加密备份

位置：`scripts/restore_encrypted.sh`

```bash
#!/bin/bash
set -euo pipefail

if [ $# -lt 1 ]; then
    echo "用法: $0 /path/to/openclaw_backup_xxx.tar.gz.enc"
    exit 1
fi

ENCRYPTED_ARCHIVE="$1"
RESTORE_TMP="/tmp/openclaw_restore_$(date +"%Y-%m-%d_%H-%M-%S")"
DECRYPTED_ARCHIVE="$RESTORE_TMP/backup.tar.gz"

if [ ! -f "$ENCRYPTED_ARCHIVE" ]; then
    echo "❌ 加密备份不存在: $ENCRYPTED_ARCHIVE"
    exit 1
fi

# 验证校验
if [ -f "$ENCRYPTED_ARCHIVE.sha256" ]; then
    echo "🔐 验证备份完整性..."
    if ! shasum -c "$ENCRYPTED_ARCHIVE.sha256"; then
        echo "❌ 校验失败！"
        exit 1
    fi
    echo "✓ 校验通过"
fi

mkdir -p "$RESTORE_TMP"

# 输入密码
if [ -z "${OPENCLAW_BACKUP_PASSWORD:-}" ]; then
    echo "请输入备份密码:"
    read -s BACKUP_PASSWORD
    echo ""
else
    BACKUP_PASSWORD="$OPENCLAW_BACKUP_PASSWORD"
fi

# 解密
echo "🔓 解密中..."
if ! openssl enc -aes-256-cbc -d -pbkdf2 -iter 100000 \
    -in "$ENCRYPTED_ARCHIVE" \
    -out "$DECRYPTED_ARCHIVE" \
    -pass pass:"$BACKUP_PASSWORD"; then
    echo "❌ 解密失败！密码错误或文件已损坏。"
    rm -rf "$RESTORE_TMP"
    exit 1
fi

echo "✓ 解密成功"

# 解压
echo "📦 解压备份..."
tar -xzf "$DECRYPTED_ARCHIVE" -C "$RESTORE_TMP"

echo "🐈‍⬛ 开始恢复..."

# 停止OpenClaw
if command -v openclaw >/dev/null 2>&1; then
    echo "⏸  停止网关..."
    openclaw gateway stop 2>/dev/null || true
    sleep 2
fi

# 备份当前数据
if [ -d "$HOME/.openclaw" ]; then
    BACKUP_OLD="$HOME/.openclaw.backup.$(date +"%Y%m%d_%H%M%S")"
    echo "💾 备份当前数据到: $BACKUP_OLD"
    mv "$HOME/.openclaw" "$BACKUP_OLD"
fi

# 恢复
if [ -d "$RESTORE_TMP/.openclaw" ]; then
    cp -a "$RESTORE_TMP/.openclaw" "$HOME/"
    echo "✓ 已恢复: ~/.openclaw"
fi

if [ -d "$RESTORE_TMP/.clawdbot" ]; then
    cp -a "$RESTORE_TMP/.clawdbot" "$HOME/"
    echo "✓ 已恢复: ~/.clawdbot"
fi

rm -rf "$RESTORE_TMP"

# 修复检查
if command -v openclaw >/dev/null 2>&1; then
    echo "🔧 执行修复检查..."
    openclaw doctor || true
    echo "▶️  重启网关..."
    openclaw gateway restart || true
    sleep 3
    openclaw status || true
fi

echo ""
echo "✅ 恢复完成！"
echo ""
if [ -n "${BACKUP_OLD:-}" ]; then
    echo "旧数据已备份到: $BACKUP_OLD"
    echo "确认恢复成功后可删除: rm -rf $BACKUP_OLD"
fi
```

---

### 3. 恢复最新备份

位置：`scripts/restore_latest.sh`

```bash
#!/bin/bash
set -euo pipefail

BACKUP_ROOT="${OPENCLAW_BACKUP_DIR:-$HOME/Desktop/OpenClaw_Backups}"

echo "🐈‍⬛ 恢复最新备份"
echo "备份目录: $BACKUP_ROOT"
echo ""

if [ ! -d "$BACKUP_ROOT" ]; then
    echo "❌ 备份目录不存在"
    exit 1
fi

cd "$BACKUP_ROOT"

# 查找最新备份（优先加密）
LATEST_ENCRYPTED=$(ls -t openclaw_backup_*.tar.gz.enc 2>/dev/null | head -1)
LATEST_PLAIN=$(ls -t openclaw_backup_*.tar.gz 2>/dev/null | grep -v ".enc" | head -1)

if [ -n "$LATEST_ENCRYPTED" ]; then
    echo "发现最新加密备份: $LATEST_ENCRYPTED"
    LATEST="$BACKUP_ROOT/$LATEST_ENCRYPTED"
    SCRIPT="restore_encrypted.sh"
elif [ -n "$LATEST_PLAIN" ]; then
    echo "发现最新备份: $LATEST_PLAIN"
    LATEST="$BACKUP_ROOT/$LATEST_PLAIN"
    SCRIPT="restore.sh"
else
    echo "❌ 未找到备份文件"
    exit 1
fi

echo ""
echo "确认恢复？[y/N]"
read -p "> " CONFIRM

if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
    echo "取消恢复"
    exit 0
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
bash "$SCRIPT_DIR/$SCRIPT" "$LATEST"
```

---

### 4. 列出可恢复的备份

位置：`scripts/list_restoreable.sh`

```bash
#!/bin/bash
set -euo pipefail

BACKUP_ROOT="${OPENCLAW_BACKUP_DIR:-$HOME/Desktop/OpenClaw_Backups}"

echo "🐈‍⬛ 可恢复的备份列表"
echo "位置: $BACKUP_ROOT"
echo ""

if [ ! -d "$BACKUP_ROOT" ]; then
    echo "❌ 备份目录不存在"
    exit 1
fi

cd "$BACKUP_ROOT"

COUNT=0

ls -lt openclaw_backup_*.tar.gz* 2>/dev/null | grep -v ".sha256" | while read -r line; do
    COUNT=$((COUNT + 1))
    SIZE=$(echo "$line" | awk '{print $5}')
    DATE=$(echo "$line" | awk '{print $6, $7, $8}')
    FILE=$(echo "$line" | awk '{print $9}')
    
    if [[ "$FILE" == *.enc ]]; then
        TYPE="🔐 加密"
        RESTORE_CMD="bash ~/.openclaw/skills/openclaw-restore/scripts/restore_encrypted.sh \"$BACKUP_ROOT/$FILE\""
    else
        TYPE="📂 普通"
        RESTORE_CMD="bash ~/.openclaw/skills/openclaw-restore/scripts/restore.sh \"$BACKUP_ROOT/$FILE\""
    fi
    
    echo "[$COUNT] $FILE"
    echo "    类型: $TYPE | 大小: $SIZE | 日期: $DATE"
    echo "    恢复: $RESTORE_CMD"
    echo ""
done

echo "快速恢复最新备份："
echo "  bash ~/.openclaw/skills/openclaw-restore/scripts/restore_latest.sh"
```

---

## 使用方法

### 方式1：直接调用脚本

```bash
# 恢复普通备份
bash ~/.openclaw/skills/openclaw-restore/scripts/restore.sh \
  ~/Desktop/OpenClaw_Backups/openclaw_backup_2026-03-13_20-00-00.tar.gz

# 恢复加密备份
bash ~/.openclaw/skills/openclaw-restore/scripts/restore_encrypted.sh \
  ~/Desktop/OpenClaw_Backups/openclaw_backup_2026-03-13_20-00-00.tar.gz.enc

# 恢复最新备份
bash ~/.openclaw/skills/openclaw-restore/scripts/restore_latest.sh

# 列出可恢复备份
bash ~/.openclaw/skills/openclaw-restore/scripts/list_restoreable.sh
```

---

### 方式2：通过 OpenClaw 调用

当用户说：
- "恢复 OpenClaw" → 执行 restore_latest.sh
- "列出备份" → 执行 list_restoreable.sh
- "恢复这个备份 [文件路径]" → 执行对应 restore 脚本

---

## 恢复后检查清单

### ✅ 必检项目

1. **网关状态**
   ```bash
   openclaw status
   ```

2. **配置验证**
   ```bash
   openclaw doctor
   ```

3. **记忆文件**
   ```bash
   cat ~/.openclaw/workspace/MEMORY.md
   ```

4. **渠道登录**
   - Telegram Bot 是否在线
   - WeChat 是否需要重新扫码

5. **API 配置**
   ```bash
   cat ~/.openclaw/config.yaml | grep -A5 "model:"
   ```

---

## 灾难恢复流程

### 场景：macOS 完全重装

#### 第1步：安装 OpenClaw

```bash
# 安装 Node.js
brew install node

# 安装 OpenClaw
npm install -g openclaw
```

---

#### 第2步：恢复备份

```bash
# 从云盘/移动硬盘拷贝备份文件
cp /Volumes/External/openclaw_backup_*.tar.gz.enc ~/Desktop/

# 恢复
bash ~/.openclaw/skills/openclaw-restore/scripts/restore_encrypted.sh \
  ~/Desktop/openclaw_backup_2026-03-13_20-00-00.tar.gz.enc
```

---

#### 第3步：验证

```bash
openclaw doctor
openclaw gateway restart
openclaw status
```

---

## 故障排查

### 问题1：解密失败

**症状**：`bad decrypt`

**原因**：密码错误或文件损坏

**解决**：
1. 确认密码正确
2. 验证备份完整性：`shasum -c backup.tar.gz.enc.sha256`
3. 尝试恢复更早的备份

---

### 问题2：恢复后网关无法启动

**症状**：`openclaw gateway start` 失败

**解决**：
```bash
# 检查配置
openclaw doctor

# 查看日志
tail -f ~/.openclaw/logs/gateway.log

# 重置配置（谨慎）
mv ~/.openclaw/config.yaml ~/.openclaw/config.yaml.broken
openclaw gateway start
```

---

### 问题3：权限问题

**症状**：`Permission denied`

**解决**：
```bash
# 修复权限
chmod -R 755 ~/.openclaw
chmod 600 ~/.openclaw/config.yaml
```

---

## 最佳实践

### 1. 恢复前备份当前数据

脚本会自动备份到 `~/.openclaw.backup.YYYYMMDD_HHMMSS`

### 2. 验证备份完整性

恢复前务必检查 SHA256：
```bash
shasum -c backup.tar.gz.sha256
```

### 3. 小范围测试

可以先恢复到临时位置测试：
```bash
tar -xzf backup.tar.gz -C /tmp/test_restore
```

### 4. 渠道重新登录

某些渠道（如 WeChat）可能需要重新扫码登录

---

## 参考

- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [灾难恢复指南](https://docs.openclaw.ai/guides/disaster-recovery)
