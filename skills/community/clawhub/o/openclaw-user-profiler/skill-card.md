## Description:

Builds or updates a concise user.md profile through conversation and recommends Claude Code skills based on the user's role.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eamanc-lab](https://clawhub.ai/user/eamanc-lab)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to create or update lightweight agent profile memory and receive role-based skill recommendations. It is intended for conversational profiling, user.md generation, and curated skill discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates or updates user.md profile memory, which can persist personal context and may be injected into future agent prompts.

Mitigation: Review the generated profile before writing it and avoid storing secrets, government IDs, health, financial, or other sensitive data.

Risk: The skill recommends external skills and may provide unpinned npx skills add commands.

Mitigation: Verify each recommended skill's source, version, publisher, and permissions before installation.

## Reference(s):

- [OpenClaw Persona Forge](https://github.com/eamanc-lab/openclaw-persona-forge)
- [User Profile Intake Guide](references/user-profile-fields.md)
- [user.md Template](references/user-md-template.md)
- [Role Skill Recommendation Catalog](references/role-skill-catalog.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown profile content, recommendation lists, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write or update user.md after user confirmation; recommendations can include third-party skill install commands.]

## Skill Version(s):

2.3.1 (source: server release and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
