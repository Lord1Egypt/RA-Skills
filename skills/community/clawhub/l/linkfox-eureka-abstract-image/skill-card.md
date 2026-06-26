## Description: <br>
Retrieves patent abstract drawings from the Eureka patent data platform using a patent ID or publication number. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve and display representative abstract images for one or more patents by patent ID or publication number. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs agents to send feedback or user intent to a separate LinkFox feedback endpoint without interrupting the user's flow. <br>
Mitigation: Send feedback only after explicit user approval, and redact sensitive user text before submission. <br>
Risk: Normal lookups send patent identifiers and the LINKFOXAGENT_API_KEY to LinkFox services. <br>
Mitigation: Use this skill only when the user accepts LinkFox processing for the requested patent identifiers, and keep the API key in an environment variable or secret store. <br>
Risk: Patent image availability depends on Eureka platform coverage and may omit some recent or unsupported records. <br>
Mitigation: Report missing abstract drawings clearly and ask the user to verify patent IDs or publication numbers before retrying. <br>


## Reference(s): <br>
- [Eureka Abstract Image API Reference](references/api.md) <br>
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/linkfox-eureka-abstract-image) <br>
- [Publisher profile](https://clawhub.ai/user/linkfox-ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown responses with patent identifiers and inline image links; optional JSON from the helper script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY; accepts up to 100 patent IDs or publication numbers per request.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
