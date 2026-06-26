# MVP Kanban Board Skill - v3.0.0

## 📖 描述

MVP 看板系统技能，支持任务管理、泳道管理、批量操作和 AI 分析。
通过 MCP 协议提供 21 个工具，支持 Web 界面、REST API 和 MCP 工具调用。

## ✨ 功能特性

- ✅ **任务管理** - 增删改查、拖拽移动、双击编辑
- ✅ **泳道管理** - 自定义泳道、颜色、图标
- ✅ **批量操作** - 批量创建/更新/删除任务
- ✅ **AI 分析** - 瓶颈识别、风险预警、建议生成
- ✅ **向量搜索** - 语义级任务搜索
- ✅ **自然语言** - 中文命令解析
- ✅ **Web 界面** - 可视化操作、拖拽交互
- ✅ **数据持久化** - SQLite 数据库

## 🚀 快速开始

### 方式 1: 从 ClawHub 安装

```bash
clawhub install mvp-kanban
```

### 方式 2: Docker 部署

```bash
docker pull your-dockerhub-username/mvp-kanban:latest

docker run -d \
  -p 9999:5000 \
  -v kanban-data:/app/data \
  --name mvp-kanban \
  your-dockerhub-username/mvp-kanban:latest
```

### 方式 3: 本地开发

```bash
git clone https://github.com/your-username/mvp-kanban.git
cd mvp-kanban/docker
pip install -r requirements.txt
python app.py
```

## 📋 使用方式

### Web 界面

访问 **http://localhost:9999**

- 点击"➕ 添加任务"创建任务
- 双击任务卡片编辑
- 拖拽任务移动
- 悬停显示操作按钮

### REST API

```bash
# 添加任务
curl -X POST http://localhost:9999/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name":"任务","lane":"feature","priority":"high"}'

# 更新任务
curl -X PUT http://localhost:9999/api/projects/1 \
  -H "Content-Type: application/json" \
  -d '{"status":"in_progress"}'

# AI 分析
curl http://localhost:9999/api/llm/analyze
```

### MCP 工具

```python
from mcp import Client

client = Client("kanban")

# 添加任务
await client.call_tool("add_project", {
    "name": "安全加固",
    "lane": "security",
    "priority": "high"
})

# AI 分析
analysis = await client.call_tool("analyze_board")
```

### 自然语言

```bash
curl -X POST http://localhost:9999/api/llm/command \
  -H "Content-Type: application/json" \
  -d '{"command":"添加一个高优先级安全任务给张三"}'
```

## 🛠️ MCP 工具（21 个）

### 任务管理（7 个）
1. `list_projects` - 列出所有项目
2. `get_project_details` - 获取项目详情
3. `add_project` - 添加项目
4. `update_project_status` - 更新状态
5. `update_project_full` - 完整更新
6. `move_project` - 移动项目
7. `delete_project` - 删除项目

### 泳道管理（5 个）
8. `list_lanes` - 列出泳道
9. `add_lane` - 添加泳道
10. `update_lane` - 更新泳道
11. `delete_lane` - 删除泳道
12. `get_lane_details` - 泳道详情

### 批量操作（3 个）
13. `batch_create_projects` - 批量创建
14. `batch_update_projects` - 批量更新
15. `batch_delete_projects` - 批量删除

### AI 功能（4 个）
16. `analyze_board` - AI 看板分析
17. `search_similar_projects` - 向量搜索
18. `nlp_command` - 自然语言命令
19. `llm_search` - 向量搜索

### 辅助功能（2 个）
20. `get_board_metrics` - 获取统计指标
21. `get_project_history` - 变更历史

## ⚙️ 配置

### MCP 配置

创建 `~/.openclaw/config/mcp.json`：

```json
{
  "mcpServers": {
    "kanban": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "your-dockerhub-username/mvp-kanban:latest",
        "python",
        "mcp_server.py"
      ],
      "cwd": "/root/.openclaw/workspace/skills/mvp-kanban",
      "env": {
        "PYTHONPATH": "/app"
      }
    }
  }
}
```

### Docker Compose

```yaml
version: 0.0.1

services:
  kanban:
    image: your-dockerhub-username/mvp-kanban:latest
    container_name: mvp-kanban
    ports:
      - "9999:5000"
    volumes:
      - kanban-data:/app/data
    environment:
      - FLASK_ENV=production
    restart: unless-stopped
```

## 📊 系统要求

- Docker 20.10+
- Python 3.12+
- 内存：512MB
- 存储：100MB

## 📖 文档

- [使用指南](USAGE_METHODS.md) - 5 种使用方式对比
- [API 文档](API.md) - 完整 REST API 说明
- [Web 界面指南](WEB_UI_GUIDE.md) - Web 功能使用
- [快速测试](QUICK_TEST.md) - 功能测试清单

## 🏷️ 泳道

默认泳道：
- 🚀 功能开发 (feature)
- 🔒 安全加固 (security)
- ⚙️ DevOps (devops)
- 🐛 Bug 修复 (bugfix)

支持自定义泳道！

## 🎯 使用场景

| 场景 | 推荐方式 |
|------|----------|
| 日常管理 | Web 界面 |
| 开发集成 | REST API |
| AI 自动化 | MCP 工具 |
| 批量导入 | REST API 批量接口 |
| 快速记录 | 自然语言命令 |

## 📝 示例

### CI/CD 集成

```python
# GitHub Actions 发现 bug 自动创建任务
import requests

requests.post("http://localhost:9999/api/projects", json={
    "name": f"修复：{bug_title}",
    "lane": "bugfix",
    "priority": "high",
    "assignee": "developer"
})
```

### AI 助手

```python
# AI 理解后自动调用 MCP
command = "添加一个高优先级的安全任务给张三"
await client.call_tool("nlp_command", {"command": command})
```

## 🔄 版本

- **Docker 镜像**: v3.0.0
- **Skill 版本**: v3.0.0
- **API 版本**: v3.0.0

## 👥 作者

DevSecOps Team

## 📄 许可证

MIT License

## 🐛 问题反馈

提交 Issue 到：https://github.com/your-username/mvp-kanban/issues

## 🎉 贡献

欢迎提交 Pull Request！

---

**访问 http://localhost:9999 开始使用！**
