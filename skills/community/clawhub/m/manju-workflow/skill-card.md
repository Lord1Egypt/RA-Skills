## Description:

漫剧全流程串联引擎 orchestrates manga-video creation from creative direction through storyboard validation, art prompts, animation prompts, editing guidance, and external tool instructions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samwang-001](https://clawhub.ai/user/samwang-001)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and production teams use this skill to generate a complete manga-video production package from a user concept. It coordinates planning, storyboard generation, quality checks, art and animation prompts, editing directions, and external tool execution guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow loads companion manju-* skills as authoritative sources and follows their future edits.

Mitigation: Review and trust all companion manju-* skill files before installation and re-review them after updates.

Risk: The workflow automatically advances through multiple stages without routine user confirmation.

Mitigation: Use it only when an automatic end-to-end manga-video workflow is desired, and review the generated production package before using external tools.

## Reference(s):

- [Source skill definition](artifact/SKILL.md)
- [Server-resolved GitHub provenance](https://github.com/samwang-001/manju-skills/tree/main/manju-workflow)
- [ClawHub skill page](https://clawhub.ai/samwang-001/skills/manju-workflow)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown production package with tables, prompts, checklists, and external tool instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Depends on five companion manju-* skills and external image, video, and editing tools for final media generation.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
