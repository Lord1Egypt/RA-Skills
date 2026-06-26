## Description: <br>
Sif Asin Summary helps Amazon sellers query and analyze ASIN-level SIF traffic-source data, including exposure distribution, organic and paid traffic shares, and period-over-period keyword movement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Amazon sellers, marketplace analysts, and developers use this skill to retrieve LinkFox SIF ASIN traffic-source data and summarize exposure/channel structure for individual products or competitor comparisons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ASIN queries and related request data are sent to LinkFox services. <br>
Mitigation: Use the skill only when that data sharing is acceptable and avoid including unnecessary sensitive business context. <br>
Risk: The skill can submit broad feedback content to a separate LinkFox feedback endpoint. <br>
Mitigation: Require explicit user approval before sending feedback and review the feedback content before submission. <br>
Risk: The skill requires a LinkFox API key. <br>
Mitigation: Use a dedicated, revocable API key stored in LINKFOXAGENT_API_KEY and rotate or revoke it when access is no longer needed. <br>


## Reference(s): <br>
- [SIF ASIN Traffic Source API Reference](references/api.md) <br>
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/linkfox-sif-asin-summary) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown summaries and tables, with JSON returned by the helper script when run directly.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY for API calls; supports up to 10 ASINs per request across the documented marketplace set.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
