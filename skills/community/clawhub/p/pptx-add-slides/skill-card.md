## Description:

Adds new slides to an existing PPTX while preserving the source deck's layout, background, fonts, colors, and other styling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuobadaidai](https://clawhub.ai/user/tuobadaidai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and file-oriented agents use this skill to add content or section slides to an existing PowerPoint deck while keeping the deck's visual style consistent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Processing untrusted or unusually large PPTX files may expose the local script to malformed input or excessive resource use.

Mitigation: Run the skill in a virtual environment, process only trusted PPTX files when possible, and apply resource limits for large or untrusted decks.

Risk: A template slide whose text regions do not match the requested content can cause truncation, blank regions, or awkward slide output.

Mitigation: Choose a representative template slide with enough text regions and inspect the generated PPTX before sharing or publishing it.

Risk: Writing a generated deck can overwrite or replace expected output if paths are chosen carelessly.

Mitigation: Use a distinct output path and keep the original source PPTX unchanged until the generated deck has been reviewed.

## Reference(s):

- [PPTX Add Slides ClawHub Skill Page](https://clawhub.ai/tuobadaidai/skills/pptx-add-slides)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands and JSON page configuration; the script produces a PPTX file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an existing PPTX, a template page number, an insertion position, and page content supplied as JSON.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
