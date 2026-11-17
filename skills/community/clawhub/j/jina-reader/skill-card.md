## Description:

Web content extraction via Jina AI Reader API. Three modes: read (URL to markdown), search (web search + full content), ground (fact-checking). Extracts clean content without exposing server IP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericsantos](https://clawhub.ai/user/ericsantos)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve clean web page content, perform web searches with extracted result content, and fact-check statements through Jina AI Reader endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted URLs, search terms, page targets, and fact-check statements are sent to Jina AI for third-party processing.

Mitigation: Do not use the skill with private intranet URLs, secrets, regulated data, or confidential research topics unless third-party processing is approved.

Risk: API keys can be exposed on shared systems if stored or handled casually.

Mitigation: Prefer JINA_API_KEY from an environment variable or a managed secret store, and keep file-based credentials restricted to the local user.

## Reference(s):

- [Jina Reader](https://jina.ai/reader)
- [ClawHub Skill Page](https://clawhub.ai/ericsantos/skills/jina-reader)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown, plain text, or JSON returned by the Jina AI Reader API wrapper]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; may use JINA_API_KEY from the environment or ~/.config/jina/api_key.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
