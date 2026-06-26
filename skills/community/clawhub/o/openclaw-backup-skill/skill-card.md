## Description: <br>
Run and schedule local OpenClaw backup operations with a bundled Bash script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[synbraino](https://clawhub.ai/user/synbraino) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create manual or regular local OpenClaw backups, schedule recurring backup runs, prune retained archives, and inspect retention behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backup archives may contain sensitive workspace context, identity files, OpenClaw configuration, and cron details. <br>
Mitigation: Store backups in a private location with restricted permissions and consider encryption before scheduling recurring runs. <br>
Risk: Recurring backup jobs can repeatedly collect broad local state into archives. <br>
Mitigation: Review exclusions and the output directory before installing or changing scheduled jobs. <br>


## Reference(s): <br>
- [OpenClaw Backup Skill Public Spec](references/spec.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to run the bundled Bash script, which creates or prunes local backup archive files.] <br>

## Skill Version(s): <br>
0.2.2 (source: release evidence and bundled script) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
