## Description:

Memory Pipeline extracts structured facts, builds knowledge graphs, generates briefings, imports external conversation exports, and applies optional performance hooks for agent consistency across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joe-rlo](https://clawhub.ai/user/joe-rlo)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to extract durable facts from notes and transcripts, build a knowledge graph, generate session briefings, ingest ChatGPT exports, and apply optional execution-discipline hooks across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private notes, transcripts, profile files, todos, and extracted facts may be sent to external LLM providers.

Mitigation: Review and prune memory inputs before running the pipeline, keep secrets out of memory files, and configure only approved providers and API keys.

Risk: Stored memory can be injected into future agent prompts and influence later work.

Mitigation: Use explicit workspace scoping, keep configured memory files narrow, and review generated briefings before relying on them.

Risk: Heartbeat automation can run memory extraction and briefing generation without a fresh manual review.

Mitigation: Leave heartbeat automation disabled until permitted sources, provider usage, and retention expectations are defined.

Risk: After-action hooks append durable notes from session outputs and tool-call summaries.

Mitigation: Set the after-action output path deliberately, review appended notes periodically, and remove sensitive or inaccurate entries.

## Reference(s):

- [Memory Pipeline ClawHub page](https://clawhub.ai/joe-rlo/skills/memory-pipeline)
- [Setup Guide](references/setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSONL, JSON, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workspace memory artifacts such as BRIEFING.md, memory/extracted.jsonl, memory/knowledge-graph.json, memory/knowledge-summary.md, and imported conversation markdown files.]

## Skill Version(s):

0.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
