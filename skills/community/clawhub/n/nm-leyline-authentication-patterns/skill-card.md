## Description:

Provides auth patterns for API keys, OAuth, and token management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers integrating external APIs use this skill for guidance on API-key, OAuth, and token authentication, credential verification, and handling authentication failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports a suspicious verdict because scanners found repository and cloud actions beyond the stated authentication-guidance purpose, and one referenced script could not be inspected.

Mitigation: Review the referenced script and proposed commands, and limit account permissions and access to what the task requires before use.

Risk: The supplied API-key setup example writes a key to a plaintext file under the home directory.

Mitigation: Use a secret manager or protected environment injection, and keep credential files out of source control and shared locations.

## Reference(s):

- [ClawHub release](https://clawhub.ai/athola/skills/nm-leyline-authentication-patterns)
- [Project homepage (skill metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/leyline)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline Python, shell, and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
