## Description: <br>
Indie Maker News aggregates public RSS and API news about solo businesses, side projects, startups, and monetization, then filters the results into action-oriented business signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kylnwu](https://clawhub.ai/user/kylnwu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External founders, indie makers, side-project developers, and solo operators use this skill to scan public news sources for monetization ideas, startup examples, tool recommendations, and cautionary lessons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts public RSS/API sources at runtime, despite local documentation that also claims no external API calls. <br>
Mitigation: Review the source list and run the skill only in environments where outbound access to those public news sources is acceptable. <br>
Risk: Aggregated news can be incomplete, unavailable, stale, or misleading because it depends on third-party public feeds. <br>
Mitigation: Verify important business or investment conclusions against primary sources before acting on the generated summaries. <br>
Risk: The artifact contains conflicting version and license signals. <br>
Mitigation: Confirm the authoritative ClawHub release version and license before publication or redistribution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kylnwu/indie-maker-news) <br>
- [36Kr RSS feed](https://36kr.com/feed) <br>
- [V2EX RSS feed](https://www.v2ex.com/index.xml) <br>
- [Hacker News RSS feed](https://hnrss.org/frontpage) <br>
- [GitHub Trending RSS feed](https://mshibanami.github.io/GitHubTrendingRSS/daily.xml) <br>
- [Wallstreetcn public API endpoint](https://api-one.wallstcn.com/apiv1/content/lives?channel=global-channel&limit=30) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; runtime scripts emit JSON and plain-text news summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [News output is time-sensitive and depends on availability of public RSS/API sources.] <br>

## Skill Version(s): <br>
1.0.5 (source: ClawHub release metadata; artifact frontmatter says 1.1.0 and package.json says 1.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
