## Description: <br>
Guides agents to configure SkillBoss for ElevenLabs voice cloning and model selection through a paid third-party AI gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to set up SkillBoss credentials, call the SkillBoss API, and route voice-cloning requests to ElevenLabs or other selected models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive SkillBoss API key for a broad paid AI platform. <br>
Mitigation: Use a restricted key or billing limits where available, and only install after confirming the agent should access the broader SkillBoss platform. <br>
Risk: Voice cloning can be misused or performed without consent. <br>
Mitigation: Clone voices only with clear authorization from the voice owner and with user review of the requested voice-cloning workflow. <br>
Risk: Prompts or audio may be sent to an external provider. <br>
Mitigation: Avoid sending confidential or regulated content unless the provider terms and data handling are approved for the use case. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kirkraman/kirk-ai-voice-cloning) <br>
- [SkillBoss setup skill](https://skillboss.co/skill.md) <br>
- [SkillBoss console](https://skillboss.co/console) <br>
- [SkillBoss products](https://skillboss.co/products) <br>
- [SkillBoss API endpoint](https://api.skillboss.co/v1/run) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with shell commands and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and may send prompts or audio to an external paid provider.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
