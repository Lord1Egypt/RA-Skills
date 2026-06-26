## Description: <br>
Guides an agent through market interpretation, event analysis, portfolio diagnosis, asset allocation, and behavioral coaching using a four-expert investment advisory workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lj22503](https://clawhub.ai/user/lj22503) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to structure investment-advisory support across market reads, event impact analysis, portfolio diagnosis, asset allocation, and behavioral correction. The workflow emphasizes KYC collection, source attribution, confidence labeling, disclaimers, and privacy handling before producing advisory reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive portfolio context or personal financial details may be exposed during advisory workflows. <br>
Mitigation: Invoke the skill explicitly, avoid sharing full identity or account numbers, and verify credential scope, logging, retention, and data destinations for any data or MCP integrations. <br>
Risk: Generated outputs could be mistaken for licensed investment advice. <br>
Mitigation: Treat outputs as informational unless reviewed under appropriate professional controls, keep disclaimers visible, and require KYC details before asset-allocation recommendations. <br>
Risk: Incomplete or stale market data can reduce the reliability of reports and recommendations. <br>
Mitigation: Require source and timestamp labels, confidence notes, and a clear downgrade path when referenced data sources are unavailable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lj22503/investment-advisory-workflow) <br>
- [Four-expert framework](references/four-experts.md) <br>
- [Six-stage capability library](references/six-stages.md) <br>
- [Shared skill documentation](references/shared-skills.md) <br>
- [Report template](templates/report-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown reports, advisory prompts, KYC questions, action checklists, and optional card-style summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should include data sources, confidence notes, disclaimers, and privacy-preserving treatment of sensitive identifiers.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence and clawhub.yaml; SKILL.md frontmatter reports 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
