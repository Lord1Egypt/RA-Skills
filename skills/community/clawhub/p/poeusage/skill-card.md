## Description: <br>
Monitor Poe API point balance and usage history from the terminal using poeusage CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rgstephens](https://clawhub.ai/user/rgstephens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and Poe API users use this skill to check point balances, inspect usage history, and summarize spend from the terminal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and relies on a third-party Homebrew tap and CLI. <br>
Mitigation: Install it only when you trust the poeusage tap and CLI maintainer. <br>
Risk: The skill requires POE_API_KEY, which is an account secret. <br>
Mitigation: Keep the key out of shared files and prefer environment variables over storing it in config. <br>
Risk: The history command can fetch all available usage records by default. <br>
Mitigation: Use limits, date filters, or no-pagination mode when you do not want a full history fetch. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rgstephens/poeusage) <br>
- [Project homepage](https://github.com/rgstephens/poeusage-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell commands and CLI output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The underlying CLI supports table, CSV, JSON, and plain text output modes.] <br>

## Skill Version(s): <br>
0.5.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
