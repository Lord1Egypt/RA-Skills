## Description: <br>
Automatic task memory and keep-alive loop for Obsidian-backed agents. Every task gets persistent notes. Arm the loop for long tasks, disarm when done. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[techieter](https://clawhub.ai/user/techieter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to keep Obsidian-backed task notes current and to run optional scheduled recovery checks for long-running agent work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring OpenClaw jobs can continue running after installation and may consume resources if they are not wanted. <br>
Mitigation: Install only when automatic task notes and recurring jobs are desired, keep the loop disarmed unless needed, and remove the five cron jobs when uninstalling. <br>
Risk: Persistent task notes may retain sensitive task context if users place secrets or confidential material in the Obsidian task folder. <br>
Mitigation: Use a dedicated Obsidian vault or Tasks folder and avoid putting secrets in task notes. <br>
Risk: The installer writes skill files, vault templates, and scheduled job configuration. <br>
Mitigation: Review the install steps before execution and remove retained vault notes during uninstall if they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/techieter/memory-keep-alive-for-obsidian) <br>
- [Publisher profile](https://clawhub.ai/user/techieter) <br>
- [README](artifact/README.md) <br>
- [Install guide](artifact/INSTALL.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown task notes, short status text, shell commands, and cron/job configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates Obsidian vault notes under Tasks/ and configures five scheduled OpenClaw jobs when installed.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
