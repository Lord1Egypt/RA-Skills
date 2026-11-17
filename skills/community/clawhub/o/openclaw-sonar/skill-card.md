## Description:

Provides a local sonar CLI for OpenRouter-backed Perplexity Sonar web search, cited research, model listing, and optional text, Markdown, or JSON file output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iamjameskeane](https://clawhub.ai/user/iamjameskeane)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run OpenRouter Sonar web search and research queries from a local CLI, list available Sonar models, and save cited results in text, Markdown, or JSON formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Searches, prompts, and optional system prompts are sent to OpenRouter for web-backed model responses.

Mitigation: Use a scoped OpenRouter API key and avoid submitting secrets, regulated data, or other sensitive content.

Risk: The CLI writes output directly to the path supplied by the user.

Mitigation: Choose output paths deliberately and review generated files before relying on or sharing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iamjameskeane/skills/openclaw-sonar)
- [OpenRouter API reference](https://openrouter.ai/docs/api/reference/overview)
- [Bun runtime](https://bun.sh)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [CLI output or files in text, Markdown, or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses OPENROUTER_API_KEY and optional OpenRouter environment variables; file output is written to the user-provided path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
