## Description:

Native Autonomous Discovery helps an agent run an open-ended hypothesis, experiment design, evidence scoring, and convergence loop over a supplied search space and observer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill to automate active exploration for open-ended questions, such as selecting a best parameter combination or narrowing possible root causes. It produces candidate hypotheses, scores them through an observer, accumulates evidence, and reports the strongest conclusion with confidence and trajectory details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local learning can retain usage history and user preferences.

Mitigation: Review the learner workflow before installation and disable or remove it unless persistent local learning is intended.

Risk: Observer Python files are loaded for scoring hypotheses.

Mitigation: Use only trusted observer files and review them before running discovery against real inputs.

Risk: Instruction write-back guidance can change skill behavior over time.

Mitigation: Review proposed instruction updates and rescan the skill before accepting changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/native-autonomous-discovery)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash examples and JSON discovery results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Discovery runs can report the best hypothesis, confidence, round count, convergence status, and evidence trajectory.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
