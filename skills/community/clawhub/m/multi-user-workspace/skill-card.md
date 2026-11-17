## Description:

Multi-user workspace management with sandbox permissions, user profiles, and relationship networks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shun-dong](https://clawhub.ai/user/shun-dong)

### License/Terms of Use:


## Use Case:

Developers and workspace administrators use this skill to structure OpenClaw workspaces for multiple users with per-user sessions, sandbox permissions, profile files, relationship files, and cross-user information boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Loose session suffix matching can route the wrong user into an admin or privileged configuration.

Mitigation: Use authenticated identities, strict user ID allowlists, and exact session bindings or full-key matches.

Risk: Profile and relationship files can expose other users' data when relationship matching, privacy rules, or consent rules are weak.

Mitigation: Use exact relationship membership checks, explicit privacy and consent rules for stored profile and relationship data, and a restricted sandbox for unmatched sessions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shun-dong/skills/multi-user-workspace)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, guidance]

**Output Format:** [Markdown with JSON5 configuration examples and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance covers workspace structure, session routing, sandbox permissions, user profiles, relationship files, and cross-user information boundaries.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
