## Description: <br>
Imou Open Device Config helps agents configure Imou and Lechange device security settings, including motion detection schedules, sensitivity, privacy mode, and IoT thing-model property or service actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imou-openplatform](https://clawhub.ai/user/imou-openplatform) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect and change Imou camera channel security configuration through the Imou Open API. It supports PaaS device motion plan, sensitivity, and privacy-mode actions, plus thing-model property and service actions for IoT devices after reading the product model. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make real configuration changes to devices reachable by the supplied Imou developer credentials. <br>
Mitigation: Review each set, property-set, and service command before execution and limit the credentials to the devices and actions intended for the task. <br>
Risk: Using an incorrect IMOU_BASE_URL can send credentials and device commands to the wrong regional endpoint. <br>
Mitigation: Set IMOU_BASE_URL explicitly to the official endpoint for the account's region before running commands. <br>
Risk: IMOU_APP_SECRET is used to obtain access tokens for device control. <br>
Mitigation: Keep IMOU_APP_SECRET out of prompts, logs, and shared files, and rotate it if it may have been exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/imou-openplatform/imou-device-config) <br>
- [Imou Open API Reference - Device Config](references/imou-config-api.md) <br>
- [Imou development specification](https://open.imou.com/document/pages/c20750/) <br>
- [Imou accessToken API](https://open.imou.com/document/pages/fef620/) <br>
- [Imou enable definition](https://open.imou.com/document/pages/389c19/) <br>
- [Imou IoT thing model overview](https://open.imou.com/document/pages/1acdf4/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON output from the bundled CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires IMOU_APP_ID, IMOU_APP_SECRET, IMOU_BASE_URL, and the requests Python package.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
