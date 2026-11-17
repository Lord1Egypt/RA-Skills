## Description:

Create stunning, animation-rich HTML presentations from scratch or convert PowerPoint files (.ppt/.pptx) to beautiful web slides.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leoyeai](https://clawhub.ai/user/leoyeai)

### License/Terms of Use:

MIT

## Use Case:

Developers, creators, educators, and business users use this skill to create new browser-based slide decks, convert PowerPoint files into web presentations, or enhance existing HTML presentations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may read presentation files, image folders, and extracted PowerPoint notes that contain confidential content.

Mitigation: Use the skill only with files intended for agent access, and review extracted assets and notes before sharing or publishing generated decks.

Risk: Optional inline editing can store deck edits in browser localStorage on the browser used for editing.

Mitigation: Avoid inline editing on shared browsers for confidential decks, or clear localStorage after editing.

Risk: PPT conversion and image processing may require installing Python packages such as python-pptx or Pillow.

Mitigation: Install dependencies in a sandboxed or pinned Python environment before processing sensitive files.

## Reference(s):

- [Style Presets Reference](references/STYLE_PRESETS.md)
- [ClawHub Skill Page](https://clawhub.ai/leoyeai/skills/myclaw-frontend-slides)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTML, CSS, JavaScript, Python, and shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces zero-dependency single-file HTML presentations and may create local preview, asset, or processed image files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
