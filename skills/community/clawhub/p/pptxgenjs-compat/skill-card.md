## Description:

This skill helps agents generate and repair pptxgenjs-created PPTX files so they avoid common PowerPoint repair dialogs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yaodongcheng](https://clawhub.ai/user/yaodongcheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when creating PowerPoint files with pptxgenjs or repairing pptxgenjs-generated PPTX files that may trigger PowerPoint content-repair dialogs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The repair script can overwrite and corrupt the original PPTX when no separate output path is provided.

Mitigation: Always pass a separate output filename, keep a backup of the original presentation, and review the generated file before replacing the source.

Risk: The skill may be activated for generic PowerPoint tasks that are unrelated to pptxgenjs.

Mitigation: Use it only for pptxgenjs-generated PPTX files or tasks that explicitly involve pptxgenjs compatibility repair.

## Reference(s):

- [pptxgenjs compatibility pitfalls](references/pptxgenjs-pitfalls.md)
- [PptxGenJS Issue #1449: Needs Repair Errors](https://github.com/gitbrent/PptxGenJS/issues/1449)
- [PptxGenJS repair-errors documentation](https://gitbrent.github.io/PptxGenJS/docs/needs-repair-errors/)
- [ECMA-376 Office Open XML standard](https://www.ecma-international.org/publications-and-standards/standards/ecma-376/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands]

**Output Format:** [Markdown guidance with inline bash, JavaScript, and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct an agent to run the bundled Python post-processing script against a pptxgenjs-generated PPTX file.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
