## Description:

Abyssale (abyssale.com). Use this skill for ANY Abyssale request — reading, creating, and updating data. Whenever a task involves Abyssale, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Abyssale account users can inspect designs, projects, fonts, and generated files, and create projects, dynamic image URLs, or banners through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute unverified remote code and enable broader, persistent agent changes; the downloaded installers were unavailable for inspection.

Mitigation: Review and install a verified CLI release separately before using this skill, and decide whether to allow its automatic skill synchronization.

Risk: Abyssale write actions change account state.

Mitigation: Confirm the exact payload and effect with the user before running a write action.

## Reference(s):

- [Abyssale API documentation](https://api-reference.abyssale.com/)
- [Abyssale](https://www.abyssale.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Abyssale skill release on ClawHub](https://clawhub.ai/oomol/skills/oo-abyssale)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON connector responses with concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions can read Abyssale data or create projects, dynamic image URLs, and banners; write actions require user confirmation.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
