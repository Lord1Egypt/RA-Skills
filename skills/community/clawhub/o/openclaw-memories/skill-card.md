## Description:

Agent memory with ALMA meta-learning, remote LLM fact extraction, and full-text search over workspace Markdown memory files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arosstale](https://clawhub.ai/user/arosstale)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use Openclaw Memory to experiment with memory-system designs, extract structured facts from conversations, and search Markdown-based memory stores for OpenClaw-style agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation text processed by the Observer may be sent to a configured remote LLM provider.

Mitigation: Avoid processing secrets or private conversations unless that provider use is approved for the data.

Risk: Environment-based API key fallback may send the wrong key to an external provider.

Mitigation: Pass an explicit provider-specific apiKey and verify it matches the selected provider.

Risk: Extracted facts may be incorrect, incomplete, or unsuitable for persistent memory.

Mitigation: Review extracted facts as untrusted before adding them to a long-lived memory store.

## Reference(s):

- [Openclaw Memory ClawHub page](https://clawhub.ai/arosstale/skills/openclaw-memories)
- [Unicode smuggling scanner reference](https://embracethered.com/blog/posts/2026/scary-agent-skills/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown prose with TypeScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Observer can make remote LLM API calls when configured; ALMA and Indexer operate offline.]

## Skill Version(s):

2.1.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
