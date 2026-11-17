## Description:

Evaluate and compare privacy solution vendors with a weighted scorecard across 12 criteria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security teams, privacy teams, and procurement stakeholders use this skill to compare privacy management vendors, consent management platforms, and data protection tools for selection or business-case work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends organization, evaluator, budget, regulatory, and vendor-evaluation details to a third-party API.

Mitigation: Use it only with approval to share those details with ToolWeb, and avoid confidential procurement notes or personal data unless approved.

Risk: Successful API calls may be billable under the configured ToolWeb account.

Mitigation: Confirm the API account, plan, and expected usage before running vendor scorecard requests.

Risk: The scorecard can influence privacy tooling and procurement decisions.

Mitigation: Have qualified privacy, security, and procurement reviewers validate vendor inputs, scores, and recommendations before acting on the output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/privacy-solution-scorecard)
- [ToolWeb API Hub](https://portal.toolweb.in)
- [Privacy scorecard API endpoint](https://portal.toolweb.in/apis/compliance/privacy-scorecard)
- [ToolWeb platform](https://toolweb.in)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summary with vendor ranking, comparison highlights, recommendations, and API error guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TOOLWEB_API_KEY and sends user-provided organization, budget, regulatory, and vendor scoring details to the ToolWeb API.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
