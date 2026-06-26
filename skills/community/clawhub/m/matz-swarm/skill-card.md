## Description: <br>
Orchestrates OpenClaw Agent Swarm workflows for multi-project coding automation, covering Obsidian task intake, Claude coding, Codex review, GitLab merge request flow, merge and sync, and done-status closure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Matzoh](https://clawhub.ai/user/Matzoh) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering teams use this skill to operate autonomous, multi-project coding workflows that turn Obsidian or chat tasks into worktree-based agent sessions, reviewed changes, merge request or pull request notifications, and merge or sync actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent autonomous repository automation can run background agents and push, merge, sync, or delete repository data with limited confirmation. <br>
Mitigation: Use a dedicated machine, container, or OS user; scope git and provider credentials to test or low-risk repositories; and keep protected branches, required reviews, and CI checks enforced server-side. <br>
Risk: The skill supports coding and review agent execution modes that bypass normal safety prompts. <br>
Mitigation: Avoid disabling safety prompts unless that risk is accepted, monitor task logs and tmux sessions, and require explicit confirmation or dry-run gates before push, merge, cleanup, and note-triggered execution. <br>
Risk: Obsidian note scanning and cron jobs can trigger task execution from local files marked ready. <br>
Mitigation: Limit the scanned Obsidian directory, keep unapproved work in draft or stopped states, and disable the scan cron job for repositories where note-triggered automation is not intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Matzoh/matz-swarm) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and operational status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May launch local scripts that create worktrees, run coding and review agents, create merge requests or pull requests, send notifications, merge changes, sync branches, and clean old task data.] <br>

## Skill Version(s): <br>
1.1.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
