## Description: <br>
Searches and analyzes GitHub repositories by keyword, language, stars, update recency, and repository details for technical research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linshengli](https://clawhub.ai/user/linshengli) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and technical analysts use this skill to find, filter, compare, and summarize GitHub repositories in a technology domain. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted inputs could cause the included scripts to run unintended local shell commands. <br>
Mitigation: Review or patch the scripts before installing, avoid untrusted repository names, and prefer safer request handling or strict allowlists for command arguments. <br>
Risk: A GitHub token may be exposed or over-privileged if configured broadly. <br>
Mitigation: Use GITHUB_TOKEN only when needed and set it to a fine-grained read-only token. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linshengli/github-search) <br>
- [GitHub Search API](https://api.github.com/search/repositories) <br>
- [GitHub Repository API](https://api.github.com/repos) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, CSV, shell commands, guidance] <br>
**Output Format:** [Markdown tables and reports, with optional JSON or CSV command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use GITHUB_TOKEN for higher GitHub API rate limits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
