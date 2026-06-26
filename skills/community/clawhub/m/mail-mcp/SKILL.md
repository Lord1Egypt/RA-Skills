# Mail MCP Skill

帮助用户使用邮件 MCP 服务，自动检查和安装 mail-mcp。

## 触发词

- 发邮件
- 收邮件
- 查邮件
- 邮箱
- email
- mail
- SMTP
- IMAP
- 附件

## 功能

1. **自动安装**: 检查 mail-mcp 是否已安装，未安装则自动从 GitHub 安装
2. **发送邮件**: 支持纯文本、HTML、附件
3. **搜索邮件**: 按 folder、条件搜索邮件
4. **管理文件夹**: 列出、创建、删除、重命名文件夹
5. **邮件操作**: 标记已读/未读、星标、移动、复制、删除

## 安装检查

### 方式一：pip 安装（推荐）

```bash
pip install git+https://github.com/AdJIa/mail-mcp-server.git
```

### 方式二：本地安装

```bash
git clone https://github.com/AdJIa/mail-mcp-server.git
cd mail-mcp-server
pip install -e .
```

### 验证安装

```bash
which mail-mcp
# 应输出: /home/xxx/.local/bin/mail-mcp
```

## 配置

### mcporter 配置

在 `~/.mcporter/mcporter.json` 中添加：

```json
{
  "mcpServers": {
    "mail-mcp": {
      "command": "mail-mcp",
      "env": {
        "IMAP_HOST": "your-imap-server.com",
        "IMAP_PORT": "993",
        "EMAIL_USER": "your-email@example.com",
        "EMAIL_PASSWORD": "your-password",
        "IMAP_SSL": "true",
        "SMTP_HOST": "your-smtp-server.com",
        "SMTP_PORT": "465",
        "SMTP_SSL": "true"
      }
    }
  }
}
```

### 环境变量说明

| 变量 | 说明 | 示例 |
|------|------|------|
| `IMAP_HOST` | IMAP 服务器地址 | `mail.qiye.aliyun.com` |
| `IMAP_PORT` | IMAP 端口 | `993` |
| `EMAIL_USER` | 邮箱账号 | `user@example.com` |
| `EMAIL_PASSWORD` | 邮箱密码 | `password` |
| `IMAP_SSL` | 启用 SSL | `true` |
| `SMTP_HOST` | SMTP 服务器地址 | `smtp.qiye.aliyun.com` |
| `SMTP_PORT` | SMTP 端口 | `465` |
| `SMTP_SSL` | 启用 SSL | `true` |
| `SMTP_STARTTLS` | 启用 STARTTLS (端口 587) | `false` |

### 常见邮箱配置

| 邮箱 | IMAP | SMTP | 备注 |
|------|------|------|------|
| Gmail | `imap.gmail.com:993` | `smtp.gmail.com:465` | 需要 App Password |
| 阿里云企业邮箱 | `mail.qiye.aliyun.com:993` | `smtp.qiye.aliyun.com:465` | |
| 腾讯企业邮箱 | `imap.exmail.qq.com:993` | `smtp.exmail.qq.com:465` | |
| QQ邮箱 | `imap.qq.com:993` | `smtp.qq.com:465` | 需要授权码 |
| Outlook | `outlook.office365.com:993` | `smtp.office365.com:587` | STARTTLS |

## 使用示例

### mcporter 调用

```bash
# 列出文件夹
mcporter call mail-mcp.list_folders

# 搜索邮件
mcporter call mail-mcp.search_emails --args '{"folder": "INBOX", "limit": 10}'

# 发送邮件
mcporter call mail-mcp.send_email --args '{
  "to": ["recipient@example.com"],
  "subject": "测试邮件",
  "body_text": "这是邮件内容"
}'

# 发送带附件的邮件
mcporter call mail-mcp.send_email --args '{
  "to": ["recipient@example.com"],
  "subject": "带附件的邮件",
  "body_text": "请查收附件",
  "attachments": [{
    "filename": "report.pdf",
    "content_type": "application/pdf",
    "data_base64": "JVBERi0xLjQK..."
  }]
}'
```

### 发送附件示例

```python
import base64

# 读取文件并编码
with open("report.pdf", "rb") as f:
    data_base64 = base64.b64encode(f.read()).decode()

# 使用 data_base64 作为 attachments[].data_base64
```

## MCP 工具列表

| 工具 | 功能 |
|------|------|
| `list_folders` | 列出所有文件夹 |
| `create_folder` | 创建文件夹 |
| `delete_folder` | 删除文件夹 |
| `rename_folder` | 重命名文件夹 |
| `search_emails` | 搜索邮件 |
| `get_email` | 获取邮件详情 |
| `mark_read` | 标记已读 |
| `mark_unread` | 标记未读 |
| `mark_flagged` | 添加星标 |
| `unmark_flagged` | 移除星标 |
| `move_email` | 移动邮件 |
| `copy_email` | 复制邮件 |
| `delete_email` | 删除邮件 |
| `get_current_date` | 获取当前时间 |
| `send_email` | 发送邮件 |
| `send_reply` | 回复邮件 |
| `send_forward` | 转发邮件 |

## 错误处理

所有工具返回结构化响应，错误格式：

```json
{
  "error": "错误描述"
}
```

## 注意事项

1. Gmail 需要使用 [App Password](https://support.google.com/accounts/answer/185833)
2. QQ邮箱需要在设置中开启 IMAP/SMTP 并获取授权码
3. 附件通过 base64 编码传输
4. 建议使用 SSL 加密连接

## 项目地址

https://github.com/AdJIa/mail-mcp-server