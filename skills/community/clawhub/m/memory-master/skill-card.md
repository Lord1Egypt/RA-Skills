## Description:

Local memory system with structured indexing, auto-write, heuristic recall, and auto-learning when local knowledge is insufficient.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lizhelong0907](https://clawhub.ai/user/lizhelong0907)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to add local persistent memory, structured indexes, recall guidance, and knowledge capture to an agent workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently change workspace-level agent instructions and memory files.

Mitigation: Review backups and file diffs before and after initialization, and run it only in workspaces where persistent instruction changes are acceptable.

Risk: Automatic memory storage can capture sensitive conversation details in local files.

Mitigation: Avoid use in sensitive workspaces unless explicit approval gates and redaction rules are added for memory writes.

Risk: Heartbeat and auto-learning behavior can introduce recurring checks or web searches beyond a user's immediate request.

Mitigation: Disable or edit the heartbeat template and require confirmation before network learning or repository actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lizhelong0907/skills/memory-master)
- [ClawHub publisher profile](https://clawhub.ai/user/lizhelong0907)
- [README](README.md)
- [Skill definition](SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and local workspace file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces persistent workspace files and rules for local memory, recall, heartbeat, and knowledge indexing.]

## Skill Version(s):

2.6.5 (source: server release metadata and package.json; SKILL.md frontmatter states 2.6.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
