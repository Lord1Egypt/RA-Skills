## Description: <br>
Fetch GitHub trending repositories by daily, weekly, or monthly periods with output in Markdown or JSON format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiangzhiyu](https://clawhub.ai/user/jiangzhiyu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to check currently trending GitHub repositories by time period and summarize repository names, languages, star counts, descriptions, and links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches and parses GitHub Trending from a live public page, so output can fail or change if the page structure changes, requests are rate limited, or network access is unavailable. <br>
Mitigation: Retry later when rate limited, space out repeated calls, and verify important repository details on GitHub before relying on them. <br>
Risk: The artifact includes a shell command that retrieves remote HTML and processes it locally. <br>
Mitigation: Review the command before execution and run it in a developer environment without unnecessary credentials exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiangzhiyu/github-trending) <br>
- [GitHub Trending](https://github.com/trending) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown table or JSON, depending on invocation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches public GitHub Trending data in real time and does not require authentication.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
