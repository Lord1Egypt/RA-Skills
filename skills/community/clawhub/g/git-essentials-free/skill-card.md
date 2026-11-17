## Description: <br>
Git基础版 helps agents guide common Git operations, basic branch management, conventional commits, conflict handling, and remote repository workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and small teams use this skill to have an agent propose and explain routine Git commands for commits, branch operations, history review, conflict triage, and remote synchronization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may propose commands that change repository state, including commits, branch changes, merges, pulls, or pushes. <br>
Mitigation: Review each generated Git command before execution, especially in repositories with remote access or stored credentials. <br>
Risk: Conflict guidance is basic and may not resolve complex merge situations automatically. <br>
Mitigation: Use the skill to identify conflict files and markers, then have a developer review and resolve the conflicting changes before committing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/git-essentials-free) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Markdown, JSON] <br>
**Output Format:** [Markdown guidance with Git command examples and optional JSON status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose repository-changing Git commands; users should review commands before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
