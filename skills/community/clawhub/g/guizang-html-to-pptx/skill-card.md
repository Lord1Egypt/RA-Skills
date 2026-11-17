## Description:

Converts an existing guizang magazine-style HTML slide deck into a real editable PowerPoint PPTX with native text, shapes, images, and matched fonts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[domainrankhq](https://clawhub.ai/user/domainrankhq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and presentation authors use this skill to export existing guizang HTML decks into editable PowerPoint files while preserving slide structure, typography, images, and visual QA artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create or update files in the presentation project, including a PPTX, an exporter script, and QA render artifacts.

Mitigation: Run it in the intended deck workspace and review generated files before committing or distributing them.

Risk: In repositories containing multiple plausible slide decks, the agent may choose the wrong HTML input.

Mitigation: Provide the exact `ppt/index.html` or `index.html` path before export.

Risk: Font or layout differences can appear when the required fonts or QA tools are unavailable.

Mitigation: Install the expected fonts and inspect the generated QA render before treating the PPTX as final.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/domainrankhq/skills/guizang-html-to-pptx)
- [Original guizang PPT skill](https://github.com/op7418/guizang-ppt-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline code and shell commands; generated PPTX, exporter, and QA files when executed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces editable PPTX files and local QA artifacts; does not use slide screenshots unless explicitly requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
