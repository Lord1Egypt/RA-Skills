## Description: <br>
Execute common Git operations: status, commit, push, pull, branch management, PR creation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liyico](https://clawhub.ai/user/liyico) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect repository state and run common Git workflows such as status, commit, push, pull, branching, checkout, merge, stash, log, and diff from an agent session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform high-impact repository operations such as commit, push, pull, branch changes, merge, stash, and diff from agent requests. <br>
Mitigation: Require dry-run output before repository-changing actions and review the exact files staged, target branch, remote, and commit message before allowing commit or push. <br>
Risk: The release security guidance notes a missing helper script that must be trusted, inspected, or replaced before use. <br>
Mitigation: Install only from a trusted publisher and inspect or replace the helper script before enabling the skill in an agent environment. <br>
Risk: Broad natural-language requests could trigger automatic commit or push behavior that includes unintended changes. <br>
Mitigation: Use explicit file lists and operation parameters, keep protected-branch safeguards enabled, and avoid automatic commit or push from broad requests. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/liyico/git-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [JSON result objects with raw Git output and operation metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include success status, error text, changed files, commit SHA, current branch, and raw Git command output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
