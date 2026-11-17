## Description:

Shows Ken measured impact as a scoreboard from Ken benchmark results, with an honest empty state when no measured results exist.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rajnandan1](https://clawhub.ai/user/rajnandan1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams evaluating Ken use this skill to display measured benchmark impact as a scoreboard, or to see an explicit empty state when no Ken benchmark results are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill could be misused to imply unmeasured savings or to trigger benchmark execution that may require credentials.

Mitigation: Keep use to display-only reported Ken benchmark results or the empty state; require separate user approval before running benchmark harnesses or accessing .env credentials.

## Reference(s):

- [Ken homepage](https://github.com/rajnandan1/ken)
- [ClawHub skill page](https://clawhub.ai/rajnandan1/skills/ken-gain)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Plain text or Markdown scoreboard with ASCII bars and an empty-state message when no measured results exist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One-shot display; does not edit files, change modes, persist state, or claim unmeasured per-repository savings.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
