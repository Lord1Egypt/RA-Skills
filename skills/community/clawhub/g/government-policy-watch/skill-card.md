## Description:

Track official government documents in the Chinng AI-Agent Portal across the US Federal Register, EU EUR-Lex, and Japanese agency feeds for regulatory monitoring, comment deadlines, effective dates, and primary-source policy reading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chinng-inta](https://clawhub.ai/user/chinng-inta)

### License/Terms of Use:

MIT-0

## Use Case:

External users, policy analysts, compliance teams, and developers use this skill to monitor official government records from the portal, identify new or revised documents, and report regulatory details with official source attribution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated or feed-derived summaries may be mistaken for official document content.

Mitigation: Report summaries as document content only when summary_source is official; otherwise state that the portal has no usable document text and link to the official source.

Risk: Regulatory deadlines, effective dates, or Japanese-era dates may be misstated if copied from generated restatements.

Mitigation: Verify substance, dates, and deadlines against the official government source URL and preserve the date format used by the source.

Risk: Automated related records or entity fields may overstate relevance.

Mitigation: Use structured fields such as country, source, document_type, agency_names, provenance, and published-date bounds when selecting and attributing records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chinng-inta/skills/government-policy-watch)
- [Chinng AI-Agent Portal MCP endpoint](https://portal.chinng-lab-srv.dev/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or text reports with official source links and optional inline shell commands for MCP setup]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should distinguish new and revised documents, include portal and official URLs, and preserve source date formats.]

## Skill Version(s):

0.2.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
