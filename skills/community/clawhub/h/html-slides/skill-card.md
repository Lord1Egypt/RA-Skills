## Description: <br>
Create interactive, self-contained HTML slide decks with sidebar navigation, comment panel, zoom controls, inline editing, and present mode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edsml-yl10823](https://clawhub.ai/user/edsml-yl10823) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external collaborators, and developers use this skill to create or enhance browser-based presentation decks for business reviews, roadmap updates, product reviews, training, and periodic reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HTML includes executable JavaScript and may be opened in a browser. <br>
Mitigation: Review the generated HTML before opening or sharing it, and confirm before launching a browser. <br>
Risk: Sensitive slide content may reference external fonts or remote images if requested. <br>
Mitigation: Use bundled or explicitly named assets for sensitive decks, and avoid external fonts or remote images unless approved. <br>
Risk: Local comments can remain on shared machines. <br>
Mitigation: Clear local comments before sharing the deck or using the same browser profile on shared devices. <br>


## Reference(s): <br>
- [Components](references/components.md) <br>
- [Design Tokens](references/design-tokens.md) <br>
- [JavaScript Controller](references/js-controller.md) <br>
- [Slide Types](references/slide-types.md) <br>
- [Viewport Chrome](references/viewport-chrome.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Self-contained HTML file with inline CSS and JavaScript, plus brief Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated decks may include browser-local comments, inline editing controls, zoom controls, present mode, bilingual text, and brand-specific assets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
