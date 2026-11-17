## Description:

Fast, low-latency text generation using Groq free-tier models for summaries, reasoning, trading analysis, and tool-assisted responses with automatic fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[silaskade](https://clawhub.ai/user/silaskade)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to route concise text-generation, summarization, reasoning, and trading-analysis prompts through Groq-hosted models with rate-limit handling and fallback configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can call external APIs and may send prompt content to Groq-hosted models.

Mitigation: Install only in a contained workspace, use a dedicated Groq API key, and review prompts and configured tools before use.

Risk: Recent conversation text can be retained locally in plaintext.

Mitigation: Disable or tightly scope memory and chat retention, and avoid using the skill with sensitive prompts unless retention is controlled.

Risk: The artifact grants broad memory and repository authority beyond basic text generation.

Mitigation: Require explicit approval before commits, pushes, trusted-instruction edits, or other repository changes.

Risk: Credential-shaped configuration values may be present in tracked config.

Mitigation: Remove credential-shaped values from tracked files and supply secrets through a dedicated environment file or secret manager.

## Reference(s):

- [Groq Bot ClawHub page](https://clawhub.ai/silaskade/skills/groq-bot)
- [Publisher profile](https://clawhub.ai/user/silaskade)
- [Sorare GraphQL API](https://api.sorare.com/graphql)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown or plain text with optional inline code and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call external APIs, retain recent conversation text locally, and use configured rate limits and fallback models.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
