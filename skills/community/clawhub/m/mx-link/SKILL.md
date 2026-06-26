---
name: office-link
description: 通过 MorphixAI 统一链接和管理第三方账号（GitHub、GitLab、Gmail、Outlook、Jira、Slack 等），并通过代理安全调用第三方 API。
metadata:
  openclaw:
    emoji: "🔗"
    requires:
      env: [MORPHIXAI_API_KEY]
---

# Office Link — 第三方账号链接与 API 代理

通过 `mx_link` 工具，统一管理第三方平台的账号链接和 API 调用。Bot 不直接持有 OAuth token，所有请求通过 MorphixAI 服务端代理，自动管理凭据。

> **重要：优先使用已有的专用 skill。** 对于已有专用 skill 的平台，**必须优先使用对应 skill**（如 `jira-workflow`、`gitlab-workflow`、`outlook-email` 等）而非 `mx_link` 的 `proxy`。专用 skill 自动处理 URL 构建、认证、数据格式转换，更可靠且更简洁。`mx_link` 仅用于：
> 1. **账号管理**（查看/链接账号）
> 2. **调用尚未有专用 skill 的平台 API**（如 Slack、Discord、Zoom、Google Sheets 等）

## 前置条件

1. **安装插件**: `openclaw plugins install openclaw-morphixai`
2. **获取 API Key**: 访问 [morphix.app/api-keys](https://morphix.app/api-keys) 生成 `mk_xxxxxx` 密钥
3. **配置环境变量**: `export MORPHIXAI_API_KEY="mk_your_key_here"`
4. **链接账号**: 访问 [morphix.app/connections](https://morphix.app/connections) 管理账号，或使用下方 `mx_link: connect` 操作

## 工具选择规则

```
用户请求操作某个平台
  ├── 有专用 skill？ → 使用专用 skill（见下方列表）
  ├── 账号未链接？ → mx_link: connect 引导授权
  └── 无专用 skill？ → mx_link: proxy 兜底代理调用
```

## 核心能力

1. **账号管理** — 查看已链接账号、引导用户链接新账号
2. **API 代理** — 通过已链接账号安全调用第三方 API（仅用于无专用工具的平台）
3. **统一入口** — 支持 40+ 第三方平台，无需各自配置

## 支持的平台

| 类别 | 平台 | app 标识 |
|------|------|----------|
| 开发工具 | GitHub | `github` |
| | GitLab | `gitlab` |
| | Jira | `jira` |
| | Linear | `linear` |
| 邮箱 | Gmail | `gmail` |
| | Outlook | `outlook` |
| 即时通讯 | Slack | `slack` |
| | Discord | `discord` |
| 文档协作 | Notion | `notion` |
| | Google Sheets | `google_sheets` |
| | Confluence | `confluence` |
| 设计 | Figma | `figma` |
| 日历 | Google Calendar | `google_calendar` |
| | Zoom | `zoom` |
| 其他 | HubSpot | `hubspot` |
| | Trello | `trello` |
| | Asana | `asana` |

> 完整列表可通过 `mx_link` 的 `list_apps` action 获取。

## 使用流程

### 1. 检查已链接账号

```
使用 mx_link 工具:
  action: list_accounts
  app_name: "github"  (可选，筛选特定平台)
```

### 2. 引导用户链接新账号

如果用户需要的平台尚未链接：

```
使用 mx_link 工具:
  action: connect
  app: "github"  (必须指定目标应用)
```

返回一个 OAuth 授权链接，发送给用户在浏览器中完成授权。链接有效期 4 小时。

> **重要：`app` 参数必须提供。** 后端返回的链接格式为：
> ```
> https://pipedream.com/_static/connect.html?token=ctok_xxx&connectLink=true
> ```
> 该链接如果缺少 `app` 参数则无法访问。当传入 `app` 参数后，生成的链接会包含 `&app=<app_name>`，例如：
> ```
> https://pipedream.com/_static/connect.html?token=ctok_xxx&connectLink=true&app=gitlab
> ```
> 只有带 `app` 参数的链接才能正常打开授权页面。

### 3. 通过代理调用第三方 API（仅限无专用 skill 的平台）

> **再次强调：** 对于已有专用 skill 的平台（见下方完整列表），**必须使用专用 skill**。`proxy` 仅作为无专用 skill 时的兜底方案。

用户授权完成后，对于没有专用 skill 的平台，用 `proxy` action 调用第三方 API：

**示例：查询 Slack 频道消息（无专用工具，使用 proxy）**
```
使用 mx_link 工具:
  action: proxy
  account_id: "apn_xxx"   (从 list_accounts 获取)
  method: "GET"
  url: "https://slack.com/api/conversations.history"
  params: { "channel": "C01234567", "limit": 10 }
```

**示例：创建 Google Sheets 行（无专用工具，使用 proxy）**
```
使用 mx_link 工具:
  action: proxy
  account_id: "apn_xxx"
  method: "POST"
  url: "https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}/values/{range}:append"
  params: { "valueInputOption": "USER_ENTERED" }
  body: {
    "values": [["2026-02-25", "完成 SDK 集成", "通过"]]
  }
```

## 已有专用 Skill（必须优先使用）

以下平台已有专用 skill，**禁止使用 `mx_link: proxy` 替代**：

| 专用 skill | 平台 | app 标识 | 使用的工具 |
|-----------|------|----------|-----------|
| `jira-workflow` | Jira Cloud | `jira` | `mx_jira` |
| `gitlab-workflow` | GitLab | `gitlab` | `mx_gitlab` |
| `github-workflow` | GitHub | `github` | `mx_github` |
| `outlook-email` | Outlook 邮箱 | `microsoft_outlook` | `mx_outlook` |
| `outlook-calendar` | Outlook 日历 | `microsoft_outlook_calendar` | `mx_outlook_calendar` |
| `ms-todo` | Microsoft To Do | `microsofttodo` | `mx_ms_todo` |
| `gmail` | Gmail | `gmail` | `mx_gmail` |
| `google-tasks` | Google Tasks | `google_tasks` | `mx_google_tasks` |
| `notion` | Notion | `notion` | `mx_notion` |
| `confluence` | Confluence Cloud | `confluence` | `mx_confluence` |
| `figma` | Figma | `figma` | `mx_figma` |

专用 skill 的优势：
- **自动账号检测** — 无需手动查 account_id
- **自动 URL 构建** — 无需知道 API 端点
- **自动格式转换** — 如 Jira Markdown→ADF、Confluence Storage Format
- **语义化参数** — `jql: "..."` 比手写 REST URL 更直观
- **内置工作流** — 每个 skill 包含常见场景的操作步骤

`mx_link` 的 `proxy` action **仅适用于**上述列表之外的应用（如 Slack、Discord、Zoom、Google Sheets 等）。

## 常见场景

### 有专用 skill → 直接使用对应 skill

```
# 查 Jira 待办 → 使用 jira-workflow skill
mx_jira: action: search_issues,
  jql: "assignee = currentUser() AND status != Done ORDER BY updated DESC"

# 查 GitLab MR → 使用 gitlab-workflow skill
mx_gitlab: action: list_merge_requests, state: "opened"

# 查 GitHub 仓库 → 使用 github-workflow skill
mx_github: action: list_repos, sort: "updated", per_page: 5

# 查今日日程 → 使用 outlook-calendar skill
mx_outlook_calendar: action: get_calendar_view,
  start_date_time: "2026-02-25T00:00:00Z", end_date_time: "2026-02-25T23:59:59Z"
```

### 无专用 skill → 兜底使用 mx_link proxy

```
# Slack 消息（无专用 skill）→ 使用 proxy
1. mx_link: list_accounts, app_name="slack"
2. mx_link: proxy, account_id="apn_xxx", method="GET",
   url="https://slack.com/api/conversations.history",
   params={"channel":"C01234567","limit":10}

# Google Sheets（无专用 skill）→ 使用 proxy
1. mx_link: list_accounts, app_name="google_sheets"
2. mx_link: proxy, account_id="apn_xxx", method="GET",
   url="https://sheets.googleapis.com/v4/spreadsheets/{id}/values/Sheet1"
```

### 账号未链接 → 引导连接

```
1. mx_link: list_accounts, app_name="slack"
     → 返回空列表
2. mx_link: connect, app: "slack"
     → 返回 OAuth 授权链接，发给用户
3. 用户完成授权后，重新操作
```

## 错误处理

- **401** — API Key 无效或已过期，提示用户到 MorphixAI 控制台 (https://morphix.app/api-keys) 重新创建
- **403** — API Key 缺少权限范围，需要全选 scope（`user:profile:read`、`link`）
- **账号未链接** — 使用 `connect` action 引导用户授权
- **第三方 API 错误** — proxy 返回第三方原始错误，根据各平台文档处理

## 配置

### 环境变量

```bash
# ~/.openclaw/.env
MORPHIXAI_API_KEY=mk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 或通过 openclaw.json

```json
{
  "morphix": {
    "apiKey": "mk_xxx"
  }
}
```

### 获取 API Key

1. 登录 MorphixAI 控制台 https://morphix.app/api-keys
2. 点击「创建 API Key」，**Scope 全选**
3. 复制保存 Key（只显示一次）

## 最佳实践

1. **专用 skill 优先** — 有专用 skill 的平台**必须用对应 skill**，`proxy` 只作为无专用 skill 时的兜底
2. **先查后连** — 总是先用 `list_accounts` 检查是否已链接，避免重复引导用户授权
3. **缓存 account_id** — 在对话中缓存 `account_id`，无需每次都查询
4. **组合使用** — 一个对话中可以跨 skill 操作（先用 `jira-workflow` 查任务，再用 `mx_link: proxy` 发 Slack 通知）
5. **优雅降级** — 如果 API Key 未配置，提示用户设置环境变量
