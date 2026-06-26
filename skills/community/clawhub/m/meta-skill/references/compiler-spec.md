# Trajectory Compiler Spec

## 1. Input Schema (Meta‑Skill)
```yaml
trace_id: string | null
raw_trajectory_log: object | string  # structured JSON preferred
expected_skill_name: string | null
description_override: string | null
```

## 2. Output Schema
```yaml
status: Success | Failed
generated_skill_id: string
skill_schema_preview: object | string
run_flow_path: string  # path to references/run-flow.md
```

## 3. DAG Construction Rules
- Every tool call is a DAG node.
- Edge A -> B when B reads A’s output field.
- DAG must be acyclic; if a cycle is detected, fail compilation.

## 4. Variable Abstraction
- Variable fields → lifted to inputs (schema includes type/required/description).
- Constant fields → embedded in the script.

## 5. Code Synthesis Requirements
- Standard error handling (try/catch)
- Missing/empty dependency → throw/raise
- No invented SDKs; only OpenClaw base tools

## 6. Registration Rules
- Output dir: `$OPENCLAW_SKILLS_DIR/<skill-name>` or `~/.openclaw/workspace/skills/<skill-name>`
- Must write `SKILL.md` + schema + plan + run script + run-flow
- Trigger hot reload or instruct user to refresh
