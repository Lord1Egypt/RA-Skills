# Plane API 参考（API Key 认证）

## 认证

所有请求需要在 header 中带 `X-API-Key`:

```bash
-H "X-API-Key: plane_api_你的实际APIKey"
```

**⚠️ 重要**：下面的示例 curl 命令全部使用占位符 `plane_api_你的实际APIKey`，**必须替换为真实的 API Key** 才能使用！

---

## API 端点

基础 URL: `http://localhost:8888/api/v1`

### 工作空间成员

```
GET /api/v1/workspaces/{workspace_slug}/members/
```

### 项目

```
GET  /api/v1/workspaces/{workspace_slug}/projects/
POST /api/v1/workspaces/{workspace_slug}/projects/
GET  /api/v1/workspaces/{workspace_slug}/projects/{project_id}/
PATCH /api/v1/workspaces/{workspace_slug}/projects/{project_id}/
```

创建项目示例：
```bash
curl -X POST "http://localhost:8888/api/v1/workspaces/agent-projects/projects/" \
  -H "X-API-Key: plane_api_你的实际APIKey" \
  -H "Content-Type: application/json" \
  -d '{"name": "项目名称", "identifier": "项目标识符"}'
```

### 任务（Issue）

```
GET  /api/v1/workspaces/{workspace_slug}/projects/{project_id}/issues/
POST /api/v1/workspaces/{workspace_slug}/projects/{project_id}/issues/
GET  /api/v1/issues/{issue_id}/
PATCH /api/v1/issues/{issue_id}/
```

创建任务示例（priority: 0=none, 1=urgent, 2=high, 3=medium, 4=low）：
```bash
curl -X POST "http://localhost:8888/api/v1/workspaces/agent-projects/projects/{项目ID}/issues/" \
  -H "X-API-Key: plane_api_你的实际APIKey" \
  -H "Content-Type: application/json" \
  -d '{"name": "任务名称", "priority": 0}'
```

更新任务：
```bash
curl -X PATCH "http://localhost:8888/api/v1/issues/{任务ID}/" \
  -H "X-API-Key: plane_api_你的实际APIKey" \
  -H "Content-Type: application/json" \
  -d '{"name": "新名称", "priority": 2}'
```

---

## 查询参数

```
GET /api/v1/workspaces/{slug}/projects/{project_id}/issues/?priority=0
GET /api/v1/issues/?search=关键词
GET /api/v1/issues/?limit=50
```

---

## 已知问题

- `priority` 参数只接受数字（0-4），不接受字符串
- `state` 参数在创建任务时可选（不填默认 Backlog）
- API Key 必须有足够的项目权限（项目成员或 Workspace Admin）
