## Description:

Schedule and manage social media posts via the Postiz API for self-hosted or cloud deployments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolmanns](https://clawhub.ai/user/coolmanns)

### License/Terms of Use:


## Use Case:

Content creators, social media operators, and automation-focused developers use this skill to schedule, draft, publish, query, update, delete, and deduplicate posts across Postiz-connected social channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes real-looking Postiz account credentials.

Mitigation: Do not use the embedded credentials; rotate the password, revoke active sessions, remove the secrets from the skill and history, and require user-supplied credentials or tokens.

Risk: Reusable Postiz session cookies are stored in an insecure temporary location.

Mitigation: Store session material only in memory or a private protected location with restrictive permissions, and clear it when no longer needed.

Risk: The skill can immediately publish or delete social posts.

Mitigation: Require explicit confirmation for immediate publish and delete actions, and prefer draft or scheduled workflows when review is needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/coolmanns/skills/postiz-ext)
- [Publisher Profile](https://clawhub.ai/user/coolmanns)
- [Postiz Dashboard](https://postiz.home.mykuhlmann.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON examples, and Python helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include platform-specific character validation, scheduling decisions, media upload steps, duplicate checks, and direct Postiz API calls.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
