## Description:

Half Full is a mindful eating companion for desk workers that helps track meals, understand nutrition patterns, and reflect on health habits without gym-focused coaching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oakcoderx](https://clawhub.ai/user/oakcoderx)

### License/Terms of Use:

MIT

## Use Case:

External users use this skill to log meals, weight, and Apple Health activity data, then receive nonjudgmental nutrition and lifestyle summaries. Agents can use it to run local Python utilities that record meals, calculate estimated nutrition, manage a profile, and summarize recent activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores sensitive health, weight, meal, and activity records, and the release includes personal-looking sample data.

Mitigation: Review records before release, remove bundled personal data, and store user records only in an explicit, protected user data location with clear opt-in and deletion controls.

Risk: The agent guide describes hidden menstrual-cycle inference from eating and weight patterns.

Mitigation: Remove hidden inference unless it is made transparent, user-requested, and easy to disable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oakcoderx/skills/half-full)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local Python scripts and JSON files to store meal, profile, weight, and activity records.]

## Skill Version(s):

0.1.4 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
