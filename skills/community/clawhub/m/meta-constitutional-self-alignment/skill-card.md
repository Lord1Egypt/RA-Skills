## Description:

A distilled constitutional self-alignment skill that checks candidate text against machine-readable principles, applies conservative revisions, and reports an audit trail with an aligned or unaligned verdict.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to review and revise generated text against explicit constitutional rules, especially where an audit trail and escalation on unresolved violations are needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may keep local cross-session notes, including prompts, preferences, or error patterns.

Mitigation: Treat learned_patterns.json as untrusted local data and avoid recording sensitive prompts, personal data, or confidential preferences.

Risk: The documentation encourages future behavior changes and possible self-modification that conflict with the stated read-only safety boundary.

Mitigation: Require manual review for any automatic edits to SKILL.md or other skill behavior before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/meta-constitutional-self-alignment)
- [Distillation report](artifact/distillation_report.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON audit output from the alignment script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce revised text, violation counts, alignment scores, iteration traces, and an ALIGNED or UNALIGNED verdict.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
