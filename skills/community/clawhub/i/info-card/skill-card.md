## Description: <br>
Info Card helps an agent generate 900x1200 PNG social-media information cards, knowledge cards, and posters from local HTML/CSS templates using Python and Playwright. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rivercrab26](https://clawhub.ai/user/rivercrab26) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to turn structured JSON card data into polished vertical PNG assets for social posts, explainers, checklists, comparisons, reports, and other visual knowledge-card formats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generator may require installing Playwright and Chromium and then running a local headless browser. <br>
Mitigation: Install browser dependencies in a controlled environment and review generated files before sharing or deploying them. <br>
Risk: Card data can include remote image or avatar URLs and rendered pages may fetch remote fonts or image resources. <br>
Mitigation: Use trusted URLs or local assets when rendering sensitive content, and avoid untrusted external resources in restricted environments. <br>
Risk: Untrusted JSON input can influence rendered HTML content and output files. <br>
Mitigation: Treat incoming card data as untrusted, inspect it before rendering, and avoid running the generator on unknown payloads without isolation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/rivercrab26/info-card) <br>
- [Info-Card design specifications](artifact/references/design-specs.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration] <br>
**Output Format:** [PNG image files and optional HTML, with command output showing the generated file path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default output is a 900x1200 3:4 PNG written to /tmp or a user-selected output path.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
