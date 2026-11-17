## Description:

Create, edit, and analyze .pptx presentation files, including slide content, layouts, comments, speaker notes, and theme details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyingduo](https://clawhub.ai/user/liuyingduo)

### License/Terms of Use:

Proprietary

## Use Case:

Developers, analysts, and presentation authors use this skill to read, create, modify, and quality-check PowerPoint decks from templates or from scratch.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The LibreOffice workflow uses an LD_PRELOAD shim, which can affect native-code execution behavior.

Mitigation: Run the skill in an isolated environment and review the LibreOffice helper before processing sensitive documents.

Risk: The skill documents unpinned or global dependency installation commands.

Mitigation: Install dependencies through an approved environment with reviewed versions instead of giving the skill broad package-management access.

Risk: Bundled Office tooling includes DOCX/XLSX and redline handling beyond a narrow PPTX-only workflow.

Mitigation: Limit input access to the presentation files needed for the task and review broader Office-document behavior before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liuyingduo/skills/pptx-2)
- [Editing Presentations](artifact/editing.md)
- [PptxGenJS Tutorial](artifact/pptxgenjs.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, and generated or modified Office presentation files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or modify .pptx files, extracted Office XML, thumbnails, PDFs, or validation reports depending on the workflow.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
