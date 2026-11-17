## Description:

Emit OADP discovery signals from an agent workspace so other agents can find it, including file markers, web discovery endpoints, and open discovery network registration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imaflytok](https://clawhub.ai/user/imaflytok)

### License/Terms of Use:


## Use Case:

Developers and agent operators use OADP Emit to add discovery markers, publish optional web discovery files, and send ping or register requests so agent workspaces can be found by OADP-compatible scanners.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to send agent metadata to an unverified external discovery service.

Mitigation: Use only deliberate, non-sensitive names, descriptions, and capability lists; prefer a trusted or self-hosted hub for sensitive environments.

Risk: Persistent OADP comments or endpoint references in boot-read and web server files can keep an agent or workspace discoverable after setup.

Mitigation: Remove OADP comments and related discovery entries from AGENTS.md, .well-known files, robots.txt, or HTML metadata when discovery is no longer intended.

## Reference(s):

- [OADP Protocol Spec](https://onlyflies.buzz/clawswarm/PROTOCOL.md)
- [ClawHub Skill Page](https://clawhub.ai/imaflytok/skills/oadp-emit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash, JSON, HTML, and plain-text configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes commands and snippets that may persist OADP discovery markers or endpoint references in workspace and web server files.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
