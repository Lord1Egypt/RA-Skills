# 备份与恢复

## 手动备份

```bash
# 备份配置文件
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.$(date +%Y%m%d)

# 备份整个配置目录
tar -czf ~/openclaw-backup-$(date +%Y%m%d).tar.gz ~/.openclaw/
```

## 自动备份

OpenClaw 会在每次配置修改时自动创建备份：
- 备份文件：`~/.openclaw/openclaw.json.bak`

## 恢复配置

```bash
# 从备份文件恢复
cp ~/.openclaw/openclaw.json.backup ~/.openclaw/openclaw.json
openclaw gateway restart
```

## 从特定日期恢复

```bash
# 查看可用备份
ls -la ~/.openclaw/openclaw.json.*

# 恢复指定日期
cp ~/.openclaw/openclaw.json.20260309 ~/.openclaw/openclaw.json
openclaw gateway restart
```

## 多 Agent 环境备份建议

由于每个 Agent 有独立的工作目录，建议单独备份：

```bash
# 备份所有 Agent 工作目录
for i in 1 2 3 4; do
  tar -czf ~/workspace${i}-backup-$(date +%Y%m%d).tar.gz \
    ~/.openclaw/workspace${i}/
done
```
