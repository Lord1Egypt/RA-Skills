## Description:

Gets Google's AI Mode answer for a query as structured JSON, including AI-generated text blocks, cited references, and shopping results for commercial queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to ask Google's AI Mode-style questions through Scavio and return grounded answers with references, including product suggestions for commercial queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries are sent to Scavio and may be billable under the API key used.

Mitigation: Use a Scavio API key approved for this workflow and avoid submitting secrets, confidential business information, or sensitive personal data unless permitted by your data-sharing requirements.

Risk: The skill returns AI-generated answers and cited sources from a third-party API.

Mitigation: Surface the references returned by the API and review them before relying on the answer.

Risk: Missing or invalid SCAVIO_API_KEY prevents API calls.

Mitigation: Configure SCAVIO_API_KEY before use and handle authentication, billing, rate limit, and temporary upstream errors.

## Reference(s):

- [Scavio Google AI Mode documentation](https://scavio.dev/docs/google-ai-mode?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-ai-mode-api)
- [Scavio rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-ai-mode-api)
- [ClawHub skill page](https://clawhub.ai/scavio-ai/skills/google-ai-mode-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown answers with cited references, JSON API responses, and inline code or shell commands when setup is needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCAVIO_API_KEY; each request costs 1 Scavio credit and returns a single AI Mode answer without pagination.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
