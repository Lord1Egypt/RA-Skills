# Cost Control

## Where tokens actually go (OpenClaw reality)

Most spend is in **cacheWrite + cacheRead**, not raw input/output.
Cache tokens cost ~10% of input tokens — so high cache hit rate = low real cost.

### Healthy metrics
- Cache hit rate > 70%: ✅ costs well-controlled
- Cache hit rate 40-70%: 🟡 room to improve
- Cache hit rate < 40%: ⚠️ too many new sessions being created

### How to check
```python
# ~/.openclaw/agents/*/sessions/*.jsonl
# Look for: u.get('cacheRead') / (u.get('input') + u.get('cacheRead'))
```

## Model routing (tiered)

| Task | Tier | Notes |
|------|------|-------|
| Simple fetch, format, notify | Cheapest (e.g. qwen-plus) | Sports results, reminders, weather |
| 固定流程任务（文章总结、写文件、数据抓取、脚本执行） | qwen-plus | 中文友好 + 省 token，质量足够 |
| 中文内容处理（总结/改写/整理） | qwen-plus | 比 claude 更懂中文语境 |
| Analysis, writing, reasoning | Mid (e.g. sonnet) | Self-improvement, strategy docs |
| Complex multi-step | High (e.g. opus) | Only when mid fails repeatedly |

**Rule:** Start with cheapest. Upgrade only when task repeatedly fails or quality matters critically.

**分工原则（2026-03-27 Paolo 确认）：**
- 主 session（claude）：判断、调度、与 Paolo 对话
- 子 agent（qwen-plus）：所有固定流程 + 中文友好型任务，用 `sessions_spawn` 派发
- 典型场景：微信文章总结、Obsidian 写入、脚本执行结果格式化、cron 数据推送

## Session discipline

Each new session = new cache write = higher cost.

Reduce session sprawl:
- Don't create isolated sessions for simple tasks
- Reuse main session for interactive work
- Use `sessionTarget: isolated` only for true fire-and-forget cron jobs

## Context discipline

Large context = expensive heartbeats.

Keep these files lean:
- `HEARTBEAT.md`: < 30 lines of active rules only
- `AGENTS.md`: startup rules, not runbooks
- `SOUL.md`: personality, not procedures
- Move long docs to `references/` (loaded on demand)

## Cron cost profile

Cheapest cron pattern:
```
Script pre-computes → 0 tokens if no output
Script has output → ~500-1000 tokens total
```

Expensive cron anti-pattern:
```
Long prompt with embedded logic → 2000+ tokens setup
+ LLM reasons through it → 1000+ output tokens
+ Every run regardless of outcome
```

## Weekly token audit

Run `scripts/token_report.py` every Monday to:
- See per-day and per-model breakdown
- Catch anomalies (single-day spike > 3x average)
- Track cache hit rate trend

If single day > 3x recent average: investigate immediately (runaway cron? loop?).

## Cron model audit (2026-03-28 实战经验)

**所有 cron 任务的模型分工原则（已验证）：**

| 任务类型 | 模型 | sessionTarget |
|---------|------|--------------|
| 脚本执行 + 结果转发 | gemini-2.0-flash-lite | isolated |
| 数据抓取 + 简短推送 | qwen-plus 或 gemini-2.0-flash-lite | isolated |
| 自我分析 / 日志读写 | qwen-plus | isolated |
| 周复盘 / cron 状态检查 | gemini-2.5-flash | isolated |
| systemEvent 类提醒 | 不消耗 AI token | main |

**已知兼容性问题（2026-03-28 确认）：**
- `gemini-2.0-flash-lite` 和 `gemini-2.5-flash` 在带 **nodes.run 工具调用**的 isolated cron session 中均返回 `400 status code (no body)`
- `gemini-2.5-flash` (preview) 作为主模型时 compaction 触发 400
- **结论：Gemini 所有版本不适合用于含 nodes.run 的 cron 任务**
- **安全替代**：nodes.run 类任务统一用 `dashscope/qwen-plus`，稳定无报错（已验证）
- Gemini 仅适合：纯文本生成、web_search、不含工具调用的简单任务

**关键发现：**
- `sessionTarget: main` 的 `agentTurn` 任务会消耗主 session Claude token，改为 `isolated` 可完全隔离成本
- `systemEvent` 类型任务本身不跑 AI，只注入文字，不需要优化
- 唯一需要 Claude 的场景：**和 Paolo 的直接对话**

**Timeout 设定经验：**
- nodes.run 执行 Python 脚本：60s 经常不够，建议 **90s**
- 纯网页抓取：60s 有时卡死，建议 **90s**
- 简单 API 调用：30s 足够

**主模型选择（2026-03-28 确认）：**
- 主 session 默认模型：`renlijia/claude-sonnet-4-6`（不用 Gemini 做主模型，压缩 API 兼容性问题）
- Gemini 2.5 Flash 做 fallback 或指定 cron 任务使用
- Gemini 作为主模型时，`compaction.mode: safeguard` 会触发 400 报错（preview 模型兼容性问题）

## Persistent cost reduction goals (Paolo, 2026-03-28)

Paolo 明确要求：**持续降低 token 消耗和使用成本**。

执行原则：
1. 每周一 Token 周报中附带优化建议（已有 cron）
2. 新增 cron 任务时默认选最便宜够用的模型，不默认 Claude
3. 定期（每月）审查所有 cron，清理僵尸任务、合并相似任务
4. 主对话保留 Claude，其他一切能省则省
