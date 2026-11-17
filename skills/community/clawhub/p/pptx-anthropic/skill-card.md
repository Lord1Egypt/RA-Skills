## Description:

Helps agents read, create, edit, validate, and visually review PowerPoint .pptx presentations using presentation-focused workflows and Office helper scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pupuking723](https://clawhub.ai/user/pupuking723)

### License/Terms of Use:

Proprietary Anthropic terms

## Use Case:

Developers and agents use this skill when a task involves PowerPoint presentations, including extracting content, adapting templates, creating decks from scratch, modifying slide XML, and checking output quality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rendering or conversion may invoke LibreOffice with a native LD_PRELOAD shim.

Mitigation: Install and run the skill only in an isolated, unprivileged environment, especially when handling untrusted presentations.

Risk: Broad Office-document helpers can modify files beyond a narrow presentation-only workflow.

Mitigation: Work on copies of presentations and avoid bundled DOCX/XLSX helpers unless that broader Office-document behavior is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pupuking723/skills/pptx-anthropic)
- [Editing Presentations](artifact/editing.md)
- [PptxGenJS Tutorial](artifact/pptxgenjs.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or modify .pptx files through external Office tooling when the agent follows the skill workflows.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
