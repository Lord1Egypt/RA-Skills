## Description:

Analyzes a patent family from a patent number or PatSnap patent URL, retrieves related family members, compares technical issues, solutions, effects, claims, and evolution, and produces an interactive HTML report for patent analysts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

External patent analysts use this skill to study a patent family, visualize relationships among family members, compare technical themes and claim structures, and summarize technology evolution and protection risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports can execute injected browser code when patent, JSON, or MCP data is untrusted or attacker-controlled.

Mitigation: Review the skill before deployment and do not open reports from untrusted data until the renderer escapes HTML, validates URLs, avoids innerHTML and inline event handlers, and safely embeds JSON.

Risk: Live analysis depends on authorized PatSnap/Eureka MCP access, so incomplete setup limits the skill to analysis framework guidance rather than database-backed conclusions.

Mitigation: Confirm MCP account authorization and tool availability before relying on generated patent-family findings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/patent-family-analyzer)
- [PatSnap Open Platform](https://open.zhihuiya.com/)

## Skill Output:

**Output Type(s):** [text, code, configuration, guidance]

**Output Format:** [Self-contained interactive HTML report with inline CSS and JavaScript]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Analyzes up to 20 family members and requires PatSnap/Eureka MCP authorization for live patent retrieval.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
