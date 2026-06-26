# one-mail - 统一邮箱管理工具

[English](./README.en.md) | 中文

一个命令行工具，用于统一管理多个邮箱账户（Gmail、Outlook、网易邮箱 163/126）。

## 安装

### 方式 1：通过 ClawHub 安装（推荐）

```bash
# 安装
clawhub install one-mail

# 初始化配置
bash scripts/setup.sh
```

### 方式 2：手动安装

```bash
# 克隆仓库
git clone https://github.com/huangbaixun/one-mail.git
cd one-mail

# 初始化配置
bash scripts/setup.sh
```

## 快速开始

### 1. 初始化配置

```bash
bash scripts/setup.sh
```

按照提示添加你的邮箱账户。

### 2. 收取邮件

```bash
# 收取所有账户的邮件
bash scripts/fetch.sh

# 只看未读邮件
bash scripts/fetch.sh --unread

# 搜索邮件
bash scripts/fetch.sh --query "AI agent"

# 指定账户
bash scripts/fetch.sh --account gmail
```

### 3. 发送邮件

```bash
# 使用默认账户发送
bash scripts/send.sh \
  --to "recipient@example.com" \
  --subject "Hello" \
  --body "Email content"

# 带附件
bash scripts/send.sh \
  --to "recipient@example.com" \
  --subject "Report" \
  --body "See attachment" \
  --attach "/path/to/file.pdf"
```

## 支持的邮箱

### Gmail
- ✅ 收取邮件
- ✅ 发送邮件
- ✅ 附件支持
- ✅ 搜索过滤
- 依赖：`gog` CLI（已配置）

### Outlook
- ✅ 收取邮件
- ✅ 发送邮件
- ✅ 附件支持（< 3MB）
- ✅ 搜索过滤
- 依赖：Microsoft Graph API

### 网易邮箱 (163.com / 126.com)
- ✅ 收取邮件
- ✅ 发送邮件
- ✅ 附件支持
- ✅ 搜索过滤
- ✅ IMAP ID 支持（自动发送客户端标识）
- 依赖：Python 3 + imaplib
- 163 服务器：imap.163.com / smtp.163.com
- 126 服务器：imap.126.com / smtp.126.com

## 配置文件

配置文件位于 `~/.onemail/`：

- `config.json` - 账户配置
- `credentials.json` - 敏感凭证（600 权限）

## 账户管理

```bash
# 列出所有账户
bash scripts/accounts.sh list

# 添加新账户
bash scripts/accounts.sh add

# 删除账户
bash scripts/accounts.sh remove --name outlook

# 设置默认账户
bash scripts/accounts.sh set-default --name gmail

# 测试账户连接
bash scripts/accounts.sh test --name gmail
```

## 高级用法

### 定时检查邮件

添加到 crontab：

```bash
# 每小时检查一次未读邮件
0 * * * * cd ~/clawd/skills/one-mail && bash scripts/fetch.sh --unread | jq -r '.[] | "\(.from): \(.subject)"'
```

### 自动回复

```bash
# 回复最新的紧急邮件
cd ~/clawd/skills/one-mail
bash scripts/fetch.sh --query "urgent" --limit 1 | \
  jq -r '.[0].id' | \
  xargs -I {} bash scripts/send.sh \
    --reply-to {} \
    --body "I'll get back to you soon"
```

### 跨账户搜索

```bash
# 搜索所有账户中包含 "invoice" 的邮件
cd ~/clawd/skills/one-mail
bash scripts/fetch.sh --query "invoice" | \
  jq -r '.[] | "\(.account) - \(.from): \(.subject)"'
```

## 输出格式

所有邮件以 JSON 格式输出：

```json
[
  {
    "id": "msg_123",
    "account": "gmail",
    "from": "sender@example.com",
    "to": "you@gmail.com",
    "subject": "Meeting tomorrow",
    "date": "2026-03-07T10:30:00Z",
    "unread": true,
    "has_attachments": false,
    "snippet": "Let's meet at 3pm..."
  }
]
```

可以使用 `jq` 进行过滤和格式化。

## 安全性

- 所有凭证存储在 `~/.onemail/credentials.json`（600 权限）
- 支持 macOS Keychain 存储（可选）
- OAuth 2.0 认证（Gmail、Outlook）
- 应用专用密码（网易邮箱）

## 故障排除

### Gmail 连接失败

确保 `gog` CLI 已正确配置：

```bash
gog gmail list --limit 1
```

### Outlook 授权失败

1. 检查 Client ID 和 Client Secret
2. 确保重定向 URI 设置为 `http://localhost`
3. 确保授权范围包含 `Mail.ReadWrite` 和 `Mail.Send`

### 网易邮箱连接失败

1. 确保已开启 IMAP/SMTP 服务
2. 使用应用专用密码，不是登录密码
3. 检查防火墙是否阻止 993/465 端口
4. **IMAP ID 问题**：one-mail 已自动发送 IMAP ID 命令，符合网易邮箱要求
5. 163 使用 imap.163.com / smtp.163.com
6. 126 使用 imap.126.com / smtp.126.com

**测试网易邮箱连接**：
```bash
python3 scripts/test-163-imap.py your@163.com your_app_password
```

## 依赖

- `bash` 4.0+
- `jq` - JSON 处理
- `curl` - HTTP 请求
- `openssl` - SSL/TLS 连接
- `python3` - IMAP/SMTP 处理（网易邮箱）
- `gog` - Gmail 操作（可选）

## 限制

- Outlook 附件大小限制：< 3MB（直接附加），大文件请使用 OneDrive 分享
- 不支持 Exchange Server（仅 Outlook.com）
- 网易邮箱连接测试待实现
- 不支持 HTML 邮件编辑（仅纯文本）

## 更新日志

- 2026-03-07: 初始版本
  - 支持 Gmail、Outlook、网易邮箱
  - 统一收发接口
  - 账户管理功能
  - JSON 输出格式

## 许可证

MIT License - see [LICENSE](LICENSE)

## 作者

Huang Baixun ([@huangbaixun](https://github.com/huangbaixun))
