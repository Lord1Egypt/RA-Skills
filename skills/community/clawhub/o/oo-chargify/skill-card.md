## Description:

Maxio Advanced Billing (maxio.com). Use this skill for ANY Maxio Advanced Billing request — searching and reading data. Whenever a task involves Maxio Advanced Billing, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and billing operators use the skill to search and read Maxio Advanced Billing customer, product, and subscription records through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions run remote CLI installer scripts, whose contents are not verified by the bundled artifact.

Mitigation: Review and approve the installer before running it, and decide whether automatic skill synchronization is acceptable; consult the documented OO_SKILLS_SYNC_DISABLED control.

Risk: The connected service provides access to Maxio billing data through the OOMOL account.

Mitigation: Connect only the intended Maxio account and review the access granted to OOMOL.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [oo CLI command reference: environment variables](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [Maxio Advanced Billing](https://www.maxio.com/product/advanced-billing)
- [Maxio API documentation](https://developers.maxio.com/)
- [OOMOL Maxio connection setup](https://console.oomol.com/connections/chargify)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Shell commands, Guidance]

**Output Format:** [JSON data returned from read-only connector actions, with text summaries and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Customer, product, and subscription lookups; supported actions include search and pagination filters.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
