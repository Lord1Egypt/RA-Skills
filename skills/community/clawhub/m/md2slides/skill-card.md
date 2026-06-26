## Description: <br>
Converts Markdown presentation or report documents into editable PPTX slide decks for PowerPoint, Keynote, or WPS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sopaco](https://clawhub.ai/user/sopaco) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to turn structured Markdown talks or reports into editable slide decks while preserving source content for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Confidential presentation text or speaker notes may be included in intermediate schema files. <br>
Mitigation: Use a dedicated working folder for confidential presentations and delete temporary schema JSON after generating the PPTX. <br>
Risk: An unintended output path could place the generated deck somewhere unexpected. <br>
Mitigation: Choose an explicit output path before running the local PPTX generation command. <br>


## Reference(s): <br>
- [Presentation Schema](references/presentation-schema.md) <br>
- [Analysis Prompt](references/analysis-prompt.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/sopaco/md2slides) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, JSON, Shell commands, Files] <br>
**Output Format:** [Markdown guidance, PresentationSchema JSON, and a PPTX file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates a local .pptx from an intermediate PresentationSchema JSON; users choose the Markdown input and output path.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
