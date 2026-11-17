## Description:

OpenClaw Cost Guard audits an OpenClaw config for token-spend and denial-of-wallet risk signals such as missing budgets, premium default models, oversized token ceilings, browser workflows, and cron jobs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x-rayluan](https://clawhub.ai/user/x-rayluan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to review OpenClaw configurations for budget gaps, expensive routine model defaults, oversized token ceilings, and recurring automation risks before scaling agent usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit reads the OpenClaw config path provided by the user, or the default ~/.openclaw/openclaw.json.

Mitigation: Run it only on config files you are comfortable letting the local skill inspect.

Risk: The JSON output can reveal model choices, budget settings, and workflow patterns.

Mitigation: Review and redact the generated JSON before sharing it outside the intended review context.

Risk: A lightweight static review can miss spend that appears only in provider invoices, usage telemetry, or downstream automations.

Mitigation: Verify cost posture against real provider billing data and usage telemetry before relying on a low-risk verdict.

Risk: A missing or invalid config prevents a trustworthy cost assessment.

Mitigation: Point the script at the real OpenClaw config path and repair invalid JSON before using the verdict for rollout decisions.

## Reference(s):

- [Cost Guard Playbook](references/cost-playbook.md)
- [OpenClaw Cost Guard on ClawHub](https://clawhub.ai/x-rayluan/skills/openclaw-agent-cost-guard)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [JSON audit report with score, verdict, summary, findings, recommendations, guardrails, and evidence; accompanying agent guidance may be Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads the selected OpenClaw config path and reports findings without modifying files or sending data elsewhere.]

## Skill Version(s):

0.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
