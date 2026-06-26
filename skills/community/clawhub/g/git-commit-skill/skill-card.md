## Description: <br>
This skill helps an agent inspect Git changes, choose an appropriate Gitmoji, run a secrets-oriented review, and prepare a confirmed commit with an optional push. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tedburner](https://clawhub.ai/user/tedburner) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill in Git repositories to summarize working-tree changes, select a Gitmoji commit type, confirm a commit message, stage files, create a commit, and optionally push to the remote branch. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can stage, commit, and push repository changes after confirmation, which may include unrelated or sensitive files if the user approves too broadly. <br>
Mitigation: Review the diff, generated commit message, staged file list, and remote branch before approving actions; stage specific files instead of broad staging when the working tree contains unrelated changes. <br>
Risk: The workflow is written in Chinese, so users who do not read Chinese may misunderstand prompts or confirmations. <br>
Mitigation: Ask the agent to translate prompts and proposed actions before approving any Git operation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tedburner/git-commit-skill) <br>
- [Gitmoji complete reference](references/gitmojis.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style conversational text with Git command proposals and commit message text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation before staging, committing, or pushing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
