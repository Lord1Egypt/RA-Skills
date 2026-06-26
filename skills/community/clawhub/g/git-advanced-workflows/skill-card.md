## Description: <br>
Master advanced Git workflows including rebasing, cherry-picking, bisect, worktrees, and reflog to maintain clean history and recover from any situation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[soponcd](https://clawhub.ai/user/soponcd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to manage complex Git history, prepare clean pull requests, apply selected commits, locate regressions, work across branches, and recover from Git mistakes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: History-editing commands can rewrite or discard local work when used on the wrong branch or commit. <br>
Mitigation: Verify the repository, branch, and remote before applying commands; create a backup branch before risky history edits; use --force-with-lease instead of force pushing blindly. <br>
Risk: Automated bisect examples can run repository scripts that may have side effects. <br>
Mitigation: Inspect repository scripts and confirm the test command is appropriate before using automated bisect. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/soponcd/git-advanced-workflows) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output; review commands before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
