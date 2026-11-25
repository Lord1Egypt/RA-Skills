---
name: model-routing-preset-builder
description: Use when the operator asks to create or change a native model-routing policy for Codex or OpenClaw.
---

# Native Routing Policy Builder

First identify the target runtime. Codex and OpenClaw have separate model
catalogs, configuration, subscription routes, and preset policies. Never apply
one runtime's defaults or model identifiers to the other.

## Codex

Use the installed `model-capability-router` as the policy baseline. For
GPT-only pstack role-aware choices, read the bundled
[`references/pstack-role-presets.json`](references/pstack-role-presets.json).
It is a packaged snapshot of the canonical Codex distribution at:

[`model-capability-router/references/pstack-role-presets.json`](https://github.com/TheAngryPit/TheAngrySkills/blob/main/skills/core/model-capability-router/references/pstack-role-presets.json)

The repository copy is authoritative. If a durable shared-policy change is
requested, edit that source in the normal TheAngrySkills repository, not this
snapshot. Do not use another locally cached copy when it disagrees with the
canonical source. Read the selected preset, preserve explicit role bindings,
and keep role-aware presets separate from pstack global budget options. Never
silently substitute for an unavailable model or effort.

## OpenClaw

Use the OpenClaw edition of the installed `model-capability-router`, especially
its `references/openclaw-subscriptions.md`. If it is not installed, read the
canonical [OpenClaw edition](https://github.com/TheAngryPit/TheAngrySkills/blob/main/skills/core/model-capability-router/references/openclaw-subscriptions.md)
and [router instructions](https://github.com/TheAngryPit/TheAngrySkills/blob/main/skills/core/model-capability-router/SKILL.md)
from the repository. Do not use the Codex preset JSON for OpenClaw.

Use OpenClaw's live native catalog and controls to check availability:

```text
/model list
/models <provider>
/model status
```

Resolve the exact provider-qualified model from the active Gateway and agent.
An available API model is not proof that an existing subscription covers it.
Preserve the current model and auth profile unless the operator requests a
change. Use `/model <provider/model> -s` for a session-only selection; `-a` or
`-g` changes configuration and needs an explicit request.

## Shared boundaries

- Read the operator's requested change and current native model/effort
  availability for the exact target.
- Preserve explicit selections, named specialists, provider/account identity,
  subscription transport, and existing task ownership.
- Change only the requested profile choices or task boundaries. Do not add
  mandatory ladders, task creation, selected-main overrides, polling, keepalive
  prompts, or speculative cache retention.
- For this operator, the OpenClaw router's starting choices include Sol 6.2
  medium for defined daily work, Sol high for sustained coordination, Astra
  6.2 medium for difficult judgment, and Fable 5.2 medium/high for demanding
  technical work when the active subscription route exposes them. These are
  recommendations, not live availability proof or permission to change an
  explicit selection.
- API token prices and public benchmark scores do not prove lower subscription
  consumption or lower cost per completed task.
- Validate identifiers and effort support against the current runtime. Report
  unavailable options rather than inventing support.
- Author durable shared-policy changes in the normal TheAngrySkills source
  repository when requested. Do not create a competing workbench copy.

Return the target runtime, current source/version, exact proposed or changed
profile, validation evidence, and remaining proof gaps. Do not modify provider
credentials or permissions.
