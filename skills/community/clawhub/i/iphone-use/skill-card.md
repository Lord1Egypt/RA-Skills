## Description: <br>
Use when a task needs a real iPhone, including operating iOS apps that have no API, exporting on-phone data, tapping, typing, scrolling, or taking screenshots through the iphone-use daemon's HTTP agent API over macOS iPhone Mirroring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leeguooooo](https://clawhub.ai/user/leeguooooo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to drive a physical iPhone for user-directed workflows in apps without APIs, including data export, screenshots, and repeatable UI automation through the iphone-use daemon. It is suited to tasks where the agent must inspect the phone state, take one action at a time, and verify the result before continuing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad operational control over a real iPhone that may already be logged into sensitive apps. <br>
Mitigation: Install and use it only for explicit, user-directed tasks, and avoid unattended banking, payment, two-factor authentication, messaging, account-change, or medical-data workflows. <br>
Risk: Phone screenshots, logs, scripts, and exported files can preserve sensitive session data after the task ends. <br>
Mitigation: Review or disable durable logs and screenshots for sensitive sessions, and delete exported phone data when the task is complete. <br>
Risk: Actions can land in the wrong app or field if the phone state changes or a human is actively using the Mac or phone. <br>
Mitigation: Probe status before acting, verify the foreground app or UI elements before text entry, back off when human activity is detected, and take one verified action at a time. <br>


## Reference(s): <br>
- [Server-resolved source import](https://github.com/leeguooooo/iphone-use/tree/main/skills/iphone-use) <br>
- [ClawHub skill page](https://clawhub.ai/leeguooooo/skills/iphone-use) <br>
- [Publisher profile](https://clawhub.ai/user/leeguooooo) <br>
- [iphone-use repository](https://github.com/leeguooooo/iphone-use) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, code, configuration] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide an agent to create replay scripts and handle screenshots or exported phone data during user-directed workflows.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
