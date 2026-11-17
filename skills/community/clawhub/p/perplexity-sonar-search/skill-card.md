## Description:

Perplexity Sonar search and answer generation through AIsa for citation-backed web answers, analytical reasoning, and long-form research reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisadocs](https://clawhub.ai/user/aisadocs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when they need Perplexity-powered search through AIsa for cited answers, stronger synthesis, multi-step reasoning, or longer research reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries, optional system prompts, and AISA_API_KEY-authenticated requests are sent to api.aisa.one for Perplexity processing.

Mitigation: Use only in environments approved for AIsa/Perplexity use and avoid submitting secrets or confidential data unless approved.

Risk: Long-form Deep Research requests may time out or require retries.

Mitigation: Narrow the query, retry later, or use Sonar Pro or Sonar Reasoning Pro when a faster answer is needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aisadocs/skills/perplexity-sonar-search)
- [OpenClaw](https://openclaw.ai)
- [AIsa Sonar API Reference](https://docs.aisa.one/reference/post_perplexity-sonar)
- [AIsa Sonar Pro API Reference](https://docs.aisa.one/reference/post_perplexity-sonar-pro)
- [AIsa Sonar Reasoning Pro API Reference](https://docs.aisa.one/reference/post_perplexity-sonar-reasoning-pro)
- [AIsa Sonar Deep Research API Reference](https://docs.aisa.one/reference/post_perplexity-sonar-deep-research)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON API responses and markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY; Sonar Deep Research uses longer timeouts and retries.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
