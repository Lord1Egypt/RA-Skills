## Description: <br>
HTML PPT Studio helps agents author professional static HTML presentations using bundled themes, layouts, full-deck templates, animations, and keyboard-ready runtime assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lewislulu](https://clawhub.ai/user/lewislulu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and agents use this skill to turn outlines, notes, or presentation requests into static HTML slide decks, pitch decks, reports, technical talks, keynote-style presentations, and Xiaohongshu-style visual posts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Confidential decks may load third-party CDN resources such as fonts, Chart.js, or highlight.js. <br>
Mitigation: Bundle external libraries and fonts locally for confidential or restricted presentations. <br>
Risk: Bundled demo slides may contain placeholder commands, API-key examples, or sensitive-tool examples that are not intended for production reuse. <br>
Mitigation: Review demo content before copying it into real projects, and confirm credential handling, command scope, and backup expectations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lewislulu/html-ppt) <br>
- [README](artifact/README.md) <br>
- [Authoring guide](artifact/references/authoring-guide.md) <br>
- [Themes catalog](artifact/references/themes.md) <br>
- [Layouts catalog](artifact/references/layouts.md) <br>
- [Animations catalog](artifact/references/animations.md) <br>
- [Full-deck templates catalog](artifact/references/full-decks.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with HTML, CSS, JavaScript, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces static HTML slide-deck files and optional PNG exports through the bundled render script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
