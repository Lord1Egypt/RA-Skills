## Description:

Finage (finage.co.uk). Use this skill for ANY Finage request — searching and reading data. Whenever a task involves Finage, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to search and read U.S. stock market data from Finage, including quotes, trades, snapshots, aggregates, previous closes, and symbol listings through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions include remote installer commands that may execute code without clear user approval.

Mitigation: Review the setup source, install a verified fixed oo CLI release, and explicitly control bundled-skill synchronization; the publisher documents OO_SKILLS_SYNC_DISABLED in the command reference.

Risk: OOMOL mediates Finage credentials and requests, while hosted connector internals were not verified.

Mitigation: Understand that requests and credentials pass through OOMOL, and connect only an account authorized for this use.

## Reference(s):

- [Finage](https://finage.co.uk)
- [Finage U.S. stocks API documentation](https://finage.co.uk/docs/api/us-stocks/stock-last-quote)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API calls, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline oo CLI commands; connector results are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action-specific schemas and response fields; actions cover U.S. stock symbols.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
