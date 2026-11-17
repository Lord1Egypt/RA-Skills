## Description:

A Chinese-language novel writing studio skill that routes user requests across research, drafting, style adaptation, QA, and long-form project management workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guzhoutingyu](https://clawhub.ai/user/guzhoutingyu)

### License/Terms of Use:

MIT-0

## Use Case:

External writers and creative teams use this skill to plan, draft, revise, style-match, and quality-check Chinese fiction projects from short stories through long-form serials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist project data, reports, style documents, and memory files.

Mitigation: Install it in an isolated writing workspace with limited file permissions, and review file writes before approval.

Risk: Project, style, or report names may influence file paths.

Mitigation: Sanitize project, style, and report names before allowing the agent to create or update files.

Risk: The workflow can load or depend on external skills.

Mitigation: Pin or verify external skills before use.

Risk: The skill includes self-evolution behavior that can update its writing guidance.

Mitigation: Disable self-evolution or manually review any instruction changes before keeping them.

Risk: Untrusted writing samples may steer future style behavior.

Mitigation: Avoid untrusted samples or review sample content before using it for style learning.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guzhoutingyu/skills/guzhou-novel-studio)
- [Workflow guide](references/workflow-guide.md)
- [File format specification](references/file-format-spec.md)
- [Research output templates](modules/researcher/references/output-templates.md)
- [QA check dimensions](modules/qa/references/check-dimensions.md)
- [Style dimensions](modules/stylist/references/style-dimensions.md)
- [Writing style reference](modules/studio/references/writing-style.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, configuration, guidance]

**Output Format:** [Chinese prose, Markdown chapters and QA reports, JSON planning/style/project files, and project configuration templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist project files, reports, style documents, and memory files during writing workflows.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
