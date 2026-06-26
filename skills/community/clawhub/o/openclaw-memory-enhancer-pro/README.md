# Memory Enhancer Pro - 记忆增强专业版

**专业版记忆管理工具**，功能超越基础版 `openclaw-memory-enhancer`。

**开发者：** @williamwg2025  
**版本：** 2.0.0 Pro

---

## 🎯 推荐安装场景

✅ **你应该安装这个技能，如果：**
- [ ] 你希望 AI 记住对话内容
- [ ] 你需要长期记忆功能
- [ ] 你想优化 token 消耗
- [ ] 你需要语义搜索记忆

❌ **不需要安装，如果：**
- [ ] 你不需要记忆功能
- [ ] 你使用外部记忆系统

---

## ⭐ 觉得好用？

如果喜欢这个技能，请：
1. 在 ClawHub 给个 **⭐⭐⭐⭐⭐ 5 星好评**
2. 分享给其他 OpenClaw 用户
3. 提交 Issue 或 PR 改进

**你的评分对我们很重要！** 帮助更多人发现这个技能。

---

## 🔗 相关技能推荐

安装了这个技能的用户也安装了：

| 技能 | 作用 | 推荐度 |
|------|------|--------|
| [auto-backup](../auto-backup) | 自动备份 | ⭐⭐⭐⭐⭐ |
| [model-switch](../model-switch) | 模型切换 | ⭐⭐⭐⭐ |
| [search-pro](../search-pro) | 联网搜索 | ⭐⭐⭐⭐ |

**推荐组合安装：**
```bash
npx clawhub install openclaw-auto-backup
npx clawhub install openclaw-model-switch
npx clawhub install openclaw-search-pro
```

---


强大的记忆管理工具，让 AI 记住所有重要信息。

[English Version](README_EN.md)

---

## ✨ 功能特性

- 🔍 **语义搜索** - 搜索所有记忆文件
- 📌 **自动提炼** - 自动提炼对话要点
- 🏷️ **智能分类** - 偏好/决策/待办/项目
- 🔗 **关联推荐** - 推荐相关记忆
- 🧹 **过期清理** - 自动清理过期记忆
- ⚡ **Token 优化** - 分析并优化 token 消耗（NEW!）

---

## 🚀 安装

```bash
cd ~/.openclaw/workspace/skills
# 技能已安装在：~/.openclaw/workspace/skills/memory-enhancer
chmod +x memory-enhancer/scripts/*.py
```

---

## 📖 使用

### 语义搜索

```bash
python3 memory-enhancer/scripts/search.py "飞书配置"
```

### 自动提炼

```bash
python3 memory-enhancer/scripts/summarize.py --session today
```

### Token 优化分析

```bash
# 分析当前 token 使用
python3 memory-enhancer/scripts/token-optimizer.py --analyze

# 生成优化建议
python3 memory-enhancer/scripts/token-optimizer.py --suggest

# 压缩旧记忆（保留最近 30 天）
python3 memory-enhancer/scripts/token-optimizer.py --compress --days 30

# 完整优化（分析 + 建议 + 压缩）
python3 memory-enhancer/scripts/token-optimizer.py --full
```

### 定时优化任务

```bash
# 启用定时任务
python3 memory-enhancer/scripts/scheduled-optimizer.py enable

# 查看状态
python3 memory-enhancer/scripts/scheduled-optimizer.py status

# 手动执行
python3 memory-enhancer/scripts/scheduled-optimizer.py analyze   # 分析
python3 memory-enhancer/scripts/scheduled-optimizer.py compress  # 压缩
python3 memory-enhancer/scripts/scheduled-optimizer.py suggest   # 建议

# 禁用定时任务
python3 memory-enhancer/scripts/scheduled-optimizer.py disable
```

**定时任务计划：**
- 每天早上 8 点：自动分析 token 使用
- 每周日凌晨 3 点：自动压缩旧记忆
- 每周一早上 8 点：生成优化建议

---

## 🛠️ 脚本列表

| 脚本 | 功能 |
|------|------|
| `search.py` | 语义搜索 |
| `summarize.py` | 自动提炼 |
| `classify.py` | 智能分类 |
| `token-optimizer.py` | Token 优化分析（NEW） |

---

## 📊 Token 优化功能

### 优化方向

| 优化项 | 预计节省 | 说明 |
|--------|---------|------|
| 智能上下文裁剪 | 30-50% | 只读取相关记忆片段 |
| 会话历史摘要 | 40-60% | 用摘要替代完整历史 |
| 记忆压缩 | 20-30% | 定期合并/压缩旧记忆 |
| Token 监控 | - | 统计 + 优化建议 |

### 使用示例

```bash
# 查看当前 token 使用统计
python3 memory-enhancer/scripts/token-optimizer.py

# 输出示例：
# 文件                    字符数      Token 数       行数
# MEMORY.md              1,878          469       91
# SESSION-STATE.md       1,734          433       71
# USER.md                  640          160       46
# 总计                   9,492        2,371
```

---

**作者：** @williamwg2025  
**版本：** 1.2.0（新增定时优化任务）

---

## 🔒 安全说明

### 文件写入 ⚠️
**本技能会写入文件：**
- **配置：** `skills/memory-enhancer/config/` (token-stats.json 等)
- **日志：** `skills/memory-enhancer/logs/` (optimizer-schedule.log)
- **清理：** 可能删除 `memory/` 目录下的旧文件

**只读：** MEMORY.md, SESSION-STATE.md, 会话历史

### 网络访问
- **不联网：** 所有操作本地执行

### 定时任务
- 需手动添加 cron 或使用 OpenClaw 内置 cron
- 建议先手动测试再启用

### 建议
1. 先运行 `--analyze` 测试
2. 确认输出符合预期
3. 启用定时任务前备份 `~/.openclaw/`

---

**作者：** @williamwg2025  
**版本：** 1.0.1  
**许可证：** MIT-0
