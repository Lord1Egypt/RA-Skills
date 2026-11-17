## Description:

Provides local OpenClaw productivity utilities for cost tracking, memory retrieval, compaction status, permission checks, tool tracking, task coordination, slash commands, and token-budget monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bw520333](https://clawhub.ai/user/bw520333)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to inspect local agent activity, monitor cost and token budgets, retrieve locally stored memory context, and manage optional local utility features.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Permission checks are advisory and should not be treated as a security boundary.

Mitigation: Review tool actions before execution and rely on the host agent or operating system sandbox for enforcement.

Risk: Memory retrieval and consolidation can influence future agent context from locally stored files.

Mitigation: Review stored memory content before injecting it into an agent session, and disable or limit memory features when working with sensitive tasks.

Risk: Dream consolidation can delete processed log files when run with force-style arguments.

Mitigation: Run consolidation in dry-run mode first and back up ~/.openclaw/bw-openclaw-boost/memory before force execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bw520333/skills/openclaw-boost-tools)
- [Publisher profile](https://clawhub.ai/user/bw520333)
- [Artifact version manifest](artifact/version.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text reports and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are local operational summaries and configuration guidance; some tools read OpenClaw status or local files under ~/.openclaw/bw-openclaw-boost.]

## Skill Version(s):

1.0.0 (source: server release evidence; artifact version manifest reports current tool version 1.0.7)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
