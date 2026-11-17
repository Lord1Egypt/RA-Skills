## Description:

Use Perplexity API for web-grounded AI search with source citations for current information, factual queries about recent events, and research-style answers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haru3613](https://clawhub.ai/user/haru3613)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to send Perplexity-backed web research queries, select supported Sonar models, and receive current answers in text, Markdown, or JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports unrelated GitHub WebFetch permissions.

Mitigation: Remove the GitHub WebFetch permissions unless there is a separate documented need for them.

Risk: Queries or custom system prompts may send secrets or private context to the Perplexity API.

Mitigation: Avoid sending secrets or private context in queries or custom system prompts.

Risk: A compromised API key source can affect how the curl request is authorized.

Mitigation: Use only trusted Perplexity API key sources and review key configuration before installing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/haru3613/skills/perplexity-safe)
- [Perplexity API endpoint used by the skill](https://api.perplexity.ai/chat/completions)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text, Markdown with citations, or formatted JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Perplexity API key; supports model, max-token, temperature, search-context, system-prompt, and output-format options.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
