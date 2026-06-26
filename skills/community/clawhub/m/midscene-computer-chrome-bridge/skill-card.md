## Description: <br>
Vision-driven browser automation using Midscene Bridge mode that operates from screenshots and can interact with visible browser elements without DOM or accessibility labels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quanru](https://clawhub.ai/user/quanru) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, testers, and automation users use this skill to control a prepared desktop Chrome browser through Midscene Bridge for browsing, logged-in workflows, form interaction, data extraction, UI checks, and screenshot-based validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can operate a real logged-in Chrome session and may access private or sensitive pages. <br>
Mitigation: Use a separate Chrome profile or VM, avoid banking, healthcare, admin consoles, private messages, and MFA pages, and require explicit approval before logged-in actions or data extraction. <br>
Risk: The workflow depends on the Midscene Chrome Extension, npm package, and configured model credentials. <br>
Mitigation: Verify the extension and npm package source before use, configure only the required model credentials, and avoid sharing credentials in prompts or task output. <br>
Risk: Screenshot-driven browser actions can click, type, scroll, or navigate in unintended ways if instructions are ambiguous. <br>
Mitigation: Review screenshots and command results between actions, scope tasks to intended sites, and ask for confirmation before destructive or sensitive operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/quanru/midscene-computer-chrome-bridge) <br>
- [Midscene.js](https://midscenejs.com) <br>
- [Midscene model configuration](https://midscenejs.com/model-common-config) <br>
- [Midscene Bridge mode documentation](https://midscenejs.com/bridge-mode-by-chrome-extension.html) <br>
- [Midscene Chrome Extension](https://chromewebstore.google.com/detail/midscenejs/gbldofcpkknbggpkmbdaefngejllnief) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown with inline shell commands, configuration examples, screenshots, and result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a prepared Chrome browser, Midscene Chrome Extension, and configured visual model credentials.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
