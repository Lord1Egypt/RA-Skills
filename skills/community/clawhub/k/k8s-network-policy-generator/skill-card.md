## Description:

Evaluate and compare privacy solution vendors with a weighted scorecard across 12 criteria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security teams, privacy teams, and procurement evaluators use this skill to compare privacy management vendors, score platform proposals, and prepare recommendations for privacy tool selection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scorecard inputs may include organization names, evaluator names, procurement details, budget ranges, and vendor assessments that are sent to a third-party API.

Mitigation: Omit confidential procurement details, regulated data, and direct personal identifiers unless the organization approves sharing them with ToolWeb.

Risk: The generated vendor ranking and recommendations can influence privacy platform selection decisions.

Mitigation: Review scores, assumptions, and recommendations with privacy, security, procurement, and legal stakeholders before relying on the output.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/k8s-network-policy-generator)
- [ToolWeb API Portal](https://portal.toolweb.in)
- [Privacy Scorecard API Endpoint](https://portal.toolweb.in/apis/compliance/privacy-scorecard)
- [ToolWeb Platform](https://toolweb.in)
- [OpenClaw Skills](https://toolweb.in/openclaw/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with scorecard summaries, comparison highlights, recommendations, and inline shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TOOLWEB_API_KEY and curl; scorecard inputs are sent to ToolWeb's API.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, README license section, and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
