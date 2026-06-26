## Description: <br>
Searches the web through SkillBoss API Hub for current information, news, images, and videos with configurable filters and text, Markdown, or JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[modestyrichards](https://clawhub.ai/user/modestyrichards) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to run current web, news, image, and video searches through SkillBoss API Hub. It supports research, fact-checking, resource gathering, and saved search results in text, Markdown, or JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and the SkillBoss API key are sent to an external SkillBoss/HeyBoss API service. <br>
Mitigation: Install only if the user trusts that service with search queries and credentials, and avoid searching for secrets, private project details, personal data, or regulated information. <br>
Risk: The --output option writes search results to a user-provided path and can overwrite existing files. <br>
Mitigation: Use deliberate workspace paths for saved results and inspect paths before running searches that write files. <br>


## Reference(s): <br>
- [Skill instructions](SKILL.md) <br>
- [Search script](scripts/search.py) <br>
- [SkillBoss setup guide](https://skillboss.co/skill.md) <br>
- [ClawHub skill page](https://clawhub.ai/modestyrichards/modesty-web-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, files] <br>
**Output Format:** [Plain text, Markdown, or JSON search results; optional saved files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports web, news, image, and video result sets with result limits, region, time range, safe-search, image, and video filters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
