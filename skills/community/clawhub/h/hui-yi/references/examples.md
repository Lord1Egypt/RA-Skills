# Cold Memory Examples

用在：需要快速参考一个合格 note 长什么样。

---

## Example 1 — experience

```markdown
# Migrating Postgres with zero downtime

## TL;DR
- 用 logical replication，不用 pg_dump
- cutover 可压到约 2 分钟

## Memory type
- experience

## Importance
- high

## Semantic context
如果有人在做生产库迁移并且想最小化停机，这条 note 解释为什么 logical replication 更合适。

## Triggers
- postgres migration
- logical replication

## Use this when
- 规划生产数据库迁移
- 对比 pg_dump 和 replication

## Decisions / lessons
- DO: 提前同步 sequences
- DO: 先在 staging 演练
- AVOID: 对大库直接用 pg_dump 做零停机迁移

## Memory state
- warm

## Review cadence
- interval_days: 4
- review_count: 2
- review_success: 2
- review_fail: 0
- retrieval_count: 2
- reinforcement_count: 2

## Last seen
- 2025-03-15

## Last reviewed
- 2025-03-15

## Next review
- 2025-03-19

## Confidence
- high

## Last verified
- 2025-03-15

## Related tags
- postgres
- migration
- devops
```

---

## Example 2 — fact

```markdown
# Internal API rate limits

## TL;DR
- 支付和用户服务的固定速率限制
- 设计批任务前先看这条

## Memory type
- fact

## Importance
- medium

## Semantic context
如果有人在设计 batch job、load test 或排查 429，这条 note 给出稳定的 rate limit 信息。

## Triggers
- rate limit
- 429 error

## Use this when
- 设计批量请求
- 排查 429

## Key facts
- Payment API: 500 req/s
- User service: 2000 req/s
- Auth service: 100 req/s

## Memory state
- cold

## Review cadence
- interval_days: 30
- review_count: 5
- review_success: 5
- review_fail: 0
- retrieval_count: 5
- reinforcement_count: 3

## Last seen
- 2025-02-20

## Last reviewed
- 2025-02-20

## Next review
- 2025-03-22

## Confidence
- medium

## Last verified
- 2025-02-20

## Related tags
- api
- rate-limit
- infrastructure
```

---

## Example 3 — background

```markdown
# Project Atlas — architecture history

## TL;DR
- Atlas 从 monolith 演进到 4 个服务
- 当前主要痛点是服务间延迟

## Memory type
- background

## Importance
- high

## Semantic context
如果有人在做 Atlas 架构决策、onboarding、或者考虑重新合并服务，这条 note 提供历史背景和决策理由。

## Triggers
- atlas architecture
- service split decision

## Use this when
- 做新架构决策
- onboarding
- 评估是否合并服务

## Memory state
- warm

## Confidence
- high

## Last verified
- 2025-04-01

## Related tags
- atlas
- architecture
- microservices
```

---

## Example 4 — dormant

```markdown
# Legacy vendor PDF export workaround

## TL;DR
- 老供应商导出链路的历史 workaround
- 仅罕见支持场景再看

## Memory type
- experience

## Importance
- low

## Semantic context
如果有人在处理极少见的旧导出链路问题，这条 note 还能用；平时不该主动浮出来。

## Triggers
- vendor pdf export legacy

## Use this when
- 处理历史遗留支持问题

## Memory state
- dormant

## Review cadence
- interval_days: 365
- review_count: 7
- review_success: 7
- review_fail: 0
- retrieval_count: 8
- reinforcement_count: 5

## Last seen
- 2025-01-15

## Last reviewed
- 2025-01-15

## Next review
- 2026-01-15

## Confidence
- low

## Last verified
- 2025-01-15

## Related tags
- legacy
- workaround
- vendor
```

---

## 快速判断

- `fact`：短、稳、直接可复用
- `experience`：最值钱，重点写 lesson
- `background`：给未来做综合判断
- 多次被证明有用的 note 会逐步形成 `strong memory`
- `dormant`：已经充分巩固后进入长周期归档，不是失败后的降级

一句话：

**好 note 不是写得多，而是以后真能被准时想起来。**
