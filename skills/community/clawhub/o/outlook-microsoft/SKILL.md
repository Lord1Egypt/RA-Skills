---
name: outlook-microsoft
description: "微软 Outlook 邮箱和日历管理工具（支持世纪互联版 Office 365）。当用户要求查看邮件、发送邮件、搜索邮件、管理日历日程、创建会议、查询忙闲状态时使用。注意：此 Skill 仅支持世纪互联（21Vianet）版本的 Microsoft 365，使用 login.chinacloudapi.cn / microsoftgraph.chinacloudapi.cn 端点。"
metadata:
  openclaw:
    emoji: "📮"
    requires:
      bins: ["python3"]
      env: ["OUTLOOK_CLIENT_ID", "OUTLOOK_TENANT_ID"]
    primaryEnv: "OUTLOOK_CLIENT_ID"
---

# Microsoft Outlook（日历 + 邮件）

微软世纪互联版 Outlook（日历 + 邮件）管理工具，通过 Microsoft Graph API 实现。

## 功能概览

| 功能 | 操作 |
|------|------|
| **邮件读取** | 读取收件箱、搜索邮件、按发件人筛选 |
| **邮件管理** | 标记已读/未读、删除、归档、移动 |
| **邮件发送** | 发送新邮件、回复邮件 |
| **日历查看** | 查看今日/本周日程、获取事件详情 |
| **日历创建** | 创建日程/会议、查询忙闲状态 |

## 前置要求

详见 [references/setup.md](references/setup.md)，需要：
1. 在 Azure 世纪互联门户注册应用
2. 配置 API 权限（Mail.ReadWrite、Mail.Send、Calendars.ReadWrite）
3. 获取 Client ID + Client Secret + Tenant ID
4. 完成 OAuth 授权

## 环境变量配置

```bash
# 必填
OUTLOOK_CLIENT_ID="your-azure-app-client-id"
OUTLOOK_TENANT_ID="your-tenant-id"

# 自动从 Client ID 推断，可选
OUTLOOK_CLIENT_SECRET="your-client-secret"
```

## 工具脚本

所有脚本均接受 JSON 参数，通过 stdin 传入：

### 邮件操作

```bash
# 读取收件箱（最新 N 封）
python3 skills/outlook-microsoft/scripts/outlook_mail.py inbox '{"count": 10}'

# 搜索邮件
python3 skills/outlook-microsoft/scripts/outlook_mail.py search '{"query": "关键词"}'

# 按发件人筛选
python3 skills/outlook-microsoft/scripts/outlook_mail.py from '{"sender": "xxx@company.com", "count": 10}'

# 读取单封邮件详情
python3 skills/outlook-microsoft/scripts/outlook_mail.py read '{"message_id": "邮件ID"}'

# 标记已读/未读
python3 skills/outlook-microsoft/scripts/outlook_mail.py mark-read '{"message_id": "邮件ID"}'
python3 skills/outlook-microsoft/scripts/outlook_mail.py mark-unread '{"message_id": "邮件ID"}'

# 发送邮件
python3 skills/outlook-microsoft/scripts/outlook_mail.py send '{"to": "收件人", "subject": "标题", "body": "正文"}'

# 回复邮件
python3 skills/outlook-microsoft/scripts/outlook_mail.py reply '{"message_id": "邮件ID", "body": "回复内容"}'

# 删除邮件
python3 skills/outlook-microsoft/scripts/outlook_mail.py delete '{"message_id": "邮件ID"}'

# 获取附件列表
python3 skills/outlook-microsoft/scripts/outlook_mail.py attachments '{"message_id": "邮件ID"}'
```

### 日历操作

```bash
# 查看今日日程
python3 skills/outlook-microsoft/scripts/outlook_calendar.py today

# 查看本周日程
python3 skills/outlook-microsoft/scripts/outlook_calendar.py week

# 查看指定日程详情
python3 skills/outlook-microsoft/scripts/outlook_calendar.py read '{"event_id": "事件ID"}'

# 创建日程（单次）
python3 skills/outlook-microsoft/scripts/outlook_calendar.py create '{
  "subject": "会议标题",
  "start": "2026-04-03T10:00:00",
  "end": "2026-04-03T11:00:00",
  "location": "会议室",
  "body": "会议描述"
}'

# 快速创建（1小时日程）
python3 skills/outlook-microsoft/scripts/outlook_calendar.py quick '{"subject": "快速会议", "start": "2026-04-03T14:00"}'

# 删除日程
python3 skills/outlook-microsoft/scripts/outlook_calendar.py delete '{"event_id": "事件ID"}'

# 查询忙闲
python3 skills/outlook-microsoft/scripts/outlook_calendar.py freebusy '{"start": "2026-04-03T09:00", "end": "2026-04-03T18:00"}'

# 查看所有日历
python3 skills/outlook-microsoft/scripts/outlook_calendar.py calendars
```

### 授权操作

```bash
# 首次使用：获取设备码并完成授权
python3 skills/outlook-microsoft/scripts/outlook_auth.py authorize

# 测试连接是否正常
python3 skills/outlook-microsoft/scripts/outlook_auth.py test

# 查看当前 Token 状态
python3 skills/outlook-microsoft/scripts/outlook_auth.py status

# 手动刷新 Token
python3 skills/outlook-microsoft/scripts/outlook_auth.py refresh
```

## 日期时间格式

- 所有日期时间使用 ISO 8601 格式：`YYYY-MM-DDTHH:MM:SS`
- 示例：`2026-04-03T10:00:00` 表示 2026年4月3日上午10:00
- 时区：自动使用中国标准时间（CST, UTC+8）

## 错误处理

常见错误码：
- `AUTH_001`：未授权，需要先运行 `authorize` 完成 OAuth 授权
- `AUTH_002`：Token 过期，运行 `refresh` 刷新
- `AUTH_003`：权限不足，检查 Azure App 的 API 权限配置
- `API_001`：网络错误，检查网络连接
- `API_002`：Graph API 调用失败，检查 Client ID / Tenant ID 配置

## 相关文件

- 配置文件：`~/.outlook-microsoft/`
  - `config.json` - Client ID、Secret、Tenant ID
  - `credentials.json` - OAuth Token（自动管理）
- 安装指南：[references/setup.md](references/setup.md)
