---

name: postgres-job-queue
slug: postgres-job-queue
displayName: "Postgres Job Queue"
version: 1.0.1
summary: "基于关系型数据库的作业"
description: "基于关系型数据库的作业队列,优先级/批量认领/进度跟踪。关系型数据库-based job queue with priority scheduling, batch claiming,。触发关键词: based, priority, 关系型数据库, job, queue, postgres。提供专业能力支持,覆盖多场景工作流,支持自动化处理。"
license: "MIT"
tools:
  - read
tags:
  - jobs
  - err
  - job
  - default
  - status
category: "Creative"
pricing_tier: "L2-标准级"

---

> **功能说明**: 本技能涵盖 自动化处理、专业能力支持、认领/进度跟踪、化处理 等核心能力。

# Postgres Job Queue

Production-ready job queue using 关系型数据库 with priority scheduling, batch claiming, and progress tracking.

---

## When to Use

* Need job queue but want to avoid Redis/RabbitMQ dependencies
* Jobs need priority-based scheduling
* Long-running jobs need progress visibility
* Jobs should survive service restarts

---

## Schema Design

```sql
CREATE TABLE jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_type VARCHAR(50) NOT NULL,
    priority INT NOT NULL DEFAULT 100,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    data JSONB NOT NULL DEFAULT '{}',

    -- Progress tracking
    progress INT DEFAULT 0,
    current_stage VARCHAR(100),
    events_count INT DEFAULT 0,

    -- Worker tracking
    worker_id VARCHAR(100),
    claimed_at TIMESTAMPTZ,

    -- Timing
    created_at TIMESTAMPTZ DEFAULT NOW(),
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,

    -- Retry handling
    attempts INT DEFAULT 0,
    max_attempts INT DEFAULT 3,
    last_error TEXT,

    CONSTRAINT valid_status CHECK (
        status IN ('pending', 'claimed', 'running', 'completed', 'failed', 'cancelled')
    )
);

-- Critical: Partial index for fast claiming
CREATE INDEX idx_jobs_claimable ON jobs (priority DESC, created_at ASC)
    WHERE status = 'pending';
CREATE INDEX idx_jobs_worker ON jobs (worker_id)
    WHERE status IN ('claimed', 'running');
```

---

## Batch Claiming with SKIP LOCKED

```sql
CREATE OR REPLACE FUNCTION claim_job_batch(
    p_worker_id VARCHAR(100),
    p_job_types VARCHAR(50)[],
    p_batch_size INT DEFAULT 10
) RETURNS SETOF jobs AS $$
BEGIN
    RETURN QUERY
    WITH claimable AS (
        SELECT id
        FROM jobs
        WHERE status = 'pending'
          AND job_type = ANY(p_job_types)
          AND attempts < max_attempts
        ORDER BY priority DESC, created_at ASC
        LIMIT p_batch_size
        FOR UPDATE SKIP LOCKED  -- Critical: skip locked rows
    ),
    claimed AS (
        UPDATE jobs
        SET status = 'claimed',
            worker_id = p_worker_id,
            claimed_at = NOW(),
            attempts = attempts + 1
        WHERE id IN (SELECT id FROM claimable)
        RETURNING *
    )
    SELECT * FROM claimed;
END;
$$ LANGUAGE plpgsql;
```

---

## Go Implementation

```go
const (
    PriorityExplicit   = 150  // User-requested
    PriorityDiscovered = 100  // System-discovered
    PriorityBackfill   = 30   // Background backfills
)

type JobQueue struct {
    db       *pgx.Pool
    workerID string
}

func (q *JobQueue) Claim(ctx context.Context, types []string, batchSize int) ([]Job, error) {
    rows, err := q.db.Query(ctx,
        "SELECT * FROM claim_job_batch($1, $2, $3)",
        q.workerID, types, batchSize,
    )
    if err != nil {
        return nil, err
    }
    defer rows.Close()

    var jobs []Job
    for rows.Next() {
        var job Job
        if err := rows.Scan(&job); err != nil {
            return nil, err
        }
        jobs = append(jobs, job)
    }
    return jobs, nil
}

func (q *JobQueue) Complete(ctx context.Context, jobID uuid.UUID) error {
    _, err := q.db.execute(ctx, `
        UPDATE jobs
        SET status = 'completed',
            progress = 100,
            completed_at = NOW()
        WHERE id = $1`,
        jobID,
    )
    return err
}

func (q *JobQueue) Fail(ctx context.Context, jobID uuid.UUID, errMsg string) error {
    _, err := q.db.execute(ctx, `
        UPDATE jobs
        SET status = CASE
                WHEN attempts >= max_attempts THEN 'failed'
                ELSE 'pending'
            END,
            last_error = $2,
            worker_id = NULL,
            claimed_at = NULL
        WHERE id = $1`,
        jobID, errMsg,
    )
    return err
}
```

---

## Stale Job Recovery

```go
func (q *JobQueue) RecoverStaleJobs(ctx context.Context, timeout time.Duration) (int, error) {
    result, err := q.db.execute(ctx, `
        UPDATE jobs
        SET status = 'pending',
            worker_id = NULL,
            claimed_at = NULL
        WHERE status IN ('claimed', 'running')
          AND claimed_at < NOW() - $1::interval
          AND attempts < max_attempts`,
        timeout.String(),
    )
    if err != nil {
        return 0, err
    }
    return int(result.RowsAffected()), nil
}
```

---

## Decision Tree

| Scenario | Approach |
| --- | --- |
| Need guaranteed delivery | 关系型数据库 queue |
| Need sub-ms latency | Use Redis instead |
| < 1000 jobs/sec | 关系型数据库 is fine |
| > 10000 jobs/sec | Add Redis layer |
| Need strict ordering | Single worker per type |

---

## Related Skills

* **Related:** service-layer-architecture — Service patterns for job handlers
* **Related:** realtime/dual-stream-architecture — Event publishing from jobs

---

## NEVER Do

* **NEVER use SELECT then UPDATE** — Race condition. Use SKIP LOCKED.
* **NEVER claim without SKIP LOCKED** — Workers will deadlock.
* **NEVER store large payloads** — Store references only.
* **NEVER forget partial index** — Claiming is slow without it.

## 前置条件
### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent( Code / Cursor / Codex /  CLI等)
- **操作系统**: Windows / macOS / Linux

### 依赖说明
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
- 本Skill基于Markdown指令,无需额外API Key(除内容中明确标注的外部API)

### 可用性分类
- **分类**: MD+execute(纯Markdown指令,部分功能需要exec命令行执行能力)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent执行任务

## 功能能力
- 关系型数据库-based job queue with priority scheduling, batch claiming,
  and progress tracking
- 触发关键词: based, priority, 关系型数据库, job, queue, postgres

## 快速入门指引
1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

## 应用场景
| 场景 | 输入 | 输出 |
|------|------|------|
| 基础使用 | 用户请求 | 处理结果 |

**不适用于**：需要人工判断的复杂决策场景

## 示例

### 示例1：基础用法

```
# 请参考上方使用说明进行配置和调用
result = "ready"
```

## 异常应对
| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 检查网络连接后重试，参考国内替代方案 |

## 疑问解答
### Q1: 如何开始使用Postgres Job Queue？
A: 请先阅读使用流程章节，确认环境满足依赖说明中的要求。

### Q2: 遇到错误怎么办？
A: 请参考错误处理章节，按照表格中的处理方式操作。

### Q3: Postgres Job Queue有什么限制？
A: 请参考已知限制章节了解具体限制。

## 注意事项
- 需要API Key，无Key环境无法使用
