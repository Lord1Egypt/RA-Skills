# 看板系统 API 文档 v3.0

## 📖 概述

看板系统 v3.0 提供双模式接口：
- **REST API** - 传统 HTTP 接口
- **MCP** - LLM 原生工具接口

## 🔧 快速开始

### REST API 调用

```bash
# 获取看板数据
curl http://localhost:9999/api/kanban

# 添加任务
curl -X POST http://localhost:9999/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name":"新任务","lane":"security","assignee":"张三","priority":"high"}'

# 自然语言命令
curl -X POST http://localhost:9999/api/llm/command \
  -H "Content-Type: application/json" \
  -d '{"command":"添加一个高优先级的安全任务给张三"}'
```

### MCP 调用

```python
# 通过 MCP 客户端
from mcp import Client

client = Client("kanban")

# 添加任务
result = client.call_tool("add_project", {
    "name": "安全加固",
    "lane": "security",
    "priority": "high",
    "assignee": "张三"
})

# 分析看板
analysis = client.call_tool("analyze_board")
```

---

## 📡 REST API

### 基础接口

#### GET /api/kanban
获取完整看板数据（项目、泳道、指标）

**响应:**
```json
{
  "projects": [...],
  "lanes": [...],
  "metrics": {...}
}
```

#### GET /api/metrics
获取统计指标

**响应:**
```json
{
  "total_projects": 10,
  "completed": 3,
  "in_progress": 4,
  "todo": 3,
  "success_rate": 45
}
```

#### GET /api/projects
获取所有项目

**查询参数:**
- `status` - 过滤状态 (todo, in_progress, done)
- `lane` - 过滤泳道

#### GET /api/projects/:id
获取单个项目详情

#### POST /api/projects
创建新项目

**请求体:**
```json
{
  "name": "任务名称",
  "lane": "feature",
  "status": "todo",
  "assignee": "张三",
  "priority": "high",
  "tasks": 5,
  "description": "任务描述"
}
```

#### PUT /api/projects/:id
更新项目

**请求体:**
```json
{
  "status": "in_progress",
  "lane": "security"
}
```

#### DELETE /api/projects/:id
删除项目

---

### AI 接口

#### POST /api/llm/command
**自然语言命令接口** - LLM 可直接调用

**请求体 (自然语言模式):**
```json
{
  "command": "添加一个高优先级的安全任务给张三"
}
```

**请求体 (MCP 模式):**
```json
{
  "tool": "add_project",
  "params": {
    "name": "安全加固",
    "lane": "security",
    "priority": "high",
    "assignee": "张三"
  }
}
```

**响应:**
```json
{
  "success": true,
  "action": "add_project",
  "result": {
    "id": 8,
    "name": "安全加固",
    "lane": "security",
    ...
  }
}
```

**支持的自然语言命令:**
- "添加一个高优先级的安全任务给张三"
- "创建任务 用户认证模块，泳道是功能开发"
- "把项目 3 移到进行中"
- "删除项目 5"
- "查看待办任务"
- "分析看板状态"

---

#### GET /api/llm/analyze
**AI 看板分析** - 识别瓶颈、风险和建议

**响应:**
```json
{
  "generated_at": "2026-03-21T17:00:00",
  "summary": {
    "total_projects": 10,
    "completion_rate": "45%",
    "in_progress": 4,
    "todo": 3
  },
  "bottlenecks": [
    {
      "type": "wip_too_high",
      "message": "进行中的项目 (4) 远多于已完成项目 (2)",
      "severity": "medium",
      "suggestion": "考虑减少并行工作，优先完成现有任务"
    }
  ],
  "risks": [
    {
      "type": "high_priority_pending",
      "message": "有 3 个高优先级任务未完成",
      "projects": ["安全加固", "CI/CD 流水线"],
      "severity": "high"
    }
  ],
  "suggestions": ["优先处理高优先级任务"],
  "lane_analysis": {
    "feature": {"total": 4, "completed": 1, "completion_rate": "25%"},
    "security": {"total": 3, "completed": 1, "completion_rate": "33%"}
  }
}
```

---

#### POST /api/llm/search
**向量搜索** - 搜索相似任务

**请求体:**
```json
{
  "query": "用户认证",
  "limit": 5
}
```

**响应:**
```json
{
  "query": "用户认证",
  "results": [
    {
      "id": 6,
      "name": "用户认证模块",
      "similarity": 0.92
    }
  ],
  "count": 1
}
```

---

#### GET /api/history
**变更历史**

**查询参数:**
- `project_id` - 过滤项目
- `limit` - 返回数量（默认 50）

---

## 🛠️ MCP 工具

看板系统提供以下 MCP 工具：

| 工具名 | 描述 | 参数 |
|--------|------|------|
| `list_projects` | 列出所有项目 | status?, lane? |
| `get_project_details` | 获取项目详情 | project_id |
| `add_project` | 添加项目 | name, lane?, status?, assignee?, priority?, tasks?, description?, tags? |
| `update_project_status` | 更新状态 | project_id, status |
| `move_project` | 移动项目 | project_id, lane, status? |
| `delete_project` | 删除项目 | project_id |
| `get_board_metrics` | 获取指标 | - |
| `search_similar_projects` | 向量搜索 | query, limit? |
| `get_project_history` | 变更历史 | project_id, limit? |
| `add_lane` | 添加泳道 | lane_id, name, color?, icon? |
| `list_lanes` | 列出泳道 | - |
| `analyze_board` | 分析看板 | - |

---

## 📊 数据模型

### Project (项目)
```json
{
  "id": 1,
  "name": "任务名称",
  "status": "todo",
  "lane": "feature",
  "progress": 0,
  "tasks": 5,
  "completed": 0,
  "assignee": "张三",
  "priority": "high",
  "description": "任务描述",
  "tags": ["标签 1", "标签 2"],
  "created_at": "2026-03-21T10:00:00",
  "updated_at": "2026-03-21T10:00:00"
}
```

### Lane (泳道)
```json
{
  "id": "feature",
  "name": "功能开发",
  "color": "#667eea",
  "icon": "🚀"
}
```

### 状态枚举
- `todo` - 待办
- `in_progress` - 进行中
- `done` - 已完成

### 泳道枚举
- `feature` - 功能开发
- `security` - 安全加固
- `devops` - DevOps
- `bugfix` - Bug 修复

### 优先级枚举
- `high` - 高
- `medium` - 中
- `low` - 低

---

## 🔍 示例场景

### 场景 1: LLM 自动添加任务
```python
# LLM 解析用户指令后调用
response = requests.post('http://localhost:9999/api/llm/command', json={
    "command": "添加一个高优先级的安全扫描任务给李四，5 个子任务"
})
```

### 场景 2: 自动分析瓶颈
```python
# 定时任务调用分析接口
response = requests.get('http://localhost:9999/api/llm/analyze')
analysis = response.json()

if analysis['risks']:
    # 发送通知
    send_notification(f"发现 {len(analysis['risks'])} 个风险")
```

### 场景 3: 智能搜索
```python
# 用户搜索"认证相关任务"
response = requests.post('http://localhost:9999/api/llm/search', json={
    "query": "用户认证登录",
    "limit": 5
})
```

### 场景 4: MCP 工具调用
```python
# 通过 MCP 客户端
from mcp import Client

client = Client("kanban")

# 添加任务
client.call_tool("add_project", {
    "name": "CI/CD 优化",
    "lane": "devops",
    "priority": "medium",
    "assignee": "王五"
})

# 分析看板
analysis = client.call_tool("analyze_board")
print(analysis['suggestions'])
```

---

## 🚀 部署

### Docker 部署
```bash
docker-compose up -d
```

### 本地开发
```bash
pip install -r requirements.txt
python app.py
```

### MCP Server
```bash
python mcp_server.py
```

---

## 📝 更新日志

### v3.0.0 (2026-03-21)
- ✅ 添加 SQLite 持久化
- ✅ 集成 sqlite-vec 向量搜索
- ✅ 新增 MCP Server
- ✅ 新增自然语言解析器
- ✅ 新增 AI 分析接口
- ✅ 新增变更日志

### v2.0.0 (2026-03-21)
- ✅ 泳道支持
- ✅ 拖拽交互
- ✅ 实时指标

### v1.0.0 (2026-03-21)
- ✅ 基础看板功能
