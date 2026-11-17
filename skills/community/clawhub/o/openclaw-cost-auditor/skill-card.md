## Description:

Tracks and reports OpenClaw API usage, model costs, token consumption, and forecast spending with optimization recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gblockchainnetwork](https://clawhub.ai/user/gblockchainnetwork)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to audit OpenClaw logs for API spend, token usage, top cost drivers, and spending forecasts. It can also surface optimization guidance such as quantization or pruning recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OpenClaw logs can contain operational or user activity data.

Mitigation: Use the skill only for intended OpenClaw cost audits and review the log directory before sharing or processing logs.

Risk: Cost estimates may be inaccurate because the bundled script applies a fixed $10 per million tokens rate.

Mitigation: Validate provider pricing and billing assumptions before using estimates for financial decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gblockchainnetwork/skills/openclaw-cost-auditor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and cost summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include token totals, estimated costs, forecasts, and optimization recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact heading)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
