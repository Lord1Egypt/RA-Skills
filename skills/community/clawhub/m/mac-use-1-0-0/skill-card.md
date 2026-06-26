## Description: <br>
Control macOS GUI apps visually by taking screenshots, detecting on-screen text, clicking, scrolling, typing, and verifying results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yidahis](https://clawhub.ai/user/yidahis) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to let an agent operate visible macOS desktop applications through a screenshot, OCR, action, and verification loop. It is suited to supervised GUI workflows where the agent needs to inspect text, select controls, type content, scroll, and verify the resulting screen state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read screen contents and control the macOS GUI once Screen Recording and Accessibility permissions are granted. <br>
Mitigation: Use it only for supervised, bounded tasks and grant permissions only to a trusted host process. <br>
Risk: Sensitive workflows may expose private data or allow unintended actions through clicks, typing, keypresses, or posting flows. <br>
Mitigation: Avoid password managers, banking, admin settings, private messages, payment flows, deletion flows, and public posting unless each step is explicitly confirmed. <br>
Risk: Screenshots, element maps, and clipboard contents may persist after a session. <br>
Mitigation: Clear /tmp/mac_use*.png, /tmp/mac_use_elements.json, and the clipboard after sensitive sessions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yidahis/mac-use-1-0-0) <br>
- [Publisher profile](https://clawhub.ai/user/yidahis) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands; script commands return JSON and write annotated screenshot files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS, Python 3, Screen Recording permission, Accessibility permission, and local temporary files under /tmp.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
