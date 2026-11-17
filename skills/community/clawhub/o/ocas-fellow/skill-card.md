## Description:

Fellow is an empirical experimentation engine invoked by Mentor to evaluate, compare, and promote improvements to OCAS skills, prompts, heuristics, and workflows using benchmark-driven experiments, returning the best variant with lineage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[indigokarasu](https://clawhub.ai/user/indigokarasu)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use Fellow through Mentor to run controlled benchmark experiments for skill, prompt, heuristic, and workflow improvements. It compares baselines and variants, records experiment evidence, and returns promotion decisions with lineage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags a silent daily self-update that can overwrite skill files from GitHub.

Mitigation: Install only with operator-approved, pinned, and verified updates, or remove the self-update path before deployment.

Risk: The security guidance notes persistent experiment records and daily background update behavior.

Mitigation: Review storage locations, retention needs, and scheduled jobs before installation, especially in shared or production agent environments.

Risk: Experiment outputs can influence skill promotion decisions, and artifact guidance notes that flawed experiment programs can optimize the wrong target.

Mitigation: Require Mentor-side review of experiment requests, benchmarks, guardrails, and promotion thresholds before applying recommendations.

## Reference(s):

- [Fellow Schemas](references/schemas.md)
- [Journal](references/journal.md)
- [Fellow Gotchas](references/gotchas.md)
- [Interactive Menu](references/interactive-menu.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Configuration, Guidance]

**Output Format:** [Markdown instructions with JSON schemas, JSON cycle results, JSON journal records, and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes experiment evidence, results, journals, and update status for Mentor-driven experiment cycles.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact metadata reports 2.7.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
