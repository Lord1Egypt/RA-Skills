## Description: <br>
Retrieves full patent description and specification text from the Eureka patent data platform by patent ID or publication number. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Patent analysts, inventors, and IP teams use this skill to retrieve and review detailed specification text for known patents when they already have a patent ID or publication number. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Patent identifiers and query details are sent to LinkFox/Eureka services. <br>
Mitigation: Use only when sharing those identifiers with LinkFox/Eureka is approved for the user's environment. <br>
Risk: The skill instructs agents to send feedback and user-intent details to a separate LinkFox feedback service. <br>
Mitigation: Require explicit approval before feedback submission and redact confidential patent strategy, unpublished invention details, client names, and sensitive conversation content. <br>
Risk: The skill requires a LinkFox API key. <br>
Mitigation: Store LINKFOXAGENT_API_KEY as a secret, avoid printing it in logs, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [Eureka patent description API reference](references/api.md) <br>
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/linkfox-eureka-description) <br>
- [LinkFox Skills](https://skill.linkfox.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with JSON API responses and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY and known patent IDs or publication numbers; batch lookups support up to 100 patents.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
