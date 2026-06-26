---
name: mail-126
author: Phal Studio
description: |
  126.com 网易邮箱管理 CLI。支持收取/发送邮件、搜索邮件、邮件管理和邮件统计。
  当用户提到邮件、邮箱、email、发邮件、收邮件、查邮件、126邮箱时触发。
  支持其它 skill 和定时任务调用，所有命令输出 JSON 格式。
trigger_words:
  - 邮件
  - 邮箱
  - email
  - 发邮件
  - 收邮件
  - 查邮件
  - 126邮箱
  - 126邮箱管理
  - mail
  - inbox
---

# Mail-126 — 网易邮箱管理 CLI

## 概述

| 模块 | 命令 | 功能 |
|------|------|------|
| 初始化 | `init` | 创建数据目录和默认配置 |
| 配置 | `config setup / verify` | 配置邮箱账号和授权码、验证连接 |
| 收件箱 | `inbox list / read / search` | 列出、读取、搜索邮件 |
| 发送 | `send / reply / forward` | 发送新邮件、回复、转发 |
| 管理 | `manage mark / delete / move` | 标记已读/未读、删除、移动邮件 |
| 统计 | `stats today / range / by-sender / folders` | 邮件统计分析 |

## When to Run

- 用户提到「邮件」「邮箱」「email」「发邮件」「收邮件」「查邮件」「126邮箱」
- 其他 skill 或定时任务需要发送/接收邮件
- 用户需要查看邮件统计信息

## 邮箱服务器配置

| 服务 | 地址 | 端口 | 协议 |
|------|------|------|------|
| IMAP | imap.126.com | 993 | SSL |
| SMTP | smtp.126.com | 465 | SSL |
| POP3 | pop.126.com | 995 | SSL |

> **注意**: 使用本工具前，用户需要在网易邮箱设置中开启 IMAP/SMTP 服务并获取「授权码」（非登录密码）。

## Workflow

### 1. 初始化流程

首次使用时：

```bash
# Step 1: 初始化数据目录
python3 SKILL_DIR/scripts/mail_manager.py init

# Step 2: 配置邮箱账号（需要用户提供邮箱地址和授权码）
python3 SKILL_DIR/scripts/mail_manager.py config setup --email "user@126.com" --auth-code "XXXXXXXXXX"

# Step 3: 验证连接
python3 SKILL_DIR/scripts/mail_manager.py config verify
```

如果用户未提供授权码，**主动引导**：
1. 登录 mail.126.com → 设置 → POP3/SMTP/IMAP → 开启 IMAP/SMTP 服务
2. 按提示用手机发送短信获取授权码
3. 将授权码提供给 CLI 配置

### 2. 收取邮件

```bash
# 列出最近10封邮件
python3 SKILL_DIR/scripts/mail_manager.py inbox list --limit 10

# 列出指定文件夹的邮件（已发送、草稿等）
python3 SKILL_DIR/scripts/mail_manager.py inbox list --folder "Sent Messages" --limit 5

# 读取邮件详情
python3 SKILL_DIR/scripts/mail_manager.py inbox read --uid 12345

# 搜索邮件 - 按发件人
python3 SKILL_DIR/scripts/mail_manager.py inbox search --from "sender@example.com"

# 搜索邮件 - 按主题和日期
python3 SKILL_DIR/scripts/mail_manager.py inbox search --subject "会议" --since "2026-04-01"

# 搜索邮件 - 按日期范围
python3 SKILL_DIR/scripts/mail_manager.py inbox search --since "2026-04-01" --until "2026-04-11"
```

### 3. 发送邮件

```bash
# 发送新邮件
python3 SKILL_DIR/scripts/mail_manager.py send \
  --to "recipient@example.com" \
  --subject "测试邮件" \
  --body "这是一封测试邮件的内容。"

# 发送带抄送的邮件
python3 SKILL_DIR/scripts/mail_manager.py send \
  --to "a@b.com,c@d.com" \
  --cc "e@f.com" \
  --subject "会议通知" \
  --body "明天下午3点开会。"

# 发送带附件的邮件
python3 SKILL_DIR/scripts/mail_manager.py send \
  --to "a@b.com" \
  --subject "文件" \
  --body "请查收附件" \
  --attachments "/path/to/file1.pdf,/path/to/file2.docx"

# 回复邮件
python3 SKILL_DIR/scripts/mail_manager.py reply --uid 12345 --body "收到，谢谢！"

# 转发邮件
python3 SKILL_DIR/scripts/mail_manager.py forward --uid 12345 --to "forward@target.com" --note "请查看此邮件"
```

### 4. 邮件管理

```bash
# 标记已读
python3 SKILL_DIR/scripts/mail_manager.py manage mark --uid 12345 --flag read

# 标记未读
python3 SKILL_DIR/scripts/mail_manager.py manage mark --uid 12345 --flag unread

# 标记星标
python3 SKILL_DIR/scripts/mail_manager.py manage mark --uid 12345 --flag starred

# 取消星标
python3 SKILL_DIR/scripts/mail_manager.py manage mark --uid 12345 --flag unstarred

# 删除邮件
python3 SKILL_DIR/scripts/mail_manager.py manage delete --uid 12345

# 移动邮件到指定文件夹
python3 SKILL_DIR/scripts/mail_manager.py manage move --uid 12345 --folder "已处理"
```

### 5. 邮件统计

```bash
# 今日邮件统计
python3 SKILL_DIR/scripts/mail_manager.py stats today

# 指定日期范围统计
python3 SKILL_DIR/scripts/mail_manager.py stats range --since "2026-04-01" --until "2026-04-11"

# 按发件人统计 Top 10
python3 SKILL_DIR/scripts/mail_manager.py stats by-sender --limit 10

# 文件夹概览
python3 SKILL_DIR/scripts/mail_manager.py stats folders
```

### 6. 附件下载

```bash
# 下载指定邮件的所有附件
python3 SKILL_DIR/scripts/mail_manager.py inbox download --uid 12345 --output-dir "/path/to/save"

# 下载指定邮件的特定附件
python3 SKILL_DIR/scripts/mail_manager.py inbox download --uid 12345 --attachment "report.pdf" --output-dir "/path/to/save"
```

## 网易邮箱特殊文件夹映射

| 中文名 | IMAP 文件夹名 |
|--------|---------------|
| 收件箱 | INBOX |
| 已发送 | Sent Messages |
| 草稿 | Drafts |
| 已删除 | Trash |
| 垃圾邮件 | Junk |
| 病毒邮件 | Virus |

## 数据字段参考

详细字段说明见 `references/data-schema.md`。

### 邮件摘要字段 (inbox list)

| 字段 | 说明 |
|------|------|
| uid | 邮件唯一ID |
| from | 发件人 |
| to | 收件人 |
| subject | 主题 |
| date | 日期 |
| flags | 标记（seen/flagged 等） |
| size | 大小（字节） |

### 邮件详情字段 (inbox read)

| 字段 | 说明 |
|------|------|
| uid | 邮件唯一ID |
| from | 发件人 |
| to | 收件人列表 |
| cc | 抄送列表 |
| subject | 主题 |
| date | 日期 |
| body_text | 纯文本正文 |
| body_html | HTML正文（如有） |
| attachments | 附件列表（名称+大小） |

## Output Format

所有命令输出 JSON：

```json
// 成功
{
  "status": "success",
  "data": { ... },
  "message": "操作描述"
}

// 失败
{
  "status": "error",
  "data": null,
  "message": "错误描述"
}
```

## 交互风格

- **纯 CLI 调用**: 所有操作通过命令行参数完成，无交互式输入
- **JSON 输出**: 标准化 JSON 格式，便于其他 skill/定时任务解析
- **中文友好**: 自动处理 GBK/UTF-8 编码
- **超时控制**: 默认 30 秒超时，网络操作最多重试 2 次
- **安全存储**: 授权码使用 Base64 编码存储，日志中不输出敏感信息
