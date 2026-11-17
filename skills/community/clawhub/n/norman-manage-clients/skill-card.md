## Description:

Manage business clients - list, search, create, or update client information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stanlee000](https://clawhub.ai/user/stanlee000)

### License/Terms of Use:


## Use Case:

Business users and agents use this skill to list, search, create, and update Norman Finance client records, including contact, tax, payment, and notes fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can list client contact details and outstanding balances.

Mitigation: Review requests and outputs involving real customer data before approval.

Risk: The skill can create or update client records, and creation guidance does not explicitly require a final confirmation step.

Mitigation: Confirm intended record changes with the user before approving create or update actions.

Risk: Broad activation wording may trigger client-management behavior for general references to clients, contacts, customers, or Kunden.

Mitigation: Check that the request is specifically about Norman Finance client records before using the skill.

## Reference(s):

- [Norman Finance](https://norman.finance)
- [ClawHub skill listing](https://clawhub.ai/stanlee000/skills/norman-manage-clients)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Markdown]

**Output Format:** [Markdown guidance with client-management tool calls and tabular client summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the Norman Finance MCP server for client records.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
