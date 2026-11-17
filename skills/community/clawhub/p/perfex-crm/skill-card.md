## Description:

Work in a Perfex CRM through the Perfex Connect MCP server. Find customers, invoices, leads and tickets, read records, and prepare changes that a person approves in Perfex.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sbakelongmit](https://clawhub.ai/user/sbakelongmit)

### License/Terms of Use:

MIT-0

## Use Case:

CRM staff use the skill to find and read customer, invoice, lead, and ticket records, then prepare requested changes for approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A change may be committed after agreement in chat without a separate approval inside Perfex.

Mitigation: Use a scoped read-only token by default; enable Ask Before Every Change when every write needs separate approval inside Perfex.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sbakelongmit/skills/perfex-crm)

## Skill Output:

**Output Type(s):** [Text, Configuration, Guidance]

**Output Format:** [Natural language responses and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CRM record links and approval request details.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
