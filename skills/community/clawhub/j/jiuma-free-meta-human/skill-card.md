## Description: <br>
九马AI免费数字人视频生成技能，使用九马AI API将文本内容或音频内容生成口型同步的数字人视频，并支持选择不同数字人形象和音色。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dddcn1](https://clawhub.ai/user/dddcn1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create Jiuma-hosted digital-human videos from text or audio inputs, then check generation status and retrieve the resulting video URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user generation inputs to Jiuma and relies on a reusable Jiuma API key stored locally in plaintext. <br>
Mitigation: Use only on trusted machines, avoid sensitive personal or regulated content, and delete or protect the local .jiuma credential files after use. <br>
Risk: The skill may return login or recharge links during authentication, low balance, or account-required flows. <br>
Mitigation: Verify login and recharge links before using them, and do not scan payment or login QR codes from untrusted sessions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dddcn1/jiuma-free-meta-human) <br>
- [Jiuma API service endpoint](https://api.jiuma.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces task IDs, status messages, login or payment links when required, and final video URLs returned by Jiuma.] <br>

## Skill Version(s): <br>
1.0.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
