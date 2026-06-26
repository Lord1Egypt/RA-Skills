---
name: outlook-calendar
description: Microsoft Outlook 日历集成。管理日历和事件，创建/更新/删除事件，按日期范围查看日程。通过 MorphixAI 代理安全访问 Microsoft Graph API。
metadata:
  openclaw:
    emoji: "📅"
    requires:
      env: [MORPHIXAI_API_KEY]
---

# Microsoft Outlook Calendar

通过 `mx_outlook_calendar` 工具管理 Outlook 日历：查看日历列表、事件 CRUD、日期范围查询。

## 前置条件

1. **安装插件**: `openclaw plugins install openclaw-morphixai`
2. **获取 API Key**: 访问 [morphix.app/api-keys](https://morphix.app/api-keys) 生成 `mk_xxxxxx` 密钥
3. **配置环境变量**: `export MORPHIXAI_API_KEY="mk_your_key_here"`
4. **链接账号**: 访问 [morphix.app/connections](https://morphix.app/connections) 链接 Outlook Calendar 账号，或通过 `mx_link` 工具链接（app: `microsoft_outlook_calendar`）

## 核心操作

### 查看用户信息

```
mx_outlook_calendar:
  action: get_me
```

### 列出日历

```
mx_outlook_calendar:
  action: list_calendars
```

### 列出事件

```
mx_outlook_calendar:
  action: list_events
  top: 10
  order_by: "start/dateTime desc"
```

### 按日期范围查看日程

```
mx_outlook_calendar:
  action: get_calendar_view
  start_date_time: "2026-03-01T00:00:00Z"
  end_date_time: "2026-03-31T23:59:59Z"
  top: 50
```

### 获取事件详情

```
mx_outlook_calendar:
  action: get_event
  event_id: "AAMkADxx..."
```

### 创建事件

```
mx_outlook_calendar:
  action: create_event
  subject: "项目评审会"
  start: "2026-03-01T14:00:00"
  end: "2026-03-01T15:30:00"
  time_zone: "Asia/Shanghai"
  body: "讨论 Q1 项目进展和 Q2 计划"
  location: "会议室 A"
  attendees:
    - email: "colleague@company.com"
      name: "张三"
      type: "required"
    - email: "manager@company.com"
      type: "optional"
```

### 更新事件

```
mx_outlook_calendar:
  action: update_event
  event_id: "AAMkADxx..."
  subject: "更新后的会议标题"
  start: "2026-03-01T15:00:00"
  end: "2026-03-01T16:00:00"
  time_zone: "Asia/Shanghai"
```

### 删除事件

```
mx_outlook_calendar:
  action: delete_event
  event_id: "AAMkADxx..."
```

## 常见工作流

### 查看今日日程

```
1. mx_outlook_calendar: get_calendar_view,
   start_date_time: "2026-02-25T00:00:00Z",
   end_date_time: "2026-02-25T23:59:59Z"
```

### 安排会议

```
1. mx_outlook_calendar: get_calendar_view → 查看空闲时间
2. mx_outlook_calendar: create_event → 创建会议，自动发送邀请
```

### 每周回顾

```
1. mx_outlook_calendar: get_calendar_view,
   start_date_time: "本周一", end_date_time: "本周日"
2. 汇总会议数量和时间分布
```

## 注意事项

- 日期时间格式为 ISO 8601（如 `2026-03-01T10:00:00`）
- `time_zone` 使用 IANA 时区名（如 `Asia/Shanghai`、`America/New_York`），默认 `UTC`
- `get_calendar_view` 按实际发生时间返回事件（展开重复事件）
- `list_events` 返回原始事件定义（不展开重复事件）
- 创建带参会者的事件会自动发送会议邀请邮件
- `calendar_id` 通常省略，使用默认日历
- `account_id` 参数通常省略，工具自动检测已链接的 Outlook Calendar 账号
