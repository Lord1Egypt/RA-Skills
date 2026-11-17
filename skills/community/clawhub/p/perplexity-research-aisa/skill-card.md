## Description:

Produce citation-backed deep research answers through Perplexity Sonar models via AISA for synthesized research, comparative analysis, and long-form cited answers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for cited research synthesis, comparative analysis, and long-form answers through AISA-backed Perplexity Sonar and related search endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research prompts, URLs, and retrieved content may be sent to AISA-backed external APIs.

Mitigation: Avoid secrets, private documents, internal URLs, and sensitive business data; review intended queries before execution.

Risk: The bundled client exposes broader web search and URL extraction behavior than the concise skill description advertises.

Mitigation: Review the available commands before deployment and restrict usage to the advertised Perplexity research workflow unless the broader surface is explicitly accepted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bibaofeng/skills/perplexity-research-aisa)
- [AISA service](https://aisa.one)
- [AISA API endpoint](https://api.aisa.one/apis/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or terminal text with citations and source URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY and may return API usage metadata when provided by the external service.]

## Skill Version(s):

1.0.0 (source: server release metadata, target metadata, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
