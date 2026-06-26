## Description: <br>
Memory Workflow helps agents maintain continuity by loading session memory, creating daily summaries, and prompting for real-time updates to long-term memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rocky2046](https://clawhub.ai/user/rocky2046) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to add local assistant memory workflows, including session memory loading, daily note generation, and weekly memory review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates broad local persistence for assistant memory, which can retain sensitive personal or operational details. <br>
Mitigation: Avoid storing secrets or sensitive account, health, or financial details; keep long-term memory concise and review retained notes regularly. <br>
Risk: The skill installs recurring cron automation that writes local files. <br>
Mitigation: Review the crontab entry, scripts, and configuration before installation, and install only when ongoing local memory automation is intended. <br>
Risk: Configuration parsing and weekly cleanup behavior could execute unintended shell content or remove notes outside the intended retention policy. <br>
Mitigation: Restrict configuration edits to trusted users, validate configuration values and paths, and back up important memory notes before enabling cleanup. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rocky2046/memory-workflow) <br>
- [Project Homepage](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local memory files, daily note templates, and cron-based summary automation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
