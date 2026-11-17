## Description:

TickTick (ticktick.com). Use this skill for ANY TickTick request — reading, creating, updating, and deleting data. Whenever a task involves TickTick, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using TickTick can ask an agent to read and organize their tasks, projects, and habits through their connected account. The skill also supports creating, updating, completing, moving, and deleting TickTick items, with confirmation safeguards for changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute unverified software whose documented effects extend to other installed agent skills.

Mitigation: Review and approve the CLI installation separately; consult the publisher's command reference for OO_SKILLS_SYNC_DISABLED=1 if you want to prevent broader skill changes.

Risk: TickTick task data passes through OOMOL, and writes or deletions can change account data.

Mitigation: Account for OOMOL in the data path, confirm the exact payload for writes, and require explicit approval for destructive actions.

## Reference(s):

- [TickTick](https://ticktick.com)
- [TickTick API documentation](https://developer.ticktick.com/docs/index.html)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI command and environment variable reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [OOMOL TickTick connection](https://console.oomol.com/connections/ticktick)
- [ClawHub TickTick release](https://clawhub.ai/oomol/skills/oo-ticktick)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [oo CLI commands with JSON input and structured JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the live action schema for payloads; state-changing actions require user confirmation and destructive actions require explicit approval.]

## Skill Version(s):

1.0.6 (source: evidence release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
