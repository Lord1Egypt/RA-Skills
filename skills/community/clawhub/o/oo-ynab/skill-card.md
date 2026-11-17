## Description:

YNAB (ynab.com). Use this skill for ANY YNAB request — searching and reading data. Whenever a task involves YNAB, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using YNAB through an OOMOL-connected account can retrieve plans, accounts, categories, payees, months, transactions, and user information with the oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting YNAB gives OOMOL access to sensitive financial information.

Mitigation: Connect only the YNAB account intended for these requests and review what information each action returns.

Risk: Setup can execute unverified installation code without clear user control, and the remote installer and hosted connector implementation remain unverified.

Mitigation: Review and approve a specific CLI version before setup, and consider disabling automatic skill synchronization.

## Reference(s):

- [YNAB homepage](https://www.ynab.com)
- [YNAB API documentation](https://api.ynab.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON data returned through the oo CLI, with command examples in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned data depends on the selected YNAB read action and may include sensitive financial information.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
