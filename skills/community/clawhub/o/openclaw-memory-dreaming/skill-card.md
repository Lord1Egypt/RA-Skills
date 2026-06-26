## Description: <br>
A Markdown and JSON memory framework with conversation archiving for AI agents, providing persistent long-term memory, recall tracking, temporal fact chains, dream-cycle consolidation, and optional AI-generated conversation summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ptburkis](https://clawhub.ai/user/ptburkis) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators of OpenClaw or similar AI agents use this skill to maintain persistent file-based memory, archive conversations, summarize group context, and run periodic consolidation workflows without requiring a vector database or graph store. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory files and chat archives can preserve sensitive personal or operational information over time. <br>
Mitigation: Install only after deciding what channels and files may be archived, and do not store passwords, tokens, API keys, or session secrets in MEMORY.md or daily notes. <br>
Risk: Conversation summarization can send raw chat transcript content to an external LLM provider. <br>
Mitigation: Review transcripts, configure exclusions, rely on the built-in secret redaction, or use a self-hosted summarization model when external processing is not acceptable. <br>
Risk: Broad archive runs and silent nightly jobs can collect more conversation history than intended. <br>
Mitigation: Avoid `--all` and unattended scheduled jobs until approved channels, groups, retention expectations, and exclusions are scoped. <br>


## Reference(s): <br>
- [Architecture Reference](artifact/references/architecture.md) <br>
- [Cold Start Guide](artifact/references/cold-start.md) <br>
- [Cron Templates](artifact/references/cron-templates.md) <br>
- [Dream Cycle Procedure](artifact/references/dream-cycle.md) <br>
- [Project Homepage](https://github.com/ptburkis/openclaw-memory-dreaming) <br>
- [ClawHub Skill Page](https://clawhub.ai/ptburkis/openclaw-memory-dreaming) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory, metadata, archive, summary, digest, and log files when the included scripts are run.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
