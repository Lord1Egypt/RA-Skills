## Description: <br>
Translates text between Chinese and English using Xfyun, Doubao, Tencent Yuanbao, DeepL, or Iciba, with automatic language detection and selectable target language and engine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paudyyin](https://clawhub.ai/user/paudyyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents can use this skill to translate Chinese and English text, choose a target language and translation provider, and return translated text. Users should avoid confidential, legal, personal, proprietary, or account-sensitive content unless they are comfortable sending it to the selected provider. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User text may be sent to third-party translation or chat providers, and fallback behavior may use a different provider if the first one fails. <br>
Mitigation: Do not use this skill for confidential, legal, personal, proprietary, or account-sensitive text unless the selected provider and fallback behavior are acceptable. <br>
Risk: The artifact claims translation content stays local, while the security evidence says the skill sends text to third-party websites. <br>
Mitigation: Treat provider transmission as expected behavior and review the selected provider's terms, account state, and network requirements before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paudyyin/multi-platform-translator) <br>
- [Xfyun translation](https://fanyi.xfyun.cn/console/trans/text) <br>
- [DeepL translator](https://www.deepl.com/zh/translator) <br>
- [Iciba](https://www.iciba.com/) <br>
- [Doubao chat](https://www.doubao.com/chat) <br>
- [Tencent Yuanbao chat](https://yuanbao.tencent.com/chat/naQivTmsDa) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance] <br>
**Output Format:** [Plain text translation result with brief error guidance when translation fails] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports text, target language, and engine selection; may fall back across providers if the selected engine fails.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
