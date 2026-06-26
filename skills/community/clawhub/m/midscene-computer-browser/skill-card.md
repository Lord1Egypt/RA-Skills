## Description: <br>
Vision-driven browser automation with Midscene for browsing, data extraction, form interaction, screenshots, and UI verification from page screenshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quanru](https://clawhub.ai/user/quanru) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and agents use this skill to automate browser workflows, collect page data, capture screenshots, and validate UI behavior. It can run in isolated Puppeteer mode or connect to an existing Chrome session through CDP or Bridge when account state is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automate browser pages and, in CDP or Bridge mode, may see or act inside logged-in Chrome sessions. <br>
Mitigation: Prefer isolated Puppeteer mode for general tasks, use a dedicated browser profile for account work, close sensitive tabs before CDP or Bridge use, and require clear user intent before operating an existing browser session. <br>
Risk: The skill requires model API credentials for Midscene's visual automation. <br>
Mitigation: Use limited-scope model API keys, store them in environment variables or local configuration, and avoid exposing them in prompts, logs, screenshots, or reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/quanru/midscene-computer-browser) <br>
- [Midscene.js](https://midscenejs.com) <br>
- [Midscene model configuration](https://midscenejs.com/model-common-config) <br>
- [Midscene Bridge mode documentation](https://midscenejs.com/bridge-mode-by-chrome-extension.html) <br>
- [Midscene Chrome Extension](https://chromewebstore.google.com/detail/midscenejs/gbldofcpkknbggpkmbdaefngejllnief) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated screenshot or report file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce screenshots and Midscene report files during browser automation.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
