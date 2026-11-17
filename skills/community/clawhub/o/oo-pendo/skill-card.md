## Description:

Use Pendo through an OOMOL-connected account to search and read page and feature data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Pendo users use this skill to inspect page and feature data through their OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic installation can execute unchecked code and skill synchronization can make broader changes to an agent's skills.

Mitigation: Review the CLI setup, prefer a verified fixed release installed under your control, and set OO_SKILLS_SYNC_DISABLED=1 if you do not want automatic synchronization.

Risk: Connecting Pendo gives OOMOL access through the configured integration credentials.

Mitigation: Connect only an account authorized for this use and review the connection before running Pendo actions.

## Reference(s):

- [Pendo API documentation](https://engageapi.pendo.io/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [Pendo homepage](https://www.pendo.io)

## Skill Output:

**Output Type(s):** [API data, JSON, Guidance]

**Output Format:** [JSON results with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pendo page and feature lookups, action schemas, and integration status.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
