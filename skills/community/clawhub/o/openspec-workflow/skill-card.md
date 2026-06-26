## Description: <br>
Guides agents through an OpenSpec-based development lifecycle using OpenSpec CLI, Claude Code, GitHub CLI, and git to draft artifacts, review them, implement tasks, ship pull requests, and support auto-archiving after merge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BobbyRadford](https://clawhub.ai/user/BobbyRadford) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering agents use this skill to run an OpenSpec-centered change lifecycle: create and review spec artifacts, delegate implementation, prepare pull requests, and optionally configure auto-archiving after merge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sub-agents may be launched with broad automatic authority and permission prompts bypassed. <br>
Mitigation: Review the skill before installation, remove skip-permissions flags where possible, and require explicit approval for long-running review or implementation agents. <br>
Risk: The workflow can modify files, create commits, push branches, open pull requests, and delete merged branches. <br>
Mitigation: Run it only in a disposable or well-backed-up repository unless those repository actions are intended and approved. <br>
Risk: The bundled auto-archive workflow uses repository write and pull-request permissions. <br>
Mitigation: Review the workflow YAML and permission scope before adding it to a repository. <br>


## Reference(s): <br>
- [OpenSpec Auto-Archive on Merge](references/archive-action.md) <br>
- [Review Loop Protocol](references/review-loop.md) <br>
- [ClawHub skill page](https://clawhub.ai/BobbyRadford/openspec-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to create OpenSpec artifacts, workflow YAML, commits, pull requests, and issue comments when authorized.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
