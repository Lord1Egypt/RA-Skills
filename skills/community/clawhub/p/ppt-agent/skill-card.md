## Description: <br>
Ppt Agent guides an agent through a style-confirmation, outline, planning, and SVG design workflow to create editable Bento Grid slide pages for PowerPoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianchangNorth](https://clawhub.ai/user/tianchangNorth) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and presentation creators use this skill to turn a topic and audience context into a PPT outline, page-by-page planning notes, and editable SVG slide artwork. It is suited for reports, proposals, courses, and executive presentations that need structured content before visual design. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated slide content can contain incorrect or misleading facts. <br>
Mitigation: Review and fact-check generated outlines, planning notes, and slide text before using them in a presentation. <br>
Risk: The optional Python SVG script can create or overwrite page_XX.svg files in the selected output directory. <br>
Mitigation: Run the script only with trusted inputs and an output directory where creating or overwriting those files is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tianchangNorth/ppt-agent) <br>
- [Publisher profile](https://clawhub.ai/user/tianchangNorth) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Outline prompt](artifact/prompts/outline.md) <br>
- [Planning prompt](artifact/prompts/planning.md) <br>
- [SVG design prompt](artifact/prompts/design.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [JSON outline, markdown planning notes, and SVG code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Final SVG pages use a 1280 by 720 viewBox and are intended to be editable after import into PowerPoint 2016 or later.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
