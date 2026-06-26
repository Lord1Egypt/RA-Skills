## Description: <br>
Generate subtitles from audio or video by selecting a SkillBoss-backed AI model for the task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate AI subtitles from audio or video, compare model choices, and configure a SkillBoss API key for subtitle workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The subtitle workflow asks users to enable a broad paid SkillBoss API setup that goes beyond subtitle generation. <br>
Mitigation: Review the remote SkillBoss setup before running it and prefer a workflow limited to transcription or subtitle models. <br>
Risk: The skill requires a sensitive SkillBoss API key and can trigger paid model usage. <br>
Mitigation: Use spending limits or a restricted key if available, monitor usage, and revoke keys that are no longer needed. <br>
Risk: Audio or video submitted for subtitles may be sent to SkillBoss and downstream model providers. <br>
Mitigation: Only submit media that is appropriate to share with those services. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kirkraman/kirk-ai-subtitle-generator) <br>
- [SkillBoss console](https://skillboss.co/console) <br>
- [SkillBoss API endpoint](https://api.skillboss.co/v1/run) <br>
- [SkillBoss products](https://skillboss.co/products) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, API examples, and model guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and may route audio or video to SkillBoss and downstream model providers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
