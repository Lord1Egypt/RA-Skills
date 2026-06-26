# Heartbeat Cooling Playbook

用在：定期 cooling、heartbeat 维护、整理 daily notes。

---

## 目标

Cooling 不只是“归档”，还要顺手决定：
- 什么值得进 cold memory
- 什么只是普通记录
- 什么未来值得 resurfacing

---

## 什么时候跑

- 默认：每周一次
- 或者：积累了 5+ 条 daily notes
- 或者：用户明确要求 archive / cool / cleanup

先看：
- `memory/heartbeat-state.json`
- `coldMemory.lastArchive`

---

## 预检查

如果 helper 可用，先跑：

```bash
python3 skills/hui-yi/scripts/cool.py scan
```

没有 helper 就手工看最近 `memory/YYYY-MM-DD*.md`。

---

## 四步流程

### Pass 1：筛选

逐条看 recent daily notes，问三件事：

1. 这是低频高价值吗？
2. 30 天后还值得留吗？
3. 它是一个 memory unit 吗，而不是一个零散词或临时碎片？

都满足再继续。

### Pass 2：路由

按类型放对地方。

> 注意：下表是给 agent 的**路由建议**，由 agent 在主记忆层（OpenClaw 侧）按用户授权执行。
> Hui-Yi 自身的脚本只读写 `memory/cold/` 和 `memory/heartbeat-state.json`，
> 从不直接写 `MEMORY.md`、`TOOLS.md`、`.learnings/`、`AGENTS.md`、`SOUL.md`。

| 内容 | 去哪 |
|---|---|
| 高频背景 | `MEMORY.md` |
| 工具/路径/环境坑 | `TOOLS.md` |
| 新错误、新纠正 | `.learnings/` |
| 工作规则/行为规则 | `AGENTS.md` / `SOUL.md` |
| 低频长期知识 | `memory/cold/` |

### Pass 3：写 cold note

1. 先查 `index.md` 是否已有同主题 note
2. 有就 merge，没有就新建
3. 压缩噪音，保留：
   - stable facts
   - lessons
   - rationale
   - decision context
4. 设好：
   - importance
   - state
   - last_seen
   - next_review（必要时）

默认建议：
- 重要且近期可能复用 → `warm`
- 稳定参考资料 → `cold`
- 很少用但不能丢 → `dormant`

### Pass 4：轻维护

如果有时间，再做：
- merge 重复 note
- 降低 stale / noisy note 的权重
- 看 `retrieval-log.md`
  - 从没被召回的 note
  - 常无匹配的 query
  - 常被召回但没用的 note
  - 常被证明有用的 note

---

## 收尾

1. `python3 skills/hui-yi/scripts/rebuild.py`
   ⚠️  **必须跑**：`decay.py` 只修改 `.md` 文件，不更新 `tags.json` / `index.md`。
   如果这轮跑过 `decay.py`，rebuild 不能省略；或改用 `decay.py --rebuild` 合并两步。
2. `python3 skills/hui-yi/scripts/cool.py done <reviewed> <archived> <merged>`
3. 更新 heartbeat 状态
4. 除非用户问，不要主动汇报一大堆冷却结果

---

## 不要做的事

- 不要把整个 cold archive 全读一遍
- 不要把当天临时状态塞进 cold memory
- 不要创建大量近似 note
- 不要存 secrets
- 不要因为词频高就把内容当成长期记忆
- 不要编造过于精确的 review 数据

一句话：

**cooling 的目标不是多存，而是把以后真正可能有用的东西存准。**