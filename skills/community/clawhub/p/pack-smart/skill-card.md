## Description: <br>
Get a customized packing list based on destination, season, trip type, and activities, with related travel booking support powered by Fliggy through the flyai CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to request packing guidance and related travel options for a destination, season, trip type, or activity. The agent gathers missing trip details, runs flyai CLI searches, and returns user-readable Markdown with booking links when results are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install and run an external npm CLI and send packing or travel queries through that provider workflow. <br>
Mitigation: Use the skill only in an environment where external CLI installation and provider calls are permitted, and review CLI commands before execution. <br>
Risk: The skill may write raw user queries and command details to a local execution log. <br>
Mitigation: Avoid entering sensitive trip details unless local logging is acceptable, and clear or disable the log where policy requires it. <br>
Risk: The skill is oriented around booking-link results. <br>
Mitigation: Treat returned booking links as external travel-provider results and review destination, price, and provider details before acting. <br>


## Reference(s): <br>
- [Pack Smart ClawHub page](https://clawhub.ai/xiejinsong/pack-smart) <br>
- [templates.md](references/templates.md) <br>
- [playbooks.md](references/playbooks.md) <br>
- [fallbacks.md](references/fallbacks.md) <br>
- [runbook.md](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands for failure recovery] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results should be derived from flyai CLI output and include booking links when available; raw JSON should not be shown to users.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
