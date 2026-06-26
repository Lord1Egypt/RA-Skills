---
name: ms-todo
description: Microsoft To Do 任务管理集成。管理任务列表和任务，创建、完成、删除任务。通过 MorphixAI 代理安全访问 Microsoft Graph API。
metadata:
  openclaw:
    emoji: "✅"
    requires:
      env: [MORPHIXAI_API_KEY]
---

# Microsoft To Do

通过 `mx_ms_todo` 工具管理 Microsoft To Do 中的任务列表和任务。

## 前置条件

1. **安装插件**: `openclaw plugins install openclaw-morphixai`
2. **获取 API Key**: 访问 [morphix.app/api-keys](https://morphix.app/api-keys) 生成 `mk_xxxxxx` 密钥
3. **配置环境变量**: `export MORPHIXAI_API_KEY="mk_your_key_here"`
4. **链接账号**: 访问 [morphix.app/connections](https://morphix.app/connections) 链接 MS To Do 账号，或通过 `mx_link` 工具链接（app: `microsofttodo`）

## 核心操作

### 列出任务列表

```
mx_ms_todo:
  action: list_task_lists
```

### 创建任务列表

```
mx_ms_todo:
  action: create_task_list
  display_name: "项目待办"
```

### 列出任务

```
mx_ms_todo:
  action: list_tasks
  list_id: "AQMkADxx..."
  top: 20
```

### 查看任务详情

```
mx_ms_todo:
  action: get_task
  list_id: "AQMkADxx..."
  task_id: "AQMkADxx..."
```

### 创建任务

```
mx_ms_todo:
  action: create_task
  list_id: "AQMkADxx..."
  title: "完成 API 文档"
  body: "编写 REST API 接口文档，包含请求/响应示例"
  importance: "high"
  due_date: "2026-03-01"
```

### 更新任务

```
mx_ms_todo:
  action: update_task
  list_id: "AQMkADxx..."
  task_id: "AQMkADxx..."
  title: "更新后的标题"
  importance: "normal"
```

### 完成任务

```
mx_ms_todo:
  action: complete_task
  list_id: "AQMkADxx..."
  task_id: "AQMkADxx..."
```

### 删除任务

```
mx_ms_todo:
  action: delete_task
  list_id: "AQMkADxx..."
  task_id: "AQMkADxx..."
```

## 常见工作流

### 每日任务管理

```
1. mx_ms_todo: list_task_lists → 找到目标列表
2. mx_ms_todo: list_tasks, list_id: "xxx" → 查看当前任务
3. mx_ms_todo: create_task → 添加新任务
4. mx_ms_todo: complete_task → 完成已做的任务
```

## 注意事项

- `importance` 可选值：`low`、`normal`、`high`
- `status` 可选值：`notStarted`、`inProgress`、`completed`、`waitingOnOthers`、`deferred`
- `due_date` 格式为 `YYYY-MM-DD`
- `account_id` 参数通常省略，工具自动检测已链接的 MS To Do 账号
