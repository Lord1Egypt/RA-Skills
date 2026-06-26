## Description: <br>
Uses Playwright to automate local pages, static HTML, or online pages for screenshots, element discovery, console log capture, and UI testing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[carpedx](https://clawhub.ai/user/carpedx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA engineers use this skill to inspect and test web pages by capturing screenshots, listing visible UI elements, and collecting browser console logs. It supports direct page URLs, local HTML files, and workflows that require starting a local service before automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Screenshots and console logs may capture sensitive page content from the pages or files the user opens. <br>
Mitigation: Run the skill only against pages the user is authorized to inspect, and avoid sensitive or authenticated pages unless capture is necessary. <br>
Risk: The server helper can start local services and run user-specified commands. <br>
Mitigation: Use the helper only with trusted commands and expected local ports. <br>
Risk: Opening file URLs can expose local HTML content to automation outputs. <br>
Mitigation: Review local file paths before use and keep generated screenshots or logs in an appropriate output location. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/carpedx/playwright-web-test) <br>
- [Publisher profile: carpedx](https://clawhub.ai/user/carpedx) <br>
- [Artifact README](README.md) <br>
- [Skill definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration] <br>
**Output Format:** [Console text with MEDIA file references for screenshots and local log files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes screenshots and console logs to a local output directory, defaulting to /tmp/playwright-web-test.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
