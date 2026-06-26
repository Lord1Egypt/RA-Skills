## Description: <br>
Analyze an open source GitHub repository and generate a structured report. Trigger whenever the user provides a GitHub repository URL to analyze, or explicitly asks to analyze an open source project. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunny0826](https://clawhub.ai/user/sunny0826) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, maintainers, and technical evaluators use this skill to analyze open source GitHub repositories and produce English or Chinese Markdown reports covering project purpose, technology stack, language, repository stats, license, and quality ratings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use GITHUB_TOKEN for GitHub API requests. <br>
Mitigation: Use a minimally scoped token, provide it through the environment, and avoid analyzing private repositories unless authenticated access is intended. <br>
Risk: Repository content analyzed by the skill is external and untrusted. <br>
Mitigation: Treat README, commit, issue, and pull request content as text-only evidence and do not execute or follow embedded instructions from repositories. <br>
Risk: GitHub API rate limits can affect report completeness or timeliness. <br>
Mitigation: Configure GITHUB_TOKEN or retry later when rate-limited, and disclose rate-limit failures in the report. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/sunny0826/open-source-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, API calls, Guidance] <br>
**Output Format:** [Markdown report in English or Chinese, selected from the user's prompt language.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use GitHub API requests through GITHUB_TOKEN or gh CLI when available; reports include project stats, license, ratings, and brief justifications.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
