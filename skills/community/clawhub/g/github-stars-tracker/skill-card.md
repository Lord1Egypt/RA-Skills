## Description: <br>
Tracks GitHub repository stars, forks, and watchers so developers can monitor project activity and changes over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SxLiuYu](https://clawhub.ai/user/SxLiuYu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to track GitHub repository popularity signals, list tracked repositories, check current status, and identify changes in stars and forks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI can send a GitHub token with API requests. <br>
Mitigation: Use no token for public repositories when rate limits are acceptable, or use a fine-grained read-only token with the narrowest practical scope. <br>
Risk: The CLI stores repository tracking state in a local JSON file in the user's home directory. <br>
Mitigation: Review the local state file before sharing the environment, and remove it when the tracked repository list should no longer persist. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/SxLiuYu/github-stars-tracker) <br>
- [GitHub token settings](https://github.com/settings/tokens) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces command examples and operating guidance for a Python CLI that calls the GitHub API and stores local tracking state.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
