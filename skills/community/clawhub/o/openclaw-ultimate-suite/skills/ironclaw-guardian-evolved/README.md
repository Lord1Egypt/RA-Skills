# IronClaw Guardian Evolved 🛡️

融合三大安全技能的进化版守护系统：

| 来源 | 核心能力 |
|------|----------|
| **IronClaw** | 实时威胁分类、prompt injection 检测、技能扫描 |
| **Guardian** | Gateway 监控、自动修复、git 回滚、每日快照 |
| **Security Guard** | 危险命令阻断、秘密泄露防护、审计日志 |

## 🚀 快速启动

### 1. 初始化 Git
```bash
cd ~/.openclaw/workspace
git config --global user.email "guardian@example.com"
git config --global user.name "Guardian"
git init && git add -A && git commit -m "initial"
```

### 2. 安装守护脚本
```bash
cp scripts/guardian.sh ~/.openclaw/guardian.sh
chmod +x ~/.openclaw/guardian.sh
```

### 3. 启动 Guardian
```bash
nohup ~/.openclaw/guardian.sh >> /tmp/openclaw-guardian.log 2>&1 &
```

### 4. 验证
```bash
pgrep -a -f "guardian.sh"
tail -f /tmp/openclaw-guardian.log
```

## 🛡️ 使用 IronClaw 检测

### 扫描技能文件
```bash
python3 scripts/ironclaw_audit.py scan /path/to/skill/SKILL.md
```

### 检查危险命令
```bash
python3 scripts/ironclaw_audit.py check "rm -rf /tmp"
```

### 检测 prompt injection
```bash
python3 scripts/ironclaw_audit.py message "可疑消息内容"
```

## 📊 修复阶梯

1. 每 30 秒检测 Gateway 状态
2. 宕机 → 运行 `openclaw doctor --fix` (最多 3 次)
3. 仍宕机 → `git reset --hard` 回滚
4. 全部失败 → 冷却 300 秒

## 📝 审计日志

路径：`~/.openclaw/logs/ironclaw.audit.jsonl`

格式：JSONL，包含 timestamp/event/label/confidence

---

**Stay safe out there, claws!**
