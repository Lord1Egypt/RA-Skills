## Description: <br>
Notcrawl helps agents search local Notion archives, check freshness, inspect pages and databases, export Markdown, run SQL counts, and work with the Notcrawl repository. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openclaw](https://clawhub.ai/user/openclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use Notcrawl to inspect local Notion archive content before browsing or using live Notion API calls, report exact source dates and gaps, and refresh the archive only when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may expose sensitive Notion archive content to an agent during search or reporting. <br>
Mitigation: Use it only with Notion archives you are comfortable letting the agent inspect, and limit API sync to a least-privilege Notion integration token scoped to intended content. <br>
Risk: Out-of-date local archives can produce stale answers. <br>
Mitigation: Check freshness with notcrawl doctor or notcrawl status before recent or current questions, and sync only when stale or explicitly requested. <br>
Risk: SQL access could damage archive data if used for writes. <br>
Mitigation: Use read-only SQL only and do not mutate the archive. <br>


## Reference(s): <br>
- [Notcrawl homepage](https://github.com/openclaw/notcrawl) <br>
- [ClawHub Notcrawl skill](https://clawhub.ai/openclaw/notcrawl) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with concise source summaries and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bounded local archive reads; read-only SQL; optional API sync requires NOTION_TOKEN.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
