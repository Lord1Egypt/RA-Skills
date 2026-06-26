## Description: <br>
Harness Evolve helps an agent consume research logs, run system self-checks, produce architecture optimization proposals or safe maintenance changes, and write a daily evolution summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dottythehomeless](https://clawhub.ai/user/dottythehomeless) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent maintainers use this skill to turn research backlog and recent system observations into auditable maintenance actions, review proposals, and daily status summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically change and commit project files. <br>
Mitigation: Run it on a branch, define safe_files and config_files explicitly, and review diffs and commits before merging. <br>
Risk: Maintenance proposals may affect runtime agent behavior if applied without review. <br>
Mitigation: Keep runtime configuration changes proposal-only and require human approval before applying them. <br>
Risk: A configured notify_command can run a shell notification command. <br>
Mitigation: Leave notify_command unset unless the command and repository configuration are fully trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dottythehomeless/harness-evolve) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown summaries, review proposals, file edits or commits, and optional shell notification command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May overwrite the daily evolution summary file and create git commits for safe file changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter says 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
