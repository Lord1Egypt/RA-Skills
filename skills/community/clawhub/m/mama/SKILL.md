---
name: multi-account-mail-agent
name_cn: 多账户邮箱智能体
description: "通用多账户 IMAP/SMTP 邮箱代理。用于检查邮箱、列出账号、搜索邮件、读取邮件正文/链接/附件、下载附件、生成回复草稿、转发邮件、显式发送邮件、标记已读/未读、移动邮件，以及按关键词和截止时间生成邮件巡检摘要。支持默认账号、指定账号和跨账号操作；从某账号读取的邮件应继续使用同一账号处理回复、转发和草稿发送，避免账号交叉。触发关键词：多账户邮箱智能体、邮箱智能体、检查邮箱、查看邮箱、搜索邮件、读取邮件、邮件附件、回复草稿、转发邮件、发送邮件、截止时间邮件、邮件巡检。"
description_cn: "多账户 IMAP/SMTP 邮箱代理：同账号闭环查读搜转发发送，支持关键词与截止时间巡检。"
---

# 多账户邮箱智能体

使用本 skill 代理一个或多个本地邮箱账号。优先通过 `scripts/mail.py` 执行单次邮箱操作，通过 `scripts/process_digest.py` 执行巡检摘要；需要配置、关键词、定时或故障细节时再读取 `references/` 下的对应文档。

用户可见名称统一使用“多账户邮箱智能体”。

## 执行原则

- 先判断是否已配置邮箱账号，再执行读取、搜索、发送或巡检。
- 默认使用配置中的 `default_account`；用户指定账号时添加 `--account <账号ID>`；跨账号搜索或巡检时添加 `--all-accounts`。
- 从某个账号读取到的邮件，后续回复草稿、转发草稿和草稿发送默认继续使用同一账号。
- 优先生成草稿；只有用户明确要求发送，才使用发送命令或 `forward --send`。
- 不把客户端值、授权码、连接配置内容写入聊天、日志、摘要、推送或发布包。
- 附件、草稿、摘要和缓存默认写入 skill 目录下的 `.temp/`。

## 首次运行

首次触发时，检查本地连接配置是否存在：

- `scripts/mail_config.json`：初始化脚本在用户本机生成的多账号 IMAP/SMTP 配置
- `scripts/digest_config.py`：初始化脚本在用户本机生成的巡检关键词、检查时间和推送偏好

这些文件属于本地运行配置，不属于 skill 发布内容；缺少时读取 [首次运行导引](references/first-run-guide.md)。只要求用户提供完整邮箱账号和客户端值；系统会根据邮箱域名识别常见服务商，未识别时尝试 `imap.<domain>:993` 和 `smtp.<domain>:465`。

```bash
python "<skill_dir>/scripts/init_config.py" --user "user@<域名>"
python "<skill_dir>/scripts/init_config.py" --account work --user "user@<域名>" --set-default
```

客户端值不要放进命令行参数。优先使用交互输入、临时文件、环境变量或 stdin：

```bash
python "<skill_dir>/scripts/init_config.py" --user "user@<域名>" --value-file "/tmp/mail-value.txt"
python "<skill_dir>/scripts/init_config.py" --user "user@<域名>" --value-env MAIL_VALUE
python "<skill_dir>/scripts/init_config.py" --user "user@<域名>" --value-stdin
```

连接失败或服务商识别错误时，读取 [邮箱配置](references/config-guide.md) 和 [故障处理](references/troubleshooting-guide.md)。

## 单次邮箱操作

统一入口是 `scripts/mail.py`。

列出账号：

```bash
python "<skill_dir>/scripts/mail.py" accounts
python "<skill_dir>/scripts/mail.py" accounts --json
```

搜索邮件：

```bash
python "<skill_dir>/scripts/mail.py" search --query "材料" --since 2026-07-01 --limit 20
python "<skill_dir>/scripts/mail.py" search --all-accounts --parallel-accounts 4 --query "材料" --limit 20
python "<skill_dir>/scripts/mail.py" search --from "sender@<域名>" --has-attachment --json
```

读取邮件正文、链接和附件信息：

```bash
python "<skill_dir>/scripts/mail.py" read --uid 123 --mailbox INBOX
python "<skill_dir>/scripts/mail.py" read --account work --uid 123 --mailbox INBOX --json
```

下载附件：

```bash
python "<skill_dir>/scripts/mail.py" attachments --uid 123 --output-dir "<skill_dir>/.temp/attachments"
```

默认阻止高风险扩展名附件；用户明确确认需要时才添加 `--allow-risky`。可用 `--max-bytes` 限制单个附件大小。

生成回复草稿：

```bash
python "<skill_dir>/scripts/mail.py" reply-draft --uid 123 --body "收到，我会按要求处理。"
```

转发邮件。默认生成草稿；只有用户明确要求立即发送时才添加 `--send`：

```bash
python "<skill_dir>/scripts/mail.py" forward --uid 123 --to "recipient@<域名>"
python "<skill_dir>/scripts/mail.py" forward --uid 123 --to "recipient@<域名>" --send
```

显式发送草稿或新邮件。`send` 必须添加 `--confirm`：

```bash
python "<skill_dir>/scripts/mail.py" send --draft "<skill_dir>/.temp/work_reply_draft_YYYYMMDD_HHMMSS.eml" --confirm
python "<skill_dir>/scripts/mail.py" send --to "recipient@<域名>" --subject "主题" --body "正文" --confirm
```

标记和移动。移动邮件必须添加 `--confirm`：

```bash
python "<skill_dir>/scripts/mail.py" mark-seen --uid 123
python "<skill_dir>/scripts/mail.py" mark-seen --uid 123 --unseen
python "<skill_dir>/scripts/mail.py" move --uid 123 --folder Archive --confirm
```

## 巡检摘要

巡检入口是 `scripts/process_digest.py`。用于读取最近邮件，按关键词、截止时间和时间敏感事项生成摘要、待办和推送输出。

```bash
python "<skill_dir>/scripts/process_digest.py" --since-hours 2
python "<skill_dir>/scripts/process_digest.py" --all-accounts --since-hours 2
python "<skill_dir>/scripts/process_digest.py" --since-hours 2 --json
python "<skill_dir>/scripts/process_digest.py" --since-hours 2 --review
```

常用维护命令：

```bash
python "<skill_dir>/scripts/process_digest.py" --add-keyword "材料报送"
python "<skill_dir>/scripts/process_digest.py" --cleanup-days 7 --json
```

跨账号巡检会优先读取主账号，再并发读取其他账号；可用 `--parallel-accounts` 和 `--account-timeout` 调整并发数与等待时间。重复处理缓存保存在 `.temp/processed_message_ids.json`。

## 安全边界

- 默认不发送邮件，只生成草稿。
- `mail.py send` 必须显式 `--confirm`。
- `mail.py move` 必须显式 `--confirm`。
- `forward --send` 视为用户显式直接发送。
- 暂不提供删除邮件命令。
- 草稿记录来源账号时，不允许用其他账号发送。
- 不保存或展示客户端值；本地配置文件不应进入发布包。

## 按需读取的参考文档

- 配置和初始化：[config-guide.md](references/config-guide.md)、[first-run-guide.md](references/first-run-guide.md)
- 定时巡检：[schedule-guide.md](references/schedule-guide.md)
- 关键词：[keyword-guide.md](references/keyword-guide.md)
- 截止时间识别：[deadline-detection-guide.md](references/deadline-detection-guide.md)
- 通道回推：[channel-routing-guide.md](references/channel-routing-guide.md)
- 输出结构：[output-format-guide.md](references/output-format-guide.md)
- 故障处理：[troubleshooting-guide.md](references/troubleshooting-guide.md)
