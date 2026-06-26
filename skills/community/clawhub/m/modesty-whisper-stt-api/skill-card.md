## Description: <br>
Provides agents with setup and API guidance for using OpenAI Whisper speech-to-text through SkillBoss with a SkillBoss API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[modestyrichards](https://clawhub.ai/user/modestyrichards) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to configure a SkillBoss API key and call the OpenAI Whisper speech-to-text model through SkillBoss when they need transcription without managing direct provider accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is presented as a Whisper transcription helper but installs or routes users toward a broader paid SkillBoss API gateway. <br>
Mitigation: Install only if the broader gateway is acceptable, and require explicit approval before any non-Whisper action. <br>
Risk: Using the service requires a sensitive SkillBoss API key and may send audio or request data to SkillBoss. <br>
Mitigation: Store the key only in the SKILLBOSS_API_KEY environment variable, rotate it if exposed, and avoid sending sensitive audio unless approved. <br>
Risk: Pay-as-you-go API calls can create charges. <br>
Mitigation: Use spending limits or restricted keys where available, and confirm expected costs before running transcription jobs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/modestyrichards/modesty-whisper-stt-api) <br>
- [SkillBoss console](https://skillboss.co/console) <br>
- [SkillBoss API endpoint](https://api.skillboss.co/v1/run) <br>
- [SkillBoss products](https://skillboss.co/products) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with bash, curl, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for live API use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
