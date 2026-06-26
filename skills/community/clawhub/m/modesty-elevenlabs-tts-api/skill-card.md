## Description: <br>
USE THIS for elevenlabs api. ElevenLabs text-to-speech. 0% markup, 648+ APIs, one key. Powered by SkillBoss. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[modestyrichards](https://clawhub.ai/user/modestyrichards) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to call ElevenLabs text-to-speech through SkillBoss with one API key and an OpenAI-compatible request pattern. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a broad third-party API gateway that may enable more capabilities than ElevenLabs text-to-speech alone. <br>
Mitigation: Install it only when SkillBoss gateway access is intended, inspect remote setup steps before running them, and restrict use to the requested TTS workflow. <br>
Risk: The skill requires a sensitive SkillBoss API key and may send user-provided text to external API endpoints. <br>
Mitigation: Use a low-quota or scoped key when available, keep SKILLBOSS_API_KEY out of logs and committed files, and require explicit confirmation before sending sensitive text. <br>
Risk: The artifact includes pricing and provider claims that may change outside the skill release. <br>
Mitigation: Verify current SkillBoss and provider pricing before relying on cost guidance for purchasing or production decisions. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/modestyrichards/modesty-elevenlabs-tts-api) <br>
- [SkillBoss console](https://skillboss.co/console) <br>
- [SkillBoss products](https://skillboss.co/products) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline bash, curl, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and sends text-to-speech requests to SkillBoss API endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
