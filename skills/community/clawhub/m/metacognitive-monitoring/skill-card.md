## Description:

Metacognitive Monitoring helps agents assess confidence, uncertainty, novelty, scope fit, and task necessity during execution, then choose whether to proceed, degrade, seek help, defer, or flag overconfidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill as a reliability safeguard for long-running or higher-risk tasks, especially when an agent needs to decide whether to continue, add verification, ask for help, or defer low-value work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can keep local decision history and preferences that may influence future agent behavior.

Mitigation: Review learned_patterns.json before reuse, treat stored values as untrusted data, and require human approval before adopting saved preferences.

Risk: The skill describes automatic behavior changes and SKILL.md rewrites based on accumulated alerts.

Mitigation: Run it only in a controlled skill directory and require human review before any skill documentation or threshold changes are applied.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/metacognitive-monitoring)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [JSON decision records, plain text calibration metrics, and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local standard-library Python scripts; learning history and preferences may persist in learned_patterns.json.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
