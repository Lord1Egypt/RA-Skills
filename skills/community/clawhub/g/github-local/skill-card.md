## Description: <br>
Interact with GitHub using the `gh` CLI. Use `gh issue`, `gh pr`, `gh run`, and `gh api` for issues, PRs, CI runs, and advanced queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[morrison230](https://clawhub.ai/user/morrison230) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to have an agent propose GitHub CLI commands for issues, pull requests, workflow runs, and GitHub API queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may lead an agent to propose GitHub CLI commands that change repository or account state. <br>
Mitigation: Require explicit confirmation before running commands that merge, close, comment, rerun, cancel, delete, or otherwise change state. <br>
Risk: Commands run through the local `gh` CLI use the currently authenticated GitHub account and token scopes. <br>
Mitigation: Check the active `gh` account and token scopes before use. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a locally installed and authenticated GitHub CLI for commands to run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
