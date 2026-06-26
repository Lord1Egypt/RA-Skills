## Description: <br>
Mxyj Heartplus Ecg helps Apple Watch and Heartplus App users in mainland China trigger ECG measurement notifications, complete Heartplus authorization, and retrieve generated ECG analysis reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mxyjhelowin](https://clawhub.ai/user/mxyjhelowin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Apple Watch and iPhone users with mainland China phone numbers use this agent skill to start ECG measurement flows through Heartplus, authorize account access, and view ECG report lists or detailed reports. <br>

### Deployment Geography for Use: <br>
China mainland <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive health, account, phone, authorization, and report-cache data may be handled or left in the skill directory. <br>
Mitigation: Use the skill only on a trusted personal machine, do not share sessionKeys, and manually remove local phone, auth, and report-cache data when finished. <br>
Risk: The skill may download and run an external native healthgateway helper. <br>
Mitigation: Install only when the publisher, Heartplus service, and external binary source are trusted, and verify the configured downloads and hashes before execution. <br>
Risk: ECG report guidance may be misunderstood as emergency or diagnostic medical advice. <br>
Mitigation: Preserve the artifact's medical disclaimers and direct users with chest pain, chest tightness, fainting, breathing difficulty, or other urgent symptoms to contact a doctor or emergency services. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mxyjhelowin/mxyj-heartplus-ecg) <br>
- [Heartplus App Store listing](https://apps.apple.com/cn/app/%E5%BF%83%E8%84%8F-%E5%BF%83%E7%8E%87-%E5%BF%83%E8%B7%B3-%E5%BF%83%E8%84%8F%E5%81%A5%E5%BA%B7%E6%A3%80%E6%B5%8B/id1584620848) <br>
- [Apple Watch ECG support](https://support.apple.com/zh-cn/120277) <br>
- [SessionKey guide](references/SessionKey获取说明.md) <br>
- [Report output guide](references/报告输出说明.md) <br>
- [Script and flow guide](references/脚本与流程说明.md) <br>
- [uv installer for Linux](https://astral.sh/uv/install.sh) <br>
- [uv installer for Windows](https://astral.sh/uv/install.ps1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports and concise text with inline shell commands or configuration values.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ECG report tables that should be passed through as Markdown; depends on Heartplus authorization, a session key, and local command execution.] <br>

## Skill Version(s): <br>
0.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
