## Description: <br>
Generate hyper-personalized cold email sequences using AI. Turn lead data into high-converting outreach campaigns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, marketing, and growth users use this skill to generate personalized cold email sequences for individual prospects or lead lists from contact and company data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lead contact data is sent to the external SkillBoss API. <br>
Mitigation: Use the skill only when you are authorized to process and transmit the prospect data, omit optional personal fields when possible, and review SkillBoss privacy, retention, and compliance terms before use. <br>
Risk: The skill requires a sensitive SkillBoss API key. <br>
Mitigation: Use a scoped API key, store it in the SKILLBOSS_API_KEY environment variable, and rotate or revoke it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kirkraman/kirk-cold-email) <br>
- [SkillBoss setup guide](https://skillboss.co/skill.md) <br>
- [SkillBoss API endpoint](https://api.skillboss.co/v1/pilot) <br>
- [SkillBoss API key settings](https://app.skillboss.co/settings) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON and Python examples for API-backed cold email sequence generation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and sends lead contact data to SkillBoss.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
