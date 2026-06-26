## Description: <br>
Controls an Android phone through ADB and GLM from natural-language instructions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moroiser](https://clawhub.ai/user/moroiser) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, testers, and advanced users use this skill to configure ADB-based Android phone automation and issue natural-language tasks such as opening apps, searching, navigating, typing, and taking over manually on sensitive screens. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires broad ADB-level automation over a connected Android phone and depends on external, unpinned code and an APK. <br>
Mitigation: Use a dedicated test device when possible, pin and verify the Open-AutoGLM repository and ADB Keyboard APK before use, and revoke USB debugging plus remove ADB Keyboard after finishing. <br>
Risk: Phone screenshots may be sent to the external GLM API and could expose private chats, credentials, payment details, or banking screens. <br>
Mitigation: Avoid banking, payment, password, and private-chat screens; require manual takeover for sensitive screens; and confirm every write, purchase, settings, or delete action before execution. <br>


## Reference(s): <br>
- [Phone Controller ClawHub release](https://clawhub.ai/moroiser/phone-controller) <br>
- [Publisher profile](https://clawhub.ai/user/moroiser) <br>
- [Open-AutoGLM project](https://github.com/zai-org/Open-AutoGLM) <br>
- [ADB Keyboard APK](https://github.com/senzhk/ADBKeyBoard/blob/master/ADBKeyboard.apk) <br>
- [BigModel GLM API](https://open.bigmodel.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with setup steps, shell command examples, operating rules, and safety guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an Android device with USB debugging, ADB Keyboard, Open-AutoGLM, and a GLM API key.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
