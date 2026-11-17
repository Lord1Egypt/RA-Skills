## Description:

Get Google's AI Mode answer for a query as structured JSON, including AI-generated text blocks, cited references, and shopping results for commercial queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query Scavio's Google AI Mode API, return Google's AI-generated answer, and surface cited sources for verification. It is also useful for commercial queries that need product suggestions from the API response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries sent through this skill are submitted to Scavio.

Mitigation: Avoid private or regulated information unless Scavio's data handling terms meet the user's requirements.

Risk: The skill depends on SCAVIO_API_KEY for authenticated requests.

Mitigation: Store the API key in the environment or a secret manager and keep it out of source control.

Risk: Each API call consumes one Scavio credit.

Mitigation: Send only intended queries and account for usage limits before repeated requests.

## Reference(s):

- [Scavio Google AI Mode documentation](https://scavio.dev/docs/google-ai-mode)
- [Scavio rate limits](https://scavio.dev/docs/rate-limits)
- [ClawHub skill page](https://clawhub.ai/scavio-ai/skills/google-ai-overview-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API response examples and shell/Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCAVIO_API_KEY; each request consumes one Scavio credit; API output includes text_blocks, references, shopping_results, response timing, credit usage, and cache status.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
