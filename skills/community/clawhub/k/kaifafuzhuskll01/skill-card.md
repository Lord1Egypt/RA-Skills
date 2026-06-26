## Description: <br>
Generates self-contained HTML presentation decks and can optionally export editable PPTX files using preset deck modes, fixed 1280x720 slides, keyboard navigation, and reusable layout templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomm1399](https://clawhub.ai/user/tomm1399) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to plan, draft, review, and generate structured presentation decks from a topic, mode, and chapter count. It is suited to Chinese-first business or technical presentations that need HTML preview output and optional PPTX handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill generates presentation files in the workspace and can run a local PPTX export script when requested. <br>
Mitigation: Review the planned outline and output paths before approving implementation or export. <br>
Risk: Rendered HTML loads Google Fonts, which may disclose network access patterns when opened. <br>
Mitigation: Avoid confidential decks unless the font dependency is removed, blocked, or replaced with local fonts. <br>
Risk: Presentation content may be inaccurate, incomplete, or unsuitable for the intended audience. <br>
Mitigation: Review generated slide data and final rendered output before sharing or presenting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tomm1399/kaifafuzhuskll01) <br>
- [Publisher profile](https://clawhub.ai/user/tomm1399) <br>
- [Content rules](references/content-rules.md) <br>
- [Design system](references/design-system.md) <br>
- [Base HTML template](assets/base-template.html) <br>
- [PPTX export script](scripts/export_pptx.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance plus generated HTML files, JSON slide data, and optional PPTX files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces workspace files such as master_config.json, slides_data.json, output/<slug>-presentation.html, and optional output/<slug>-presentation.pptx.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
