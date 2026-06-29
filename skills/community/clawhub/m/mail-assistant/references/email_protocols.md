# 邮箱协议配置参考 (163 / QQ)

## 163 邮箱

| 协议 | 服务器地址 | SSL 端口 | 非 SSL 端口 |
|------|-----------|---------|------------|
| SMTP | smtp.163.com | 465 | 25 |
| IMAP | imap.163.com | 993 | 143 |
| POP3 | pop.163.com | 995 | 110 |

### 认证方式

- **密码类型:** 客户端授权密码（需在网页端开启 SMTP/IMAP 服务并设置授权码）
- 登录账号: 完整邮箱地址（如 `user@163.com`）
- 登录密码: **授权码**，不是邮箱登录密码

### 开启步骤

1. 登录 163 邮箱网页版
2. 设置 → POP3/SMTP/IMAP
3. 勾选开启 IMAP/SMTP 服务
4. 按指引发送短信获取授权码
5. 保存授权码用于配置

### ⚠️ 授权码安全

授权码是邮箱的客户端访问凭证，具备完整的邮件读写发送权限。

- **不要** 将授权码提交到任何版本控制系统（Git）
- **不要** 分享包含授权码的配置文件
- 建议在 accounts/ 目录中添加 `.gitignore` 文件，内容为 `*.json`
- 定期（如每 3 个月）在网页邮箱中重新生成授权码
- 不再使用此 Skill 时，及时在网页邮箱中撤销授权码

### 账户 JSON 配置

```json
{
  "id": "my-163",
  "type": "163",
  "user": "yourname@163.com",
  "smtp": {
    "host": "smtp.163.com",
    "port": 465,
    "auth": "your_authorization_code"
  },
  "imap": {
    "host": "imap.163.com",
    "port": 993,
    "auth": "your_authorization_code"
  }
}
```

## QQ 邮箱

| 协议 | 服务器地址 | SSL 端口 | 非 SSL 端口 |
|------|-----------|---------|------------|
| SMTP | smtp.qq.com | 465 | 25 |
| IMAP | imap.qq.com | 993 | 143 |
| POP3 | pop.qq.com | 995 | 110 |

### 认证方式

- **密码类型:** QQ 邮箱授权码（需在网页端生成）
- 登录账号: 完整邮箱地址（如 `user@qq.com`）
- 登录密码: **授权码**，不是 QQ 密码

### 开启步骤

1. 登录 QQ 邮箱网页版
2. 设置 → 账户 → POP3/IMAP/SMTP 服务
3. 点击"开启"
4. 发送短信验证获取授权码
5. 保存授权码用于配置

### ⚠️ 授权码安全

授权码是邮箱的客户端访问凭证，具备完整的邮件读写发送权限。

- **不要** 将授权码提交到任何版本控制系统（Git）
- **不要** 分享包含授权码的配置文件
- 建议在 accounts/ 目录中添加 `.gitignore` 文件，内容为 `*.json`
- 定期（如每 3 个月）在网页邮箱中重新生成授权码
- 不再使用此 Skill 时，及时在网页邮箱中撤销授权码

### 账户 JSON 配置

```json
{
  "id": "my-qq",
  "type": "qq",
  "user": "yourname@qq.com",
  "smtp": {
    "host": "smtp.qq.com",
    "port": 465,
    "auth": "your_authorization_code"
  },
  "imap": {
    "host": "imap.qq.com",
    "port": 993,
    "auth": "your_authorization_code"
  }
}
```

## 常见问题

### 为什么不能用邮箱密码而要用授权码？

授权码是由邮箱系统专门为客户端登录生成的独立密码，比直接使用邮箱密码更安全：
- 可随时撤销/重新生成
- 不影响网页端登录
- 可以单独控制每个客户端

### IMAP vs POP3

| 特性 | IMAP | POP3 |
|------|------|------|
| 多设备同步 | ✅ 服务器端保存状态 | ❌ 通常下载后删除 |
| 文件夹支持 | ✅ 支持所有文件夹 | ❌ 仅收件箱 |
| 推荐 | ✅ 推荐 | ❌ |

**本 Skill 使用 IMAP。**

### 无法连接排查

1. 确认授权码正确（注意不要包含空格）
2. 确认 SSL 端口正确
3. 确认已在网页端开启 SMTP/IMAP 服务
4. 检查防火墙是否阻止了对应端口
5. 尝试 Telnet 测试连接:
   ```
   openssl s_client -connect smtp.qq.com:465 -crlf
   openssl s_client -connect imap.qq.com:993 -crlf
   ```
