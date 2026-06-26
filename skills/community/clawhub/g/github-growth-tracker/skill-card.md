## Description: <br>
Track GitHub repo growth across stars, forks, issues, commits, and watchlist comparisons with periodic text digests and trend analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[99rebels](https://clawhub.ai/user/99rebels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to monitor GitHub repository growth, compare their projects against a watchlist, and generate recurring status digests for repositories they track. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a GitHub token and can save it locally in plaintext when setup is run with --token. <br>
Mitigation: Use a least-privilege fine-grained GitHub token, prefer the GITHUB_TOKEN environment variable, and set SKILL_DATA_DIR to a directory the user controls. <br>


## Reference(s): <br>
- [GitHub Growth Tracker homepage](https://github.com/99rebels/github-growth-tracker) <br>
- [Channel Formatting](references/formatting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or channel-formatted Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces repository metric digests, trend indicators, watchlist comparisons, and setup or tracking commands.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
