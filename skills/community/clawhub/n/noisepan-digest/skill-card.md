## Description: <br>
Set up automated news digests using noisepan for signal extraction, entropia for source verification, and Hacker News blind spot detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ppiankov](https://clawhub.ai/user/ppiankov) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure automated daily news briefs, curate RSS feeds, score noisy sources, verify selected links, and schedule digest generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to install and run third-party noisepan and entropia binaries. <br>
Mitigation: Use Homebrew or a user-local bin directory where possible, verify release checksums, and run version or doctor commands before using the tools. <br>
Risk: The skill includes helper scripts and scheduled jobs that fetch external feeds and execute local commands. <br>
Mitigation: Review generated scripts before enabling cron jobs, keep the schedule explicit, and limit writes to user-owned configuration and cache paths. <br>
Risk: The Reddit prefetch wrapper starts a temporary HTTP server for cached RSS content. <br>
Mitigation: Bind the temporary server to 127.0.0.1 when using the wrapper and stop the process after the pull completes. <br>


## Reference(s): <br>
- [Noisepan Digest on ClawHub](https://clawhub.ai/ppiankov/noisepan-digest) <br>
- [Noisepan project](https://github.com/ppiankov/noisepan) <br>
- [Entropia project](https://github.com/ppiankov/entropia) <br>
- [Agent-Native CLI Convention](https://ancc.dev) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, YAML configuration examples, cron setup steps, and digest table templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup instructions for noisepan, entropia, RSS feed configuration, optional helper scripts, and scheduled digest prompts.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
