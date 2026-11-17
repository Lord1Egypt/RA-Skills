## Description:

Operate Magileads through an OOMOL-connected account to read and manage contact lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to inspect Magileads contact lists and, when requested, create, update, or delete them through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI installation instructions can execute remote code whose full effects were not verified.

Mitigation: Review and approve installation separately, and use a pinned, verified release.

Risk: Changes and deletions can affect contact-list data in the connected Magileads account.

Mitigation: Confirm the intended changes or deletion target before running the action.

## Reference(s):

- [Magileads](https://www.magileads.com/)
- [Magileads API documentation](https://api.magileads.net/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON connector responses and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Connector results depend on the selected contact-list action.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
