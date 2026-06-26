---
name: imperial-orchestrator
description: High-availability multi-role model router for OpenClaw. Discovers available models, maps them to role-based departments, routes tasks by complexity and domain, avoids dead auth chains, and degrades gracefully when providers fail.
version: 0.1.0
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
    skillKey: imperial-orchestrator
    emoji: 🏯
---

# Imperial Orchestrator

Use this skill when the user wants **OpenClaw to coordinate many models intelligently** instead of relying on a single default model.

This skill implements a pragmatic version of a **三省六部 / multi-role court** pattern:

- **中枢总管**: receives the request, classifies it, selects an execution mode, and keeps the session alive
- **内阁规划**: breaks down larger tasks into sub-tasks
- **六部执行**: coding, ops, security, legal, writing, finance, project management
- **都察院审核**: optional review pass when quality or safety matters
- **生存模式**: if providers fail, keep working with the best remaining model or a local fallback

## Goals

1. Discover all available models from local config and optional health snapshot files.
2. Match tasks to the best role and model set.
3. Avoid **401 retry storms** by opening an auth circuit breaker.
4. Prefer **cross-provider fallback** over same-provider fallback.
5. Keep the main session alive by switching to **degraded mode** if necessary.

## Important reality checks

- OpenClaw loads skills from bundled skills, `~/.openclaw/skills`, or `<workspace>/skills`. Workspace skills have the highest precedence.
- Skills are AgentSkills-compatible folders centered on `SKILL.md` with YAML frontmatter.
- OpenClaw supports agent-specific workspaces and community usage shows coding-agent delegation, but model overrides and sub-agent routing can still be inconsistent depending on provider/version.
- Therefore this skill is intentionally built as a **hybrid** of policy + scripts instead of assuming every runtime route works natively.

## What this skill contains

- `config/model_registry.yaml`: model capability tags and routing preferences
- `config/agent_roles.yaml`: role definitions with forbidden actions and model strategies
- `config/agent_prompts.yaml`: deep system prompts for each role (identity, rules, red lines)
- `config/routing_rules.yaml`: deterministic routing hints
- `config/failure_policies.yaml`: auth breaker, retry, degrade rules
- `config/benchmark_tasks.yaml`: standardized test tasks per category (coding/writing/reasoning/ops/security/finance)
- `scripts/router.py`: main planner/router/selector (now with benchmark-aware scoring)
- `scripts/health_check.py`: discover models from openclaw.json
- `scripts/model_validator.py`: probe each model with real API calls to verify availability
- `scripts/benchmark.py`: run the same task against all models, score and rank by category
- `scripts/emit_openclaw_status.py`: print machine-readable routing state
- `scripts/route_and_update.sh`: unified CLI entry point
- `examples/`: sample config patches and install docs

## 三省六部角色体系

每个角色配备深度 system prompt（定义在 `config/agent_prompts.yaml`），包含身份认同、职责边界、行为准则、协作意识和生死线五个维度。

### 中枢

| 角色 | 官衔 | 朝制对应 | 核心使命 |
|------|------|---------|---------|
| **router-chief** | 中枢总管 | 天子/中枢院 | 系统的生命线——分类、路由、维持心跳 |

### 三省

| 角色 | 官衔 | 朝制对应 | 核心使命 |
|------|------|---------|---------|
| **cabinet-planner** | 内阁首辅 | 中书省 | 草拟方略——将混沌拆解为有序步骤 |
| **censor-review** | 都御史 | 门下省/都察院 | 封驳审核——质量的最后守门人 |

### 六部

| 角色 | 官衔 | 朝制对应 | 核心使命 |
|------|------|---------|---------|
| **ministry-coding** | 工部尚书 | 工部 | 兴修工程——编码、调试、架构 |
| **ministry-ops** | 工部侍郎 | 工部·营缮司 | 维护驿站——部署、运维、CI/CD |
| **ministry-security** | 兵部尚书 | 兵部 | 戍边防务——安全审计、威胁建模 |
| **ministry-writing** | 礼部尚书 | 礼部 | 文教礼仪——文案、文档、翻译 |
| **ministry-legal** | 刑部尚书 | 刑部 | 律法刑狱——合同、合规、条款 |
| **ministry-finance** | 户部尚书 | 户部 | 钱粮赋税——定价、毛利、结算 |

### 急递铺

| 角色 | 官衔 | 朝制对应 | 核心使命 |
|------|------|---------|---------|
| **emergency-scribe** | 急递铺令 | 急递铺 | 系统永不宕机的最后保障 |

## Operating rules

### 1) Treat 401 as toxic

If a model fails with an auth error:

- mark the model as `auth_dead`
- cool down the whole auth chain / provider profile
- do **not** keep retrying sibling models on the same auth chain first
- prefer a different provider or a local fallback

### 2) Main router must stay light

Never assign the largest prompt, heaviest workspace, or the most fragile provider to the router-chief.

### 3) Cross-provider fallback first

Fallback order should be:

1. same role, different provider
2. same role, local fallback
3. secondary role with adjacent duties
4. emergency-scribe

### 4) Degrade instead of dying

If the best specialist models are unavailable:

- still answer with architecture, checklists, pseudocode, or a reduced plan
- do not return `All models failed` if **any** model remains viable

## Suggested workflow

### 统一入口（推荐）

```bash
# 验证 → 路由（一条命令搞定）
bash scripts/route_and_update.sh full "Fix WireGuard peer sync bug"

# 单独路由
bash scripts/route_and_update.sh route "写一段产品介绍文案"

# 探活所有模型
bash scripts/route_and_update.sh validate

# 跑基准测试（全部类别）
bash scripts/route_and_update.sh benchmark

# 只测 coding 类别
bash scripts/route_and_update.sh benchmark coding

# 查看排行榜
bash scripts/route_and_update.sh leaderboard
```

### 手动操作

```bash
# 1. 发现模型
python3 scripts/health_check.py --openclaw-config ~/.openclaw/openclaw.json --write-state .imperial_state.json

# 2. 探活验证（真正调 API 确认模型可用）
python3 scripts/model_validator.py --openclaw-config ~/.openclaw/openclaw.json --state-file .imperial_state.json

# 3. 跑基准测试
python3 scripts/benchmark.py --openclaw-config ~/.openclaw/openclaw.json --state-file .imperial_state.json

# 4. 路由（自动读取 benchmark 分数加持）
python3 scripts/router.py --task "Design a distributed lock service" --state-file .imperial_state.json

# 5. 记录失败
python3 scripts/router.py --task "any" --record-failure modelstudio/qwen3.5-plus auth --write-state
```

## Output contract

The router returns JSON including:

- `mode`: direct / plan_then_execute / multi_agent / degraded
- `lead_role` + `lead_title` (角色官衔)
- `lead_system_prompt` (深度角色提示词，可直接注入 agent)
- `review_roles` + `review_system_prompts`
- `forbidden_actions` (角色禁止行为列表)
- `selected_model`
- `fallback_chain`
- `survival_model`
- `reasoning` (含 benchmark 分数信息)

## Integration notes

This skill does **not** hard-code one provider API. Instead it prepares routing decisions and failure state so you can:

- feed the selected model into your OpenClaw agent config
- spawn the right sub-agent
- call your own shell wrapper around provider endpoints
- keep a machine-readable health snapshot for external automation

## Install

### Workspace-only

Copy this folder to:

```text
<your-workspace>/skills/imperial-orchestrator
```

### Global shared install

Copy this folder to:

```text
~/.openclaw/skills/imperial-orchestrator
```

## Safety

- Never send secrets into prompts.
- Keep auth probe payloads minimal.
- Treat provider and token health as separate state from model quality.
- Do not assume a model is safe to route merely because it appears in config.
