## Description:

Guides an agent through building formula-driven Excel financial models for 3-statement models, DCF valuation, LBOs, SaaS unit economics, sensitivity analysis, debt schedules, and fundraising projections using OfficeCLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iceyliu](https://clawhub.ai/user/iceyliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to create auditable Excel financial models with structured assumptions, calculation sheets, outputs, validation gates, and OfficeCLI command patterns. It is intended for complex modeling workflows such as 3-statement forecasts, DCFs, LBOs, ARR models, scenarios, and sensitivities rather than simple spreadsheets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions include mutable remote installer commands that pipe directly into a shell.

Mitigation: Prefer a versioned OfficeCLI release with checksum or signature verification, and review the base officecli-xlsx dependency before use.

Risk: Financial models can contain stale formula caches, unresolved cross-sheet references, or unbalanced statements if generated commands are not verified.

Mitigation: Run the skill's stated balance, cash reconciliation, cache, and hardcode audits before relying on any generated workbook.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iceyliu/skills/officecli-financial-model)
- [OfficeCLI releases](https://github.com/iOfficeAI/OfficeCLI/releases)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Files]

**Output Format:** [Markdown guidance with inline bash commands for producing a formula-driven .xlsx workbook]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs focus on Excel workbooks with formulas, named ranges, scenario or sensitivity structures, validation checks, and OfficeCLI verification commands.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
