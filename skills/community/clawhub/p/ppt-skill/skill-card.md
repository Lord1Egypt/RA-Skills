## Description: <br>
Creates polished Reveal.js HTML presentations with layouts, styling guidance, charts, speaker notes, and validation helpers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cao-yuu](https://clawhub.ai/user/cao-yuu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content creators, and presentation authors use this skill to generate browser-based Reveal.js slide decks, customize their visual design, and check charts or slide overflow before sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated decks may fetch Reveal.js, Chart.js, fonts, or other browser assets from CDNs when opened. <br>
Mitigation: Use the skill only when CDN loading is acceptable, or review generated HTML and replace external assets with approved local copies before distribution. <br>
Risk: Generated output paths can overwrite existing presentation files. <br>
Mitigation: Choose explicit output paths and review target filenames before running scaffold or validation commands. <br>
Risk: Browser-based checking steps use Puppeteer or decktape against HTML decks. <br>
Mitigation: Run those checks only on decks you created or otherwise trust. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cao-yuu/ppt-skill) <br>
- [Publisher profile](https://clawhub.ai/user/cao-yuu) <br>
- [Advanced Reveal.js Features](revealjs/references/advanced-features.md) <br>
- [Adding Charts to Reveal.js Presentations](revealjs/references/charts.md) <br>
- [Base Reveal.js Styles](revealjs/references/base-styles.css) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with HTML, CSS, JavaScript, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local presentation files and validation commands for Reveal.js decks.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
