## Description:

OOMOL Fusion API (oomol.com). Use this skill for ANY OOMOL Fusion API request — reading, creating, updating, and deleting data. Whenever a task involves OOMOL Fusion API, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use the skill to inspect Fusion API action schemas and run reads, writes, media generation, and other supported tasks through an OOMOL-connected account. Review the payload and expected effect before write or destructive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the skill suspicious based on an unverified remote installer; the partial scan did not inspect the installer or its resulting changes.

Mitigation: Consider avoiding installation until the CLI installer can be independently verified and its effects understood.

Risk: Some API actions may send content to OOMOL or another provider, and generation or editing may run without confirmation.

Mitigation: Review the action's data flow and whether generation or editing requires confirmation before running it.

## Reference(s):

- [OOMOL Fusion API](https://www.oomol.com)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [OOMOL Fusion API skill page](https://clawhub.ai/oomol/skills/oo-fusion-api)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [JSON action payloads, shell commands, and API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected API action; some actions create or modify external data or generate media.]

## Skill Version(s):

1.0.12 (source: frontmatter; server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
