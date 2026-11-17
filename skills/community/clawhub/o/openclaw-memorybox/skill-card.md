## Description:

MemoryBox is a zero-dependency memory maintenance CLI for OpenClaw that keeps MEMORY.md lean with 3-tier hierarchical organization and can work alongside Mem0, Supermemory, QMD, or standalone.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ramsbaby](https://clawhub.ai/user/ramsbaby)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use MemoryBox to inspect, organize, archive, and reduce bloat in MEMORY.md-based agent memory directories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented install flow clones code from GitHub and symlinks it into /usr/local/bin with sudo, making the command system-wide.

Mitigation: Review the repository first, install from a pinned commit or signed release, and prefer a user-local path such as ~/.local/bin.

Risk: The CLI is intended to read and modify agent memory directories.

Mitigation: Run it only against memory directories you are comfortable letting the tool inspect and change, and keep backups for important MEMORY.md content.

## Reference(s):

- [MemoryBox ClawHub release](https://clawhub.ai/ramsbaby/skills/openclaw-memorybox)
- [MemoryBox GitHub repository](https://github.com/Ramsbaby/openclaw-memorybox)
- [OpenClaw Self-Healing companion repository](https://github.com/Ramsbaby/openclaw-self-healing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides use of a local CLI that can report diagnostics, health scores, duplicate content, stale content, archive actions, and memory-structure recommendations.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
