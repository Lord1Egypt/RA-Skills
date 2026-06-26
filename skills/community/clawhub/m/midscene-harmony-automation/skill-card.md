## Description: <br>
Vision-driven HarmonyOS NEXT device automation using Midscene that controls connected devices from screenshots via HDC for taps, swipes, text input, app launches, assertions, shell commands, screenshots, and report conversion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quanru](https://clawhub.ai/user/quanru) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA engineers use this skill to automate and validate HarmonyOS NEXT apps or device workflows from screenshots, including launching apps, interacting with visible UI, asserting screen states, and summarizing reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad connected-device control, including raw HDC shell commands and UI actions that can make irreversible device or account changes. <br>
Mitigation: Install only for trusted test devices and test accounts, and require explicit approval before raw HDC shell commands, deletion, account changes, message sending, purchases, or other irreversible actions. <br>
Risk: Screenshots and model-provider calls can expose secrets, personal data, or sensitive app state during visual automation. <br>
Mitigation: Avoid screens containing secrets or personal data, and review the Midscene npm package and selected model provider before use. <br>
Risk: The skill requires sensitive model credentials to run Midscene automation. <br>
Mitigation: Provide credentials through trusted environment configuration and avoid committing or displaying API keys in reports, screenshots, or prompts. <br>


## Reference(s): <br>
- [Midscene.js](https://midscenejs.com) <br>
- [Midscene Model Configuration](https://midscenejs.com/model-common-config) <br>
- [DevEco Studio](https://developer.huawei.com/consumer/cn/deveco-studio/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional report Markdown or JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate screenshots, logs, replay reports, and converted report files during device automation.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
