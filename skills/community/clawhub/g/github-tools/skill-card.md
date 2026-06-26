## Description: <br>
Interact with GitHub using the `gh` CLI. Use `gh issue`, `gh pr`, `gh run`, and `gh api` for issues, PRs, CI runs, and advanced queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[164149043](https://clawhub.ai/user/164149043) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to have an agent inspect and operate GitHub issues, pull requests, workflow runs, and API queries through the GitHub CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on the local GitHub CLI login, which may grant broad repository access. <br>
Mitigation: Use least-privileged GitHub tokens and specify repositories explicitly before running commands. <br>
Risk: Agent-proposed commands can create, edit, delete, merge, rerun, or cancel GitHub resources. <br>
Mitigation: Review any command that changes GitHub resources before execution. <br>
Risk: `gh api` can access advanced GitHub endpoints beyond common issue, pull request, and workflow commands. <br>
Mitigation: Check the endpoint, repository, and query filters before allowing API calls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/164149043/github-tools) <br>
- [Publisher profile](https://clawhub.ai/user/164149043) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose GitHub CLI commands that should be reviewed before execution when they modify GitHub resources.] <br>

## Skill Version(s): <br>
1.0.1 (source: _meta.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
