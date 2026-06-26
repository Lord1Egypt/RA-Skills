## Description: <br>
Runs an OpenClaw autonomous research loop that iteratively modifies files, executes a verification command, commits passing changes, and discards failing changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run repeated code-change attempts against a chosen verification command, keeping successful iterations and rolling back failed ones. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The loop can run arbitrary shell commands through the task and verification command. <br>
Mitigation: Review CLAUDE_TASK and the verification command before execution, and run only in a disposable worktree with no secrets or important local-only files. <br>
Risk: Failed iterations may reset and clean repository files, including untracked work. <br>
Mitigation: Start from a clean branch or worktree, preserve any needed changes elsewhere, and disable rollback behavior if file deletion is not acceptable. <br>
Risk: Successful iterations can create commits automatically. <br>
Mitigation: Review generated commits and diffs before publishing, merging, or using the output in a production workflow. <br>


## Reference(s): <br>
- [Karpathy Autoresearch Reference Implementation](https://github.com/uditgoenka/autoresearch) <br>
- [ClawHub Skill Page](https://clawhub.ai/zhaobod1/huo15-autoresearch-loop) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown or terminal text with shell command invocations and JSON state updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains local loop state and logs under ~/.openclaw/tmp when executed.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter is 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
