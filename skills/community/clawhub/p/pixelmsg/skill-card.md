## Description: <br>
pixelmsg renders HTML templates into pixel-perfect PNG image cards with Playwright so agents can send rich visual messages instead of plain text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clarence-g](https://clawhub.ai/user/clarence-g) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use pixelmsg to turn weather, GitHub, todo, report, dashboard, and announcement content into PNG cards for chat or compatible agent runtimes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Template rendering may execute local template JavaScript and contact third-party CDNs or Open-Meteo. <br>
Mitigation: Render only trusted templates, avoid secrets or private reports in templates that load remote assets, and vendor or block remote assets when network disclosure is not acceptable. <br>
Risk: Generated images copied into a shared workspace can overwrite existing files or expose the wrong rendered card if filenames are reused. <br>
Mitigation: Use unique output filenames and review the destination path before sending the image. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clarence-g/pixelmsg) <br>
- [README.md](README.md) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Code, Guidance] <br>
**Output Format:** [PNG image files with text paths or MEDIA lines, plus HTML templates and shell or Node commands for rendering.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Screenshots are cropped to the selected element by default and can target mobile, tablet, desktop, custom dimensions, output directories, URL parameters, full-page capture, and device scale.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
