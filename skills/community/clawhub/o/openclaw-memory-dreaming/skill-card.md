## Description:

Memory Dreaming is a Markdown and JSON memory framework for AI agents that provides persistent long-term memory, conversation archiving, decay scoring, recall boosting, fact supersession, and dream-cycle consolidation without a vector database or external memory service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ptburkis](https://clawhub.ai/user/ptburkis)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to give OpenClaw agents persistent file-based memory, conversation archives, recall tracking, supersession chains, and dream-cycle maintenance without adding a vector database or graph store.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Readable local memory files and conversation archives can preserve sensitive information, including credentials, in plaintext.

Mitigation: Do not store raw passwords, API keys, tokens, or secrets in memory; use secret manager references and review memory and archive files before broad use.

Risk: Bulk archiving with all-channel options or silent scheduled jobs can collect more chat history than intended.

Mitigation: Use explicit channel and group allowlists first, review archive scope manually, and avoid silent cron templates until the retention policy is clear.

Risk: Conversation summarisation can send transcript text to a configured third-party LLM provider.

Mitigation: Confirm that transcript sharing is acceptable, configure exclude patterns and redaction, or use a self-hosted model when transcripts must remain local.

## Reference(s):

- [Memory Dreaming homepage](https://github.com/ptburkis/openclaw-memory-dreaming)
- [ClawHub skill page](https://clawhub.ai/ptburkis/skills/openclaw-memory-dreaming)
- [Architecture Reference](references/architecture.md)
- [Dream Cycle Reference](references/dream-cycle.md)
- [Cold Start Guide](references/cold-start.md)
- [Cron Templates](references/cron-templates.md)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON snippets and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local Markdown and JSON memory files, archives, summaries, digests, and maintenance logs when its scripts are run.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
