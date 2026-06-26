## Description: <br>
Provides command-line guidance for using the IndexTTS voice cloning and text-to-speech API to manage voice models, reference audio, TTS jobs, downloads, and quota checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cxhcccvvvsder](https://clawhub.ai/user/cxhcccvvvsder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content teams use this skill to create and manage voice-clone models and synthesize speech through a paid IndexTTS enterprise API. Users should already have an IndexTTS API sign credential and authorization to use any reference voice audio. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports voice cloning and text-to-speech workflows that can misuse another person's voice without consent. <br>
Mitigation: Use only reference voice audio with explicit authorization, document consent for cloning workflows, and review generated speech for impersonation or misleading use before distribution. <br>
Risk: Audio samples, reference clips, text prompts, and generated speech are uploaded to or downloaded from a third-party IndexTTS API service. <br>
Mitigation: Confirm the provider's retention, deletion, and access terms before use, and avoid uploading sensitive, private, or regulated audio or text unless approved for that provider. <br>
Risk: The skill requires an API signing secret for a paid enterprise account. <br>
Mitigation: Store INDEX_API_SIGN in an approved secret store or environment variable, avoid committing it to files or logs, and rotate it if exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cxhcccvvvsder/indextts-voice) <br>
- [IndexTTS website](https://indextts.cn) <br>
- [IndexTTS developer documentation](https://indextts.cn/main/developer) <br>
- [IndexTTS API base URL](https://openapi.lipvoice.cn/api/third/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with CLI commands, configuration examples, JSON API responses, and downloaded audio files when commands are executed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires INDEX_API_SIGN for authenticated IndexTTS API calls; INDEX_BASE_URL defaults to https://openapi.lipvoice.cn.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence and artifact changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
