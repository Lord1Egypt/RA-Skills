## Description:

Recovers broken agent state via crash recovery, context overflow, and merge conflict protocols

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use these procedures to recover work after an agent crash, context loss, merge conflict, or inconsistent task, Git, and disk state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recovery steps can alter Git state while work ownership or intent is unclear.

Mitigation: Inspect Git status, diffs, and stashes first; limit changes to work you intend to commit or stash, and escalate when ownership or intent is uncertain.

Risk: A referenced recovery file was only partly inspected by the security scan.

Mitigation: Review the relevant recovery instructions before applying them, especially before aborting a merge or changing staged or unstaged work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-leyline-damage-control)
- [Related Leyline plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/leyline)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with procedural checklists, decision trees, and inline shell or YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Organized into recovery modules for distinct failure classes]

## Skill Version(s):

1.10.4 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
