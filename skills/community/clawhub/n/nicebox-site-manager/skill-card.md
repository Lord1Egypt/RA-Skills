## Description:

Manage AI-built websites via NiceBox OpenClaw API. Supports article publishing, viewing messages, and checking site status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ravchen](https://clawhub.ai/user/ravchen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site operators use this skill to publish articles, inspect incoming site messages, and check site status for NiceBox-hosted AI-built websites through the OpenClaw API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A custom base URL can receive the NiceBox API key.

Mitigation: Keep AIBOX_BASE_URL on the documented NiceBox HTTPS endpoint and avoid passing custom --base-url values.

Risk: The API key can publish site content and read site messages.

Mitigation: Use a narrowly scoped API key and run commands only from trusted environments and invocation paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ravchen/skills/nicebox-site-manager)
- [NiceBox OpenClaw API endpoint](https://ai.nicebox.cn/api/openclaw)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with shell commands and formatted JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and AIBOX_API_KEY; AIBOX_BASE_URL can override the default API endpoint.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
