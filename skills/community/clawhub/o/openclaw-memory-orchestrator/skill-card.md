## Description:

Production-grade memory optimization, compression, and adaptive retrieval routing for OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[che52078](https://clawhub.ai/user/che52078)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to compress, deduplicate, canonicalize, index, and route OpenClaw memory for long-running agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently rewrite local OpenClaw memory files.

Mitigation: Back up memory-records.jsonl before running dedupe, canonicalize, optimize, or gc commands.

Risk: The skill can export memory summaries and metadata to remote services when remote sync is enabled.

Mitigation: Keep remote sync and Mem0 sync disabled unless exported data and the destination HTTPS endpoint have been reviewed and approved.

Risk: The installer output includes dependency and optional Ollama fallback commands that should be reviewed before use.

Mitigation: Avoid curl-to-shell installation paths and pin chromadb in a controlled environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/che52078/skills/openclaw-memory-orchestrator)
- [Full OpenClaw Memory Orchestrator package](https://github.com/che52078/openclaw-memory-orchestrator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON or Markdown reports from included scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some scripts read from and write to the configured OpenClaw workspace.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter: 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
