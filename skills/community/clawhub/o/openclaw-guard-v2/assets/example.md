# OpenClaw Guard 使用示例

## 场景：修改核心配置文件

假设你需要修改 `AGENTS.md`：

### 1. 启动守护（推荐方式）

```bash
cd ~/openclaw/skills/openclaw-guard

# 在修改前启动守护，设置 3 分钟超时
./scripts/guard.sh start 180
```

输出：
```
[2026-03-12 12:00:00] 🛡️ 守护启动，180秒后检查...
[2026-03-12 12:00:00] 📦 已备份: /home/user/.openclaw/openclaw.json
[2026-03-12 12:00:00] 📦 已备份: /home/user/.openclaw/workspace/AGENTS.md
...
[2026-03-12 12:00:00] ✅ 完成备份: 6 个文件
[2026-03-12 12:00:00] 💤 等待 180 秒...
```

### 2. 执行危险操作

```bash
# 修改配置文件
vim ~/openclaw/workspace/AGENTS.md

# 测试修改
openclaw gateway restart
```

### 3. 成功后停止守护

如果一切正常，手动停止守护：

```bash
./scripts/guard.sh stop
```

输出：
```
[2026-03-12 12:02:00] ✅ 守护进程已停止
```

### 4. 如果 AI 挂了...

3 分钟后，守护脚本会自动：
1. 恢复备份的配置文件
2. 重启 Gateway
3. 记录事件到 `incident_log.txt`

## 查看状态

```bash
./scripts/guard.sh status
```

输出：
```
🛡️ 守护运行中 (PID: 12345, 超时: 180s)
📦 最近备份: /home/user/.openclaw/backups/backup_20260312_120000 (时间: 20260312_120000)
```

## 清理旧备份

```bash
# 清理 7 天前的备份
./scripts/guard.sh clean 7
```

## 配合 AGENTS.md 使用

在 `AGENTS.md` 中添加规则：

```markdown
## ⚠️ 危险操作规则

修改以下文件前必须启动守护：
- AGENTS.md, SOUL.md, USER.md, MEMORY.md
- openclaw.json
- 任何系统配置文件

命令：
1. 启动: ./scripts/guard.sh start 180
2. 执行操作
3. 成功后: ./scripts/guard.sh stop
```

## 定时健康检查

添加到 crontab：

```bash
# 每 5 分钟检查 Gateway 状态
*/5 * * * * /path/to/openclaw-guard/scripts/guard.sh check
```

## 故障排查

### 查看日志

```bash
tail -f ~/.openclaw/backups/guard.log
```

### 查看事件记录

```bash
cat ~/.openclaw/backups/incident_log.txt
```

### 手动回滚

```bash
# 查看可用备份
ls -la ~/.openclaw/backups/backup_*/

# 手动恢复
cp ~/.openclaw/backups/backup_20260312_120000/* ~/.openclaw/
systemctl --user restart openclaw-gateway
```