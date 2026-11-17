## Description:

Provides real-time financial news monitoring by forwarding user requests to a remote Prana service and returning the service response.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyffeifeifei](https://clawhub.ai/user/cyffeifeifei)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query live financial news and market updates through a Prana-hosted capability. The Python or Node client sends the user message to the remote service and prints the returned JSON for display.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User prompts and API credentials are forwarded to a remote Prana service.

Mitigation: Review the remote service and endpoint before installation, use only trusted base URLs, and avoid entering sensitive trading or account information.

Risk: Fetched API keys can be saved locally in plaintext configuration.

Mitigation: Disable automatic API-key fetching or plaintext key storage unless explicitly needed, and protect or remove any locally saved key file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cyffeifeifei/skills/prana-cyf-20260327)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON returned on standard output, with text or markdown content when included by the remote service.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The client may poll for asynchronous results and returns the remote service response without local summarization.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
