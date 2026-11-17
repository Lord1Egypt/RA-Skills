## Description:

Control and inspect Home Assistant via REST API for entities, states, services, scenes, scripts, and automations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hogar23](https://clawhub.ai/user/hogar23)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to inspect Home Assistant state, resolve named entities, and execute service calls for configured devices and automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can inspect and control physical Home Assistant devices using a long-lived token.

Mitigation: Use a narrowly permissioned token where possible, run the self-check before actions, and review the action preview before allowing service calls.

Risk: Public or remote Home Assistant URLs configured with HTTP may expose sensitive token-backed traffic.

Mitigation: Use HTTPS for HA_URL_PUBLIC and any remote access URL; keep local HTTP endpoints limited to trusted local networks.

Risk: High-impact device actions such as locks, alarms, covers, doors, or climate changes can affect safety or property.

Mitigation: Keep confirmation prompts enabled for risky domains and avoid --yes unless the user explicitly requested the exact action.

Risk: Generated entity and naming reference files can reveal private household metadata.

Mitigation: Treat generated references as private configuration and avoid publishing real entity names, hostnames, or tokens.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hogar23/skills/home-assistant-control)
- [Home Assistant Entity Map](references/entities.md)
- [Home Assistant Naming Context](references/naming-context.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Home Assistant API responses or generated local reference files when the user runs the bundled scripts.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
