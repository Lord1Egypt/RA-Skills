## Description:

B2B lead lists with verified emails, work-email lookup, LinkedIn profile enrichment and company search via Parvenu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parvenudev](https://clawhub.ai/user/parvenudev)

### License/Terms of Use:

MIT-0

## Use Case:

Sales, recruiting, and business development teams use the skill to build B2B lead lists, find work emails, enrich LinkedIn profiles, and search for companies through Parvenu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports an external POST, and it does not confirm what data is transmitted.

Mitigation: Review request fields before use and avoid submitting sensitive data unless its transmission to Parvenu is approved.

Risk: Some Parvenu API actions consume credits from the user's account.

Mitigation: Tell the user the likely credit cost before billed calls, confirm before calls over about 50 credits, and report credits used.

## Reference(s):

- [Parvenu developer documentation](https://developer.parvenu.io)
- [Parvenu](https://parvenu.io)
- [Parvenu MCP server](https://enterprise.parvenu.io/mcp)

## Skill Output:

**Output Type(s):** [Text, Structured data, Guidance]

**Output Format:** [Text summaries and structured lead, contact, profile, and company results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected workflow, filters, and data returned by Parvenu.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
