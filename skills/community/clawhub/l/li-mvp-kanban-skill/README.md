# 🚀 MVP Kanban Skill 快速开始

## 1️⃣ 安装

### 从 ClawHub 安装
```bash
clawhub install mvp-kanban
```

### 手动安装
```bash
# 1. 拉取 Docker 镜像
docker pull your-dockerhub-username/mvp-kanban:latest

# 2. 复制 Skill 到 OpenClaw
cp -r mvp-kanban-skill ~/.openclaw/workspace/skills/mvp-kanban

# 3. 配置 MCP
cp ~/.openclaw/workspace/skills/mvp-kanban/mcp.json ~/.openclaw/config/mcp.json
```

## 2️⃣ 启动

### Docker 启动
```bash
docker run -d \
  -p 9999:5000 \
  -v kanban-data:/app/data \
  --name mvp-kanban \
  your-dockerhub-username/mvp-kanban:latest
```

### Docker Compose 启动
```bash
cd ~/.openclaw/workspace/skills/mvp-kanban
docker-compose up -d
```

## 3️⃣ 验证

### 检查容器状态
```bash
docker ps | grep kanban
```

### 检查健康状态
```bash
curl http://localhost:9999/api/health
```

### 访问 Web 界面
打开浏览器访问：**http://localhost:9999**

## 4️⃣ 使用

### Web 界面
- 点击"➕ 添加任务"
- 双击任务编辑
- 拖拽任务移动

### REST API
```bash
curl -X POST http://localhost:9999/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name":"任务","lane":"feature"}'
```

### MCP 工具
```python
from mcp import Client
client = Client("kanban")
await client.call_tool("add_project", {"name": "任务", "lane": "feature"})
```

## 5️⃣ 配置 MCP

编辑 `~/.openclaw/config/mcp.json`：

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
      "cwd": "/root/.openclaw/workspace/skills/mvp-kanban"
    }
  }
}
```

## 6️⃣ 测试

运行测试脚本：
```bash
cd ~/.openclaw/workspace/skills/mvp-kanban
python mcp_client.py
```

## 7️⃣ 停止

```bash
docker stop mvp-kanban
docker rm mvp-kanban
```

## 📖 更多文档

- [SKILL.md](SKILL.md) - 完整技能说明
- [API.md](API.md) - API 文档
- [WEB_UI_GUIDE.md](WEB_UI_GUIDE.md) - Web 界面指南
- [USAGE_METHODS.md](USAGE_METHODS.md) - 使用方式对比

---

**🎉 开始使用吧！**
