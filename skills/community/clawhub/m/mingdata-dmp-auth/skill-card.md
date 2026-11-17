## Description:

Mingdata DMP API credential management and unified API gateway for Access Key/Secret Key setup, request signing, and HTTP request handling across Mingdata DMP audience selection, insight, and delivery skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mingri26](https://clawhub.ai/user/mingri26)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to configure Mingdata DMP credentials and route authenticated Mingdata DMP API calls through a shared request-signing helper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles long-lived Mingdata DMP Access Key and Secret Key credentials with broad authenticated DMP access.

Mitigation: Install only when the publisher is trusted, use the narrowest available DMP credentials, and rotate any production keys that were pasted into chat or shell commands.

Risk: The artifact claims credential storage is local-only while recommending OpenClaw environment-variable injection.

Mitigation: Confirm where OpenClaw stores env.DMP_AK and env.DMP_SK before relying on the local-only security claim.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mingri26/skills/mingdata-dmp-auth)
- [Mingdata Open Platform](https://open.mingdata.com)
- [Mingdata DMP Open API base endpoint](https://open.mingdata.com/api/open-api)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Mingdata DMP Access Key and Secret Key credentials to sign requests and return API responses or error details.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
