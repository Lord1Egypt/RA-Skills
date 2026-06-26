# 🚀 MVP Kanban Skill - Quick Start

**Version:** 0.0.1 | **Author:** 北京老李 | **License:** MIT

## 1️⃣ Installation

### Install from ClawHub
```bash
clawhub install mvp-kanban
```

Auto-completes:
- ✅ Check Docker
- ✅ Build Docker image
- ✅ Start service
- ✅ Configure MCP

### Manual Installation
```bash
# 1. Copy Skill
cp -r mvp-kanban-complete-skill ~/.openclaw/workspace/skills/mvp-kanban

# 2. Enter directory
cd ~/.openclaw/workspace/skills/mvp-kanban

# 3. Build image
cd docker
docker build -t mvp-kanban:latest .

# 4. Start service
docker-compose up -d
```

## 2️⃣ Verification

### Check service status
```bash
# View container
docker ps | grep kanban

# Health check
curl http://localhost:9999/api/health
```

### Access Web UI
Open browser: **http://localhost:9999**

## 3️⃣ Usage

### Web Interface
- Click "➕ Add Task"
- Double-click task to edit
- Drag and drop to move

### REST API
```bash
curl -X POST http://localhost:9999/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name":"Task","lane":"feature"}'
```

### MCP Tools
```python
from mcp import Client
client = Client("kanban")
await client.call_tool("add_project", {"name": "Task", "lane": "feature"})
```

## 4️⃣ Quick Commands

```bash
# Start
clawhub run mvp-kanban start

# Stop
clawhub run mvp-kanban stop

# Restart
clawhub run mvp-kanban restart

# View logs
clawhub run mvp-kanban logs

# Health check
clawhub run mvp-kanban health

# Backup data
clawhub run mvp-kanban backup

# Restore data
clawhub run mvp-kanban restore
```

## 5️⃣ Configuration

### Change Port
Edit `docker/docker-compose.yml`:
```yaml
ports:
  - "8080:5000"  # Change to 8080
```

Restart:
```bash
clawhub run mvp-kanban restart
```

### Data Backup
```bash
# Backup
clawhub run mvp-kanban backup

# Restore
clawhub run mvp-kanban restore
```

## 6️⃣ Development

### Local Development Mode
```bash
cd ~/.openclaw/workspace/skills/mvp-kanban/src

# Install dependencies
pip install -r requirements.txt

# Run
python app.py
```

## 7️⃣ Troubleshooting

### Service won't start
```bash
# View logs
docker-compose logs

# Check port usage
netstat -tlnp | grep 9999
```

### MCP tools unavailable
```bash
# Check MCP config
cat ~/.openclaw/config/mcp.json

# Restart MCP
openclaw gateway restart
```

### Database locked
```bash
# Restart container
docker-compose restart

# Or rebuild
docker-compose down
docker-compose up -d
```

## 📖 More Documentation

- [SKILL.md](SKILL.md) - Complete skill description
- [docs/API.md](docs/API.md) - API documentation
- [docs/WEB_UI_GUIDE.md](docs/WEB_UI_GUIDE.md) - Web interface guide
- [docs/USAGE_METHODS.md](docs/USAGE_METHODS.md) - Usage comparison
- [docs/QUICK_TEST.md](docs/QUICK_TEST.md) - Quick test

---

**🎉 Start using it!**

Visit: **http://localhost:9999**
