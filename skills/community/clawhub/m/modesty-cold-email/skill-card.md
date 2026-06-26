## Description: <br>
Generate hyper-personalized cold email sequences using AI. Turn lead data into high-converting outreach campaigns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[modestyrichards](https://clawhub.ai/user/modestyrichards) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales and go-to-market teams use this skill to generate personalized cold email sequences from lead data. Developers can also use the included API request and parsing examples to integrate SkillBoss cold-email generation into outreach workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lead data is sent to SkillBoss for processing. <br>
Mitigation: Use only when authorized to share the lead data, minimize unnecessary personal data, and review applicable privacy and compliance requirements before deployment. <br>
Risk: The skill requires a sensitive SkillBoss API key. <br>
Mitigation: Store SKILLBOSS_API_KEY in a secure environment or secret store and avoid committing it to code, prompts, logs, or shared files. <br>
Risk: Generated outreach may include inaccurate claims or messaging that is unsuitable for a recipient or campaign. <br>
Mitigation: Review generated sequences before sending and align them with approved campaign language, consent requirements, and organizational outreach policies. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/modestyrichards/modesty-cold-email) <br>
- [SkillBoss API Hub endpoint](https://api.skillbossai.com/v1/pilot) <br>
- [SkillBoss API key settings](https://app.skillbossai.com/settings) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request and response examples, plus Python code snippets; generated outreach content is returned as JSON strings from the API.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and sends lead data to the SkillBoss API Hub.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
