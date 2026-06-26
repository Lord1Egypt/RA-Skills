## Description: <br>
Use when the user wants a single clean commit created from current changes with safe staging, message drafting, and non-interactive git usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wimi321](https://clawhub.ai/user/wimi321) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to have an agent inspect repository changes, stage only relevant files, draft a concise commit message, and create one non-amended git commit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may commit from the wrong repository or include unintended local changes. <br>
Mitigation: Run the skill only in the intended repository and review the diff, staged files, and commit message when possible. <br>
Risk: Repositories can contain secrets or unrelated local changes that should not be committed. <br>
Mitigation: Confirm staged files before commit, especially in repositories that may contain secrets or unrelated work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wimi321/git-commit-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown status updates with git command execution and commit summary text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces one non-amended commit when the repository has relevant changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
