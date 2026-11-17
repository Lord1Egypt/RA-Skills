## Description:

Novel Craft is a Chinese-language long-form fiction workflow for planning serialized novels, tracking settings, foreshadowing, timelines, continuity, and ripple effects from outline or setting changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gongsunyanming](https://clawhub.ai/user/gongsunyanming)

### License/Terms of Use:

MIT-0

## Use Case:

Authors and writing agents use this skill to create, continue, revise, and check long serialized novels while preserving continuity across outlines, settings, foreshadowing, timelines, and chapter drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create and update many project files, including chapter drafts, outlines, timelines, settings, summaries, and ripple logs.

Mitigation: Use version control or backups before running the skill and review file diffs after major operations.

Risk: Ripple operations may automatically rewrite affected chapter text after setting, outline, timeline, or foreshadowing changes.

Mitigation: Prefer manual approval for ripple rewrites, especially for depth 3 changes or broad continuity edits.

Risk: The skill may perform web research after genre or style selection.

Mitigation: Disable or manually approve web research where external browsing is not desired.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gongsunyanming/skills/novel-craft)
- [project-schema.yaml](artifact/references/project-schema.yaml)
- [outline-template.yaml](artifact/references/outline-template.yaml)
- [setting-schema.yaml](artifact/references/setting-schema.yaml)
- [foreshadow-schema.yaml](artifact/references/foreshadow-schema.yaml)
- [timeline-schema.yaml](artifact/references/timeline-schema.yaml)
- [ripple-report-template.yaml](artifact/references/ripple-report-template.yaml)
- [style-guide.md](artifact/references/style-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Chinese-language prose, Markdown drafts, YAML project files, continuity reports, and revision guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update project files for outlines, settings, foreshadowing registries, timelines, chapters, summaries, and ripple logs.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
