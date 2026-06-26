# 看板系统 v3.0 - 使用总结

## 🎉 已完成功能

### ✅ 阶段 1：基础增强

| 功能 | 状态 | 说明 |
|------|------|------|
| SQLite 持久化 | ✅ | 单文件数据库，零运维 |
| sqlite-vec 集成 | ✅ | 向量搜索支持 |
| MCP Server | ✅ | 12 个 MCP 工具 |
| 自然语言解析 | ✅ | 中文 NLP 支持 |
| 双模式 API | ✅ | REST + MCP |

---

## 📊 核心功能演示

### 1. 自然语言命令

```bash
# 添加任务
curl -X POST http://localhost:9999/api/llm/command \
  -H "Content-Type: application/json" \
  -d '{"command":"添加一个高优先级的安全任务给张三，5 个子任务"}'

# 移动任务
curl -X POST http://localhost:9999/api/llm/command \
  -H "Content-Type: application/json" \
  -d '{"command":"把项目 3 移到进行中"}'

# 查询任务
curl -X POST http://localhost:9999/api/llm/command \
  -H "Content-Type: application/json" \
  -d '{"command":"查看待办任务"}'
```

### 2. MCP 工具调用

```python
from mcp import Client

client = Client("kanban")

# 添加项目
result = client.call_tool("add_project", {
    "name": "安全加固",
    "lane": "security",
    "priority": "high",
    "assignee": "张三"
})

# 分析看板
analysis = client.call_tool("analyze_board")
print(analysis['risks'])
```

### 3. 向量搜索

```bash
# 搜索相似任务
curl -X POST http://localhost:9999/api/llm/search \
  -H "Content-Type: application/json" \
  -d '{"query":"用户认证","limit":5}'
```

### 4. AI 分析

```bash
# 获取看板分析
curl http://localhost:9999/api/llm/analyze
```

---

## 🔧 sqlite-vec 使用示例

### 本地测试

```bash
cd /root/.openclaw/workspace/mvp-kanban
python3 EXAMPLE_VECTOR_USAGE.py
```

### 输出示例

```
============================================================
SQLite + sqlite-vec 向量搜索示例
============================================================

1. 连接数据库...
   ✓ sqlite-vec 已加载

2. 创建表结构...
   ✓ 表已创建

3. 插入测试数据...
   ✓ 插入：用户认证模块
   ✓ 插入：支付网关集成
   ✓ 插入：安全审计日志
   ✓ 插入：CI/CD 流水线
   ✓ 插入：Docker 容器化

4. 向量搜索测试...

   🔍 搜索：'用户登录'
      - Docker 容器化：容器化部署方案 (相似度：0.8009)
      - 支付网关集成：接入支付宝微信支付 (相似度：0.7928)

   🔍 搜索：'支付'
      - 用户认证模块：实现用户登录注册功能 (相似度：0.8330)
      - 支付网关集成：接入支付宝微信支付 (相似度：0.8311)

   🔍 搜索：'安全'
      - 支付网关集成：接入支付宝微信支付 (相似度：0.7972)
      - 安全审计日志：记录敏感操作日志 (相似度：0.7944)

   🔍 搜索：'部署'
      - Docker 容器化：容器化部署方案 (相似度：0.8547)
      - 安全审计日志：记录敏感操作日志 (相似度：0.8162)
```

---

## 📁 文件结构

```
mvp-kanban/
├── app.py                  # Flask 主应用
├── database.py             # 数据库模块（SQLite + sqlite-vec）
├── mcp_server.py           # MCP Server
├── nlp_parser.py           # 自然语言解析器
├── requirements.txt        # Python 依赖
├── mcp.json               # MCP 配置
├── API.md                 # API 文档
├── VECTOR_SEARCH.md       # 向量搜索指南
├── EXAMPLE_VECTOR_USAGE.py # 向量搜索示例
├── templates/
│   └── index.html         # 前端页面
├── docker-compose.yml     # Docker 配置
└── Dockerfile             # Docker 镜像
```

---

## 🚀 部署方式

### Docker 部署（推荐）

```bash
cd /root/.openclaw/workspace/mvp-kanban
docker compose up -d
```

访问：http://localhost:9999

### 本地开发

```bash
pip install -r requirements.txt
python app.py
```

### MCP Server

```bash
# 独立运行
python mcp_server.py

# 或通过 MCP 客户端配置
# 在 MCP 配置中添加:
{
  "mcpServers": {
    "kanban": {
      "command": "python",
      "args": ["mcp_server.py"],
      "cwd": "/root/.openclaw/workspace/mvp-kanban"
    }
  }
}
```

---

## 🎯 MCP 工具列表

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
| `analyze_board` | AI 分析看板 | - |

---

## 🌟 自然语言支持

### 支持的命令类型

1. **添加任务**
   - "添加一个高优先级的安全任务给张三"
   - "创建任务 用户认证模块，泳道是功能开发"
   - "添加 bug 修复任务，低优先级，给李四"

2. **更新状态**
   - "把项目 3 移到进行中"
   - "将任务 5 改为已完成"

3. **移动任务**
   - "把项目 2 移到安全泳道"
   - "将任务移到 DevOps"

4. **删除任务**
   - "删除项目 5"
   - "移除任务 3"

5. **查询**
   - "查看待办任务"
   - "列出所有安全相关的任务"

6. **分析**
   - "分析看板状态"
   - "有哪些瓶颈和风险"

---

## 📈 数据库模式

### projects 表

```sql
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    status TEXT DEFAULT 'todo',
    lane TEXT DEFAULT 'feature',
    progress INTEGER DEFAULT 0,
    tasks INTEGER DEFAULT 0,
    completed INTEGER DEFAULT 0,
    assignee TEXT DEFAULT '',
    priority TEXT DEFAULT 'medium',
    description TEXT DEFAULT '',
    tags TEXT DEFAULT '[]',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    name_embedding BLOB,          -- 名称向量
    description_embedding BLOB    -- 描述向量
);
```

### lanes 表

```sql
CREATE TABLE lanes (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    color TEXT DEFAULT '#667eea',
    icon TEXT DEFAULT '📌',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### change_log 表

```sql
CREATE TABLE change_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    action TEXT NOT NULL,
    old_data TEXT,
    new_data TEXT,
    changed_by TEXT DEFAULT 'system',
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## ⚠️ 已知问题

### SQLite 并发锁

**问题：** 多 worker 模式下 SQLite 文件锁冲突

**解决方案：**
1. 使用单 worker 多线程模式（已实施）
2. 启用 WAL 模式（已实施）
3. 设置合理的超时时间（30 秒）

**配置：**
```dockerfile
# Dockerfile
CMD ["gunicorn", "--workers", "1", "--threads", "4", ...]
```

```python
# database.py
conn = sqlite3.connect(DB_PATH, timeout=30.0, check_same_thread=False)
conn.execute('PRAGMA journal_mode=WAL')
```

---

## 🎓 下一步优化

### 短期
- [ ] 修复数据库并发问题
- [ ] 添加前端向量搜索 UI
- [ ] 完善错误处理

### 中期
- [ ] 集成真实 embedding 模型（sentence-transformers）
- [ ] 添加用户认证
- [ ] 支持批量操作

### 长期
- [ ] 迁移到 PostgreSQL + pgvector（如需大规模）
- [ ] 添加实时协作
- [ ] 支持 Webhook 通知

---

## 📚 参考文档

- [API.md](./API.md) - 完整 API 文档
- [VECTOR_SEARCH.md](./VECTOR_SEARCH.md) - 向量搜索指南
- [EXAMPLE_VECTOR_USAGE.py](./EXAMPLE_VECTOR_USAGE.py) - 使用示例

---

*版本：v3.0.0 | 更新时间：2026-03-21*
