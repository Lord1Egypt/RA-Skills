# OpenClaw Token 经济性审计方法论

**三层审计框架** — 用于系统性分析 OpenClaw 实例的 token 消耗根因

---

## 实测数据基准（2026-03-05）

| 类别 | Tokens | 成本 | 占比 |
|------|--------|------|------|
| Input（未缓存）| 6.4M | $64.64 | **82.6%** |
| Cache Read | 13.2M | $6.54 | 8.4% |
| Cache Write | 1.6M | $6.10 | 7.8% |
| Output | 79.5K | $0.97 | 1.2% |

**关键洞察**：Cache Read/Write = 8.2x（缓存本身健康），但 Input 未缓存占 82.6%，说明缓存机制存在根本性绕过。

---

## 三层根因框架

### Layer 1：架构层（高影响，低频变化）

**A1. System Prompt 体积漂移**

常驻 prompt 文件（SOUL.md、TOOLS.md、AGENTS.md）随时间积累非核心内容，每会话 token 消耗线性增长。

典型原因：
- 将修复记录、Debug 教训直接写入 SOUL.md
- 语义路由规则在 prompt 中重复声明（已由 message-injector 管理）
- 子代理 SOUL.md 包含模型配置表（应由 openclaw.json 管理）

**修复原则**：
- 核心身份/能力 → SOUL.md（≤6KB）
- 历史教训 → `memory/LESSONS/lessons.md`
- 路由规则 → message-injector extension（不在 prompt 中）
- 模型配置 → openclaw.json（不在 SOUL.md 中）

**A2. 多 Agent 乘数效应**

Full Coding Team（7 agent）= 7× system prompt 开销。每个子代理都带完整 system prompt 上下文。

建议触发分级：
| 规模 | 条件 | 启用策略 |
|------|------|---------|
| Nano | ≤3 文件改动 | 主代理直接（1× 开销）|
| Small | ≤500 行新模块 | 主代理 + QA（2× 开销）|
| Full | >500 行，3+ 域 | 完整 7 代理团队（7× 开销）|

---

### Layer 2：Extension/Skill 层（中影响，可程序化修复）

**B1. Cron Job 配置违规**

三类常见违规：
1. `sessionKey` 非 null → 历史对话污染，context 膨胀
2. 缺少 `timeoutSeconds` → 任务挂起，持续消耗
3. 使用 opus 系列模型 → 定时任务成本暴增 10-40x

**B2. LLM 侧缓存命中率低**

Anthropic prompt cache TTL = 5 分钟。以下操作会导致缓存失效：
- `sessions.patch` 频繁调用（即使模型未变）→ 解决：PATCH_CACHE_TTL = 30 分钟
- `prependContext` 每条消息不同（声明分数 0.97/0.98 变化）→ 解决：extractDeclKey() 过滤噪声

**B3. 孤儿 Session 积累**

`session_model_state.json` 中长期存在无活动 session，增加状态文件体积和 reconcile 扫描开销。建议每 7 天清理一次。

---

### Layer 3：使用习惯层（参考，需用户意识）

**C1. 模型选择**

定时任务、监控、轻量分析 → gemini-2.5-flash（成本约为 claude-opus 的 1/40）
代码生成、深度分析 → claude-sonnet / gemini-2.5-pro
复杂推理 → claude-opus（仅用于真正需要的场景）

**C2. 长会话未压缩**

对话历史积累 = 每轮 Input tokens 呈线性增长。
建议：session context 超过 50% 时触发 `/compact`，超过 70% 时强制压缩。

**C3. 自我监控任务的成本控制**

监控任务使用高成本模型 = 监控成本本身失控。
原则：监控/运维类任务永远使用最低成本模型（gemini-flash 等）。

---

## 修复优先级 ROI 排序

| 修复项 | 预期节省 | 难度 | 优先级 |
|--------|---------|------|------|
| Cron Job 合规（B1）| 中 | 低（自动修复）| ⭐⭐⭐⭐⭐ |
| System Prompt 瘦身（A1）| 高 | 中 | ⭐⭐⭐⭐ |
| PATCH_CACHE_TTL 延长（B2-M3）| 中 | 低（一行改动）| ⭐⭐⭐⭐ |
| prependContext 稳定（B2-M1）| 中高 | 中（需代码改动）| ⭐⭐⭐⭐ |
| 孤儿 Session 清理（B3）| 低 | 低（自动修复）| ⭐⭐⭐ |
| 压缩硬限制（C2）| 高 | 中 | ⭐⭐⭐ |
| Cron 任务合并（C3）| 中 | 中 | ⭐⭐⭐ |
| 触发分级（A2）| 高 | 低（规则约定）| ⭐⭐⭐ |

---

## 数据采集方法

```bash
# 获取过去 N 天的 token 消耗明细
openclaw gateway usage-cost --json --days 2

# 返回结构示例
{
  "daily": [{
    "date": "2026-03-05",
    "totalTokens": 21300000,
    "totalCost": 78.24,
    "inputTokens": 6400000,
    "cacheReadTokens": 13200000,
    "cacheWriteTokens": 1600000,
    "outputTokens": 79500
  }]
}
```

**关键指标**：
- `inputTokens / totalTokens` > 60% → system prompt 过大或缓存命中率低
- `cacheReadTokens / cacheWriteTokens` < 3x → 缓存利用率低（正常应 >5x）
- `totalCost / day` > $30 → 检查 cron job 模型配置

---

*本文档由 2026-03-05 OpenClaw token 经济性审计总结，适用于 OpenClaw v0.12+*
