## Description: <br>
OpenClaw Cleaner helps an agent inspect, snapshot, diff, checkpoint, back up, restore, and optimize an OpenClaw workspace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[computersniper](https://clawhub.ai/user/computersniper) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users can use this skill to let an agent manage workspace housekeeping tasks such as snapshots, diffs, checkpoints, backups, health checks, and optimization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and copy broad workspace contents into .cleaner-backups, which may include private code, prompts, or secrets. <br>
Mitigation: Use it first on non-sensitive projects and inspect or delete generated backups after use. <br>
Risk: The skill can change and restore OpenClaw state files without confirmation. <br>
Mitigation: Require manual review before optimize or restore actions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/computersniper/openclaw-cleaner) <br>
- [Publisher profile](https://clawhub.ai/user/computersniper) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and structured JavaScript return objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create workspace backup, snapshot, checkpoint, and progress files under .cleaner-backups when used by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 2.1.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
