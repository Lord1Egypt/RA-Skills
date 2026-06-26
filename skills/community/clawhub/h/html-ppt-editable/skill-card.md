## Description: <br>
Adds browser-based inline editing to HTML presentations, including text edits, color adjustment, draggable text boxes, contenteditable editing, and localStorage persistence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nicshliu](https://clawhub.ai/user/nicshliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, presentation authors, and agents use this skill to add inline editing controls to existing HTML slide decks and save edited HTML locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The editing snippet runs inside the presentation page and can modify or download the page HTML. <br>
Mitigation: Install it only into HTML presentations you intend to edit, preferably a copy, and review the snippet before using it on sensitive documents. <br>
Risk: Edited content is stored locally in the browser and may be constrained by localStorage behavior and limits. <br>
Mitigation: Save downloaded HTML copies after important edits and avoid relying on browser storage as the only record of changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nicshliu/html-ppt-editable) <br>
- [Draggable text extension](references/draggable.js) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Guidance, Configuration] <br>
**Output Format:** [Markdown with HTML, CSS, and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides zero-dependency browser snippets for local HTML presentation editing.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
