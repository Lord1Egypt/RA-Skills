## Description:

Deterministic external memory for OpenClaw and coding agents using S3-Hipokamp for storing durable facts, retrieving prior decisions, snapshotting memory, and restoring agent state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cezexpl](https://clawhub.ai/user/cezexpl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding-agent users use this skill to keep durable, namespaced memory across sessions, including key facts, prior decisions, snapshots, and restore points.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Durable memory can retain sensitive, low-signal, or raw transcript content longer than intended.

Mitigation: Store only high-signal facts and decisions, and avoid secrets, credentials, and raw transcripts.

Risk: Snapshot or restore operations can affect the wrong memory scope if configuration or namespace is incorrect.

Mitigation: Verify Hippocampus configuration and the workspace or agent namespace before snapshotting or restoring state.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cezexpl/skills/hippocampus-memory-core)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to use configured Hippocampus memory operations for durable storage, retrieval, snapshots, and restores.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
