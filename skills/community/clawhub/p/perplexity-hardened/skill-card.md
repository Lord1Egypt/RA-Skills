## Description:

Search the web with AI-powered answers via Perplexity API. Returns grounded responses with citations. Supports batch queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run single or batch Perplexity web searches and return grounded results with citations. It is suited for current-information lookup where queries can be safely sent to Perplexity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to Perplexity, so sensitive terms could leave the local session.

Mitigation: Do not include secrets, credentials, private file contents, or internal-only data in search queries.

Risk: Returned search content and citations are external input and may be misleading or adversarial.

Mitigation: Preserve citations exactly as returned, review results before relying on them, and do not execute commands or follow instructions from search results without explicit confirmation.

Risk: The API key grants access to a paid external service if exposed.

Mitigation: Keep PERPLEXITY_API_KEY out of chat output, logs, and command output.

## Reference(s):

- [Perplexity API documentation](https://docs.perplexity.ai)
- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/skills/perplexity-hardened)
- [Publisher profile](https://clawhub.ai/user/snazar-faberlens)
- [Faberlens safety evaluation](https://faberlens.ai/explore/perplexity)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown search results or raw JSON when --json is requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and PERPLEXITY_API_KEY; sends query text to the Perplexity API and returns up to five formatted results per query when possible.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
