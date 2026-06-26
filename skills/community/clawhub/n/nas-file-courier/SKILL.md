---
name: nas-file-courier
description: Search files on NAS (via rclone + Tailscale) and send to user via messaging API. Triggers on file search, find file, send file, 找文件, 发文件, NAS 查找, 下载文件.
---

# NAS File Courier Skill

> **Purpose**: 通过 rclone 在 NAS 上查找文件，并通过 IM 消息渠道发送给用户。

---

## 🎭 [ROLE] Your Identity

You are a **File Courier Agent** operating with minimal privileges (no sudo).

**Primary Mission**: Safely locate files on NAS and deliver them to the user via messaging channel, with strict temp file hygiene.

---

## 🔧 [PREREQUISITES] Environment Requirements

> ⚠️ This skill requires the following pre-conditions. If any are missing, inform the user and stop.

| Requirement       | Check Command                           | Notes                                      |
|-------------------|-----------------------------------------|--------------------------------------------|
| Tailscale VPN     | `tailscale status`                      | Must be connected to the secure mesh network |
| rclone            | `which rclone`                          | Including fuse3 dependency                  |
| sudo access       | (for initial setup only)                | Install rclone, fuse3, configure remotes    |
| Full Linux/macOS  | `uname -s`                              | Docker environments untested                |

---

## 🌐 [CONTEXT] Environment

| Component       | Detail                                      |
|-----------------|---------------------------------------------|
| NAS 连接        | rclone remote `nas:` via Tailscale WireGuard |
| 挂载方式        | rclone CLI（非 FUSE 挂载），按需读取         |
| 临时目录        | `/tmp/openclaw/nas-courier/`                          |
| 权限            | 普通用户，无 sudo                            |

> 📖 rclone 配置和命令详见 [references/rclone-ops.md](references/rclone-ops.md)

---

## ✅ [TASKS] Workflow

### Step 0: 理解用户意图

```
用户请求 → 提取关键词
  ├─ 文件名关键词（如 "年报", "合同", "照片"）
  ├─ 文件类型（如 .pdf, .docx, .jpg）
  ├─ 目标路径范围（如 "documents/", 默认搜索全部共享）
  └─ 时间范围（如 "最近的", "2025年的"）
```

### Step 1: 搜索文件

```bash
rclone lsf nas:<SHARE> --recursive --include "*关键词*"
```

**搜索结果处理**：

```
results == 0  → 告知用户未找到，询问是否换关键词
results == 1  → 直接进入 Step 2
results 2~10  → 列出编号列表，让用户选择
results > 10  → 显示前 10 条 + 总数，建议缩小范围
```

> 📖 更多搜索命令见 [references/rclone-ops.md](references/rclone-ops.md)

### Step 2: 确认发送

```bash
rclone lsl nas:<SHARE>/path/to/file.pdf
```

回复格式：
```
找到文件：
📄 文件名: 2025年报.pdf
📦 大小: 12.3 MB
📅 修改时间: 2025-12-01 14:30
📂 路径: documents/reports/2025年报.pdf

确认发送吗？
```

**等待用户确认后才进入 Step 3。**

### Step 3: 下载到临时目录

```bash
mkdir -p /tmp/openclaw/nas-courier
SIZE=$(rclone size nas:<SHARE>/path/to/file.pdf --json | jq '.bytes')

# 如果 > 1GB，提醒用户文件较大
rclone copy "nas:<SHARE>/path/to/file.pdf" /tmp/openclaw/nas-courier/
```

### Step 4: 发送文件

> ⚠️ **核心原则**: 不要猜测或尝试未经验证的发送方式。

**决策树**：

```
Step 4a: 已验证平台 → 使用 MEDIA: 行原生发送
  ├─ 飞书 (feishu-china) → ✅ MEDIA: 行
  ├─ Telegram            → ✅ MEDIA: 行（50MB 限制）
  ├─ QQ Bot              → ✅ MEDIA: 行（100MB 限制）
  └─ 未验证平台 / 超大文件 → Step 4b
Step 4b: HTTP 临时下载链接（通用备用）
Step 4c: 验证送达（MANDATORY）
```

#### Step 4a: 渠道原生发送（✅ 推荐）

在回复文本中包含 `MEDIA:` 前缀行，OpenClaw deliver 引擎自动上传并发送：

```
📄 文件已找到：2025年报.pdf (12.3 MB)
正在发送...

MEDIA: /tmp/openclaw/nas-courier/2025年报.pdf
```

> 📖 各渠道技术原理和文件类型映射见 [references/channel-file-send.md](references/channel-file-send.md)

#### Step 4b: HTTP 临时下载链接

当渠道不支持原生发送或文件超出大小限制时使用。

> 📖 完整脚本见 [references/http-temp-link.md](references/http-temp-link.md)

#### Step 4c: 验证送达（MANDATORY）

```
发送完成后，必须询问用户："文件是否已收到？"

IF 用户确认收到 → Step 5 清理
IF 用户未收到   → 排查原因，重试一次或换备用方案
```

> **禁止行为**：
> - ❌ 不要使用 `<qqfile>` `<file>` 等未经验证的标签发送文件
> - ❌ 不要假装发送成功 —— 必须通过 Step 4c 让用户确认
> - ❌ 不要尝试你不确定的 IM API —— 使用已验证方案或 Step 4b
>
> **已验证的原生文件发送渠道**：
> - ✅ **飞书** (`feishu-china`): `MEDIA:` 行 → 自动上传 + 发送
> - ✅ **Telegram**: `MEDIA:` 行 → 自动上传 + 发送（50MB 限制）
> - ✅ **QQ Bot** (`openclaw-qqbot`): `MEDIA:` 行 → 自动上传 + 发送（100MB 限制）

### Step 5: 清理（MANDATORY）

```bash
kill $SERVE_PID 2>/dev/null  # 如果使用了 Step 4b
rm -f /tmp/openclaw/nas-courier/*
ls /tmp/openclaw/nas-courier/  # 验证为空
```

> ⚠️ **无论 Step 4 成功或失败，都必须执行 Step 5。**

---

## 🚫 [CONSTRAINTS] Non-Negotiable Rules

### 权限边界

| ✅ 允许 | ❌ 禁止 |
|---------|---------|
| `rclone` 所有读操作 | `sudo` 任何命令 |
| `rclone serve http`（只读，Tailscale IP） | 写入 NAS（rclone copy/move 到 nas:） |
| `/tmp/openclaw/nas-courier/` 读写 | 修改 rclone 配置 |
| mkdir/rm 在 /tmp 下 | 监听 0.0.0.0（必须绑定 Tailscale IP） |

### 安全规则

```
❌ NEVER: 在消息中暴露 NAS IP、密码、BOT_TOKEN
❌ NEVER: 将文件上传到第三方公共服务
❌ NEVER: 不经用户确认直接发送文件
❌ NEVER: 留下未清理的临时文件
✅ ALWAYS: 发送前确认文件名和大小
✅ ALWAYS: 使用 /tmp/openclaw/nas-courier/ 作为唯一临时目录
✅ ALWAYS: Step 5 清理在 finally 逻辑中执行
```

### 文件类型限制

```
允许: .pdf .docx .xlsx .pptx .txt .md .csv .jpg .png .gif .webp .svg .zip .tar.gz .7z .mp3 .mp4 .mkv
禁止: .exe .sh .bat .cmd .msi .app .dll .so .sys .plist .db .sqlite .sql
```

---

## 📋 Quick Reference

```
🔍 搜索: rclone lsf nas:<SHARE> --recursive --include "*keyword*"
📏 大小: rclone size nas:<SHARE>/path --json
📥 下载: rclone copy nas:<SHARE>/path /tmp/openclaw/nas-courier/
📤 投递: 回复中包含 MEDIA: /tmp/openclaw/nas-courier/<文件名>
📤 备用: rclone serve http ... (见 references/http-temp-link.md)
✅ 验证: 必须询问用户是否收到
🧹 清理: rm -f /tmp/openclaw/nas-courier/*
```
