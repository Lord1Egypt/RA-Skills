# 🚀 MVP Kanban Skill

**版本 Version:** v0.0.2  
**作者 Author:** 北京老李  
**许可证 License:** MIT

---

## 📖 描述 Description

**中文：**  
MVP 看板系统 - 完整的任务管理技能，包含 Docker 镜像和源代码。  
支持任务管理、泳道管理、批量操作、AI 分析和向量搜索。

**English:**  
MVP Kanban Board - Complete task management skill with Docker image and source code.  
Supports task management, lane management, batch operations, AI analysis, and vector search.

---

## 🚀 快速开始 Quick Start

### 从 ClawHub 安装 Install from ClawHub

```bash
clawhub install mvp-kanban
```

### 手动安装 Manual Installation

```bash
# 复制 Copy
cp -r mvp-kanban-complete-skill ~/.openclaw/workspace/skills/mvp-kanban

# 构建镜像 Build image
cd ~/.openclaw/workspace/skills/mvp-kanban/docker
docker build -t mvp-kanban:latest .

# 启动 Start
docker-compose up -d
```

---

## 🎯 使用方式 Usage

### Web 界面 Web UI

访问 Visit: **http://localhost:9999**

- 点击任务 Click task
- 双击编辑 Double-click to edit
- 拖拽移动 Drag and drop

### REST API

```bash
# 添加任务 Add task
curl -X POST http://localhost:9999/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name":"Task","lane":"feature"}'
```

### MCP 工具

```python
from mcp import Client
client = Client("kanban")
await client.call_tool("add_project", {"name": "Task", "lane": "feature"})
```

---

## 🛠️ MCP 工具 Tools (21)

| 类别 Category | 数量 Count |
|----------|--------|
| 任务管理 Task Management | 7 |
| 泳道管理 Lane Management | 5 |
| 批量操作 Batch Operations | 3 |
| AI 功能 AI Features | 4 |
| 辅助功能 Auxiliary | 2 |

---

## 📋 功能特性 Features

- ✅ 任务管理 Task Management
- ✅ 泳道管理 Lane Management  
- ✅ 批量操作 Batch Operations
- ✅ AI 分析 AI Analysis
- ✅ 向量搜索 Vector Search
- ✅ 自然语言 Natural Language
- ✅ Web 界面 Web UI
- ✅ 数据持久化 Data Persistence

---

## 📖 文档 Documentation

| 文档 Doc | 说明 Description |
|------|------|
| [SKILL.md](SKILL.md) | 技能说明 Skill Description |
| [PRIVACY_POLICY.md](PRIVACY_POLICY.md) | 隐私政策 Privacy Policy |
| [SECURITY_AUDIT.md](SECURITY_AUDIT.md) | 安全审计 Security Audit |
| [docs/API.md](docs/API.md) | API 文档 API Reference |
| [docs/QUICK_TEST.md](docs/QUICK_TEST.md) | 快速测试 Quick Test |

---

## 🔒 安全 Security

- ✅ 无敏感信息 No sensitive info
- ✅ 无隐私收集 No data collection
- ✅ 本地存储 Local storage
- ✅ 开源透明 Open source

**安全评分 Security Score:** 97/100

---

## 📊 系统要求 Requirements

- Docker 20.10+
- Python 3.12+
- 内存 Memory: 512MB
- 存储 Storage: 100MB

---

## 👤 作者 Author

**北京老李**

---

## 📄 许可证 License

MIT License

---

**🎉 开始使用 Start Now!**

访问 Visit: http://localhost:9999
