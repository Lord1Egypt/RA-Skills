## Description: <br>
Fetches Douyin hot-search and trending-board data, including titles, popularity values, detail links, labels, content types, and cover image URLs when available. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marjoriebroad](https://clawhub.ai/user/marjoriebroad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and social-media operators use this skill to retrieve current Douyin trending topics for monitoring, reporting, and content planning workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive SkillBoss API key. <br>
Mitigation: Use a limited-scope key, store it only in the runtime environment, and rotate it if logs or generated files may have exposed execution context. <br>
Risk: Automation artifacts include Telegram-style delivery metadata and a fixed chat_id in generated JSON. <br>
Mitigation: Do not connect generated JSON to any messaging tool unless the destination chat_id is yours and intentionally configured. <br>
Risk: Helper scripts invoke Node through an execSync command wrapper. <br>
Mitigation: Avoid untrusted arguments and replace command-string execution with safer argument passing before broader deployment. <br>
Risk: The Douyin web endpoint and returned data structure may change or rate-limit frequent access. <br>
Mitigation: Handle empty or changed responses, limit request frequency, and review output before using it for operational decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/marjoriebroad/mar-douyin-hot-trend) <br>
- [Publisher profile](https://clawhub.ai/user/marjoriebroad) <br>
- [Douyin hot search endpoint](https://www.douyin.com/aweme/v1/hot/search/list/) <br>
- [SkillBoss API base](https://api.heybossai.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [Console text, Markdown trend summaries, and JSON result files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and SKILLBOSS_API_KEY; default trend limit is 50 for the direct script and 10 for automation helpers.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter and package.json report 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
