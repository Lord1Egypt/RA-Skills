## Description: <br>
Uses the Grok API to perform web searches, with a default relay endpoint intended to reduce cost. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xianyu110](https://clawhub.ai/user/xianyu110) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to send search queries to a Grok-compatible chat completions endpoint and receive concise answers for current information needs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and bearer API tokens may be sent to the configured endpoint, including a third-party relay by default. <br>
Mitigation: Set GROK_API_URL explicitly to the official xAI endpoint or another trusted provider, and use a separate revocable key for relay services. <br>
Risk: The documentation is inconsistent about whether the default endpoint is the official xAI API or a relay. <br>
Mitigation: Review the shell script before installing and confirm endpoint defaults in the local version before running searches. <br>
Risk: Search prompts may contain sensitive or confidential information. <br>
Mitigation: Avoid sensitive searches unless the endpoint, key handling, and provider terms are acceptable for the use case. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xianyu110/grok-api-search) <br>
- [xAI API endpoint](https://api.x.ai/v1) <br>
- [xAI console](https://console.x.ai/) <br>
- [Default relay provider](https://apipro.maynor1024.live/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text responses with optional source references; Markdown documentation includes bash examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GROK_API_KEY; GROK_API_URL can route requests to xAI or a relay endpoint.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
