---
name: gotoemail
version: 1.0.1
emoji: "📧"
homepage: https://github.com/feixuelingcloud/gotoemail
description: 绑定邮箱账户并管理邮件。支持 163/126/QQ/雅虎邮箱（IMAP/SMTP+授权码）、Gmail（IMAP+App密码）、企业邮箱（自定义IMAP/SMTP服务器，端口可配）。不支持需要 OAuth 的邮箱（Outlook/M365/iCloud）。触发词：绑定邮箱、添加邮箱、配置邮箱、读邮件、查收邮件、发邮件、bind email、setup email、connect mailbox。
metadata:
  openclaw:
    requires:
      bins: [python]
---

# GoToEmail

## 绑定流程

### 第一步：确认邮箱类型

```
⚡ 推荐（授权码方式）
  1. 163邮箱 / 126邮箱 / yeah.net
  2. QQ邮箱 / Foxmail

其他方式
  3. Gmail              — App 密码
  4. 雅虎邮箱 (Yahoo)   — App 密码
  5. 企业邮箱           — 自定义 IMAP/SMTP

❌ 不支持：Outlook / M365 / iCloud（OAuth 类，请在宿主应用中配置）
```

### 第二步：引导获取授权码

授权码/App密码获取步骤见 `references/providers.md` 的「授权码获取指南」节。

### 第三步：收集凭据

- **163 / QQ / Yahoo / Gmail**：邮箱地址 + 授权码/App密码  
- **企业邮箱**：额外收集 IMAP服务器、IMAP端口（默认993）、SMTP服务器、SMTP端口（默认465）

### 第四步：测试连接

通过 stdin 传入 JSON 运行脚本：

```bash
echo '{"email":"user@163.com","password":"授权码"}' | python scripts/test_connection.py
```

企业邮箱需额外传入自定义服务器：

```bash
echo '{"email":"user@corp.com","password":"pass","imap_host":"imap.corp.com","smtp_host":"smtp.corp.com"}' | python scripts/test_connection.py
```

- 返回 `{"ok":true,...}` → 绑定成功，告知用户并保存配置  
- 返回 `{"ok":false,"error":"..."}` → 根据错误信息排查（见 `references/providers.md` 错误处理节）

---

## 邮件操作

### 获取邮件列表

```bash
echo '{"email":"...","password":"...","imap_host":"imap.163.com","imap_port":993,"folder":"INBOX","limit":20,"unread_only":false}' | python scripts/list_emails.py
```

返回字段：`uid`、`subject`、`from`、`date`、`unread`

### 读取单封邮件

```bash
echo '{"email":"...","password":"...","imap_host":"imap.163.com","uid":"1234","mark_as_read":true}' | python scripts/read_email.py
```

返回字段：`subject`、`from`、`to`、`date`、`body`（纯文本）、`attachments`

### 发送邮件

```bash
echo '{"email":"...","password":"...","smtp_host":"smtp.163.com","smtp_port":465,"to":"收件人@example.com","subject":"主题","body":"正文内容"}' | python scripts/send_email.py
```

`to` 接受字符串或列表；可选字段：`cc`、`bcc`、`html_body`

---

## 服务器快速参考

| 提供商 | IMAP 服务器:端口 | SMTP 服务器:端口 |
|--------|----------------|----------------|
| 163邮箱 | imap.163.com:993 | smtp.163.com:465 |
| 126邮箱 | imap.126.com:993 | smtp.126.com:465 |
| QQ邮箱  | imap.qq.com:993  | smtp.qq.com:465  |
| Gmail  | imap.gmail.com:993 | smtp.gmail.com:465 |
| 雅虎   | imap.mail.yahoo.com:993 | smtp.mail.yahoo.com:465 |

企业邮箱：用户自定义，全程 SSL/TLS。

👉 完整授权码获取步骤与错误排查见 `references/providers.md`
