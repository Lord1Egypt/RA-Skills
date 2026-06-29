## Description: <br>
Financial Modeling Prep helps agents search and retrieve market, company, financial statement, valuation, calendar, and news data through the OOMOL oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to answer Financial Modeling Prep data requests by inspecting live connector schemas and running market, company, financial statement, valuation, calendar, and news actions through an authenticated OOMOL connection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive credentials for an OOMOL-connected Financial Modeling Prep account. <br>
Mitigation: Use the authenticated connector flow and do not ask users for raw API keys or tokens. <br>
Risk: Action inputs and outputs depend on live connector schemas and authenticated execution. <br>
Mitigation: Inspect the action schema before building payloads and confirm exact payloads before any action marked write or destructive. <br>
Risk: Security guidance treats associated maintainer, migration, review, and notification flows as privileged. <br>
Mitigation: Verify targets, use dry-run output where available, and confirm before writes, emails, or review-tool submissions. <br>


## Reference(s): <br>
- [Financial Modeling Prep homepage](https://financialmodelingprep.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-financial-modeling-prep) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads or connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the oo CLI and an authenticated Financial Modeling Prep connection; connector responses include data and meta.executionId.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
