## Description:

Habit Tracker Pro helps users build and manage personal habits with check-ins, statistics, achievements, data analysis, and social sharing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaising-openclaw1](https://clawhub.ai/user/kaising-openclaw1)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to add personal habits, record check-ins, view statistics, track achievements, and review habit progress through ClawHub CLI guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation command uses a mutable npm latest tag.

Mitigation: Prefer a pinned clawhub installer version when installing or reproducing this release.

Risk: The metadata declares a curl binary requirement that is not explained by the artifact behavior.

Mitigation: Review the runtime environment and confirm whether curl is actually required before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaising-openclaw1/skills/habit-tracker-pro)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language habit-tracking guidance; no generated files declared.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
