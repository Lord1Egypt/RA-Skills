## Description:

Use this skill to read, create, update, and delete Ragie data through the OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to retrieve Ragie content and manage documents, partitions, and connections through their OOMOL-connected Ragie account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required CLI can silently install or refresh skills across other agents.

Mitigation: Review its skill synchronization behavior and set OO_SKILLS_SYNC_DISABLED=1 before invoking oo when only Ragie access is needed.

Risk: The remote installer and exact installed CLI version are unverified.

Mitigation: Review the installer separately and confirm the CLI version before use.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-ragie)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Ragie homepage](https://www.ragie.ai)
- [Ragie API documentation](https://docs.ragie.ai/docs/step-1-create-an-api-key)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Text]

**Output Format:** [oo CLI commands with JSON payloads and connector results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses depend on the Ragie action and may include retrieved content or operation status.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
