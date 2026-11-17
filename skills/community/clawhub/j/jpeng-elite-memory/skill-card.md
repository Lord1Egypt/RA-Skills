## Description:

Elite Longterm Memory helps AI agents preserve context across sessions with write-ahead logging, vector recall, git-notes, local memory files, and optional cloud memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to set up persistent memory workflows that keep active task state, durable decisions, semantic recall, daily logs, and optional cloud-backed memories across coding sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory may store conversation details, secrets, or private project data longer than intended.

Mitigation: Review what gets stored, avoid saving secrets or private project data, and treat durable memory as an intentional opt-in workflow.

Risk: Optional cloud memory integrations can sync sensitive context outside the local workspace.

Mitigation: Use Mem0 and SuperMemory only when cloud storage is approved, and review data handling before enabling API keys.

Risk: Unpinned package execution can run a newer package version than the reviewed artifact.

Mitigation: Pin package versions for installation and deployment, and inspect package contents before running setup commands.

Risk: Memory deletion, export, and sync workflows can remove or propagate stored context.

Mitigation: Back up memory stores and inspect targets before deleting, exporting, or syncing memory data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/skills/jpeng-elite-memory)
- [Publisher profile](https://clawhub.ai/user/jpengcheng523-netizen)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)
- [memory-lancedb plugin](https://clawdhub.com/skills/lancedb-memory)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate local memory files and configuration guidance when its CLI is used.]

## Skill Version(s):

1.2.3 (source: server release, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
