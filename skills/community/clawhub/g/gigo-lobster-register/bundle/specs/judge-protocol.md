# 云端裁判协议

## 端点

`POST {gateway_base}/judge`

## 请求

```json
{
  "run_id": "run_xxx",
  "task_id": "a17",
  "rubric_id": "a17_rubric_v1",
  "agent_output_excerpt": "string, ≤8000 chars",
  "context": {
    "git_diff": "string, ≤16000 chars",
    "tool_calls_summary": [
      {"name": "Edit", "count": 3}
    ]
  },
  "dimensions_to_judge": ["soul", "brain"],
  "client_version": "v2.0.0"
}
```

约定：
- `rubric_id` 由云端事先入库，本地只持有 id 字符串。
- 整个请求体由 `task_bundle_crypto` 加密后再走 HTTPS（与 v1 一致）。

## 响应

```json
{
  "scores": {"soul": 78, "brain": 65},
  "judge_model": "MiniMax-M2.7",
  "judge_version": "2026-04",
  "consensus": "single",
  "fallback_used": false,
  "latency_ms": 820
}
```

`consensus`: `single` | `averaged`（同模型 2 次取均值）| `arbitrated`（仲裁模型介入）。

## 错误

- `429`：限流，harness 应指数退避重试 ≤3 次
- `500`：云端故障，harness 落 `judge_pending`，本地 report 部分分
- `404`：rubric_id 不存在，harness 视为评估器失败，scores 该项给 0

## Provider 抽象（云端）

云端按环境变量决定调用哪个 provider：

```bash
GIGO_JUDGE_PROVIDER=deepseek           # deepseek | qwen | doubao | custom
GIGO_JUDGE_MODEL=MiniMax-M2.7
GIGO_JUDGE_API_KEY=...
GIGO_JUDGE_ENDPOINT=...                # custom 时必填
GIGO_JUDGE_ARBITER_PROVIDER=qwen       # 仲裁
GIGO_JUDGE_ARBITER_MODEL=qwen-max
```

## Prompt 模板

```text
你是 GIGO Lobster Taster 的评分员。请阅读评分细则，对 agent 的输出按维度打 0-100 分。

[评分细则]
{rubric_markdown}

[Agent 输出]
{agent_output_excerpt}

[补充上下文]
{context_block}

请输出严格 JSON，不要包裹任何 markdown：
{"scores": {"<dim>": <int 0-100>, ...}, "reasoning": "<≤200 字>"}
```

`reasoning` 仅入云端日志，不下发给本地。

## 缓存

云端按 `sha256(rubric_id + agent_output_excerpt + context)` 做请求缓存，TTL 7 天。
