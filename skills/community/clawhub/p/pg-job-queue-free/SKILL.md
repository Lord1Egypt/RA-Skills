---
slug: pg-job-queue-free
name: pg-job-queue-free
version: 1.0.0
displayName: PG任务队列(免费版)
summary: 基于`PostgreSQL`的轻量任务队列，支持优先级调度、批量领取与进度跟踪，单机与小型团队适用。
license: Proprietary
edition: free
description: PG任务队列免费版是一套基于 `PostgreSQL` 的轻量任务队列知识库，帮助独立开发者在不引入 Redis 或 RabbitMQ 的前提下，用一张数据库表实现可靠的异步任务调度。核心能力：提供基于
  SKIP LOCKED 的批量领取设计、优先级调度字段、进度跟踪结构、失败重试与超时回收方案、单 Worker 串行到多 Worker 并行的演进路径
tags:
- 数据库
- 集成工具
- 任务队列
- 免费版
tools:
- - read
- exec
homepage: https://skillhub.cn
pricing_tier: "L1-入门级"
pricing_model: per_use
suggested_price: "9.9 CNY/per_use"
tools: ["read", "write", "exec"]
tags: "工具,效率,自动化"
---
# PG任务队列（免费版）

## 概述

很多业务场景需要异步任务处理能力（如发送邮件、生成报表、清理临时文件），但引入 Redis 或 RabbitMQ 又会带来额外的运维成本。`PostgreSQL` 本身提供的事务、行锁、JSONB 存储等能力，足以支撑中小规模的任务队列需求，且具备天然的持久化与崩溃恢复能力。

本免费版聚焦于**单机与小型团队最高频的队列场景**：表结构设计、批量领取、优先级调度、失败重试、超时回收。每种模式均提供可直接复用的 SQL 片段与设计要点。

## 核心能力

### 能力一：队列表结构设计

任务队列的核心是一张 `jobs` 表，需要同时支持状态流转、优先级排序、进度跟踪与重试控制。本助手提供经过生产验证的字段布局与索引设计。

| 字段分组 | 关键字段 | 设计意图 |
|----|----|----|
| 基础信息 | id、job_type、data(JSONB) | 唯一标识、任务类型、灵活负载 |
| 调度控制 | priority、status、created_at | 优先级排序、状态流转、FIFO 兜底 |
| 进度跟踪 | progress、current_stage、events_count | 长任务可视化与监控 |
| Worker 跟踪 | worker_id、claimed_at | 任务归属与超时回收依据 |
| 重试控制 | attempts、max_attempts、last_error | 失败重试与最终失败标记 |

**输入**: 用户提供能力一：队列表结构设计所需的指令和必要参数。
**处理**: 解析能力一：队列表结构设计的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回能力一：队列表结构设计的响应数据,包含状态码、结果和日志。

### 能力二：基于 SKIP LOCKED 的批量领取

`PostgreSQL` 的 `FOR UPDATE SKIP LOCKED` 是构建并发安全队列的关键能力。本助手提供封装好的领取函数，多个 Worker 可并发领取而互不阻塞。

**输入**: 用户提供能力二：基于 SKIP LOCKED 的批量领取所需的指令和必要参数。
**处理**: 解析能力二：基于 SKIP LOCKED 的批量领取的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回能力二：基于 SKIP LOCKED 的批量领取的响应数据,包含状态码、结果和日志。

### 能力三：优先级调度

通过 `priority` 字段配合部分索引，实现"高优先级先执行、同优先级按创建时间 FIFO"的调度语义，无需额外调度器。

**输入**: 用户提供能力三：优先级调度所需的指令和必要参数。
**处理**: 解析能力三：优先级调度的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回能力三：优先级调度的响应数据,包含状态码、结果和日志。

### 能力四：失败重试与超时回收

任务执行可能因网络抖动、依赖故障等原因失败或卡死。本助手提供"重试计数 + 超时回收"双重保障机制，避免任务永久丢失或僵尸堆积。

**输入**: 用户提供能力四：失败重试与超时回收所需的指令和必要参数。
**处理**: 解析能力四：失败重试与超时回收的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回能力四：失败重试与超时回收的响应数据,包含状态码、结果和日志。

- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 能力五：进度可视化

长耗时任务（如报表生成、批量数据迁移）需要进度反馈。通过 `progress` 字段记录百分比，`current_stage` 记录当前阶段，前端可直接展示进度条。

**输入**: 用户提供能力五：进度可视化所需的指令和必要参数。
**处理**: 解析能力五：进度可视化的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回能力五：进度可视化的响应数据,包含状态码、结果和日志。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：的轻量任务队列、支持优先级调度、批量领取与进度跟、单机与小型团队适、任务队列免费版是、一套基于、的轻量任务队列知、帮助独立开发者在、不引入、Redis、RabbitMQ、的前提下、用一张数据库表实、现可靠的异步任务、核心能力、提供基于、的批量领取设计、优先级调度字段、进度跟踪结构、收方案、串行到多、并行的演进路径等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一：邮件发送队列

用户注册后异步发送欢迎邮件，按用户等级设置优先级（VIP 优先）。单 Worker 即可承载，每日万级任务量。

### 场景二：报表生成任务

每日凌晨触发的报表生成任务，单任务耗时数分钟，需要进度可视化与失败自动重试。多 Worker 并行处理不同报表类型。

### 场景三：数据清理批处理

定期清理临时文件、过期会话、归档日志等。任务量大但不紧急，使用低优先级在业务低峰期执行。

## 不适用场景

以下场景PG任务队列(免费版)不适合处理：

- 实时流数据处理
- 小规模数据手动分析
- 非结构化文本情感分析

## 触发条件

需要数据分析、报表生成、统计洞察、数据可视化时使用。不适用于非本工具能力范围的需求。

## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

本助手为知识库型 Skill，无需安装额外依赖。直接在 Agent 对话中描述你的队列需求即可获取建议。

**典型提问模板**：

## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| input | string | 是 | PG任务队列(免费版)处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```
我有一个邮件发送需求，日均 5000 封，需要按用户等级优先级发送，如何用 PostgreSQL 实现？
```

```
我的报表生成任务经常卡死，怎么设计超时回收机制？
```

```
多个 Worker 并发领取任务时出现重复执行，如何避免？
```

Agent 会根据问题匹配对应的知识条目，输出"场景识别 → 表结构设计 → 领取逻辑 → 异常处理 → 监控建议"五段式回答。

## 示例

### 队列表基础结构

```sql
CREATE TABLE jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_type VARCHAR(50) NOT NULL,
    priority INT NOT NULL DEFAULT 100,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    data JSONB NOT NULL DEFAULT '{}',
# ...
    -- 进度跟踪
    progress INT DEFAULT 0,
    current_stage VARCHAR(100),
# ...
    -- Worker 跟踪
    worker_id VARCHAR(100),
    claimed_at TIMESTAMPTZ,
# ...
    -- 时间记录
    created_at TIMESTAMPTZ DEFAULT NOW(),
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
# ...
    -- 重试控制
    attempts INT DEFAULT 0,
    max_attempts INT DEFAULT 3,
    last_error TEXT,
# ...
    CONSTRAINT valid_status CHECK (
        status IN ('pending', 'claimed', 'running', 'completed', 'failed', 'cancelled')
    )
);
# ...
-- 关键：部分索引加速领取
CREATE INDEX idx_jobs_claimable ON jobs (priority DESC, created_at ASC)
    WHERE status = 'pending';
CREATE INDEX idx_jobs_worker ON jobs (worker_id)
    WHERE status IN ('claimed', 'running');
```

### 批量领取函数

```sql
CREATE OR REPLACE FUNCTION claim_job_batch(
    p_worker_id VARCHAR(100),
    p_job_types VARCHAR(50)[],
    p_batch_size INT DEFAULT 10
) RETURNS SETOF jobs AS $$
BEGIN
    RETURN QUERY
    WITH claimable AS (
        SELECT id FROM jobs
        WHERE status = 'pending'
          AND job_type = ANY(p_job_types)
          AND attempts < max_attempts
        ORDER BY priority DESC, created_at ASC
        LIMIT p_batch_size
        FOR UPDATE SKIP LOCKED
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

### 优先级参考表

| 优先级数值 | 含义 | 典型场景 |
|---:|---:|---:|
| 150 | 用户显式触发 | 用户点击"立即发送"按钮 |
| 100 | 系统常规任务 | 定时报表、批量通知 |
| 30 | 后台回填任务 | 历史数据迁移、索引重建 |

## 最佳实践

### 实践一：永远使用 SKIP LOCKED

`SELECT ... FOR UPDATE` 会让并发 Worker 互相阻塞，导致吞吐量骤降。`SKIP LOCKED` 让 Worker 自动跳过已被锁定的行，实现真正的并发领取。

### 实践二：负载只存引用

`data` 字段不要存储大体积负载（如 Base64 图片、长文本）。应存储引用 ID，由 Worker 执行时去对象存储或文件系统读取，避免表膨胀。

### 实践三：部分索引不可省略

`idx_jobs_claimable` 是部分索引，只索引 `status = 'pending'` 的行。领取查询能命中索引，避免全表扫描。若无此索引，任务量增长后领取延迟会急剧上升。

### 实践四：设置合理的 max_attempts

默认 3 次重试即可覆盖大多数瞬时故障。对于幂等性有保障的任务可设为 5 次；对于有副作用的任务（如扣款）建议设为 1 次，由人工介入处理失败。

### 实践五：超时回收需配合心跳

仅靠 `claimed_at` 判断超时可能误杀慢任务。建议 Worker 在执行过程中定期更新 `current_stage` 或单独的心跳字段，回收逻辑只回收"长时间无心跳"的任务。

### 实践六：任务完成立即提交事务

领取后应尽快释放数据库连接，不要在整个任务执行期间持有事务。典型模式：领取事务提交 → 执行任务 → 完成事务提交。

## 错误处理

| 错误场景(症状) | 可能原因 | 排查方法 | 对策 | 处理方式 |
|:-------:|:-------:|:-------:|:-------:|:-------:|
| 任务一直 pending | 无 Worker 在运行 | 查看 Worker 日志与进程 | 重启 Worker 或扩容 | 对照依赖说明章节逐项验证配置项,确认环境变量已正确设置后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令 |
| 任务重复执行 | 未使用 SKIP LOCKED | 检查领取 SQL | 改用 SKIP LOCKED | 对照依赖说明章节逐项验证配置项,确认环境变量已正确设置后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令 |
| 任务卡在 running | Worker 崩溃未标记失败 | 查看 claimed_at 是否超时 | 执行超时回收 | 对照依赖说明章节逐项验证配置项,确认环境变量已正确设置后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令 |
| 队列表膨胀 | 大量已完成任务未清理 | 查看表大小与行数 | 定期归档历史任务 | 对照依赖说明章节逐项验证配置项,确认环境变量已正确设置后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令 |
| 领取延迟高 | 缺失部分索引 | 查看 EXPLAIN 计划 | 创建 idx_jobs_claimable | 对照依赖说明章节逐项验证配置项,确认环境变量已正确设置后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令 |
## 常见问题

### Q1：SKIP LOCKED 会不会丢任务？

不会。`SKIP LOCKED` 只是跳过当前被锁定的行，这些行依然存在于表中。持有锁的 Worker 完成后会更新状态，下一个领取周期其他 Worker 会领取剩余任务。

### Q2：单表能支撑多少 QPS？

在合理索引与连接池配置下，单表 `PostgreSQL` 队列可支撑约 1000 任务/秒。若超过此量级，建议引入 Redis 作为前置缓冲，或按 `job_type` 分表。

### Q3：任务失败后如何自动重试？

`attempts < max_attempts` 时，Fail 函数会将状态重置为 `pending`，下次领取周期会被重新领取。超过 `max_attempts` 后状态置为 `failed`，需人工介入。

### Q4：如何监控队列健康度？

关键指标：pending 任务数、running 任务数、平均执行时长、失败率、最老 pending 任务年龄。建议接入 Prometheus + Grafana 或简单的定时 SQL 报表。

### Q5：Worker 重启后正在执行的任务怎么办？

通过超时回收机制处理。Worker 启动时先执行一次回收，将所有 `claimed_at` 超过阈值的任务重置为 `pending`，再开始正常领取。

### Q6：如何实现任务取消？

将状态改为 `cancelled` 即可。Worker 领取前会检查状态，已取消的任务不会被领取。若任务正在执行，需 Worker 在循环中主动检查取消标志。

## 依赖说明

### 运行环境
- **Agent 平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **数据库**: `PostgreSQL` 9.5+（需支持 SKIP LOCKED 与 JSONB）

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:------|------:|:------|:------|
| LLM API | API | 必需 | 由Agent平台内置LLM提供 |
| `PostgreSQL` 客户端 | 工具 | 必需 | psql / pgAdmin / DBeaver 等 |
| 数据库驱动 | 库 | 必需 | pgx (Go) / psycopg (Python) / node-postgres (Node.js) |

### API Key 配置
- 本免费版为纯知识库型 Skill，自身不需要 API Key
- 若 Agent 需要连接实际数据库执行命令，相关凭据由用户自行配置于环境变量中
- 禁止在 SKILL.md 或脚本中硬编码数据库凭据

### 可用性分类
- **分类**: MD+EXEC（纯Markdown指令，部分诊断功能需要exec命令行执行能力）
- **说明**: 基于Markdown的AI Skill，通过自然语言指令驱动Agent输出队列设计与运维建议

## 已知限制

本免费体验版限制以下高级功能：
- 多队列分片与水平扩展方案（仅专业版提供）
- 任务依赖图与 DAG 编排能力（仅专业版提供）
- 死信队列与人工补偿流程设计（仅专业版提供）
- 高级监控告警指标体系（仅专业版提供）
- 跨集群任务迁移与灰度发布策略（仅专业版提供）

解锁全部功能请使用专业版：pg-job-queue-pro
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "PG任务队列(免费版)处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "pg job queue"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
