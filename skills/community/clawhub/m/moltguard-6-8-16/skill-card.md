## Description:

MoltGuard is an OpenClaw security guard that helps protect agents and users from prompt injection, data exfiltration, and malicious commands hidden in files and web content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouhuihui008](https://clawhub.ai/user/zhouhuihui008)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to install, configure, test, and operate MoltGuard security protection for prompt injection, data exfiltration, malicious command, and sensitive-data risk detection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installed plugin may send sensitive prompt, command, file-derived, PII, or secret-related security data to a Core service.

Mitigation: Confirm the Core endpoint and data handling requirements before enabling the plugin, and use an enterprise Core deployment when organizational policy requires it.

Risk: The skill directs users to install external plugin code that was not included in this artifact review.

Mitigation: Install only a pinned, verified plugin version and review or scan the plugin package before deployment.

Risk: The plugin creates and stores an API key under the user's OpenClaw credentials directory.

Mitigation: Protect the credentials directory, limit access to the host account, and rotate the API key if exposure is suspected.

## Reference(s):

- [MoltGuard homepage](https://github.com/openguardrails/openguardrails/tree/main/moltguard)
- [ClawHub skill page](https://clawhub.ai/zhouhuihui008/skills/moltguard-6-8-16)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and OpenClaw slash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes installation, status, API-key, dashboard, enterprise enrollment, update, and uninstall guidance.]

## Skill Version(s):

6.8.16 (source: SKILL.md frontmatter and artifact/_meta.json; ClawHub release version: 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
