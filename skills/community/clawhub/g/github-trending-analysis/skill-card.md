## Description: <br>
Fetches and summarizes GitHub Trending repositories by day, week, or month, with optional language filters, comparisons, and weekly or monthly trend reports in Chinese. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhuxiaoke27](https://clawhub.ai/user/zhuxiaoke27) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and technical readers use this skill to inspect current GitHub Trending projects, compare trend periods, filter by programming language, and generate Chinese-language weekly or monthly trend reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill browses public GitHub Trending and repository pages, so summaries may be affected by unavailable pages, changed README content, or incomplete fetched content. <br>
Mitigation: Verify important repository details directly on GitHub before making technical or adoption decisions. <br>
Risk: Optional in-memory caching can retain fetched public trend data during an agent session. <br>
Mitigation: Use the skill only for public repository research and avoid adding private or credential-bearing content to prompts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhuxiaoke27/github-trending-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/zhuxiaoke27) <br>
- [GitHub Trending](https://github.com/trending) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Chinese Markdown summaries, comparisons, and trend reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include repository metadata, star and fork counts, README-derived feature summaries, trend comparisons, and weekly or monthly recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
