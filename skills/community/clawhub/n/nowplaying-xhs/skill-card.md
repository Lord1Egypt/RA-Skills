## Description: <br>
当前院线推荐 - 实时检索公映影片 + 多维度评分 + 附近影院排片 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seeu1688](https://clawhub.ai/user/seeu1688) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to produce current moviegoing recommendations with ratings, box-office context, and nearby showtime guidance. It can be run on demand or scheduled to generate a Markdown report for weekend viewing decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use sensitive API credentials for live web search. <br>
Mitigation: Configure credentials through environment variables, do not print API keys, and review commands before running troubleshooting steps that inspect the environment. <br>
Risk: Location-aware showtime lookup can expose more location detail than needed. <br>
Mitigation: Use approximate city-level location when possible and avoid sharing precise coordinates unless necessary for the user's request. <br>
Risk: Browser and chart workflows can start local tooling or serve files from temporary directories. <br>
Mitigation: Serve only a dedicated temporary directory, stop the local server immediately after use, and avoid installing Agent Browser globally unless that behavior is explicitly desired. <br>
Risk: Live movie, rating, and showtime data can be stale, incomplete, or scraped from changing pages. <br>
Mitigation: Label data freshness in the report and direct users to verify final showtimes and prices in the official ticketing app before purchase. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/seeu1688/nowplaying-xhs) <br>
- [Publisher profile](https://clawhub.ai/user/seeu1688) <br>
- [README](README.md) <br>
- [Configuration guide](CONFIG.md) <br>
- [Rotten Tomatoes in-theaters listings](https://www.rottentomatoes.com/browse/movies_in_theaters) <br>
- [Variety film coverage](https://variety.com/v/film/) <br>
- [Bocha web search API](https://api.bocha.cn/v1/web-search) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with tables, links, rankings, and optional generated chart artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write dated report files under /tmp and may require live web access, API keys, or browser tooling for complete showtime and chart workflows.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
