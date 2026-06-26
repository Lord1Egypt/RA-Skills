## Description: <br>
Create stunning, animation-rich HTML presentations from scratch or by converting PowerPoint files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luis1213899](https://clawhub.ai/user/luis1213899) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, creators, trainers, and presenters use this skill to create browser-native HTML slide decks, convert PowerPoint files into web presentations, and enhance existing HTML presentations with distinctive visual styles and animation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional deployment helpers can publish decks and bundled assets to a public Vercel URL. <br>
Mitigation: Review the deck, asset folder, speaker notes, and images for secrets or sensitive business material before deployment; use local HTML or PDF export for sensitive decks and remove the Vercel project when the URL should no longer be public. <br>
Risk: Optional PDF export can download or install external tooling such as Playwright and Chromium when missing. <br>
Mitigation: Run export helpers in an environment where runtime package downloads are acceptable, and review command output before relying on generated artifacts. <br>


## Reference(s): <br>
- [Style Presets](references/STYLE_PRESETS.md) <br>
- [HTML Template](references/html-template.md) <br>
- [Viewport Base CSS](references/viewport-base.css) <br>
- [Animation Patterns](references/animation-patterns.md) <br>
- [ClawHub skill page](https://clawhub.ai/luis1213899/html-frontend-slides) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with inline HTML, CSS, JavaScript, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces self-contained HTML presentations and may optionally produce PDF exports or deployment commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
