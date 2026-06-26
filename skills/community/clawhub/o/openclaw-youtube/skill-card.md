## Description: <br>
Searches YouTube videos, channels, rankings, and trends through AIsa for research, competitor scouting, and content discovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content researchers use this skill to run YouTube search, top-video discovery, and competitor research workflows backed by AIsa results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires AISA_API_KEY and sends YouTube search queries to AIsa. <br>
Mitigation: Use a scoped or dedicated key when possible, avoid confidential queries, monitor usage, and rotate the key if it is exposed. <br>
Risk: Returned YouTube titles, URLs, metrics, and rankings may be incomplete or unavailable from upstream results. <br>
Mitigation: Keep summaries grounded in returned data and state clearly when no results or fields are returned. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bibaofeng/openclaw-youtube) <br>
- [AIsa API endpoint](https://api.aisa.one/apis/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY; results depend on AIsa service responses and public YouTube availability.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
