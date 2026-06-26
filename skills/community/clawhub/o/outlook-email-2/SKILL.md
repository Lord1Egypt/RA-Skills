---
name: outlook-email
description: Microsoft Outlook 邮件集成。收发邮件、搜索邮件、管理邮件文件夹。通过 MorphixAI 代理安全访问 Microsoft Graph API。
metadata:
  openclaw:
    emoji: "📧"
    requires:
      env: [MORPHIXAI_API_KEY]
---

# Outlook 邮件

通过 `mx_outlook` 工具管理 Microsoft Outlook 邮箱：读取、搜索、发送和回复邮件。

## 前置条件

1. **安装插件**: `openclaw plugins install openclaw-morphixai`
2. **获取 API Key**: 访问 [morphix.app/api-keys](https://morphix.app/api-keys) 生成 `mk_xxxxxx` 密钥
3. **配置环境变量**: `export MORPHIXAI_API_KEY="mk_your_key_here"`
4. **链接账号**: 访问 [morphix.app/connections](https://morphix.app/connections) 链接 Outlook 账号，或通过 `mx_link` 工具链接（app: `microsoft_outlook`）

## 核心操作

### 查看当前用户

```
mx_outlook:
  action: get_me
```

### 列出邮件

```
mx_outlook:
  action: list_messages
  top: 10
```

**指定文件夹：**
```
mx_outlook:
  action: list_messages
  folder_id: "sentitems"
  top: 5
```

### 查看邮件详情

```
mx_outlook:
  action: get_message
  message_id: "AAMkADxx..."
```

### 搜索邮件

```
mx_outlook:
  action: search_messages
  query: "发票"
  top: 5
```

### 发送邮件

```
mx_outlook:
  action: send_mail
  subject: "项目周报"
  body: "本周完成了以下工作：\n1. 完成用户模块\n2. 修复了 3 个 bug"
  to: ["colleague@company.com"]
  cc: ["manager@company.com"]
```

**发送 HTML 邮件：**
```
mx_outlook:
  action: send_mail
  subject: "项目进度更新"
  body: "<h2>项目进度</h2><p>本周进展顺利</p>"
  body_type: "HTML"
  to: ["team@company.com"]
```

### 回复邮件

```
mx_outlook:
  action: reply_to_message
  message_id: "AAMkADxx..."
  comment: "收到，我会尽快处理。"
```

### 列出邮件文件夹

```
mx_outlook:
  action: list_folders
```

## 常见工作流

### 查看未读邮件并回复

```
1. mx_outlook: list_messages, top: 10
     → 检查未读邮件（isRead: false）
2. mx_outlook: get_message, message_id: "xxx"
     → 查看具体内容
3. mx_outlook: reply_to_message, message_id: "xxx", comment: "回复内容"
```

### 搜索特定邮件

```
1. mx_outlook: search_messages, query: "from:boss@company.com 本周"
```

## 注意事项

- `folder_id` 支持内置名称：`inbox`、`drafts`、`sentitems`、`deleteditems`、`archive`
- 搜索使用 Microsoft Graph `$search` 语法
- `body_type` 默认为 `"Text"`，如需 HTML 格式需显式指定 `"HTML"`
- `account_id` 参数通常省略，工具自动检测已链接的 Outlook 账号
