## Description:

Meta Deep Research helps an agent run structured deep-research workflows that move from outline creation to parallel evidence gathering and Markdown report synthesis, with added self-verification, reflection, adversarial checks, and local learning state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and research-focused agent users use this skill to plan research topics, collect structured findings, and synthesize traceable Markdown reports. It is suited to literature reviews, benchmark comparisons, technical evaluation, competitive analysis, and due diligence workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create research files and keep local learning history.

Mitigation: Run it in a dedicated workspace and review generated research outputs and learned_patterns.json before sharing or reusing them.

Risk: The learner helper accepts a skill directory path and updates local state.

Mitigation: Run the learner only against trusted skill directories and avoid elevated privileges.

Risk: Web-dependent research can be incomplete, stale, or affected by confirmation bias.

Mitigation: Require source review, uncertainty notes, and adversarial checks before relying on generated reports for decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/meta-deep-research)
- [Distillation report](artifact/distillation_report.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown reports, YAML research outlines and result files, and JSON learning-state records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local research files and update learned_patterns.json when the learner helper is used.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
