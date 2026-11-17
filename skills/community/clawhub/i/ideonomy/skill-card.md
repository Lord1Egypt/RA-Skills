## Description:

Ideonomy Engine helps agents generate structured creative prompts through ideonomic lenses for brainstorming, debugging, strategy, ethics, diagnostics, and other problem-solving contexts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[morpheis](https://clawhub.ai/user/morpheis)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product teams, and agents use this skill to turn open-ended problems into structured prompts and ideonomic lenses for brainstorming, root-cause analysis, strategy, ethical reflection, and decision-making.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a globally installed, unpinned third-party npm CLI whose package contents are not included in the artifact for review.

Mitigation: Review the npm package and publisher before installing; prefer a pinned version matching the skill metadata, a project-local install, and inspection of package contents and lifecycle scripts before running it around sensitive files or credentials.

Risk: The skill produces structured prompts rather than answers, so outputs may be incomplete, irrelevant, or unsuitable for direct action without review.

Mitigation: Treat generated lenses and questions as reasoning aids; review and adapt them before using them to make decisions or modify systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/morpheis/skills/ideonomy)
- [Publisher profile](https://clawhub.ai/user/morpheis)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with CLI commands and optional structured JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reasoning output can be constrained by profile, selected divisions, lens count, concise mode, or JSON mode.]

## Skill Version(s):

0.3.4 (source: artifact/SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
