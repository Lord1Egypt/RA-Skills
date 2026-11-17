## Description:

Memory Booster helps WorkBuddy agents retrieve recent local memory, save conversation snapshots, semantically search prior notes, archive older memory files, and generate domain-specific memory skill templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikeliang2000](https://clawhub.ai/user/mikeliang2000)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to reduce assistant memory loss across WorkBuddy conversations by warming up context, saving compact memory snapshots, searching historical notes, and organizing older local memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read, index, persist, mix, and report broad local WorkBuddy memory across detected workspaces.

Mitigation: Set explicit memory_dirs before use, review which memory files will be indexed, and limit the skill to workspaces where this behavior is approved.

Risk: Analytics behavior is present in the artifact metadata and may be unsuitable for sensitive memory data.

Mitigation: Disable or remove analytics before deployment unless tracking has been reviewed and approved for the target environment.

Risk: Silent startup hooks can cause memory warmup behavior without enough user control.

Mitigation: Avoid SOUL.md silent startup hooks or require explicit user invocation before reading and summarizing memory.

Risk: Archive workflows can modify and remove local memory files when execution mode is used.

Mitigation: Run archive workflows in dry-run mode first, review the planned changes, and keep backups before using archive_memory.py --exec.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mikeliang2000/skills/memory-booster)
- [Publisher homepage](https://hermesai.ltd)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands, structured reports, and generated skill/configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write or update local memory files when the user invokes save or archive workflows.]

## Skill Version(s):

6.0.3 (source: server release metadata; artifact frontmatter and meta.json list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
