## Description:

QuickBooks Online (quickbooks.intuit.com). Use this skill for ANY QuickBooks Online request — reading, creating, updating, and deleting data. Whenever a task involves QuickBooks Online, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to retrieve QuickBooks records and reports or manage accounting data in a connected QuickBooks Online company. The skill guides the agent to check each action's input schema and seek confirmation before changes or deletions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup may run downloaded installer code that the security review could not inspect.

Mitigation: Review setup before installing; prefer a manually installed, reviewed, verified CLI release, and require approval before software or skill changes.

Risk: Actions can change financial records, and some deletions are permanent.

Mitigation: Before any write, confirm the exact payload and effect with the user; before a destructive action, confirm its target and obtain explicit approval.

## Reference(s):

- [QuickBooks Online](https://quickbooks.intuit.com)
- [QuickBooks Online Accounting API documentation](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/account)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-quickbooks)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [QuickBooks record or report data returned as JSON, with text summaries and guidance as needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected QuickBooks company and the requested action.]

## Skill Version(s):

1.0.2 (source: server-resolved release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
