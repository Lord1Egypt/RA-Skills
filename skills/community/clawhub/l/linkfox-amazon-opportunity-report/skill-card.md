## Description: <br>
Generates AI-powered Amazon US market opportunity reports for a keyword across market potential, product characteristics, reviews, customer profile, search trends, and pricing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, product researchers, and agents use this skill to request keyword-level Amazon US market insight reports for product selection and market entry decisions. <br>

### Deployment Geography for Use: <br>
United States marketplace coverage; skill availability otherwise Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may send user comments, complaints, praise, business context, or inferred intent to a separate feedback API without explicit approval. <br>
Mitigation: Require explicit user approval before using the feedback API and avoid sending sensitive business context or inferred intent as feedback. <br>
Risk: The report API requires a LinkFox API key and sends Amazon keyword requests to LinkFox for report generation. <br>
Mitigation: Use a dedicated LinkFox API key and disclose that searched keywords are sent to LinkFox before requesting a report. <br>


## Reference(s): <br>
- [API reference](references/api.md) <br>
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/linkfox-amazon-opportunity-report) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, API calls, Shell commands, Guidance] <br>
**Output Format:** [Markdown report returned in an API response, with a JSON wrapper when using the bundled script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY; supports the Amazon US marketplace only; reports are point-in-time snapshots.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
