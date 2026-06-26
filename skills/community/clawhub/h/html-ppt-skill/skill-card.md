## Description: <br>
Creates browser-based HTML slide decks with 16:9 slides, scroll-snap navigation, keyboard and wheel controls, and browser print-to-PDF export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[boboy-j](https://clawhub.ai/user/boboy-j) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content creators, and business users use this skill to generate presentation decks as standalone HTML/CSS/JavaScript instead of traditional PPTX files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated decks may load Google Fonts when opened, which can contact a third-party font service. <br>
Mitigation: Review generated HTML before sharing or presenting, and replace remote font links with approved local or bundled fonts when offline or privacy-sensitive use is required. <br>
Risk: The skill prefers HTML output for broad PPT or slide-deck requests, which may not match workflows requiring PPTX files. <br>
Mitigation: State the required output format explicitly when a PPTX file is needed. <br>
Risk: Generated slide files may be saved as local artifacts and can contain user-provided presentation content. <br>
Mitigation: Inspect generated files before distribution and avoid including confidential content unless the storage and sharing path is approved. <br>


## Reference(s): <br>
- [HTML PPT design system](references/design-system.md) <br>
- [Blank starter template](assets/blank-starter.html) <br>
- [ClawHub release page](https://clawhub.ai/boboy-j/html-ppt-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance and HTML/CSS/JavaScript code for slide deck files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated decks may include browser navigation controls and print styles for PDF export.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
