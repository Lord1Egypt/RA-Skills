## Description:

eSignatures.com (esignatures.com). Use this skill for ANY eSignatures.com request — reading, creating, updating, and deleting data. Whenever a task involves eSignatures.com, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to inspect eSignatures.com templates and contracts, create templates or contracts, and retrieve contract content through their connected account. It also supports withdrawing contracts when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup may execute a downloaded CLI installer before its contents have been reviewed.

Mitigation: Review the setup behavior, use a separately reviewed fixed CLI release, and require approval before running downloaded installers.

Risk: The connected account provides access to contract data and can perform actions with external effects.

Mitigation: Use an appropriately scoped connected account and confirm the exact payload before writes or withdrawals.

## Reference(s):

- [eSignatures.com API documentation](https://esignatures.com/docs/api)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [eSignatures.com](https://esignatures.com)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON responses with concise text summaries and action guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may read contract data, create contracts or templates, or withdraw contracts. Writes and withdrawals require user confirmation.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
