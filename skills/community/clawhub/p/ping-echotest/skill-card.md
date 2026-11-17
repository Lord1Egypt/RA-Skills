## Description:

A tiny smoke-test skill that echoes back any text you send it.

This skill is for research and development only.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release maintainers use this skill as a deterministic echo probe to verify skill ingestion, publishing, and end-to-end registry loading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes an executable script.

Mitigation: Review and scan the script before deployment; evidence.security reports no network, credential, persistence, or destructive behavior.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/terrycarter1985/skills/ping-echotest)
- [Publisher Profile](https://clawhub.ai/user/terrycarter1985)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text echo response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deterministic output prefixed with "pong:"; no external network or credentials required.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
