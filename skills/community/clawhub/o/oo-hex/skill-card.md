## Description:

Hex (hex.tech). Use this skill for ANY Hex request — reading, creating, updating, and deleting data. Whenever a task involves Hex, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to inspect Hex projects and runs, start project runs, and cancel in-progress runs through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup executes unverified remote code and may make broad changes to the agent environment.

Mitigation: Use a reviewed CLI release, explicitly approve local setup changes, and retain confirmations before starting or canceling Hex runs.

## Reference(s):

- [Hex API documentation](https://learn.hex.tech/docs/api-integrations/api/overview)
- [Hex](https://hex.tech)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Structured Hex project and run data with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Hex account and the selected action.]

## Skill Version(s):

1.0.5 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
