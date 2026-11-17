## Description:

Memory Stack Core provides a WAL, Working Buffer, and three-layer memory integration for OpenClaw agents so critical state can survive context compaction and session restarts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neroagent](https://clawhub.ai/user/neroagent)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to persist critical conversation state across context compaction and session restarts with WAL entries, a working buffer, and memory health checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad local persistence may store prompts, paths, URLs, decisions, assistant outputs, and other sensitive conversation details on disk.

Mitigation: Use the skill only in workspaces where those details are acceptable to retain, and add opt-in capture, redaction, review, and deletion controls before using it with secrets or sensitive client data.

Risk: Persisted conversation content can carry stale or adversarial instructions into later sessions.

Mitigation: Review WAL and working-buffer entries before relying on them for recovery, and treat restored content as context to verify rather than instructions to follow automatically.

## Reference(s):

- [Memory Stack Core on ClawHub](https://clawhub.ai/neroagent/skills/memory-stack-core)
- [neroagent Publisher Profile](https://clawhub.ai/user/neroagent)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [JSON tool responses, JSONL memory entries, and Markdown working-buffer content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local memory files in the current workspace; capture limits can be configured.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
