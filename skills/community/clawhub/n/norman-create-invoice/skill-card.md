## Description:

Creates and optionally sends a new Norman Finance invoice to a client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stanlee000](https://clawhub.ai/user/stanlee000)

### License/Terms of Use:


## Use Case:

Finance operators and external users use this skill to collect client and invoice details, create an invoice in Norman Finance, review the total, and optionally send it by email.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect client, line item, VAT, date, or amount details could create an inaccurate invoice record.

Mitigation: Review the collected invoice details and generated summary before allowing the invoice workflow to proceed.

Risk: Sending the invoice emails billing information to the selected client.

Mitigation: Approve sending only after confirming the invoice is ready to email.

## Reference(s):

- [Norman Finance](https://norman.finance)
- [ClawHub Skill Page](https://clawhub.ai/stanlee000/skills/norman-create-invoice)

## Skill Output:

**Output Type(s):** [Text, API Calls, Guidance]

**Output Format:** [Conversational text with invoice summaries and confirmation prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create invoice records and send invoice email through Norman Finance MCP tools after user review.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
