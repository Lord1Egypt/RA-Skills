# Mail-126 数据字段参考

## 配置文件 (config.json)

路径: `~/mail126_data/config.json`

```json
{
  "email": "user@126.com",
  "auth_code": "BASE64_ENCODED_AUTH_CODE",
  "imap_server": "imap.126.com",
  "imap_port": 993,
  "smtp_server": "smtp.126.com",
  "smtp_port": 465,
  "created_at": "2026-04-11T16:00:00"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| email | string | 邮箱地址 |
| auth_code | string | Base64 编码的授权码 |
| imap_server | string | IMAP 服务器地址 |
| imap_port | int | IMAP 端口 |
| smtp_server | string | SMTP 服务器地址 |
| smtp_port | int | SMTP 端口 |
| created_at | string | 配置创建时间 (ISO 8601) |

---

## 邮件摘要 (inbox list)

```json
{
  "status": "success",
  "data": {
    "folder": "INBOX",
    "total": 128,
    "emails": [
      {
        "uid": 12345,
        "from": "张三 <zhangsan@example.com>",
        "to": "user@126.com",
        "subject": "会议通知",
        "date": "2026-04-11 14:30:00",
        "flags": ["seen"],
        "size": 10240
      }
    ]
  },
  "message": "列出 10 封邮件（共 128 封）"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| folder | string | 当前文件夹名 |
| total | int | 文件夹邮件总数 |
| emails | array | 邮件列表 |
| emails[].uid | int | 邮件唯一标识 |
| emails[].from | string | 发件人（含名称和地址） |
| emails[].to | string | 收件人 |
| emails[].subject | string | 邮件主题 |
| emails[].date | string | 日期时间 |
| emails[].flags | array | 标记列表：seen(已读), flagged(星标), answered(已回复) |
| emails[].size | int | 邮件大小（字节） |

---

## 邮件详情 (inbox read)

```json
{
  "status": "success",
  "data": {
    "uid": 12345,
    "from": "张三 <zhangsan@example.com>",
    "to": ["user@126.com"],
    "cc": ["other@example.com"],
    "subject": "会议通知",
    "date": "2026-04-11 14:30:00",
    "body_text": "明天下午3点开会...",
    "body_html": "<html>...</html>",
    "attachments": [
      {
        "filename": "会议议程.pdf",
        "content_type": "application/pdf",
        "size": 204800
      }
    ]
  },
  "message": "读取邮件 UID 12345"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| body_text | string | 纯文本正文（优先提取） |
| body_html | string | HTML 正文（如有） |
| attachments | array | 附件列表 |
| attachments[].filename | string | 附件文件名 |
| attachments[].content_type | string | MIME 类型 |
| attachments[].size | int | 附件大小（字节） |

---

## 搜索结果 (inbox search)

与 `inbox list` 格式相同，增加搜索条件字段：

```json
{
  "status": "success",
  "data": {
    "query": {
      "from": null,
      "subject": "会议",
      "since": "2026-04-01",
      "until": null
    },
    "total": 5,
    "emails": [ ... ]
  },
  "message": "找到 5 封匹配邮件"
}
```

---

## 发送结果 (send / reply / forward)

```json
{
  "status": "success",
  "data": {
    "to": ["recipient@example.com"],
    "cc": [],
    "subject": "测试邮件",
    "size": 512,
    "attachments_count": 0
  },
  "message": "邮件发送成功"
}
```

---

## 管理操作结果 (manage)

```json
{
  "status": "success",
  "data": {
    "uid": 12345,
    "action": "mark",
    "flag": "read"
  },
  "message": "邮件已标记为已读"
}
```

---

## 统计结果 (stats)

### today / range

```json
{
  "status": "success",
  "data": {
    "period": "2026-04-11",
    "total": 15,
    "unread": 8,
    "by_folder": {
      "INBOX": 10,
      "Sent Messages": 3,
      "Junk": 2
    },
    "top_senders": [
      {"sender": "zhangsan@example.com", "count": 5},
      {"sender": "lisi@example.com", "count": 3}
    ]
  },
  "message": "今日共收到 15 封邮件"
}
```

### by-sender

```json
{
  "status": "success",
  "data": {
    "period": "最近30天",
    "senders": [
      {"sender": "张三 <zhangsan@example.com>", "count": 45, "latest": "2026-04-11"},
      {"sender": "李四 <lisi@example.com>", "count": 32, "latest": "2026-04-10"}
    ]
  },
  "message": "Top 10 发件人统计"
}
```

### folders

```json
{
  "status": "success",
  "data": {
    "folders": [
      {"name": "INBOX", "display": "收件箱", "total": 128, "unread": 23},
      {"name": "Sent Messages", "display": "已发送", "total": 56, "unread": 0},
      {"name": "Drafts", "display": "草稿", "total": 3, "unread": 0},
      {"name": "Trash", "display": "已删除", "total": 12, "unread": 0},
      {"name": "Junk", "display": "垃圾邮件", "total": 8, "unread": 8}
    ]
  },
  "message": "共 5 个文件夹"
}
```

---

## 附件下载结果 (inbox download)

```json
{
  "status": "success",
  "data": {
    "uid": 12345,
    "output_dir": "/path/to/save",
    "downloaded": [
      {"filename": "report.pdf", "size": 204800, "path": "/path/to/save/report.pdf"}
    ]
  },
  "message": "下载 1 个附件到 /path/to/save"
}
```
