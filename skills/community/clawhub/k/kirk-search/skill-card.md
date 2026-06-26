## Description: <br>
Neural web search and content extraction via SkillBoss API Hub, requiring SKILLBOSS_API_KEY for finding documentation, code examples, research papers, and company information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run web searches, find code and documentation context, and extract full text from URLs through the SkillBoss API Hub. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and URLs are sent to a third-party hosted API. <br>
Mitigation: Do not submit secrets, proprietary code, internal URLs, private documents, or authenticated links unless that sharing is approved by the organization. <br>
Risk: The skill requires a sensitive API credential in SKILLBOSS_API_KEY. <br>
Mitigation: Store the key in the environment, avoid committing it to files or logs, and rotate it if it is exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kirkraman/kirk-search) <br>
- [SkillBoss setup guide](https://skillboss.co/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON API responses and Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and sends search queries or submitted URLs to the SkillBoss/HeyBoss API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
