## Description:

Interact with arbitrary third-party or self-hosted services (AWS, Slack, Google Drive, Dropbox, GitHub, GitLab, Linear, Coolify...) using their HTTP APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hynek-urban](https://clawhub.ai/user/hynek-urban)

### License/Terms of Use:


## Use Case:

Developers and agents use Latchkey to make authenticated HTTP API requests to supported third-party or self-hosted services through latchkey curl while relying on user-managed credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enable broad authenticated API access through a credential-injecting curl wrapper.

Mitigation: Use least-privilege or read-only credentials, verify each endpoint and request body before execution, and avoid broad cloud or payment credentials.

Risk: The latchkey package handles credentials for outbound API requests.

Mitigation: Pin or audit the latchkey package before trusting it with secrets, and install it only in environments where authenticated API access is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hynek-urban/skills/latchkey)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include authenticated HTTP request commands and credential setup guidance; API responses come from the contacted external services.]

## Skill Version(s):

2.3.0+5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
