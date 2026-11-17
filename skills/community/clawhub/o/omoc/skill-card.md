## Description:

OMOC runtime for /goal, /ralplan, /team, /ralph, memory, leases, verifiers, and non-overlapping loops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jkobject](https://clawhub.ai/user/jkobject)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use OMOC to coordinate durable planning, team execution, bounded Ralph cycles, memory compaction, and verification gates for long-running agent work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mailbox commands can be aimed outside the intended state folder to read or modify JSON files.

Mitigation: Avoid untrusted worker or mailbox names and fix path validation before using this skill in a sensitive workspace.

Risk: The runtime writes workflow state under .omoc/ in the current project.

Mitigation: Use it only in workspaces where local state writes are acceptable and review generated .omoc/ files before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jkobject/skills/omoc)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)
- [OMOC Ralph Cycle Prompt](artifact/templates/ralph-cycle.md)
- [OMOC Team Worker Prompt](artifact/templates/team-worker.md)
- [OMOC Verifier Prompt](artifact/templates/verifier.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance, shell command examples, JSON state files, and command-line JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local workflow, memory, goal, team, mailbox, Ralph, and review state under .omoc/.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
