# HEARTBEAT.md — Instant Genius 追加内容
# 将以下内容追加到 HEARTBEAT.md 的适当位置

## 🧠 Self-Improving Check (Instant Genius)

- 读 `./skills/instant-genius/references/learning-signals.md` 了解规则
- 用 `~/self-improving/heartbeat-state.md` 追踪上次运行
- 如果 `~/self-improving/` 中没有文件变更，跳过
- 如有变更：刷新 index.md、整理过大的文件、合并重复条目
- 不确认不删除任何数据

## 📝 Memory Maintenance (Instant Genius)

每 3-5 天一次心跳时：

1. 扫描最近的 `memory/YYYY-MM-DD.md` 文件
2. 识别值得长期保留的事件、教训、洞察
3. 更新 `MEMORY.md`（精选提炼，不是全搬）
4. 删除 MEMORY.md 中过时的信息
5. 更新 `~/self-improving/index.md` 的行数统计

## 🚀 Proactive Value Discovery (Instant Genius)

心跳时检查（每周 2-3 次轮换）：

- 关注领域的新动态（AI、工具、框架）
- ClawHub/GitHub 上的高质量新 skill
- 用户项目相关的工具更新
- 任何对用户真正有用的东西

**通知条件**：
- 发现确实有趣且对用户有用时才通知
- 遵守冷却规则（间隔 ≥ 2 小时）
- 23:00-09:00 不发

**通知格式**（简洁，不废话）：
```
💡 发现一个有趣的东西：[一句话说明]
[为什么对你有用]
[链接/下一步]
```

## 🔄 Autonomy Observation (Optional)

如果你有 autonomy 引擎，心跳时记录：
```json
{"ts": "ISO时间", "actions_24h": N, "blocked": N, "pending_notify": N, "notes": "..."}
```
