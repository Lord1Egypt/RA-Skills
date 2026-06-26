## Description: <br>
Transcribes audio from URLs or local files into text using multilingual automatic speech recognition via SkillBoss API Hub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to transcribe audio from URLs or local files into JSON text transcripts for automated workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio files, fetched URL content, and optional language hints are sent to a hosted SkillBoss/HeyBoss transcription API. <br>
Mitigation: Use only audio that is approved for the provider's privacy, retention, billing, and security terms; avoid confidential, regulated, or internal-only recordings unless those terms meet requirements. <br>
Risk: The skill requires a sensitive API key for transcription requests. <br>
Mitigation: Store SKILLBOSS_API_KEY as a secret or environment variable and do not commit it to source control. <br>


## Reference(s): <br>
- [ClawHub ASR skill page](https://clawhub.ai/kirkraman/jx-asr) <br>
- [SkillBoss API Hub](https://heybossai.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON] <br>
**Output Format:** [JSON response containing transcript text at .result.text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and returns clear errors when the API key is missing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact manifest and changelog mention 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
