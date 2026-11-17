## Description:

Search and read Checkly data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to find Checkly checks and read check details, results, statuses, and account information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions use remote installers and the resulting CLI executable was not verified.

Mitigation: Review and approve the CLI installation separately before setup.

Risk: Agent-skill synchronization may introduce broader agent changes without clear approval.

Mitigation: Decide whether agent-skill synchronization is acceptable before enabling it.

Risk: OOMOL may hold Checkly credentials and process requests.

Mitigation: Use a read-only Checkly API key and decide whether OOMOL's credential handling is acceptable.

## Reference(s):

- [Checkly API documentation](https://www.checklyhq.com/docs/api/)
- [Checkly](https://www.checklyhq.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API data, Text, Guidance]

**Output Format:** [JSON results summarized as text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Checkly information]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
