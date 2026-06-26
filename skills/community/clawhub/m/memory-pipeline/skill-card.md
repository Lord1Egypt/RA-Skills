## Description: <br>
Complete agent memory + performance system that extracts structured facts, builds knowledge graphs, generates briefings, and adds execution-discipline hooks and external knowledge ingestion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joe-rlo](https://clawhub.ai/user/joe-rlo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to maintain durable agent memory across sessions, consolidate notes and transcripts into structured facts, and generate compact briefings for future work. It also supports optional performance hooks for briefing injection, tool policy enforcement, result compression, and after-action notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist notes, transcripts, imported ChatGPT conversations, and generated memory files in the workspace. <br>
Mitigation: Review generated memory files, avoid importing highly sensitive exports, and use dry-run or review workflows before indexing large archives. <br>
Risk: Workspace memory may be processed by configured external LLM providers during extraction, embedding, or briefing generation. <br>
Mitigation: Install only when this processing is acceptable, use dedicated API keys, and understand which provider keys are configured before running the pipeline. <br>
Risk: Optional after-action hooks can append session notes automatically. <br>
Mitigation: Disable or tightly configure after-action hooks when durable session logging is not desired. <br>


## Reference(s): <br>
- [Setup Guide](references/setup.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/joe-rlo/memory-pipeline) <br>
- [Publisher Profile](https://clawhub.ai/user/joe-rlo) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown briefings, JSONL extracted facts, JSON knowledge graphs, markdown summaries, and configuration-driven hook behavior] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes workspace memory files and can call configured LLM providers for extraction, embeddings, and briefing generation.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
