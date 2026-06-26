## Description: <br>
Interact with GitHub using Personal Access Tokens for repository listing, cloning, branching, pushing, pull requests, issues, and repository information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dannyshmueli](https://clawhub.ai/user/dannyshmueli) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to perform GitHub repository operations with a user-provided Personal Access Token instead of OAuth-based account authorization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A GitHub Personal Access Token can grant broad repository read or write access within its scopes. <br>
Mitigation: Use a fine-grained, short-lived token limited to the specific repository and revoke it when the task is complete. <br>
Risk: Persisting the token in TOOLS.md can expose a high-value credential to future agent sessions or workspace readers. <br>
Mitigation: Prefer passing the token at runtime or through a temporary environment variable, and avoid storing it in durable workspace files. <br>
Risk: The push workflow can stage and publish all local changes without an explicit diff review step. <br>
Mitigation: Manually review git status and diffs before allowing commit or push operations. <br>


## Reference(s): <br>
- [ClawHub GitHub Token skill page](https://clawhub.ai/dannyshmueli/github-token) <br>
- [GitHub Personal Access Tokens](https://github.com/settings/tokens) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke GitHub API requests and git commands using a user-provided token.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
