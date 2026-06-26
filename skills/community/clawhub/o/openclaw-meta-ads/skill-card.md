## Description: <br>
Shared Meta Ads skill for OpenClaw agents to analyze Meta ad accounts, campaigns, ad sets, ads, insights, and lead-form data with a production-safe read-first workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sebclawops](https://clawhub.ai/user/sebclawops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw agents and their operators use this skill for Meta Ads reporting, account audits, creative and audience diagnostics, lead-form review, and structured recommendations before any live ad changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meta Ads tokens and account identifiers could be exposed if copied into files or chat. <br>
Mitigation: Use secure environment injection for credentials, keep tokens out of tracked files and conversation logs, and prefer read-only scopes where possible. <br>
Risk: Lead-form data may contain personal information. <br>
Mitigation: Retrieve only the minimum lead fields needed for the task and scrub PII before broader analysis or sharing. <br>
Risk: Agent-assisted recommendations could affect live ad delivery or budgets if applied without review. <br>
Mitigation: Keep the workflow read-first and require explicit approval before pausing, enabling, editing, changing budgets, or changing creative. <br>


## Reference(s): <br>
- [Openclaw Meta Ads on ClawHub](https://clawhub.ai/sebclawops/openclaw-meta-ads) <br>
- [Account Structure](references/account-structure.md) <br>
- [API Setup](references/api-setup.md) <br>
- [Audit Workflows](references/audit-workflows.md) <br>
- [Browser Fallback](references/browser-fallback.md) <br>
- [Insights and Query Patterns](references/insights-queries.md) <br>
- [Optimization Heuristics](references/optimization.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, recommendations, query examples, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-first workflow; live account changes require explicit approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
