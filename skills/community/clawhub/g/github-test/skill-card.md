## Description: <br>
Interact with GitHub using the `gh` CLI for issues, pull requests, workflow runs, and advanced API queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yqghlx](https://clawhub.ai/user/yqghlx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to ask an agent for GitHub CLI commands and guidance for checking pull request status, inspecting workflow runs, querying GitHub data, and formatting JSON output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GitHub CLI commands may run against the wrong account or repository if authentication or context is unclear. <br>
Mitigation: Confirm `gh` is authenticated to the intended GitHub account and specify `--repo owner/repo` when repository context is not explicit. <br>
Risk: Commands that comment, close, merge, rerun, cancel, delete, or use write-capable `gh api` requests can modify GitHub resources. <br>
Mitigation: Review write-capable commands before execution and use appropriately scoped GitHub tokens. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the user's existing GitHub CLI authentication and repository context.] <br>

## Skill Version(s): <br>
0.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
