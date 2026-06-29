## Description: <br>
Interact with GitHub using the `gh` CLI for issues, pull requests, CI runs, workflow runs, and advanced GitHub API queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[khurramjamil12](https://clawhub.ai/user/khurramjamil12) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to guide agent interactions with GitHub through the GitHub CLI, including reviewing pull request checks, inspecting workflow runs, querying GitHub APIs, and producing structured command output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to use the user's existing GitHub CLI authentication, so requested write operations may change GitHub data within the active `gh` permission scope. <br>
Mitigation: Review the repositories and permissions available to `gh` before installation, and confirm any agent-suggested write operation before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/khurramjamil12/github-1) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with inline bash commands and GitHub CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include GitHub CLI commands that read or change GitHub data depending on the user's request and the active `gh` authentication scope.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
