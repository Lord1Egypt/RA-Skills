## Description:

Operate Customer.io through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People working with Customer.io use this skill to manage customer profiles and events through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup guidance uses remote CLI installers without pinning a version and does not clearly disclose possible changes to other agent skills through automatic synchronization.

Mitigation: Install a pinned, verified CLI yourself and review or disable automatic synchronization of other agent skills before enabling the skill.

Risk: The skill operates on customer data through connected-account permissions.

Mitigation: Review OOMOL's handling of customer data and the connected account's permissions; retain explicit approval for all writes and deletions.

## Reference(s):

- [Customer.io](https://customer.io/)
- [Customer.io Track API documentation](https://docs.customer.io/integrations/api/track/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [JSON payloads and connector responses, with inline shell commands and guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action schemas are checked before requests; writes and deletions require explicit user approval.]

## Skill Version(s):

1.0.5 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
