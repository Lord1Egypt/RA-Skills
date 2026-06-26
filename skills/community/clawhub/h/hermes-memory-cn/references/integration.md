# AGENTS.md 集成指南

在 AGENTS.md 的 Memory 部分添加以下内容：

```markdown
### 🧠 记忆系统（Hermes-Memory）

**后端：** SQLite + sqlite-vec + text2vec-base-chinese（768维本地embedding）
- 数据库：`memory/memory.db`
- CLI：`/opt/homebrew/bin/python3.12 memory/memdb.py`

**实时写入（每次回复后执行）：**
检查对话中有没有新的、值得长期记住的信息：
- 持仓变动（买了/卖了/加仓/减仓/清仓/止盈/止损）→ type=portfolio
- 策略相关（新策略/改策略/情绪周期/买点卖点）→ type=strategy
- 教训/纠正（用户纠正你/发现错误/踩坑）→ type=lesson, severity=high
- 偏好变化（以后用/记住/我喜欢/改用）→ type=preference
- 隐含信息（新方向/新项目/生活变化/决策）→ type=fact
- 重要决策 → type=fact

**执行方式：**
```bash
# 关键词匹配
/opt/homebrew/bin/python3.12 memory/memory_tool.py check "用户说的内容"
# 隐含信息直接写入
/opt/homebrew/bin/python3.12 memory/memdb.py add "内容" --type fact
# 建立实体关系
/opt/homebrew/bin/python3.12 memory/memdb.py relate "某科技股" "属于" "医药板块"
```

**回答问题前：** 涉及过往持仓、策略、教训、偏好，先 search 数据库。
**Cron：** 每晚23点执行 decay + export Markdown备份。
```

## Cron 配置

每晚23点的记忆整合 cron payload：

```
【记忆整合】执行以下步骤：
1. 运行 `/opt/homebrew/bin/python3.12 memory/memdb.py decay --days 30` 标记过期记忆
2. 运行 `/opt/homebrew/bin/python3.12 memory/memdb.py export --dir memory/entities` 同步Markdown备份
3. 检查 memory/daily/ 今天有无新日志，有则用 `memory_tool.py check` 提取关键信息
4. 更新 MEMORY.md 索引
5. 运行 `/opt/homebrew/bin/python3.12 memory/memdb.py stats` 确认数据完整
```
