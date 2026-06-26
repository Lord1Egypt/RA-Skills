## Description: <br>
Interact with GitHub using the `gh` CLI. Use `gh issue`, `gh pr`, `gh run`, and `gh api` for issues, PRs, CI runs, and advanced queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lovefromio](https://clawhub.ai/user/lovefromio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to guide GitHub work through the `gh` CLI, including issues, pull requests, CI runs, and advanced API queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act through the user's existing GitHub CLI authentication and permissions. <br>
Mitigation: Use a least-privilege GitHub token for private repositories or organization accounts. <br>
Risk: GitHub CLI write or API actions may affect issues, pull requests, CI runs, or repository state. <br>
Mitigation: Review proposed `gh` commands before allowing write operations or advanced API actions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lovefromio/lovefromio-github) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown] <br>
**Output Format:** [Markdown guidance with inline bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include GitHub CLI commands and structured `gh --json` or `gh api --jq` query examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
