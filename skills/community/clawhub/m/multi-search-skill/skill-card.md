## Description:

Search 8 knowledge domains in one query: live web, academic papers, scholarly works, arXiv preprints, biomedical papers, chemical compounds, government datasets, and dictionary resources via x402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plagtech](https://clawhub.ai/user/plagtech)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and research-oriented agents use this skill to select relevant search domains, call paid gateway endpoints, and synthesize cited results from web, academic, scientific, government, chemistry, biomedical, and dictionary sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, article URLs, and research parameters are sent to the configured gateway and downstream data providers.

Mitigation: Avoid submitting sensitive data and use the default or another trusted HTTPS gateway only after reviewing its data-handling expectations.

Risk: Broad multi-domain searches can trigger paid x402 or API usage.

Mitigation: Limit searches to relevant domains, monitor account usage, and keep the API key or subscription credential scoped and protected.

Risk: Setting RESEARCH_GATEWAY_URL changes where requests and credentials are sent.

Mitigation: Leave RESEARCH_GATEWAY_URL unset unless intentionally using a trusted HTTPS gateway.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/plagtech/skills/multi-search-skill)
- [Publisher profile](https://clawhub.ai/user/plagtech)
- [OpenClaw](https://openclaw.ai)
- [ClawHub](https://clawhub.ai)
- [Default research gateway](https://gateway.spraay.app)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses from gateway calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search outputs should identify which domains were queried and cite returned URLs, DOIs, PMIDs, or arXiv IDs when available.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
