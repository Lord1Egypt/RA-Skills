
### Continuous Monitoring
Watch agent status in real-time:
```bash
python3 {baseDir}/scripts/monitor.py --watch --interval 5
```

### JSON Output
Get machine-readable output:
```bash
python3 {baseDir}/scripts/visualize.py --format json
```

**Example JSON:**
```json
{
  "agents": [
    {
      "id": "main",
      "model": "anthropic/claude-sonnet-4-6",
      "workspace": "/Users/user/.openclaw/workspace",
      "sessions": 0
    }
  ],
  "total": 2
}
```

---

## 📖 Use Cases

### 1. Debugging Agent Issues
When an agent isn't responding:
```bash
# Check if agent is running
python3 {baseDir}/scripts/monitor.py

# View agent details
python3 {baseDir}/scripts/visualize.py
```

### 2. Managing Multiple Projects
Track agents across different projects:
```bash
# See all agents and their workspaces
python3 {baseDir}/scripts/visualize.py
```

### 3. Optimizing Agent Performance
Monitor which agents are most active:
```bash
# Watch real-time activity
python3 {baseDir}/scripts/monitor.py --watch
```

---

## 🎯 Common Scenarios

**Scenario: "Which agents do I have?"**
```bash
python3 {baseDir}/scripts/visualize.py
```

**Scenario: "Is my agent still running?"**
```bash
python3 {baseDir}/scripts/monitor.py
```

**Scenario: "What's my agent doing right now?"**
```bash
python3 {baseDir}/scripts/monitor.py --watch
```

---

## 💡 Tips

- Use `--format json` for integration with other tools
- Run `monitor.py --watch` in a separate terminal for continuous monitoring
- Check agent status before sending important tasks

---

## 🐛 Troubleshooting

**Problem: "No agents found"**
- Make sure OpenClaw Gateway is running: `openclaw status`
- Check your agent configuration

**Problem: "Script not found"**
- Ensure you're running from the correct directory
- Check that Python 3 is installed: `python3 --version`

---

## 📝 Changelog

### v1.0.0 (2026-03-14)
- Initial release
- Agent visualization
- Status monitoring
- Basic communication tools
- Task flow tracking

---

## 🤝 Contributing

Found a bug or have a feature request? 
- Open an issue on GitHub
- Join the OpenClaw Discord community

---

## 📄 License

MIT License - feel free to use and modify!
