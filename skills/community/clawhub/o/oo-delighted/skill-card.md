## Description:

Use Delighted through the connected OOMOL account to read survey data and metrics, create or update people, manage unsubscribes, and delete records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers use this skill to work with people, survey responses, and metrics in a connected Delighted account. It supports reading data, creating or updating people, unsubscribing people, and deleting records; state-changing actions require confirmation as described in the skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The first-time setup fallback may execute downloaded software, and managed-skill synchronization may change skills installed for other agents.

Mitigation: Review and approve CLI installation separately, and check managed-skill synchronization settings before using setup.

Risk: Delighted account data passes through OOMOL, while the remote installers and hosted connector implementation were not verified.

Mitigation: Connect only the intended Delighted account and consider this data flow when choosing which account to use.

## Reference(s):

- [Delighted skill release](https://clawhub.ai/oomol/skills/oo-delighted)
- [Delighted](https://delighted.com)
- [Delighted API documentation](https://app.delighted.com/docs/api)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON responses and concise natural-language guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read actions return account data; changes and deletions require confirmation according to the skill.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
