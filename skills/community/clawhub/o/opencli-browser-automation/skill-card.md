## Description: <br>
opencli浏览器自动化 helps agents use opencli with a Chrome/Chromium browser bridge to automate browser actions, collect web data, operate AI chat sites, and run site-specific commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wxdwqy](https://clawhub.ai/user/wxdwqy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to automate browser workflows through opencli, including page navigation, element interaction, screenshots, JavaScript evaluation, web data extraction, and repeated interactions with sites that may already be logged in. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can grant broad automation control over logged-in browser sessions. <br>
Mitigation: Use a dedicated low-privilege browser profile, avoid sensitive accounts, and disable the extension or daemon when automation is finished. <br>
Risk: The skill includes workflows that execute JavaScript or generated opencli commands in the browser. <br>
Mitigation: Review every eval or generated command before running it, especially on authenticated sites or pages containing private data. <br>
Risk: The release evidence reports insufficient install-source assurance for the separate opencli extension. <br>
Mitigation: Install only when the opencli extension source is trusted and matches the intended release. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wxdwqy/opencli-browser-automation) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline shell and JavaScript command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes browser setup guidance, command sequences, troubleshooting notes, and cautions for logged-in browser automation.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
