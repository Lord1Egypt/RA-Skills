## Description: <br>
HTML Mender helps agents create a browser-editable copy of a local or saved HTML slide deck, then export clean source HTML with text, image, background, and layout edits applied. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuhaoyupku](https://clawhub.ai/user/wuhaoyupku) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and content creators use this skill to turn local HTML presentations or generated slide pages into editable browser files for small visual edits, then download a clean HTML result without modifying the original file by default. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated .editable.html file contains the original HTML content plus the editor runtime, creating a local editable copy of the source document. <br>
Mitigation: Use it only for local files that are acceptable to open in a browser and duplicate locally; avoid authenticated pages or sensitive documents unless that local copy is acceptable. <br>
Risk: Unsaved browser edits can be lost because local draft saving is disabled. <br>
Mitigation: Download the edited HTML before refreshing, closing, or navigating away from the editable page. <br>
Risk: Relative CSS or image assets may not resolve if generated files are moved away from the original document location. <br>
Mitigation: Keep editable and exported HTML next to the original assets, and review the downloaded HTML before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wuhaoyupku/skills/html-mender) <br>
- [HTML Mender homepage](https://github.com/wuhaoyupku/html-mender) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated HTML files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a .editable.html file next to the input unless --out is provided; requires local Node.js.] <br>

## Skill Version(s): <br>
0.1.15 (source: server release evidence and SKILL.md version notes) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
