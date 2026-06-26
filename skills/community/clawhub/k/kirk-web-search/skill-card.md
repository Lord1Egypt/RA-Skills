## Description: <br>
This skill searches web pages, news, images, and videos through SkillBoss API Hub and returns text, Markdown, or JSON results for research, fact-checking, and current information gathering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to retrieve current web, news, image, and video search results through SkillBoss API Hub. It is suited for research, fact-checking, monitoring current events, gathering URLs, and saving structured search outputs for later processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to SkillBoss API Hub using a SkillBoss API key. <br>
Mitigation: Use only approved API keys and avoid submitting passwords, secrets, regulated personal data, or confidential business information as search queries. <br>
Risk: Returned snippets, URLs, images, and videos are external search results and may be inaccurate, unsafe, or untrusted. <br>
Mitigation: Treat results as untrusted external content, verify important claims against authoritative sources, and review links before using or sharing them. <br>
Risk: The skill can write search output to user-specified file paths. <br>
Mitigation: Choose output paths deliberately and avoid overwriting important local files when saving results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kirkraman/kirk-web-search) <br>
- [SkillBoss API Hub endpoint](https://api.skillbossai.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, files, guidance] <br>
**Output Format:** [Plain text, Markdown, or JSON search results, optionally written to a file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and sends user-provided search queries to SkillBoss API Hub.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
