## Description:

Heleni Memory Architecture guides PA agents in maintaining persistent memory through deductive memory entries, session summaries, project files, and long-term memory promotion rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netanel-abergel](https://clawhub.ai/user/netanel-abergel)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to help an agent decide what to remember, where to write it, and when to promote conversational context into long-term memory. It is intended for PA-style agents that maintain memory files and periodic self-review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent self-review jobs and instruction-file edits can change agent behavior without enough user control.

Mitigation: Review proposed cron jobs and require user approval before unattended edits to MEMORY.md, AGENTS.md, SKILL.md, or related behavior files.

Risk: Memory files can accumulate sensitive or inaccurate long-term context.

Mitigation: Follow the skill's stated exclusion rule for secrets and credentials, review memory writes, and compact or correct stale entries regularly.

Risk: The artifact proposes sourcing a local .context file in shell.

Mitigation: Use a data-only configuration format instead of shell-sourcing configuration, especially when the file may be edited by an agent.

Risk: The artifact recommends committing and pushing memory changes to Git.

Mitigation: Confirm the Git destination and inspect memory diffs before committing or pushing persistent memory files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/netanel-abergel/skills/heleni-memory-architecture)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and memory-entry templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes file-writing conventions for memory logs, project memory, long-term memory, and scheduled self-review workflows.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
