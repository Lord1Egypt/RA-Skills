## Description:

Audits Claude Code skill files for structure, content quality, cross-platform and cross-agent compatibility, prerequisite declarations, and trigger-description accuracy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[niracler](https://clawhub.ai/user/niracler)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to review Claude Code skills before distribution by running structural validation, invoking skill-creator for content quality, and checking compatibility and prerequisite coverage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local shell and Python validation runs against skill files.

Mitigation: Inspect the bundled scripts and run them in a controlled workspace before acting on the review output.

Risk: Review findings may influence skill behavior, distribution readiness, or release decisions.

Mitigation: Treat findings as guidance and confirm changes with the target skill owner before release.

Risk: The workflow expects skill-creator for deeper content review.

Mitigation: Mark content review incomplete or stop for dependency setup when skill-creator is unavailable.

## Reference(s):

- [Compatibility Checklist](artifact/references/compatibility-checklist.md)
- [ClawHub Skill Page](https://clawhub.ai/niracler/skills/nini-skill-reviewer)
- [Release v0.3.0 Changelog](https://github.com/niracler/skill/releases/tag/v0.3.0)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown review report with shell command snippets and validation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are review findings and suggested remediation steps; users should review results before changing or releasing a skill.]

## Skill Version(s):

0.3.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
