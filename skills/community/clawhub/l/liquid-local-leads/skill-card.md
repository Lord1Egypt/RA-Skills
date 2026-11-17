## Description:

Helps sales teams find US local businesses by category and place, with graded contact emails, phone numbers, verified websites, and buying signals through a paid leads API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leftychris13](https://clawhub.ai/user/leftychris13)

### License/Terms of Use:

MIT-0

## Use Case:

Sales teams and agencies use the skill to identify local business prospects, filter for buying signals, and prepare lead lists for CRM or outreach. It also supports business lookup by phone or domain and website technology checks.

### Deployment Geography for Use:

United States (30 states listed as covered in the skill)

## Known Risks and Mitigations:

Risk: Paid lead searches and lookups can incur x402 charges.

Mitigation: Check the free count and quoted price before approving a paid request; set a lead limit.

Risk: Lead exports include contact details that may be misused for outreach.

Mitigation: Handle emails and phone numbers in accordance with applicable privacy, consent, and anti-spam rules.

Risk: The example payment command runs a third-party npx client.

Mitigation: Review or pin the client before running it.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/leftychris13/skills/liquid-local-leads)
- [Liquid Leads API](https://api.liquidagent.ai/v1/leads)
- [Liquid Leads MCP endpoint](https://api.liquidagent.ai/mcp)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Lead data, Guidance]

**Output Format:** [Markdown guidance and shell commands; lead results may be exported as CSV]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl; paid requests use x402 payments.]

## Skill Version(s):

1.3.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
