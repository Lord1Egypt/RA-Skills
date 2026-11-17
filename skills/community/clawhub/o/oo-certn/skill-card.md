## Description:

Connects an OOMOL account to Certn to search and read background-check cases and related records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Teams and agents use the skill to retrieve Certn cases and related users, groups, events, packages, questionnaires, and tags through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup may run downloaded installer code whose changes have not been inspected.

Mitigation: Review and verify the CLI installer and any bundled skill changes before installation; use a narrowly scoped Certn connection.

Risk: The skill accesses sensitive Certn records through an OOMOL-connected account.

Mitigation: Use only the access scope needed for the task and review the data returned before sharing it.

## Reference(s):

- [Certn API documentation](https://centric-api-docs.certn.co/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Certn homepage](https://certn.co)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands]

**Output Format:** [Certn connector results in JSON, invoked with oo CLI shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results and pagination fields depend on the selected Certn action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
