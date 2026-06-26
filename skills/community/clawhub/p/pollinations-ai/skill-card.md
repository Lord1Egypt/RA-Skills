## Description: <br>
Generate images, music, and video using Pollinations AI API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kanfred](https://clawhub.ai/user/kanfred) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to generate images, audio, and videos from text prompts through Pollinations AI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, generation parameters, API key-authenticated requests, and generated media are sent to Pollinations AI. <br>
Mitigation: Do not use confidential or regulated content in prompts, and deploy only where Pollinations AI processing is acceptable. <br>
Risk: Unpinned dependencies can change behavior over time in production environments. <br>
Mitigation: Pin requests and Pillow versions in production deployments and review updates before rollout. <br>
Risk: Optional Telegram sharing can send generated images outside the local workspace. <br>
Mitigation: Set TELEGRAM_CHAT_ID only for the intended chat and leave it unset when Telegram sharing is not required. <br>


## Reference(s): <br>
- [Pollinations API Documentation](https://gen.pollinations.ai/api/docs) <br>
- [Pollinations Website](https://pollinations.ai/) <br>
- [ClawHub Skill Page](https://clawhub.ai/kanfred/pollinations-ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with Python CLI commands; runtime outputs are JPG, MP3, and MP4 media files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires POLLINATIONS_API_KEY, writes generated media to allowed output directories, and can optionally share images through Telegram when TELEGRAM_CHAT_ID is set.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
