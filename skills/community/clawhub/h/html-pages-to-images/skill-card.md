## Description: <br>
Converts multiple HTML page elements into separate high-resolution image files with configurable selector, viewport size, and output directory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shiker1996](https://clawhub.ai/user/shiker1996) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to render selected elements from trusted local HTML into PNG screenshots for content workflows and batch page export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill renders active HTML in Chromium, which may load scripts, styles, fonts, or remote resources from supplied HTML. <br>
Mitigation: Use trusted HTML only or run the skill in an isolated environment; consider blocking external requests before deployment. <br>
Risk: The bundled legacy conversion script deletes a hard-coded output directory without confirmation. <br>
Mitigation: Prefer the main index.js API with a dedicated output directory and avoid running the legacy convert-pages.js directly unless its paths have been reviewed. <br>
Risk: Chromium is launched with no-sandbox flags. <br>
Mitigation: Avoid no-sandbox mode where possible and contain execution with OS-level isolation when processing untrusted inputs. <br>
Risk: Image filenames may be derived from HTML page content. <br>
Mitigation: Sanitize page-derived filename components before using the skill with untrusted or user-supplied HTML. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shiker1996/html-pages-to-images) <br>
- [Publisher profile](https://clawhub.ai/user/shiker1996) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON] <br>
**Output Format:** [PNG image files plus a JSON-style execution result] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates one PNG per matched HTML element and returns image paths, count, and output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
