## Description: <br>
Professional SOP with Machine-Gated Planning, Native-CLI Config, and Audit-Hardened Private Sandbox Storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chyern](https://clawhub.ai/user/chyern) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to structure multi-step work with planning gates, task tracking, approval records, configurable sub-agent use, and optional context snapshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist sensitive task context when snapshots are enabled. <br>
Mitigation: Keep snapshots disabled unless the local runtime isolation and logging behavior are understood and acceptable. <br>
Risk: The snapshot clear command may report success while leaving saved context on disk. <br>
Mitigation: Do not rely on the clear command to remove sensitive saved context; manually inspect and remove stored snapshot files when handling sensitive work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chyern/multi-step-workflow) <br>
- [Publisher profile](https://clawhub.ai/user/chyern) <br>
- [Agent-Skills repository](https://github.com/chyern/Agent-Skills) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text, markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local JSON state files for approvals, task progress, and optional context snapshots.] <br>

## Skill Version(s): <br>
4.4.5 (source: server release metadata, SKILL.md frontmatter, manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
