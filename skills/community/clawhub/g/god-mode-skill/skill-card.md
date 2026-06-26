## Description: <br>
God's eye view of your dev repos. Multi-project tracking across GitHub/Azure DevOps. AI learns from your commits to upgrade your agents.md. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wetzja04-dot](https://clawhub.ai/user/wetzja04-dot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and teams use this skill to monitor activity across multiple repositories, review commits, pull requests, and issues, and receive guidance for improving agent instruction files from observed work patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access private repository metadata and source-adjacent context through authenticated GitHub or Azure tooling. <br>
Mitigation: Use only with repositories you are authorized to analyze and prefer least-privilege credentials. <br>
Risk: Agent instruction content and commit context may be sent to configured LLM providers during analysis. <br>
Mitigation: Review provider configuration before running analysis and avoid submitting sensitive repository content to providers that are not approved for that data. <br>
Risk: Repository activity, analysis results, and logs are cached locally under ~/.god-mode. <br>
Mitigation: Purge ~/.god-mode when cached data is no longer needed or should not remain on the machine. <br>
Risk: The skill can propose and apply updates to AGENTS.md files. <br>
Mitigation: Review the exact diff before accepting any AGENTS.md update. <br>
Risk: The documented curl-to-bash install path executes remote shell content. <br>
Mitigation: Inspect and pin the install script before using that path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wetzja04-dot/god-mode-skill) <br>
- [README](README.md) <br>
- [Configuration example](config.example.yaml) <br>
- [Testing guide](TESTING.md) <br>
- [Monthly review cron example](examples/monthly-review-cron.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text, Markdown summaries, JSON command output, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read repository metadata, cache local activity data, and propose or apply AGENTS.md changes after user review.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
