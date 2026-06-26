## Description: <br>
Inspect and maintain a Mac through repeatable terminal-first checks for disk usage, large files, launch agents, login items, power settings, sleep/wake behavior, networking, and OpenClaw health. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[benboby](https://clawhub.ai/user/benboby) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and Mac users use this skill to inspect storage, background processes, power settings, networking, and OpenClaw health before choosing small, reversible maintenance actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Maintenance actions can affect files, startup behavior, power settings, installed software, or security configuration if executed without review. <br>
Mitigation: Start with read-only inspection and require confirmation before deletions, startup item changes, power-setting changes, software installs or removals, and firewall, SSH, or other security changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/benboby/mac-maintenance) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise maintenance summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Groups findings into checked items, findings, recommended actions, and next steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
