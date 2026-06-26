# Design Pattern Reference

## Fork-Join (Parallel Processing)

Multiple child Agents process sharded tasks in parallel, with results aggregated before replying to the user.

```
Main Agent
  ├─ spawn analyzer-1 (Shard A) ──→ [1. announcement]
  ├─ spawn analyzer-2 (Shard B) ──→ [2. announcement]
  └─ spawn analyzer-3 (Shard C) ──→ [3. announcement]
                                      ↓
                              Aggregate results → Reply to user
```

**Applicable Scenarios:** Parallel data analysis, large file shard processing, batch review.

## Master-Worker (Master-Slave Collaboration)

Create persistent expert Agents; the main Agent queries each expert and synthesizes their opinions.

```javascript
// 1. Create expert Agents (persistent)
sessions_spawn({ agent: "security-expert", label: "security", mode: "session" });
sessions_spawn({ agent: "perf-expert",     label: "performance", mode: "session" });

// 2. Main Agent queries the experts
const security = await sessions_send({ label: "security", message: "Are there any security risks?" });
const perf = await sessions_send({ label: "performance", message: "Where are the performance bottlenecks?" });

// 3. Synthesize expert opinions
return synthesize(security, perf);
```

**Applicable Scenarios:** Code requires both security and performance reviews, multi-dimensional evaluation.

## Pipeline (Assembly Line)

At each stage, spawn an Agent; the output of one serves as the input for the next, akin to a factory assembly line.

```
PDF → Extractor ─→ Raw Text → Cleaner ─→ Clean Text → Summarizer ─→ Summary
     (spawn)                     (spawn)                     (spawn)
```

**Applicable Scenarios:** Data processing pipelines, multi-stage content refinement.

## Comparative Summary

| Pattern | Spawn Count | Parallel | Communication Method | Typical Scenario |
|---------|-------------|----------|----------------------|------------------|
| Fork-Join | N in parallel | ✅ | announcement | Parallel data analysis |
| Master-Worker | N persistent | ❌ | sessions_send | Expert collaboration |
| Pipeline | N sequential | ❌ | announce chaining | Multi-stage processing |