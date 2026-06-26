## Description: <br>
Git workflow assistant. Generates commit messages, PR descriptions, branch management suggestions, and automates common Git operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michealxie001](https://clawhub.ai/user/michealxie001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate Conventional Commit-style messages, draft pull request descriptions, inspect branch state, and receive Git workflow guidance for local repositories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated commit, rebase, merge, push, and branch-cleanup guidance can affect repository history or working tree state if followed without review. <br>
Mitigation: Review git status, diffs, and each proposed command before applying changes, especially before commit, push, rebase, merge, or cleanup operations. <br>
Risk: Commit messages, filenames, and branch names from untrusted repositories are displayed directly in terminal output. <br>
Mitigation: Use the skill in repositories you trust, and inspect displayed repository metadata before copying it into commits, pull requests, or automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/michealxie001/openclaw-gitflow) <br>
- [Conventional Commits](https://www.conventionalcommits.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text with inline Git commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are derived from local Git repository state and staged changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
