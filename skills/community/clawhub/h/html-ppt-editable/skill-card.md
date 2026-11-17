## Description:

Adds in-browser inline editing controls to HTML slide decks, including editable text, save/export controls, and an optional draggable text-box extension.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicshliu](https://clawhub.ai/user/nicshliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and presentation authors use this skill to add browser-side editing controls to generated or existing HTML slide decks so text can be adjusted in-browser and exported as HTML.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exported HTML can carry unsafe or misleading rich content if untrusted material is pasted into editable regions.

Mitigation: Avoid pasting untrusted rich content, review exported HTML before sharing, and treat the output as executable HTML.

Risk: The documentation overstates localStorage autosave and built-in dragging behavior for this release.

Mitigation: Do not rely on autosave or dragging unless those features are implemented and tested separately in the target presentation.

## Reference(s):

- [draggable.js](references/draggable.js)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown with HTML, CSS, and JavaScript code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
