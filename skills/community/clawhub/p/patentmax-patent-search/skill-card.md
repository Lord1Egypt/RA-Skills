## Description:

Searches PatentMax for patents across major jurisdictions and helps analyze claims, citations, legal status, technology trends, and patent portfolios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, patent professionals, and developers use this skill to search prior art, inspect individual patents, and summarize citation patterns, technology trends, or company portfolios. It requires a PatentMax API key and does not provide a legal opinion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Patent queries may disclose unpublished inventions, formulas, source code, or business details to an external service.

Mitigation: Redact sensitive details or obtain explicit approval before sending queries to the PatentMax API.

Risk: API calls can incur charges and expose a paid API key if configuration is shared.

Mitigation: Explain estimated costs before searching; keep the key in a private environment or secret store and check the configured API host.

Risk: Patent search results and legal-status snapshots may be incomplete or mistaken for legal conclusions.

Mitigation: Document search coverage and evidence, verify consequential status claims against official patent registers, and seek qualified legal advice for patentability or infringement decisions.

## Reference(s):

- [PatentMax skill release](https://clawhub.ai/ip930/skills/patentmax-patent-search)
- [PatentMax API platform](https://api.ip930.com/features/api-platform)
- [API reference](references/api-reference.md)
- [Search workflow](references/search-workflow.md)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown patent-search report and concise text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include search scope, patent candidates, evidence, and limitations.]

## Skill Version(s):

3.4.1 (source: skill frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
