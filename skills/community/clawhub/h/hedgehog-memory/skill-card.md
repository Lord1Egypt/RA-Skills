## Description:

HedgehogMemory provides persistent radial memory for AI agents with hierarchical compression so agents can store, summarize, search, and restore prior work context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vvxer](https://clawhub.ai/user/vvxer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use HedgehogMemory to add persistent, queryable session memory to AI agents, including compressed overviews and on-demand restoration of detailed prior context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Long-lived local memory may retain private transcripts, secrets, or environment data.

Mitigation: Keep the storage directory outside source control, avoid committing memory files, and do not save secrets or private transcripts.

Risk: Restored memory can contain stale or adversarial historical content that is reintroduced into an agent context.

Mitigation: Treat restored memory as untrusted context and review it before acting on it.

Risk: Optional LLM-based summarization may send memory content to an external API when an API key is configured.

Mitigation: Prefer the local keyword summarizer for sensitive projects or review data handling before enabling an API summarizer.

## Reference(s):

- [HedgehogMemory ClawHub release](https://clawhub.ai/vvxer/skills/hedgehog-memory)
- [HedgehogMemory project link declared by artifact](https://github.com/vvxer/HedgehogMemory)
- [HedgehogMemory issues link declared by artifact](https://github.com/vvxer/HedgehogMemory/issues)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python snippets, shell commands, and environment-variable configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Memory output is stored locally by default and may use optional OpenAI or LiteLLM summarizers when configured.]

## Skill Version(s):

0.1.1 (source: server release metadata; artifact frontmatter and pyproject.toml show 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
