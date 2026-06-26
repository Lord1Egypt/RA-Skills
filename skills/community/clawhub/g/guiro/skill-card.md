## Description: <br>
Turn structured data into shareable visual dashboards, reports, charts, and calendars. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chernojagne](https://clawhub.ai/user/chernojagne) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Guiro to turn structured results such as metrics, tables, timelines, schedules, and financial data into a short-lived shareable visual page. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Published Guiro links can expose selected payload data to anyone with the short-lived URL. <br>
Mitigation: Review payloads before creation and avoid including secrets, personal data, or confidential business data unless public link access is acceptable. <br>
Risk: The skill requires GUIRO_API_KEY for authenticated API requests. <br>
Mitigation: Treat GUIRO_API_KEY as a secret and provide it through the environment rather than embedding it in payloads, prompts, or shared outputs. <br>


## Reference(s): <br>
- [Guiro homepage](https://guiro.io) <br>
- [Guiro skill page](https://clawhub.ai/chernojagne/guiro) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with JSON payloads and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates short-lived public share links after validating the selected payload.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
