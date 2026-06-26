---
name: jira-workflow
description: Jira Cloud 项目管理集成。搜索/创建/更新 Issue，切换状态，添加评论，查看项目和看板。通过 MorphixAI 代理安全访问 Jira API。
metadata:
  openclaw:
    emoji: "🎫"
    requires:
      env: [MORPHIXAI_API_KEY]
---

# Jira 项目管理

通过 `mx_jira` 工具管理 Jira Cloud 中的 Issue、项目和工作流。所有操作通过 MorphixAI 代理，无需直接管理 OAuth token。

## 前置条件

1. **安装插件**: `openclaw plugins install openclaw-morphixai`
2. **获取 API Key**: 访问 [morphix.app/api-keys](https://morphix.app/api-keys) 生成 `mk_xxxxxx` 密钥
3. **配置环境变量**: `export MORPHIXAI_API_KEY="mk_your_key_here"`
4. **链接账号**: 访问 [morphix.app/connections](https://morphix.app/connections) 链接 Jira 账号，或通过 `mx_link` 工具链接（app: `jira`）

## 核心操作

### 查看项目列表

```
mx_jira:
  action: list_projects
  max_results: 10
```

### 搜索 Issue（JQL）

```
mx_jira:
  action: search_issues
  jql: "project = PROJ AND status != Done ORDER BY updated DESC"
  max_results: 10
```

> **重要：** JQL 必须包含限制条件（如 `project = X`），不能使用无限制查询。

### 查看 Issue 详情

```
mx_jira:
  action: get_issue
  issue_key: "PROJ-123"
```

### 创建 Issue

```
mx_jira:
  action: create_issue
  project: "PROJ"
  summary: "实现用户登录功能"
  issue_type: "Task"
  description: "实现基于 JWT 的用户登录流程\n\n**验收标准：**\n- 支持邮箱+密码登录\n- 返回 JWT token"
  priority: "High"
  labels: ["backend", "auth"]
```

> 描述支持 Markdown 格式，自动转换为 Jira ADF（Atlassian Document Format）。

### 更新 Issue

```
mx_jira:
  action: update_issue
  issue_key: "PROJ-123"
  fields: { "summary": "新标题", "priority": { "name": "High" } }
```

### 切换 Issue 状态

```
mx_jira:
  action: transition_issue
  issue_key: "PROJ-123"
  target_status: "In Progress"
```

> 自动查找匹配的 transition，无需手动指定 transition ID。
> 如果目标状态不可达，会返回所有可用的 transition 列表。

### 查看可用的状态转换

```
mx_jira:
  action: get_transitions
  issue_key: "PROJ-123"
```

### 添加评论

```
mx_jira:
  action: add_comment
  issue_key: "PROJ-123"
  body: "代码已提交到 feature 分支，请 review。\n\n**变更内容：**\n- 添加了登录 API\n- 增加了单元测试"
```

> 评论内容支持 Markdown，自动转换为 ADF。

## 常见工作流

### 每日 Standup — 查看我的待办

```
1. mx_jira: get_myself  → 获取当前用户 accountId
2. mx_jira: search_issues
   jql: "assignee = <accountId> AND status != Done ORDER BY priority DESC, updated DESC"
```

### 创建 Issue 并开始工作

```
1. mx_jira: create_issue → 获取 issue_key
2. mx_jira: transition_issue, target_status: "In Progress"
3. mx_jira: add_comment, body: "开始开发"
```

### 完成 Issue

```
1. mx_jira: add_comment, body: "开发完成，PR: <url>"
2. mx_jira: transition_issue, target_status: "Done"
```

## 注意事项

- Jira API v3 使用 ADF 格式，本工具自动转换 Markdown/纯文本，无需手动构建 ADF JSON
- JQL 查询必须包含 `project = X` 等限制条件
- `transition_issue` 只能转换到当前状态可达的目标状态
- `account_id` 参数通常省略，工具自动检测已链接的 Jira 账号
