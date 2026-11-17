## Description:

Installs or repairs Hirey AI on a local OpenClaw host so an agent can register with Hi and help the user find, contact, and coordinate with people.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yzlee](https://clawhub.ai/user/yzlee)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and developers use this skill to install, repair, and complete registration for Hirey AI on a local OpenClaw host. It prepares the host so the agent can use Hi for people-finding workflows such as job search, recruiting, housing, friendship, dating, founder or investor outreach, and lawyer search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer changes persistent OpenClaw host configuration and may alter approval behavior.

Mitigation: Review the skill before installation and proceed only when the host owner approves the OpenClaw configuration changes.

Risk: The installer stores hook tokens in local OpenClaw configuration.

Mitigation: Keep ~/.openclaw/openclaw.json readable only by the local user and rotate or reset tokens if the file may have been exposed.

Risk: Part of the workflow depends on instructions supplied by the remote Hirey AI platform.

Mitigation: Use the skill only if the user trusts Hirey AI, and review platform-supplied onboarding actions before publishing listings or contacting matches.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yzlee/skills/hirey-compatible-install)
- [Hirey AI Hi service](https://hi.hirey.ai)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, text]

**Output Format:** [Markdown with inline shell commands and structured status guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce installation handoff text, OpenClaw setup commands, registration guidance, and diagnostic status.]

## Skill Version(s):

0.1.68 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
