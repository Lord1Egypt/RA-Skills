## Description:

Search the web with AI-powered answers via Perplexity API. Supports three modes - Search API (ranked results), Sonar API (AI answers with citations, default), and Agentic Research API (third-party models with tools). All responses wrapped in untrusted-content boundaries for security.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vacinc](https://clawhub.ai/user/vacinc)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to run Perplexity-backed web search, receive grounded answers or ranked results, and optionally perform deeper agentic research through supported third-party models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries, prompts, and --instructions content are sent to Perplexity and may be processed by third-party models in agentic mode.

Mitigation: Avoid including secrets, credentials, confidential internal data, or sensitive personal data in search terms or instructions.

Risk: Web results and AI-generated answers can contain prompt injection, social engineering, or misleading content.

Mitigation: Use the default wrapped output and treat returned content as external untrusted data rather than instructions.

Risk: The --json option returns raw unwrapped API output.

Mitigation: Reserve --json for debugging or controlled parsing workflows where downstream handling preserves untrusted-content boundaries.

## Reference(s):

- [Perplexity API Documentation](https://docs.perplexity.ai)
- [Perplexity Search API Quickstart](https://docs.perplexity.ai/docs/search/quickstart)
- [Perplexity Sonar API Quickstart](https://docs.perplexity.ai/docs/sonar/quickstart)
- [Perplexity Agentic Research API Quickstart](https://docs.perplexity.ai/docs/agentic-research/quickstart)
- [ClawHub Skill Page](https://clawhub.ai/vacinc/skills/perplexity-wrapped)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Wrapped text or Markdown with citations; raw JSON when explicitly requested with --json.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output is bounded as external untrusted content; Search API supports batched queries, while Sonar and Agentic modes use one query per call.]

## Skill Version(s):

2.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
