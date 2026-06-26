## Description: <br>
Convert text to speech using SkillBoss API Hub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to turn user-provided text into MP3 voice messages through SkillBoss API Hub and return the generated audio path for delivery to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text supplied for conversion is sent to SkillBoss API Hub. <br>
Mitigation: Avoid converting secrets or highly private text and use only a revocable SKILLBOSS_API_KEY. <br>
Risk: The skill writes generated MP3 audio to a user-specified output path. <br>
Mitigation: Choose output paths deliberately and verify the MEDIA path before sharing the file. <br>
Risk: The release evidence recommends refreshing the stale package lock before npm-based use. <br>
Mitigation: Refresh and review the package lock before installing or running dependencies in production. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kirkraman/jx-tts) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Command-line instructions and MEDIA file paths for generated MP3 audio] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and sends supplied text to SkillBoss API Hub.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
