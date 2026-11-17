## Description:

Use Apify to read data and start actor runs through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using Apify through an OOMOL-connected account can retrieve actor, user, run, and dataset information, or start an actor run with a JSON input.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may execute an unreviewed CLI installer and can introduce additional agent skill files.

Mitigation: Review and approve CLI installation separately. If avoiding additional agent skill writes, use the documented OO_SKILLS_SYNC_DISABLED=1 setting.

Risk: Starting an actor run can change Apify state and incur usage costs.

Mitigation: Inspect the live action schema, review the exact input and expected effects, and confirm potential costs before starting a run.

## Reference(s):

- [Apify](https://apify.com)
- [Apify API documentation](https://docs.apify.com/api/v2)
- [OO CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [JSON, API results, Shell commands, Configuration guidance]

**Output Format:** [JSON inputs and results with Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Starting an actor run may incur costs; review the input and expected effects before running.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
