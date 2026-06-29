# Risk Rules

## Read-Only Default

This skill is read-only by default: it may query Kubernetes stdout logs, LogConfig resources, and LTS log records.

## Mutating Operations

- Creating LogConfig resources is allowed only through `huawei_create_cce_logconfig`. The tool must preview first and requires `confirm=true` before it changes the cluster.
- Deleting LogConfig resources is allowed only through `huawei_delete_cce_logconfig`. The tool must preview the exact target first and requires `confirm=true`.

## Scope Boundaries

- Do not update workloads, LogConfig resources, log groups, log streams, or LTS data.
- If a user asks for remediation based on logs, provide evidence and hand off to the relevant diagnosis or remediation skill instead of changing resources here.

## Credential Security

- Never expose AK/SK, tokens, kubeconfig certificates, or full sensitive log payloads in summaries.
- Prefer time-bounded queries. If no time range is provided, use recent logs and keep limits small.

## Data Privacy

- When logs contain secrets, credentials, cookies, authorization headers, or personal data, summarize the pattern and redact the value.
- Never include raw sensitive values in output or conversation.

## Guardrails

| Guardrail | Rule | Rationale |
|-----------|------|-----------|
| `max_auto_risk: R1` | Only read operations proceed automatically; mutating operations require `confirm=true` | Prevents unintended LogConfig creation/deletion |

## Confirmation Flow

```
Call without confirm=true → Preview output → User reviews → User confirms → Call with confirm=true
```

**No exceptions**:
- Do not skip preview for "simple" LogConfig operations
- Do not call with confirm=true without showing preview first
- Do not assume the preview is correct without user verification