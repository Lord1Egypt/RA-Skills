## Description: <br>
Generate GitHub AI trending project reports as formatted text leaderboards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[toller892](https://clawhub.ai/user/toller892) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and AI practitioners use this skill to fetch and summarize public GitHub AI, ML, and LLM repository trends as a chat-ready leaderboard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional GitHub token use could expose a credential if the token is pasted into chat, command examples, logs, or shell history. <br>
Mitigation: Use an environment variable or secret manager, prefer a least-privilege token, and avoid including tokens in visible prompts or command output. <br>
Risk: Trend results are fetched live from public GitHub search data and may be incomplete, rate-limited, or change over time. <br>
Mitigation: Treat the generated leaderboard as a point-in-time discovery aid and verify important repositories directly on GitHub before acting on the results. <br>


## Reference(s): <br>
- [GitHub AI Trends ClawHub page](https://clawhub.ai/toller892/github-ai-trends) <br>
- [toller892 ClawHub publisher profile](https://clawhub.ai/user/toller892) <br>
- [GitHub Search Repositories API](https://docs.github.com/en/rest/search/search?apiVersion=2022-11-28#search-repositories) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, JSON, API Calls] <br>
**Output Format:** [Markdown leaderboard by default, with optional JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts daily, weekly, or monthly periods; supports configurable result limits and optional GitHub token use for higher rate limits.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
