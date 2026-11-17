## Description:

Monitors real-time LLM API costs, detects runaway loops, enforces budgets, audits code risk, and reports usage across multiple providers and models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nimaansari](https://clawhub.ai/user/nimaansari)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to estimate, monitor, and report LLM spend; enforce budgets; detect runaway loops; and audit agent code for cost-risk patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can observe LLM traffic and persist local usage or error data that may include sensitive metadata.

Mitigation: Use explicit SDK wrappers where possible, set CW_LOG_DIR to a protected location, and periodically clear local cost-watchdog logs.

Risk: Global HTTP capture and tailing can broaden monitoring on shared or sensitive machines.

Mitigation: Avoid enabling global httpx capture, tailing, or detect commands on shared or highly sensitive machines unless they are required.

Risk: Live pricing lookup may contact external pricing sources.

Mitigation: Use CW_OFFLINE or CW_STATIC_ONLY when live pricing lookups are not acceptable.

## Reference(s):

- [Cost Optimization Strategies](references/optimization.md)
- [Dangerous Cost Patterns](references/patterns.md)
- [Token Counting and Cost Calculation](references/calculators.md)
- [Static Pricing Reference](references/pricing.md)
- [ClawHub skill page](https://clawhub.ai/nimaansari/skills/llm-cost-watchdog)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and CLI-oriented text with inline shell commands, code snippets, JSON summaries, and local report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local JSONL usage, error, cache, and report data under the configured cost-watchdog log directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
