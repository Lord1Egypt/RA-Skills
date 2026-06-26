## Description: <br>
Generate single-page HTML posters with multiple visual styles and support for Chinese, English, and bilingual content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ToBeWin](https://clawhub.ai/user/ToBeWin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, designers, marketers, and developers use the skill to generate ready-to-open HTML posters, flyers, promotional images, and social media visuals in Chinese, English, or bilingual formats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated poster files may load Google Fonts and html2canvas from third-party CDNs when opened in a browser. <br>
Mitigation: For privacy-sensitive or offline use, request a no-CDN version before opening or sharing the generated file. <br>
Risk: The agent creates a local HTML poster file that includes user-provided content. <br>
Mitigation: Confirm the filename, save location, and included content before generation or distribution. <br>
Risk: CSS background gradients on the main poster container may not export reliably. <br>
Mitigation: Use a solid main poster background and reserve gradients for text, buttons, borders, or decorative elements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ToBeWin/post-creator) <br>
- [Publisher profile](https://clawhub.ai/user/ToBeWin) <br>
- [Poster Style Reference Guide](references/styles.md) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [html2canvas CDN library](https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Guidance] <br>
**Output Format:** [HTML file content, typically delivered in Markdown code fences with inline CSS and browser export JavaScript] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Self-contained single-page poster output may load Google Fonts and html2canvas from third-party CDNs when opened.] <br>

## Skill Version(s): <br>
1.6.3 (source: server release, SKILL.md frontmatter, skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
