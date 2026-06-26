## Description: <br>
Pub Whisper gives agents examples for calling the SkillBoss API gateway for chat, media generation, transcription, search, document processing, email, and SMS workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ModestyRichards](https://clawhub.ai/user/ModestyRichards) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users can use this skill to discover model IDs and draft API calls for SkillBoss-hosted chat, image, video, audio, search, document, email, and SMS tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is presented as local Whisper transcription but documents a remote multi-service API gateway. <br>
Mitigation: Review carefully before installing and use it only when remote gateway behavior is intended. <br>
Risk: Audio, text, images, search queries, documents, email content, and phone numbers may leave the user's environment. <br>
Mitigation: Require explicit user approval before uploading sensitive content or sending any message. <br>
Risk: Email and SMS examples can initiate external communications. <br>
Mitigation: Confirm recipients, content, and purpose before executing email or SMS commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ModestyRichards/openai-whispers) <br>
- [Publisher profile](https://clawhub.ai/user/ModestyRichards) <br>
- [SkillBoss API base URL](https://api.heybossai.com/v1) <br>
- [SkillBoss website](https://www.skillboss.co) <br>
- [Audio Models](artifact/audio-models.md) <br>
- [Chat Models](artifact/chat-models.md) <br>
- [Image Models](artifact/image-models.md) <br>
- [Search & Scraping Models](artifact/search-models.md) <br>
- [Tool Models](artifact/tools-models.md) <br>
- [Video Models](artifact/video-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
