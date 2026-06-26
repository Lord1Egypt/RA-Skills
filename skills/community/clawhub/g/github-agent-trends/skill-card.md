## Description: <br>
Generate GitHub agent-trending project reports as formatted markdown leaderboards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mike47512](https://clawhub.ai/user/mike47512) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical users use this skill to generate daily, weekly, or monthly leaderboards of agent-related GitHub repositories for market scanning, project discovery, and comparison. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts GitHub and may use an optional GitHub token for higher rate limits. <br>
Mitigation: Invoke it intentionally and use a low-privilege GitHub token only when rate limits require authentication. <br>
Risk: The leaderboard reflects GitHub search relevance and star count, not the official GitHub Trending page. <br>
Mitigation: Treat results as a discovery signal and verify important repository choices against GitHub before acting on them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mike47512/github-agent-trends) <br>
- [GitHub Search repositories API endpoint](https://api.github.com/search/repositories) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON] <br>
**Output Format:** [Markdown leaderboard or JSON array] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses daily, weekly, or monthly activity windows; results are deduplicated and sorted by star count.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
