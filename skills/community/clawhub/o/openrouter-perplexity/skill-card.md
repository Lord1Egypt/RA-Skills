## Description:

Search the web with AI-powered answers, returning grounded responses with citations and supporting single or batch queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrnicholasbcarter-code](https://clawhub.ai/user/mrnicholasbcarter-code)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to run single or batch web searches and receive concise, cited results. Raw JSON output is available when downstream automation needs structured search responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and the OPENROUTER_API_KEY authorization token are sent to OpenRouter.

Mitigation: Install only where sending those queries and credentials to OpenRouter is acceptable, and use a dedicated key that can be rotated if needed.

Risk: The skill documentation describes Perplexity, while the executable sends requests to OpenRouter.

Mitigation: Review publisher clarification and endpoint behavior before deployment, and describe the OpenRouter dependency to users.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mrnicholasbcarter-code/skills/openrouter-perplexity)
- [OpenRouter](https://openrouter.ai/)
- [OpenRouter API Endpoint](https://openrouter.ai/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, JSON]

**Output Format:** [Markdown-formatted search summaries with citations, or raw JSON when --json is used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Displays up to five result items per response branch and truncates long snippets for readable output.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
