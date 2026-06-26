## Description: <br>
Creates and manages autonomous AI agents with self-contained workspaces, memory files, OpenClaw gateway configuration, and Discord channel bindings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[godferylindsay](https://clawhub.ai/user/godferylindsay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create specialized OpenClaw agents, bind them to Discord channels, and manage channel configuration for multi-agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make persistent Discord, OpenClaw gateway, cron, and workspace-file changes. <br>
Mitigation: Run first against a test guild and test gateway, keep affected workspaces under version control, and review generated config patches before applying them. <br>
Risk: Discord and gateway administration can affect channels, prompts, bindings, and agent access. <br>
Mitigation: Use a least-privilege Discord bot and avoid workspace rewrites or cron setup until target paths and schedules have been reviewed. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/godferylindsay/godfery-agent-council) <br>
- [Complete setup guide](https://skillboss.co/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration patches, and generated workspace files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce persistent OpenClaw gateway changes, Discord channel changes, workspace files, and optional cron jobs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
