## Description: <br>
Fast, accurate automatic speech-to-text transcription supporting 100 languages from URLs or local files via SkillBoss API Hub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[modestyrichards](https://clawhub.ai/user/modestyrichards) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to transcribe audio from URLs or local files into machine-readable text through the SkillBoss API Hub. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected audio files or URL-fetched media are sent to SkillBoss for transcription. <br>
Mitigation: Use only recordings that are permitted by SkillBoss terms, retention practices, and organizational policy; avoid confidential, regulated, or internal recordings unless explicitly approved. <br>
Risk: The skill requires a SkillBoss API key. <br>
Mitigation: Store SKILLBOSS_API_KEY in a secret manager or protected environment configuration and avoid committing or logging it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/modestyrichards/modesty-asr) <br>
- [SkillBoss API Hub](https://skillboss.co) <br>
- [Skill usage guide](artifact/SKILL.md) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands] <br>
**Output Format:** [JSON response with transcription text at .result.text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY; accepts URL or local file input and an optional language code.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
