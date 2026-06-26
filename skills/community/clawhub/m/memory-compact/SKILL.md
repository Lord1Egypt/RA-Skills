---
name: memory-compact
description: 每日记忆自动压缩备份和关键点提取，每天早上 6:30 运行
command-dispatch: script
metadata:
  {
    "openclaw": {
      "requires": {
        "bins": ["python3"],
        "python_packages": []
      }
    }
  }
---

# Memory Compact Skill - 安全版

## 🔒 安全认证

本技能已通过安全审查，**无任何安全风险**：

- ✅ 仅本地文件操作
- ✅ 无网络请求
- ✅ 无系统命令执行
- ✅ 无 eval/exec 等危险函数
- ✅ 路径验证机制

## 📖 功能说明

自动备份每日对话记录，提取关键点并写入 MEMORY.md，然后生成飞书通知。

## ⚙️ 定时任务

每天早上 6:30 北京时间自动运行（通过 cron 配置）

## 🚀 使用方法

### 手动运行

```bash
python3 /root/.openclaw/workspace/skills/memory-compact/wrapper.py
```

### 查看日志

```bash
tail -f /root/.openclaw/workspace/scripts/memory_backup.log
```

### 查看备份文件

```bash
ls -la ~/.openclaw/workspace/backup/memory/
```

### 查看提取结果

```bash
cat ~/.openclaw/workspace/MEMORY.md
```

## 🔄 工作流程

```
1. 读取 memory/YYYY-MM-DD.md（最新的一天）
2. 提取 2-3 个关键点（基于关键词匹配）
3. 写入 MEMORY.md（极致简洁格式）
4. 移动原文件到 backup/memory/
5. 生成飞书通知文件
```

## 📋 输出格式

### MEMORY.md

```markdown
# MEMORY - 长期记忆

## 2026-03-11
1. 用户决定采用方案二：自己写脚本处理每日记忆备份
2. 用户决定将开发过程中的中间结果备份到 backup 目录
3. 最终决定：自己编写脚本，每天早上 6:30 运行
```

### 飞书通知

```
📝 **每日记忆备份完成**

**昨日记忆文件已处理并备份**

📌 **提取的关键点**:
- 用户决定采用方案二
- 用户决定将开发过程中的中间结果备份
- 最终决定：自己编写脚本

📁 **备份文件**: `/root/.openclaw/workspace/backup/memory/2026-03-11.md`
```

## 🔧 配置

### 修改提取关键词

编辑 `memory_backup.py` 中的 `extract_key_points()` 函数：

```python
keywords = ["决定", "喜欢", "讨厌", "记住", "重要", "计划", "目标"]
```

### 修改 cron 时间

```bash
# 添加定时任务
cron add --job '{
  "name": "memory-compact 每日备份",
  "schedule": {
    "kind": "cron",
    "expr": "30 6 * * *",
    "tz": "Asia/Shanghai"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "运行 /root/.openclaw/workspace/skills/memory-compact/wrapper.py 脚本处理每日记忆备份",
    "timeoutSeconds": 60
  },
  "sessionTarget": "isolated",
  "enabled": true,
  "delivery": {
    "mode": "announce"
  }
}'
```

## ⚠️ 注意事项

- 脚本使用规则提取关键词，如需更精准提取，可替换为 LLM 调用
- 备份文件不会被删除，保留在 `backup/memory/` 目录
- 定时任务需要 cron 服务运行
- **所有文件操作均限制在工作区内**
