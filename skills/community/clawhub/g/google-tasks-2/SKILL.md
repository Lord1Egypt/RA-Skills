---
name: google-tasks
description: "[暂不可用] Google Tasks 任务管理集成。管理任务列表和任务，创建、完成、删除任务。通过 MorphixAI 代理安全访问 Google Tasks API。"
metadata:
  openclaw:
    emoji: "📋"
    requires:
      env: [MORPHIXAI_API_KEY]
---

# Google Tasks（暂不可用）

> **状态：暂不可用** — Google Tasks 账号尚未链接，该工具暂时不可使用。如需启用，请通过 `mx_link` 工具链接 Google Tasks 账号（app: `google_tasks`）。

通过 `mx_google_tasks` 工具管理 Google Tasks 中的任务列表和任务。

## 前置条件

1. **安装插件**: `openclaw plugins install openclaw-morphixai`
2. **获取 API Key**: 访问 [morphix.app/api-keys](https://morphix.app/api-keys) 生成 `mk_xxxxxx` 密钥
3. **配置环境变量**: `export MORPHIXAI_API_KEY="mk_your_key_here"`
4. **链接账号**: 访问 [morphix.app/connections](https://morphix.app/connections) 链接 Google Tasks 账号，或通过 `mx_link` 工具链接（app: `google_tasks`）

## 核心操作

### 列出任务列表

```
mx_google_tasks:
  action: list_task_lists
```

### 创建任务列表

```
mx_google_tasks:
  action: create_task_list
  title: "工作待办"
```

### 删除任务列表

```
mx_google_tasks:
  action: delete_task_list
  task_list_id: "MDxxxxxxxx"
```

### 列出任务

```
mx_google_tasks:
  action: list_tasks
  task_list_id: "MDxxxxxxxx"
  max_results: 20
  show_completed: false
```

### 查看任务详情

```
mx_google_tasks:
  action: get_task
  task_list_id: "MDxxxxxxxx"
  task_id: "Xxxxxxxx"
```

### 创建任务

```
mx_google_tasks:
  action: create_task
  task_list_id: "MDxxxxxxxx"
  title: "完成代码 Review"
  notes: "Review PR #42 的变更"
  due: "2026-03-01"
```

### 更新任务

```
mx_google_tasks:
  action: update_task
  task_list_id: "MDxxxxxxxx"
  task_id: "Xxxxxxxx"
  title: "更新后的标题"
  notes: "更新后的备注"
```

### 完成任务

```
mx_google_tasks:
  action: complete_task
  task_list_id: "MDxxxxxxxx"
  task_id: "Xxxxxxxx"
```

### 删除任务

```
mx_google_tasks:
  action: delete_task
  task_list_id: "MDxxxxxxxx"
  task_id: "Xxxxxxxx"
```

## 常见工作流

### 每日任务管理

```
1. mx_google_tasks: list_task_lists → 找到目标列表
2. mx_google_tasks: list_tasks, task_list_id: "xxx", show_completed: false
3. mx_google_tasks: create_task → 添加新任务
4. mx_google_tasks: complete_task → 完成已做的任务
```

## 注意事项

- `due` 日期格式为 `YYYY-MM-DD` 或 RFC 3339（如 `2026-03-01T00:00:00.000Z`）
- `status` 只有两个值：`needsAction`（待完成）和 `completed`（已完成）
- `show_completed` 默认不包含已完成任务
- `account_id` 参数通常省略，工具自动检测已链接的 Google Tasks 账号
