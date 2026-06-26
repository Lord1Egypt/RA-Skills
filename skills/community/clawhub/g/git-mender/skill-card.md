## Description: <br>
git-mender helps an agent fix GitHub issues end to end by reading the issue, analyzing repository code, implementing a fix, verifying it, and preparing a pull request. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[4ydx3906](https://clawhub.ai/user/4ydx3906) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill when they want an agent to handle a GitHub issue workflow: inspect the issue, locate or clone the repository, analyze root cause, apply a minimal code fix, run checks, and prepare changes for review. Pull request submission is gated on explicit user approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify files in a local checkout and prepare commits or pull requests. <br>
Mitigation: Review the diff and approve commit, push, fork, or pull request creation only when the changes match the intended issue fix. <br>
Risk: Tests, linters, and project tooling in an untrusted repository may execute repository code. <br>
Mitigation: Run the skill only on repositories you trust or in an isolated environment when repository code is not trusted. <br>
Risk: GitHub operations use the user's existing GitHub CLI authentication and permissions. <br>
Mitigation: Confirm the target repository, branch, and pull request destination before authorizing any GitHub operation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/4ydx3906/git-mender) <br>
- [Publisher Profile](https://clawhub.ai/user/4ydx3906) <br>
- [GitHub CLI](https://cli.github.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, code diffs, commit messages, and pull request text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify local checkout files and prepare GitHub pull request metadata after user review.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter, changelog, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
