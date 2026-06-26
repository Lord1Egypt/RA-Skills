## Description: <br>
每日 GitHub Trending 热榜推送，支持日榜和月度汇总 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lxiaodong681-lab](https://clawhub.ai/user/lxiaodong681-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to fetch GitHub Trending repositories and receive concise Chinese Markdown summaries for daily or monthly review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes live requests to GitHub and may be affected by network failures, rate limits, or changes to GitHub Trending page structure. <br>
Mitigation: Use the built-in cache fallback when available and review output freshness before relying on summaries. <br>
Risk: Fetched repository descriptions are public web content and may contain misleading or instruction-like text. <br>
Mitigation: Treat fetched repository descriptions as untrusted content and do not follow instructions embedded in summaries. <br>


## Reference(s): <br>
- [ClawHub GitHub Trending Skill](https://clawhub.ai/lxiaodong681-lab/github-trending-skill) <br>
- [GitHub Trending](https://github.com/trending) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Chinese Markdown summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Daily or monthly repository rankings with repository name, description, language, total stars, and period growth.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
