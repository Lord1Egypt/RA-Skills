## Description: <br>
Execute git operations on behalf of Workers who don't have git credentials when a Worker sends a git-request message to clone, push, pull, commit, rebase, or perform another git operation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MontyCN](https://clawhub.ai/user/MontyCN) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill when Workers lack git credentials and need a Manager to run delegated git operations in a shared workspace. It supports cloning, branching, committing, pushing, pulling, rebasing, and related git workflows with status reporting back to the requesting Worker. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Worker messages can trigger broad authenticated git actions using the Manager's host git credentials. <br>
Mitigation: Install only where Workers are fully trusted, authenticate the request origin, restrict allowed repositories and git commands, and use least-privilege repo-scoped credentials. <br>
Risk: Pushes, rebases, resets, or other history-changing git operations can alter remote repositories or shared workspaces. <br>
Mitigation: Review pushes and history-changing operations before execution, require explicit approval for destructive commands, and keep workspace synchronization markers in place to avoid concurrent edits. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown status messages with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports success or failure, summarizes completed git operations, and may include follow-up sync or remediation instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
