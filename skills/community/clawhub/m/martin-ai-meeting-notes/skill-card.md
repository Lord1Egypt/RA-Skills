## Description: <br>
AI Meeting Notes helps an agent transcribe and summarize meetings while choosing a SkillBoss-backed AI model for cost, speed, or quality. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to set up SkillBoss access, transcribe and summarize meetings, and select an AI model that fits their quality and cost requirements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting audio, transcripts, and notes may be sent to SkillBoss and downstream model providers. <br>
Mitigation: Avoid confidential, regulated, or personal meetings unless the publisher provides clear data-handling terms and the user has appropriate consent. <br>
Risk: The required SkillBoss API key can enable broader third-party API access than meeting notes alone require. <br>
Mitigation: Use narrowly scoped credentials where available, apply spend limits or monitoring, and rotate the key if exposed. <br>
Risk: Pay-as-you-go model calls can create unexpected costs. <br>
Mitigation: Select an appropriate model before use and monitor usage against a defined budget. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kirkraman/martin-ai-meeting-notes) <br>
- [SkillBoss setup skill](https://skillboss.co/skill.md) <br>
- [SkillBoss console](https://skillboss.co/console) <br>
- [SkillBoss OpenAI-compatible chat completions endpoint](https://api.skillboss.co/v1/chat/completions) <br>
- [SkillBoss products](https://skillboss.co/products) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and may send meeting content to third-party AI APIs under pay-as-you-go pricing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
