---
name: gmail
description: "[暂不可用] Gmail 邮件集成。收发邮件、搜索邮件、管理标签。通过 MorphixAI 代理安全访问 Gmail API。"
metadata:
  openclaw:
    emoji: "📬"
    requires:
      env: [MORPHIXAI_API_KEY]
---

# Gmail 邮件（暂不可用）

> **状态：暂不可用** — Gmail 账号尚未链接，该工具暂时不可使用。如需启用，请通过 `mx_link` 工具链接 Gmail 账号（app: `gmail`）。

通过 `mx_gmail` 工具管理 Gmail 邮箱：读取、搜索、发送邮件，管理标签。

## 前置条件

1. **安装插件**: `openclaw plugins install openclaw-morphixai`
2. **获取 API Key**: 访问 [morphix.app/api-keys](https://morphix.app/api-keys) 生成 `mk_xxxxxx` 密钥
3. **配置环境变量**: `export MORPHIXAI_API_KEY="mk_your_key_here"`
4. **链接账号**: 访问 [morphix.app/connections](https://morphix.app/connections) 链接 Gmail 账号，或通过 `mx_link` 工具链接（app: `gmail`）

## 核心操作

### 查看用户信息

```
mx_gmail:
  action: get_profile
```

### 列出邮件

```
mx_gmail:
  action: list_messages
  max_results: 10
```

> `list_messages` 只返回邮件 ID 列表，需用 `get_message` 获取完整内容。

### 查看邮件详情

```
mx_gmail:
  action: get_message
  message_id: "18dxxxxxxxx"
```

### 搜索邮件

```
mx_gmail:
  action: search_messages
  query: "from:boss@company.com subject:周报"
  max_results: 5
```

> Gmail 搜索语法支持：
> - `from:` / `to:` — 发件人/收件人
> - `subject:` — 主题
> - `is:unread` / `is:starred` — 未读/星标
> - `newer_than:7d` / `older_than:30d` — 时间范围
> - `has:attachment` — 有附件
> - `label:` — 标签

### 发送邮件

```
mx_gmail:
  action: send_mail
  to: "colleague@company.com"
  subject: "项目更新"
  body: "Hi，项目进展如下：\n1. 完成了 API 开发\n2. 正在编写测试"
  cc: "manager@company.com"
```

### 列出标签

```
mx_gmail:
  action: list_labels
```

### 标记已读

```
mx_gmail:
  action: mark_as_read
  message_id: "18dxxxxxxxx"
```

### 删除邮件（移入回收站）

```
mx_gmail:
  action: trash_message
  message_id: "18dxxxxxxxx"
```

## 常见工作流

### 查看未读邮件

```
1. mx_gmail: list_messages, q: "is:unread", max_results: 5
2. mx_gmail: get_message, message_id: "xxx"  → 逐条查看
3. mx_gmail: mark_as_read, message_id: "xxx"  → 标记已读
```

### 搜索并回复（通过发送新邮件）

```
1. mx_gmail: search_messages, query: "from:client@example.com"
2. mx_gmail: get_message → 查看内容
3. mx_gmail: send_mail, to: "client@example.com", subject: "Re: xxx"
```

## 注意事项

- `list_messages` 返回的是邮件 ID 列表，需用 `get_message` 获取完整内容
- 发送邮件内容为纯文本格式
- Gmail 搜索语法功能强大，建议充分利用
- `account_id` 参数通常省略，工具自动检测已链接的 Gmail 账号
