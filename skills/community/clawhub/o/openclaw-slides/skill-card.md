## Description: <br>
Create animation-rich HTML presentations from scratch or convert PowerPoint files (.ppt/.pptx) into zero-dependency web slides. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leoyeai](https://clawhub.ai/user/leoyeai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and presentation authors use this skill to create new web slide decks, convert PowerPoint files into browser-based presentations, or enhance existing HTML presentations with navigation, animations, and style presets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read presentation files and image folders provided by the user. <br>
Mitigation: Use it only in trusted OpenClaw environments and avoid sensitive decks or assets unless the environment is approved for that data. <br>
Risk: PowerPoint conversion and image processing may require installing python-pptx and Pillow from PyPI. <br>
Mitigation: Review dependency installation commands before running them and use a managed Python environment where package installation is allowed. <br>
Risk: Generated or converted slide content may preserve confidential source material in output files. <br>
Mitigation: Review generated HTML and extracted assets before sharing or publishing the deck. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leoyeai/openclaw-slides) <br>
- [Style presets reference](artifact/references/STYLE_PRESETS.md) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>
- [MyClaw skills ecosystem](https://myclaw.ai/skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTML/CSS/JavaScript code blocks and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces self-contained HTML presentation files and may create preview or processed asset files when requested.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
