## Description: <br>
Analyzes installed skills and commands for functional overlap, reports likely duplication, and guides cleanup decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexxxiong](https://clawhub.ai/user/alexxxiong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to scan installed Claude Code skills and commands, identify possible functional duplication, review status, and decide which entries to keep or disable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Resolve workflows can change local agent or plugin configuration after user confirmation. <br>
Mitigation: Review proposed actions carefully, back up local agent configuration, prefer supported disable or uninstall commands, and use dry-run or undo paths where available. <br>
Risk: Overlap findings are heuristic and may incorrectly classify skills as redundant. <br>
Mitigation: Treat scan results as decision support, use deeper comparison for high-overlap groups, and manually review unique capabilities before disabling anything. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/alexxxiong/inspirai-audit) <br>
- [Publisher profile](https://clawhub.ai/user/alexxxiong) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and terminal-style reports with inline shell commands and JSON cache examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write an audit cache and may move command files during confirmed resolve workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
