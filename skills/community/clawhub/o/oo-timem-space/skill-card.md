## Description:

Use TiMEM Space to read, create, update, and delete data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to search and manage TiMEM Space memories and related data through their OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may install software from remote endpoints whose contents were not verified during review.

Mitigation: Review and verify the oo CLI release before installing it.

Risk: Setup or memory actions can create lasting agent changes or persistent TiMEM Space data changes.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 before the first CLI invocation if skill synchronization is not wanted, and approve only the intended changes and conversation storage. Confirm the exact target and effect before write or delete actions.

## Reference(s):

- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [TiMEM Space](https://space.timem.cloud)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [CLI commands with JSON input and structured service responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands and payloads depend on the selected TiMEM Space action.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
