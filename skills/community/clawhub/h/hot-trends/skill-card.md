## Description: <br>
Fetches real hot-search and trending-topic data from Baidu Hot Search, Toutiao Hot Board, and GitHub Trending for trend analysis, market insight, and demand discovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[embracex1998](https://clawhub.ai/user/embracex1998) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and market researchers use this skill to retrieve current public trend data and filter it by platform, keyword, or GitHub language for demand discovery and market insight. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound network requests to Baidu, Toutiao, and GitHub when trend data is requested. <br>
Mitigation: Use explicit prompts for the intended source, and run it only in environments where those public network requests are acceptable. <br>
Risk: Generic trigger words such as 'trending' or '趋势' could activate the skill unintentionally. <br>
Mitigation: Prefer source-specific prompts such as 'show GitHub Trending' or 'fetch Baidu hot search'. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/embracex1998/hot-trends) <br>
- [Publisher profile](https://clawhub.ai/user/embracex1998) <br>
- [Baidu Hot Search API](https://top.baidu.com/api/board?platform=wise&tab=realtime&offset=0&limit=30) <br>
- [Toutiao Hot Board API](https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc) <br>
- [GitHub Trending](https://github.com/trending) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Console text suitable for Markdown summaries or follow-up analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns ranked trend items with titles and optional heat, language, and description fields depending on the selected source.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
