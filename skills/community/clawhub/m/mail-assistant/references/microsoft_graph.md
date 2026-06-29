# Microsoft Graph API 参考

## 认证端点

| 环境 | URL |
|------|-----|
| 设备代码请求 | `POST https://login.microsoftonline.com/{tenant}/oauth2/v2.0/devicecode` |
| 令牌轮询 | `POST https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token` |
| 令牌刷新 | `POST https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token` |

### 请求参数

**设备代码请求:**
- `client_id` — Azure 应用注册 ID
- `scope` — 空格分隔的权限列表，例如 `User.Read Mail.ReadWrite Mail.Send MailboxSettings.Read`

**令牌轮询:**
- `grant_type` — `urn:ietf:params:oauth:grant-type:device_code`
- `client_id` — Azure 应用注册 ID
- `device_code` — 从设备代码响应中获取

**令牌刷新:**
- `grant_type` — `refresh_token`
- `client_id` — Azure 应用注册 ID
- `refresh_token` — 之前获得的 refresh_token
- `scope` — 与之前相同的权限列表

## Graph API 端点 (v1.0)

基础 URL: `https://graph.microsoft.com/v1.0`

### 邮件列表

```
GET /me/messages
  ?$top=20
  &$select=id,subject,from,receivedDateTime,isRead,hasAttachments,importance
  &$orderby=receivedDateTime DESC
  &$filter=isRead eq false
  &$search="keyword"
```

### 读取单封邮件

```
GET /me/messages/{message-id}
  ?$select=id,subject,from,toRecipients,ccRecipients,receivedDateTime,isRead,body,hasAttachments,attachments
```

### 发送邮件

```
POST /me/sendMail
Content-Type: application/json

{
  "message": {
    "subject": "邮件主题",
    "toRecipients": [{"emailAddress": {"address": "user@example.com"}}],
    "ccRecipients": [{"emailAddress": {"address": "cc@example.com"}}],
    "bccRecipients": [{"emailAddress": {"address": "bcc@example.com"}}],
    "body": {
      "contentType": "Text",
      "content": "邮件正文"
    },
    "attachments": [
      {
        "@odata.type": "#microsoft.graph.fileAttachment",
        "name": "file.pdf",
        "contentBytes": "<base64>"
      }
    ]
  },
  "saveToSentItems": true
}
```

### 标记已读/未读

```
PATCH /me/messages/{message-id}
Content-Type: application/json

{ "isRead": true }
```

### 搜索

```
GET /me/messages
  ?$search="keyword"
  &$top=20
  &$select=id,subject,from,receivedDateTime,isRead
```

### 文件夹列表

```
GET /me/mailFolders
  ?$select=id,displayName,unreadItemCount,totalItemCount
```

### 下载附件

```
GET /me/messages/{message-id}/attachments/{attachment-id}/$value
```
返回附件原始内容（二进制）。仅对 fileAttachment 类型有效。

### 常用权限 (scopes)

| 权限 | 说明 |
|------|------|
| `User.Read` | 读取用户基本信息 |
| `Mail.ReadWrite` | 读取和修改邮件 |
| `Mail.Send` | 发送邮件 |
| `MailboxSettings.Read` | 读取邮箱设置 |

## 创建 Azure 应用注册

1. 访问 https://portal.azure.com → Azure Active Directory → 应用注册 → 新注册
2. 名称: `EmailAssistant`
3. 受支持的账户类型: **任何组织目录(任何 Azure AD 目录 - 多租户)和个人 Microsoft 账户**
4. 重定向 URI: 不设置（设备代码流不需要）
5. 注册后，记录 **应用程序(客户端) ID** (client_id)
6. API 权限 → 添加权限 → Microsoft Graph → 委派权限
   - 添加: `User.Read`, `Mail.ReadWrite`, `Mail.Send`, `MailboxSettings.Read`
7. 授予管理员同意（如需要）
8. 不要创建客户端密码（设备代码流不需要）

## 注意事项

- `$search` 参数仅适用于 Exchange Online 邮箱，对个人 Outlook.com 邮箱不完全支持
- 个人 Outlook.com 邮箱可能不支持某些高级筛选
- 每小时有请求限制（约 10000 请求/小时）
- 附件 base64 编码时，总消息大小限制约为 35MB（含附件）
