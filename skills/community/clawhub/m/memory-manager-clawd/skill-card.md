## Description:

Local memory management for agents. Compression detection, auto-snapshots, and semantic search. Use when agents need to detect compression risk before memory loss, save context snapshots, search historical memories, or track memory usage patterns. Never lose context again.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onlyloveher](https://clawhub.ai/user/onlyloveher)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to maintain local episodic, semantic, and procedural memory files, detect compression risk, create recovery snapshots, search prior memory, and organize flat memory notes into a structured local workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted category name or source path may cause categorize.sh to move or append files outside the intended memory directory.

Mitigation: Back up the memory directory before use, pass only trusted names and source paths, and prefer a patched version that validates filenames and confines reads and writes to the configured memory directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/onlyloveher/skills/memory-manager-clawd)
- [Moltbook agent skills community](https://www.moltbook.com/m/agentskills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text from local shell scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local memory directories, Markdown memory files, snapshot files, and a JSON state file under the configured OpenClaw workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, skill.yaml, and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
