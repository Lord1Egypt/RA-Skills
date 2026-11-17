## Description:

Deep search via Perplexity API with search, reason, and research modes for AI-grounded answers with citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericsantos](https://clawhub.ai/user/ericsantos)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to query Perplexity for current facts, complex reasoning, and deeper research reports with optional recency, domain, language, and JSON controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search prompts, filters, and the API token are sent to Perplexity.

Mitigation: Install only when that data sharing is acceptable, and provide PERPLEXITY_API_KEY through an environment variable or secret manager where possible.

Risk: Research mode can incur higher Perplexity API costs than normal search.

Mitigation: Reserve research mode for queries where deeper analysis justifies the cost.

## Reference(s):

- [Perplexity Documentation](https://docs.perplexity.ai)
- [Perplexity Chat Completions API](https://api.perplexity.ai/chat/completions)
- [ClawHub Skill Page](https://clawhub.ai/ericsantos/skills/perplexity-deep-search)
- [ClawHub Publisher Profile](https://clawhub.ai/user/ericsantos)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Plain text or JSON; answer text may include a Sources list when citations are returned.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports search, reason, and research modes plus recency, domain, language, and raw JSON options.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
