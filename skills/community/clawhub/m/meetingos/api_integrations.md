# MeetingOS API 集成文档

## 目录
1. Notion 集成配置
2. Linear 集成配置
3. Jira 集成配置
4. 飞书集成配置
5. 企业微信集成配置
6. Slack 集成配置
7. Google Calendar 集成
8. Outlook / Microsoft 365 集成

---

## 1. Notion 集成

### 前置步骤
1. 访问 https://www.notion.so/my-integrations
2. 创建新 Integration，获取 Token
3. 在目标 Database 页面右上角 → 连接 → 选择你的 Integration
4. 复制 Database URL 中的 ID（32位字符串）

### 数据库结构建议
| 字段名 | 类型 | 说明 |
|---|---|---|
| Name | Title | 任务标题 |
| Assignee | Person | 责任人 |
| Due Date | Date | 截止时间 |
| Priority | Select | High/Medium/Low |
| Status | Select | Todo/In Progress/Done |
| Meeting | Relation | 关联会议纪要页面 |

---

## 2. Linear 集成

### 获取 API Key
Settings → API → Personal API Keys → Create Key

### Team ID 获取
```graphql
query { teams { nodes { id name } } }
```

---

## 3. 飞书集成

### 创建企业应用
1. 飞书开放平台 → 创建企业自建应用
2. 权限：task:task:write, im:message:send_as_bot
3. 获取 App ID 和 App Secret

---

## 4. 企业微信集成

### 应用创建
企业微信管理后台 → 应用管理 → 创建应用
获取：Corp ID、Agent ID、Agent Secret
