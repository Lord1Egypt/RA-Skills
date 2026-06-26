## Description: <br>
Smart git commit workflow that checks remote state, inspects repository changes, decides between a new commit and a strict amend, generates conventional commit messages, and optionally pushes when requested. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hugogu](https://clawhub.ai/user/hugogu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to prepare Git commits with remote sync, conflict handling, staged diff inspection, conventional commit messaging, and optional push behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic rebase before committing can change local repository state and may encounter conflicts. <br>
Mitigation: Ask the agent to show `git status` and confirm before rebasing; if conflicts occur, abort the workflow and resolve them manually before retrying. <br>
Risk: Broad staging can include unrelated files or sensitive material. <br>
Mitigation: Review staged and unstaged diffs before commit, and exclude `.env`, key, certificate, credential, and unrelated files. <br>
Risk: Amending or pushing can rewrite or publish repository history. <br>
Mitigation: Confirm before amending or pushing, verify whether the prior commit is already published, and do not force-push protected branches. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hugogu/proper-git-commit) <br>
- [Publisher profile](https://clawhub.ai/user/hugogu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and commit message text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create persistent Git repository changes when the agent executes the suggested workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
