## Description:

Investment Workflow helps agents run scenario-driven investment research across six cases: stock analysis, industry research, market scans, industry views, hotspot impact analysis, and meeting discussion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lj22503](https://clawhub.ai/user/lj22503)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to structure investment research requests into scenario-specific workflows, gather market data, analyze stocks or industries, and produce decision-oriented research reports. It should support research and education rather than replace personalized financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce concrete buy, sell, hold, or watch recommendations from broad investment prompts.

Mitigation: Use outputs as research support only, require human review before financial decisions, and keep user-facing language clear that the report is not personalized financial advice.

Risk: The skill requests broad Bash, Exec, Read, and Write authority and can use external market-data tools and WebSearch.

Mitigation: Run it in a constrained environment and avoid exposing private files, proprietary watchlists, or account-specific trading information.

Risk: Market-data tools may fail or return incomplete data, which can make recommendations misleading.

Mitigation: Require source and timestamp labels, disclose data failures, and lower confidence when required data is missing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lj22503/skills/investment-workflow)
- [Publisher profile](https://clawhub.ai/user/lj22503)
- [Shared skill modules](references/shared-skills.md)
- [Data layer integration](references/data-layer-integration.md)
- [Investment report template](templates/report-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown reports with sourced data notes, confidence labels, and structured recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May route content to formatted outputs such as cards, HTML presentations, or WeChat-style articles when an expression layer is available.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
