## Description: <br>
A custom browser automation skill using Playwright to visit URLs, retrieve page titles, and capture screenshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1393368499](https://clawhub.ai/user/1393368499) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to automate simple browser visits, collect page titles, and save screenshots for web task workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate browser sessions against arbitrary URLs, so it may expose page content to the agent. <br>
Mitigation: Use it only on pages you intend the agent to access, and avoid banking, admin, private intranet, or confidential pages unless that access is deliberate. <br>
Risk: Screenshot actions can capture sensitive page content into a local image file. <br>
Mitigation: Review target pages before screenshotting and handle generated screenshot files as potentially sensitive. <br>
Risk: Browser automation through a local bridge may depend on environment credentials such as ZCLAW_API_KEY. <br>
Mitigation: Protect browser automation credentials in environment variables or local config files and do not share them with untrusted agents or logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1393368499/my-browser-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, files] <br>
**Output Format:** [JSON object containing status text, page title, error details, or a screenshot file path.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Screenshot actions write an image file path; browser navigation depends on network access and target page behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
