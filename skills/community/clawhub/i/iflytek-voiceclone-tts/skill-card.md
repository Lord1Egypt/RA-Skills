## Description: <br>
Use when a user asks to clone a voice, train a custom voice model, or synthesize speech with a cloned voice using the iFlytek Voice Clone API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iflytek.skills](https://clawhub.ai/user/iflytek.skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to guide an iFlytek voice-cloning workflow: train a custom voice from permitted recordings, retrieve a voice resource ID, and synthesize speech from text or files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice cloning can misuse biometric voice data or enable impersonation without consent. <br>
Mitigation: Use only voices you own or have explicit permission to clone, and avoid sensitive recordings or private text. <br>
Risk: Training audio and synthesis requests go to third-party iFlytek services. <br>
Mitigation: Do not submit confidential or regulated data unless your organization has approved the service and data handling terms. <br>
Risk: The security evidence reports insecure TLS and plain-HTTP training endpoints that may expose credentials and biometric voice data on the network. <br>
Mitigation: Fix transport security before handling real or sensitive voices, and review network exposure carefully before installing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iflytek.skills/iflytek-voiceclone-tts) <br>
- [iFlytek Voice Clone service homepage](https://www.xfyun.cn/services/voice_clone) <br>
- [iFlytek Voice Clone API documentation](https://www.xfyun.cn/doc/spark/voiceclone.html) <br>
- [iFlytek one-sentence voice clone console](https://console.xfyun.cn/services/oneSentenceV2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands and Python CLI invocations; the bundled script can produce JSON status responses and audio files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires IFLY_APP_ID, IFLY_API_KEY, and IFLY_API_SECRET; training audio must match the selected training text.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
