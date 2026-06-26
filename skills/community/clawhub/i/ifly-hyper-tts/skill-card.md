## Description: <br>
讯飞超拟人语音合成 - 支持文本转语音、语音合成（发音人/语速/语调/音量/输出格式）。大模型语音合成技能。语音合成, 文字转语音, 超拟人, TTS. 用户指令如"把这段文案读出来"时使用此Skill。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qingzhe2020](https://clawhub.ai/user/qingzhe2020) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to convert provided text into speech audio through iFlytek/Xfei hyper-realistic TTS, with optional voice, speed, volume, pitch, sample-rate, and output-file settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for synthesis is sent to iFlytek/Xfei. <br>
Mitigation: Avoid regulated, confidential, or secret text unless that use is approved for the target environment and provider account. <br>
Risk: The skill requires XFEI_APP_ID, XFEI_API_KEY, and XFEI_API_SECRET credentials. <br>
Mitigation: Use dedicated scoped credentials where possible, store them outside prompts and source files, and rotate them if exposure is suspected. <br>
Risk: The runtime depends on websocket-client from the Python package ecosystem. <br>
Mitigation: Install dependencies from a trusted package source and review dependency provenance before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/qingzhe2020/ifly-hyper-tts) <br>
- [iFlytek hyper-realistic TTS API documentation](https://www.xfyun.cn/doc/spark/super%20smart-tts.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands; runtime script output is JSON and generated audio files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces MP3 audio by default and JSON status metadata; requires python3, websocket-client, and XFEI_APP_ID, XFEI_API_KEY, and XFEI_API_SECRET.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
