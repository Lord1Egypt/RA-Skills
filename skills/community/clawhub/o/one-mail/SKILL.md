---
name: one-mail
description: 统一邮箱管理 CLI，支持 Gmail、Outlook、网易邮箱（163.com、126.com）。适用于：(1) 收取/发送邮件，(2) 跨账户搜索邮件，(3) 管理多个邮箱账户，(4) 查看邮件统计。当用户提到邮件、邮箱、email、发邮件、收邮件、查邮件时触发。
---

# one-mail

统一管理多个邮箱的 CLI 工具。配置存储在 `~/.onemail/`。

## 初始化

首次使用运行 setup 添加账户：

```bash
bash scripts/setup.sh
```

## 收取邮件

```bash
bash scripts/fetch.sh                          # 所有账户
bash scripts/fetch.sh --unread                  # 仅未读
bash scripts/fetch.sh --account gmail           # 指定账户
bash scripts/fetch.sh --query "AI agent"        # 搜索
bash scripts/fetch.sh --limit 10                # 限制数量
```

## 阅读邮件

```bash
bash scripts/read.sh --id <message_id> --account <name>
bash scripts/read.sh --account outlook --latest
bash scripts/read.sh --account gmail --query "MacBook"
bash scripts/read.sh --json                     # JSON 输出
```

## 发送邮件

```bash
bash scripts/send.sh \
  --to "recipient@example.com" \
  --subject "Hello" \
  --body "Email content"

# 指定账户 + 附件
bash scripts/send.sh \
  --account outlook \
  --to "recipient@example.com" \
  --subject "Report" \
  --body "See attachment" \
  --attach "/path/to/file.pdf"
```

注意：Outlook 附件限制 3MB。

## 账户管理

```bash
bash scripts/accounts.sh list                   # 列出账户
bash scripts/accounts.sh add                    # 添加账户
bash scripts/accounts.sh remove <account_id>    # 删除账户
bash scripts/accounts.sh set-default <id>       # 设置默认
```

## 统计

```bash
bash scripts/stats.sh
```

## 提供商要求

| 提供商 | 认证方式 | 前置条件 |
|--------|----------|----------|
| Gmail | OAuth 2.0 | 需要 `gog` CLI |
| Outlook | OAuth 2.0 (Graph API) | 需要 Mail.ReadWrite + Mail.Send 权限 |
| 网易 163 | IMAP/SMTP | 需要开启 IMAP 并使用应用密码 |
| 网易 126 | IMAP/SMTP | 需要开启 IMAP 并使用应用密码 |

## 依赖

必需：`curl`、`jq`、`python3`。可选：`gog`（Gmail OAuth）。

## 故障排除

遇到认证或连接问题时，参考 [troubleshooting.md](references/troubleshooting.md)。
