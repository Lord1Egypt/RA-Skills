## Description:

Meta Evolver is a recursive self-evolution engine that helps an agent assess local skill capabilities, plan improvements, record iteration history, and refine skill-maintenance strategy over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent maintainers use this skill to inspect a local skill ecosystem, identify capability gaps, generate a current improvement strategy, and record or reflect on completed skill updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can scan local skill metadata and persist environment-derived state.

Mitigation: Run it only in a sandboxed or disposable skill workspace where that local metadata is appropriate to inspect and store.

Risk: The skill can modify skill files, strategy files, and state files as part of its self-evolution workflow.

Mitigation: Review proposed strategies and file diffs before accepting changes or packaging updated skills.

Risk: Helper scripts assume local skill paths and can operate broadly over matching skill directories.

Mitigation: Avoid running helper scripts on untrusted paths and constrain execution to the intended skill directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/meta-evolver)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Code, Shell commands, Guidance]

**Output Format:** [Markdown strategy text, JSON state updates, code edits, and command-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify local skill files and persistent strategy/state files when executed.]

## Skill Version(s):

1.0.14 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
