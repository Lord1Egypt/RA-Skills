# 结论 Schema 规范

## 概述

本文档定义洞察挑战结论的结构化输出格式。该 schema 确保结果一致、机器可读，可供下游系统消费。机器校验由 `scripts/validate-verdict.mjs` 实现（零依赖，fail-closed），测试夹具见 `tests/fixtures/`。校验器对必填字段与类型违规返回错误（IC-V00~V13；IC-V11~V13 覆盖可选字段 `recommendation`、`metadata` 及批量外层字段 `batch_id`、`total_findings`、`summary` 的类型与计数约束）；证据期望未满足时返回警告（IC-W01：overturned 缺 counter_evidence、IC-W02：confirmed 缺 supporting_evidence、IC-W03：weakened 缺 counter_evidence），警告不改变 exit 码。

## 结论 JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["finding_id", "challenge_result", "confidence", "reasoning"],
  "properties": {
    "finding_id": {
      "type": "string",
      "description": "Original finding identifier"
    },
    "challenge_result": {
      "type": "string",
      "enum": ["overturned", "weakened", "confirmed"],
      "description": "Verdict of the challenge"
    },
    "confidence": {
      "type": "integer",
      "minimum": 0,
      "maximum": 100,
      "description": "Confidence score (0-100)"
    },
    "reasoning": {
      "type": "string",
      "description": "Detailed explanation of the verdict"
    },
    "counter_evidence": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Evidence that contradicts the finding"
    },
    "supporting_evidence": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Evidence that supports the finding"
    },
    "adjusted_severity": {
      "type": "string",
      "enum": ["none", "critical", "high", "medium", "low"],
      "description": "Recommended severity after challenge"
    },
    "recommendation": {
      "type": "string",
      "description": "Recommended action"
    },
    "metadata": {
      "type": "object",
      "properties": {
        "challenge_duration_ms": { "type": "integer" },
        "files_reviewed": { "type": "array", "items": { "type": "string" } },
        "design_docs_checked": { "type": "array", "items": { "type": "string" } },
        "challenge_strategies_applied": { "type": "array", "items": { "type": "string" } }
      }
    }
  }
}
```

## 字段定义

### finding_id
- **类型**: string
- **必填**: 是
- **描述**: 原始发现标识符（如 "HIGH-01"、"CRIT-03"）
- **示例**: "HIGH-01"

### challenge_result
- **类型**: string (enum)
- **必填**: 是
- **取值**:
  - `overturned`: 发现事实错误；源代码直接反驳主张
  - `weakened`: 发现部分正确但被夸大、范围错误或缺少上下文
  - `confirmed`: 发现准确；源代码支持所有主张

### confidence
- **类型**: integer (0-100)
- **必填**: 是
- **描述**: 挑战者对结论的置信度
- **分级**:
  - 90-100: 清晰、无歧义的证据
  - 70-89: 证据充分，有轻微不确定性
  - 50-69: 证据混合；需要判断
  - 低于 50: 证据不足

### reasoning
- **类型**: string
- **必填**: 是
- **描述**: 为何得出该结论的详细说明
- **应包含**:
  - 原始主张摘要
  - 发现了什么证据
  - 证据为何支持该结论
  - 任何注意事项或限制

### counter_evidence
- **类型**: array of strings
- **必填**: 否（但 overturned/weakened 期望有）
- **描述**: 反驳发现的具体证据
- **格式**: 每项应引用具体文件和行
- **示例**: ["src/types.ts line 64: 'resolves' IS declared in KnowledgeEdgeKind"]

### supporting_evidence
- **类型**: array of strings
- **必填**: 否（但 confirmed 期望有）
- **描述**: 支持发现的具体证据
- **格式**: 与 counter_evidence 相同

### adjusted_severity
- **类型**: string (enum)
- **必填**: 否
- **取值**:
  - `none`: 发现应完全驳回
  - `critical`, `high`, `medium`, `low`: 调整后的严重度级别
- **描述**: 考虑挑战证据后建议的严重度
- **默认**: 未指定时为原始严重度

### recommendation
- **类型**: string
- **必填**: 否
- **描述**: 建议的下一步行动
- **校验**: 出现时必须为非空 string，否则报 IC-V11
- **示例**:
  - "驳回此发现；声称的缺失不存在"
  - "降级为中严重度；问题存在但不如声称严重"
  - "确认并优先处理；发现准确且重要"

### metadata
- **类型**: object
- **必填**: 否
- **描述**: 挑战过程的额外上下文
- **校验**: 出现时必须为 object；已知子字段出现时按声明类型校验（`challenge_duration_ms` 为 integer，其余三个为 string 数组），违规报 IC-V12
- **字段**:
  - `challenge_duration_ms`: 挑战耗时
  - `files_reviewed`: 检查的文件列表
  - `design_docs_checked`: 查阅的设计文档
  - `challenge_strategies_applied`: 使用了哪些挑战策略

## 示例结论

### 被推翻的发现

```json
{
  "finding_id": "HIGH-01",
  "challenge_result": "overturned",
  "confidence": 97,
  "reasoning": "The finding's central claim is factually incorrect. Exponential backoff IS implemented in src/http/retry.ts (lines 42-49), not in the middleware file the finding searched. The 'no backoff logic found' claim comes from inspecting only src/http/middleware.ts.",
  "counter_evidence": [
    "src/http/retry.ts lines 42-49: delay computed as base * 2^attempt with ±20% jitter",
    "src/http/middleware.ts line 18: delegates all retries to retryWithBackoff(); no delay logic belongs there",
    "config/default.yaml line 12: retry.baseDelayMs is loaded and passed into the client factory"
  ],
  "supporting_evidence": [],
  "adjusted_severity": "none",
  "recommendation": "Dismiss this finding; the claimed missing backoff logic does not exist"
}
```

### 被削弱的发现

```json
{
  "finding_id": "MED-02",
  "challenge_result": "weakened",
  "confidence": 75,
  "reasoning": "The finding correctly identifies that function X lacks input validation, but overstates the severity. The function is only called internally with pre-validated data, reducing the actual risk.",
  "counter_evidence": [
    "src/service.ts: Function X is only called from Y() which validates inputs",
    "No external API exposes this function directly"
  ],
  "supporting_evidence": [
    "src/utils.ts line 45: Function X indeed lacks input validation"
  ],
  "adjusted_severity": "low",
  "recommendation": "Add defensive validation as a best practice, but do not prioritize as high severity"
}
```

### 已确认的发现

```json
{
  "finding_id": "CRIT-03",
  "challenge_result": "confirmed",
  "confidence": 95,
  "reasoning": "The finding accurately identifies a SQL injection vulnerability. User input is directly concatenated into the query string without parameterization.",
  "counter_evidence": [],
  "supporting_evidence": [
    "src/db.ts line 78: query = 'SELECT * FROM users WHERE id = ' + userId",
    "userId comes directly from req.params.id without sanitization"
  ],
  "adjusted_severity": "critical",
  "recommendation": "Immediate fix required; use parameterized queries"
}
```

## 批量处理

处理多个发现时：

```json
{
  "batch_id": "review-2026-06-12",
  "total_findings": 5,
  "verdicts": [
    { "finding_id": "HIGH-01", "challenge_result": "overturned", ... },
    { "finding_id": "HIGH-02", "challenge_result": "confirmed", ... },
    { "finding_id": "MED-01", "challenge_result": "weakened", ... }
  ],
  "summary": {
    "overturned": 1,
    "weakened": 1,
    "confirmed": 3,
    "adjusted_effort_savings": "40% of original findings dismissed or downgraded"
  }
}
```

批量外层字段校验：`batch_id` 出现时必须为非空 string；`total_findings` 出现时必须为 integer 且等于 `verdicts` 数量；`summary` 出现时必须为 object。违规报 IC-V13（`summary` 计数与实际结果不符仍报 IC-V09）。

批量输入也接受顶层数组简写（`[{...verdict}, {...verdict}]`），校验器将其视作 `{verdicts: [...]}` 处理。

## 与下游系统的集成

### 质量仪表盘
- 结论更新质量跟踪中的发现状态
- 置信度评分影响发现优先级
- 调整后的严重度触发相应工作流

### 知识系统
- 已确认的发现成为 knowhow 候选
- 挑战模式成为评审规范
- 被推翻的发现改进未来检测

### 团队技能
- 结论馈入团队评分算法
- 挑战结果为收敛标准提供信息
- 对抗模式提升团队评审质量
