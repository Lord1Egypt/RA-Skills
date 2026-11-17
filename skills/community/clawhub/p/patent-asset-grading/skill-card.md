## Description:

Patent asset grading tool that accepts batches of patent application, publication, or grant numbers, retrieves patent data through the Zhihuiya/PatSnap MCP service, identifies industry from IPC classes, scores five patent-value dimensions with industry-specific weights, and outputs Word or Excel review results with grades, score rationales, and recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Patent portfolio, IP, and business users use this skill to batch-review patent assets and produce structured grading reports for portfolio triage, maintenance planning, licensing review, or disposal recommendations. The skill depends on authorized patent-data access and should be treated as decision support, not legal or valuation advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends submitted patent identifiers to the Zhihuiya/PatSnap MCP service to retrieve patent data.

Mitigation: Confirm MCP authorization and data-sharing expectations before use, and submit only patent batches appropriate for that service.

Risk: Generated patent grades may be mistaken for legal, financial, or valuation conclusions.

Mitigation: Use the reports as decision support and have qualified patent, legal, or portfolio reviewers confirm conclusions before acting.

Risk: Report generation depends on Python packages and MCP configuration being available in the agent environment.

Mitigation: Run the skill in a controlled Python environment with reviewed dependency versions and verify MCP setup before relying on generated reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/patent-asset-grading)
- [Zhihuiya open platform](https://open.zhihuiya.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Excel .xlsx or Word .docx reports with tabular patent scores, grade labels, scoring rationale, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes up to 50 patents per batch; supports Excel or Word output and optional industry override.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
