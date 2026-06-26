# GoToEmail — 邮箱提供商参考

## 授权码 / App 密码获取指南

### 163邮箱（网易）
1. 登录 [mail.163.com](https://mail.163.com)
2. 右上角「设置」→「POP3/SMTP/IMAP」
3. 开启「IMAP/SMTP 服务」
4. 点击「新增授权码」→ 手机验证 → 复制授权码  
   ⚠️ 授权码**只显示一次**，立即保存；可随时生成新的或撤销旧的

### 126邮箱 / yeah.net
与 163邮箱流程相同，登录对应网站后进入「设置 → POP3/SMTP/IMAP」。

### QQ邮箱
1. 登录 [mail.qq.com](https://mail.qq.com)
2. 「设置」→「账户」标签
3. 找到「IMAP/SMTP 服务」→「开启」
4. 按提示发送短信验证 → 生成授权码  
   ⚠️ 授权码非QQ密码，可单独管理

### Gmail（谷歌）
> 需先开启两步验证

1. 前往 [myaccount.google.com](https://myaccount.google.com) → 「安全性」
2. 确认「两步验证」已开启
3. 搜索框输入「应用专用密码」→ 选择"邮件"
4. 生成 **16 位 App 密码**（格式：`xxxx xxxx xxxx xxxx`，输入时去掉空格）

### 雅虎邮箱（Yahoo）
1. 登录 [Yahoo](https://login.yahoo.com) → 右上角头像 →「账户安全」
2. 开启「两步验证」
3. 「管理应用密码」→ 生成新密码

### 企业邮箱（自定义 IMAP）
直接使用邮箱登录密码（部分企业邮箱也支持授权码，以实际设置为准）。  
需填写：
- IMAP 服务器地址 + 端口（默认 993，SSL）
- SMTP 服务器地址 + 端口（默认 465，SSL；或 587，STARTTLS）

---

## 错误处理

| 错误信息 | 原因 | 解决方案 |
|----------|------|----------|
| `535 Authentication failed` | 使用了登录密码而非授权码 | 改用邮箱授权码 / App 密码 |
| `IMAP认证失败: [AUTHENTICATIONFAILED]` | 同上，或授权码已过期 | 重新生成授权码 |
| `IMAP无法连接 imap.xxx.com:993` | 网络问题或 IMAP 未开启 | 检查网络；确认在邮箱设置中已开启 IMAP |
| `CERTIFICATE_VERIFY_FAILED` | SSL 证书验证失败 | 企业邮箱可尝试端口 143（IMAP）或 587（SMTP + STARTTLS） |
| `Invalid credentials` | 授权码输入错误或已撤销 | 重新生成授权码并确认复制完整 |
| `Login failed` | Gmail 未开启 App 密码 | 确认 Google 账户已开启两步验证，再生成 App 密码 |
| `Too many connections` | 并发连接超限（163/QQ 有限制） | 稍后重试；避免同时多个会话连接 |
| `SMTP认证失败` | SMTP 授权码与 IMAP 不同 | 163/QQ 的 IMAP 与 SMTP 共用同一授权码 |

---

## 已验证服务器配置

```json
{
  "163":   { "imap": "imap.163.com:993",           "smtp": "smtp.163.com:465"          },
  "126":   { "imap": "imap.126.com:993",           "smtp": "smtp.126.com:465"          },
  "yeah":  { "imap": "imap.yeah.net:993",          "smtp": "smtp.yeah.net:465"         },
  "qq":    { "imap": "imap.qq.com:993",            "smtp": "smtp.qq.com:465"           },
  "gmail": { "imap": "imap.gmail.com:993",         "smtp": "smtp.gmail.com:465"        },
  "yahoo": { "imap": "imap.mail.yahoo.com:993",    "smtp": "smtp.mail.yahoo.com:465"   }
}
```

所有连接均使用 **SSL/TLS**，端口 993（IMAP）/ 465（SMTP）。
