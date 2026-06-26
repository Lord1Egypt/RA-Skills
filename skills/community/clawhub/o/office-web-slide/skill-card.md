## Description: <br>
Web Slide helps agents turn user-provided material and style preferences into browser-ready interactive HTML presentations with layouts, themes, charts, and animations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[balancegsr](https://clawhub.ai/user/balancegsr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to create browser-based slide decks from provided content, documents, or style references. It is intended for interactive HTML presentations with built-in navigation, theme selection, layouts, charts, and animation support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read presentation source materials that may contain confidential information. <br>
Mitigation: Avoid sensitive source material where possible and review what is provided to the agent before generation. <br>
Risk: Generated HTML may include or reference external CDN libraries for advanced charts or animations. <br>
Mitigation: Ask for no CDN dependencies when offline use or stricter data-handling controls are required. <br>
Risk: Generated slide content or HTML may contain mistakes before human review. <br>
Mitigation: Review the generated HTML presentation before sharing or presenting it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/balancegsr/office-web-slide) <br>
- [Publisher profile](https://clawhub.ai/user/balancegsr) <br>
- [README](artifact/README.md) <br>
- [Slide generation guidelines](artifact/references/guidelines.md) <br>
- [HTML slide base template](artifact/references/base.html) <br>
- [Theme picker](artifact/references/theme-picker.html) <br>
- [Chart.js component reference](artifact/references/components/chart-js.html) <br>
- [SVG chart component reference](artifact/references/components/chart-svg.html) <br>
- [GSAP animation recipes](artifact/references/components/gsap-recipes.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Conversational guidance plus generated HTML, CSS, and JavaScript files for browser-based slide decks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read user-provided source material, write local HTML slide files, open browser previews, run a temporary localhost theme picker, and optionally reference CDN libraries for charts or advanced animation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact README) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
