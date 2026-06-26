## Description: <br>
Run Hive's folder-based coding-agent pipeline from OpenClaw: guided CLI setup, project init, task creation, plan/develop/review workflows, status, daemon, and guarded admin commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivankuznetsov](https://clawhub.ai/user/ivankuznetsov) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install and operate the Hive CLI from OpenClaw, initialize repositories, create tasks, move work through plan/develop/review stages, inspect status, and manage daemon or administrative workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide installation of a third-party CLI and enable a per-user background daemon. <br>
Mitigation: Confirm that the user trusts the third-party Hive CLI source before installing, and clearly state that setup enables a per-user daemon. <br>
Risk: Some Hive administrative commands can remove worktrees, stop automation, clear recovery markers, alter registry state, or rewrite installed software. <br>
Mitigation: Restate the effect and obtain explicit user confirmation before uninstall, drop, prune, force, marker-clearing, foreground daemon, or similar administrative actions. <br>


## Reference(s): <br>
- [Hive project homepage](https://github.com/ivankuznetsov/hive) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and command-output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request explicit confirmation before installers, daemon foreground processes, destructive admin actions, or force/bypass commands.] <br>

## Skill Version(s): <br>
0.1.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
