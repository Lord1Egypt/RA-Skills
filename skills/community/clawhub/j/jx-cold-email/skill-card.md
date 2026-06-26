## Description: <br>
Generate hyper-personalized cold email sequences using AI. Turn lead data into high-converting outreach campaigns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales and growth teams use this skill to turn lead data into personalized cold email sequences for single leads or batches. Developers and operators can call the SkillBoss API Hub with lead fields, sequence options, and approved CTAs to generate structured outreach content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lead details and outreach context are submitted to SkillBoss for processing. <br>
Mitigation: Use the skill only when there is a lawful basis for outreach and avoid submitting sensitive or regulated data unless approved by the organization. <br>
Risk: The skill requires a SkillBoss API key. <br>
Mitigation: Store SKILLBOSS_API_KEY in a secure secret store and avoid placing it in prompts, logs, or committed files. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/kirkraman/jx-cold-email) <br>
- [SkillBoss API Settings](https://app.skillbossai.com/settings) <br>
- [SkillBoss API Hub Endpoint](https://api.skillbossai.com/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, API Calls, Configuration] <br>
**Output Format:** [Markdown guidance with JSON request and response examples plus Python code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated email sequences are returned as JSON content from the SkillBoss API response.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
