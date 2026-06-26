## Description: <br>
AI PPT Generate helps agents use SkillBoss API Hub to generate presentation outlines and downloadable PPT files from a topic, question, or outline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate PPT outlines and presentation download URLs through the SkillBoss/HeyBossAI API. It is intended for workflows where prompts, outlines, and optional resource URLs can be sent to an external presentation-generation service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Presentation prompts, outlines, and resource URLs are sent to an external SkillBoss/HeyBossAI API. <br>
Mitigation: Avoid confidential documents, internal URLs, customer data, and proprietary templates unless the provider is approved under your organization's data-handling rules. <br>
Risk: The skill requires a SkillBoss API key. <br>
Mitigation: Provide the key through managed environment secrets, limit access to trusted runtimes, and rotate the key if it is exposed. <br>
Risk: Some documented theme and template workflow features are incomplete in this version. <br>
Mitigation: Validate the actual scripts and API responses in a non-production workflow before depending on theme, template, or custom-template behavior. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/kirkraman/martin-ai-ppt-generate) <br>
- [HeyBossAI pilot API endpoint](https://api.heybossai.com/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON responses from Python scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and sends presentation prompts or outlines to SkillBoss/HeyBossAI; successful calls return generation identifiers and PPT URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
