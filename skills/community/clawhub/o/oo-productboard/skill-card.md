## Description:

Productboard (productboard.com). Use this skill for ANY Productboard request — searching and reading data. Whenever a task involves Productboard, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers and teams use this skill to search and read Productboard workspace data through their OOMOL-connected account. It provides read operations for entities, notes, members, teams, and workspace configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup instructions run downloaded installers directly in a shell, which executes code obtained from the network.

Mitigation: Review the setup behavior before installing. Install and verify the CLI yourself, or require separate approval before the agent runs downloaded installers.

Risk: Using OOMOL to mediate access to a Productboard account introduces a third-party connection path.

Mitigation: Consider whether you want OOMOL to mediate access to your Productboard account.

## Reference(s):

- [Productboard](https://www.productboard.com)
- [Productboard API Reference](https://developer.productboard.com/reference)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [ClawHub Productboard skill page](https://clawhub.ai/oomol/skills/oo-productboard)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON action results and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read operations return Productboard data; setup and action instructions are provided as guidance.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
