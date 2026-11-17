## Description:

Use an OOMOL-connected account and the oo CLI to read and manage Fireflies meetings, transcripts, users, and related data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using Fireflies can retrieve transcripts and meeting information, manage AskFred threads and bites, and update meeting or user settings through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Missing-tool setup may execute downloaded installer code without separate approval or integrity checks; the remote installers were unavailable for inspection.

Mitigation: Review and approve a specific CLI release before installation, and disable automatic missing-tool installation.

Risk: Write and destructive actions can change or remove Fireflies data or settings.

Mitigation: Confirm the exact payload and effect before write actions, and get explicit approval before destructive actions.

## Reference(s):

- [Fireflies](https://www.fireflies.ai)
- [Fireflies API documentation](https://docs.fireflies.ai/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Fireflies ClawHub release](https://clawhub.ai/oomol/skills/oo-fireflies)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [oo CLI commands with JSON inputs and structured Fireflies responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available actions and returned data depend on the connected Fireflies account and each action's live schema.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
