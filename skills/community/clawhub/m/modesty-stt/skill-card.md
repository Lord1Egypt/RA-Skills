## Description: <br>
Transcribe audio files using SkillBoss API Hub STT. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[modestyrichards](https://clawhub.ai/user/modestyrichards) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to transcribe local audio files into text through SkillBoss API Hub. It is suited for voice-message and audio-file workflows using OGG, Opus, MP3, WAV, or M4A inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected audio recordings are uploaded to a third-party transcription API. <br>
Mitigation: Use only with recordings approved for third-party transcription, and avoid confidential, regulated, or highly personal audio unless policy permits it. <br>
Risk: The skill requires SKILLBOSS_API_KEY for authentication. <br>
Mitigation: Store SKILLBOSS_API_KEY securely, avoid committing it to source control, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/modestyrichards/modesty-stt) <br>
- [SkillBoss API endpoint](https://api.heybossai.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Plain text transcript with Markdown usage guidance and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and sends selected audio files to the SkillBoss API Hub.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
