## Description: <br>
Interact with GitHub using the `gh` CLI. Use `gh issue`, `gh pr`, `gh run`, and `gh api` for issues, PRs, CI runs, and advanced queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nidhov01](https://clawhub.ai/user/nidhov01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to ask an agent for GitHub CLI command guidance for issues, pull requests, CI runs, and GitHub API queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated GitHub CLI guidance can act with the user's authenticated GitHub permissions if the user executes it. <br>
Mitigation: Confirm the authenticated `gh` account, target repository, and intended side effects before running write, merge, comment, workflow, secret, or broad `gh api` commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nidhov01/nidhov01-github) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands should be reviewed before execution, especially for write-capable GitHub operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
