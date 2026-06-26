## Description: <br>
Use this skill to batch-sync Git repositories across machines by pushing end-of-day changes or pulling latest updates at start of day. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[niracler](https://clawhub.ai/user/niracler) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Code Sync to scan a configured code directory, categorize local Git repositories, batch push clean repositories that are ahead of upstream, batch pull clean repositories that are behind upstream, and handle dirty or divergent repositories interactively. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically push or pull many repositories under the configured code directory. <br>
Mitigation: Keep the configured base directory narrow, review repository remotes first, and ask for a scan or preview before invoking push mode when bulk publishing would be risky. <br>
Risk: Remote URLs may expose sensitive credentials if they are embedded directly in repository configuration. <br>
Mitigation: Review repository remotes and avoid storing secrets in remote URLs before using the skill across a directory tree. <br>


## Reference(s): <br>
- [ClawHub Code Sync skill page](https://clawhub.ai/niracler/nini-code-sync) <br>
- [Publisher profile: niracler](https://clawhub.ai/user/niracler) <br>
- [Release v0.3.0 changelog](https://github.com/niracler/skill/releases/tag/v0.3.0) <br>
- [Git documentation](https://git-scm.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON scan output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce repository status summaries, configuration instructions, and interactive prompts for dirty, divergent, or no-upstream repositories.] <br>

## Skill Version(s): <br>
0.3.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
