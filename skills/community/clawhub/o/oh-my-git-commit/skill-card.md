## Description:

Oh My Git Commit helps agents analyze repository diffs, group staged changes, generate Chinese Conventional Commit messages, and run git commit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hoi-lau](https://clawhub.ai/user/hoi-lau)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill when they want an agent to inspect git diffs, prepare logically grouped staging, and generate or run a Conventional Commit with a clear Chinese message.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad commit-related triggers and command execution can cause unintended repository changes.

Mitigation: Require the agent to show git status, the exact files to stage, and the final commit message before staging or committing.

Risk: A commit workflow can accidentally include secrets or unrelated files if the staged path list is not reviewed.

Mitigation: Review proposed staged files and exclude credentials, private keys, .env files, and unrelated changes before allowing git add or git commit.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hoi-lau/skills/oh-my-git-commit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with git command snippets and Conventional Commit message text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose staged file groups and a final commit message; execution can change repository state when approved.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
