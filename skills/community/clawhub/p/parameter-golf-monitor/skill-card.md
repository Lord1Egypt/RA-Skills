## Description: <br>
Monitor the openai/parameter-golf competition leaderboard by fetching pull request data from GitHub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dexhunter](https://clawhub.ai/user/dexhunter) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers, competition participants, and agents use this skill to check Parameter Golf leaderboard standings, compare scores, highlight a GitHub user's submissions, and monitor open or merged pull requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the monitor makes outbound requests to GitHub's public API. <br>
Mitigation: Use it only in environments where GitHub API access is acceptable. <br>
Risk: The watch mode continuously polls GitHub until stopped and can consume the unauthenticated API rate limit. <br>
Mitigation: Use --watch only when continuous monitoring is needed, choose an appropriate interval, and stop it when monitoring is complete. <br>


## Reference(s): <br>
- [openai/parameter-golf repository](https://github.com/openai/parameter-golf) <br>
- [Claude Code skills](https://github.com/anthropics/skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Terminal leaderboard table or JSON, with concise Markdown guidance from the agent] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can filter by user, top N entries, record status, merged pull requests, date, and polling interval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
