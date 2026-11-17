## Description:

Search global patent collections and retrieve patent details, citations, legal-status snapshots, and portfolio statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

Patent researchers, developers, and businesses use this skill to search for prior art, review patent documents and citations, check legal-status snapshots, and explore company or technology portfolios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API-key forwarding and persistent credential storage require review.

Mitigation: Restrict credential destinations, store keys in host-managed secrets rather than chat, use a spending-limited key, and set a task budget.

Risk: Confidential invention details submitted for patent research may undergo downstream processing.

Mitigation: Review the provider’s privacy policy before submitting confidential invention details.

## Reference(s):

- [PatentMax API Platform](https://api.ip930.com/features/api-platform)
- [ClawHub skill release](https://clawhub.ai/ip930/skills/global-patent-search)
- [API Reference](references/api-reference.md)
- [Search Workflow](references/search-workflow.md)
- [Query Syntax](references/query-syntax.md)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON, CSV, PDF, Patent figure files]

**Output Format:** [JSON records and natural-language summaries, with optional CSV, PDF, and image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results and legal-status data are informational, not legal opinions; verify consequential decisions against official patent registers and qualified counsel.]

## Skill Version(s):

1.1.3 (source: frontmatter; confirmed by release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
