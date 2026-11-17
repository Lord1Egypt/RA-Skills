## Description:

Challenges the user for a secret word before allowing access to sensitive files or system commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cenralsolution](https://clawhub.ai/user/cenralsolution)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to add an advisory secret-word gate before sensitive file or command workflows, with local session unlock, emergency reset, and audit logging behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may overestimate the skill as a real MFA or access-control boundary for secrets, shell commands, .env files, or deletions.

Mitigation: Treat it as an advisory prompt workflow unless the surrounding runtime separately enforces access checks.

Risk: The skill writes authentication state and audit logs locally under ~/.openclaw.

Mitigation: Review local storage behavior before installation and use strong, unique secret words when testing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cenralsolution/skills/mfa-word)
- [ClawHub Publisher Profile](https://clawhub.ai/user/cenralsolution)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [Text responses and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may write a local vault and audit log under ~/.openclaw when its tools are used.]

## Skill Version(s):

1.1.0 (source: package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
