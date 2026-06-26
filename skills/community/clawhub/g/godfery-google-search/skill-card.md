## Description: <br>
Search the web using SkillBoss API Hub. Use this when you need live information, documentation, or to research topics and the built-in web_search is unavailable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw agents use this skill to run live web searches through SkillBoss API Hub when current information, documentation lookup, or topic research is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive SkillBoss API key. <br>
Mitigation: Keep SKILLBOSS_API_KEY private, store it outside committed files, and do not commit .env files. <br>
Risk: Search queries are sent to SkillBoss and may expose sensitive information if users include it. <br>
Mitigation: Avoid searching for credentials, private documents, internal URLs, or confidential business details. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kirkraman/godfery-google-search) <br>
- [SkillBoss API Hub Endpoint](https://api.skillbossai.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON search results from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and sends search queries to SkillBoss.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
