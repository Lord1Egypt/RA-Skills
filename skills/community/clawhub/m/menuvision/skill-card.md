## Description: <br>
Build beautiful HTML photo menus from restaurant URLs, PDFs, or photos using Gemini Vision and AI image generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ademczuk](https://clawhub.ai/user/ademczuk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Restaurant owners, designers, and automation users can use MenuVision to turn restaurant URLs, PDFs, or photos into structured menu data, generated food images, and a responsive HTML menu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Menu content, screenshots, PDFs, photos, and generated prompts may be sent to Google Gemini for extraction and image generation. <br>
Mitigation: Use appropriate menu inputs, prefer a dedicated Google API key, and review generated menu data and images before relying on the output. <br>
Risk: Optional GitHub Pages publishing can push generated HTML and image files using a GitHub personal access token. <br>
Mitigation: Set GITHUB_PAT only when intentionally publishing to a repository you control, scope the token narrowly, and review generated files before publishing. <br>


## Reference(s): <br>
- [ClawHub MenuVision listing](https://clawhub.ai/ademczuk/menuvision) <br>
- [Project homepage](https://github.com/ademczuk/MenuVision) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with generated Python scripts, JSON menu data, image files, and self-contained or deployable HTML output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GOOGLE_API_KEY for Gemini processing; optional GitHub publishing uses GITHUB_PAT only when the user chooses to publish generated menu files.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
