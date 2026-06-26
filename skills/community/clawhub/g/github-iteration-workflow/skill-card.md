## Description: <br>
Automates an end-to-end GitHub issue workflow for listing and analyzing open issues, planning grouped fixes, creating branches and commits, opening pull requests, monitoring CI/CD, merging, and reporting deployment status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gdyshi](https://clawhub.ai/user/gdyshi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and repository maintainers use this skill to coordinate batch GitHub issue fixes from triage through pull request creation, CI/CD follow-up, merge, deployment verification, and final reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent through a broad GitHub maintainer workflow with write access, including pushing code, creating pull requests, fixing CI failures, merging, and using admin merge. <br>
Mitigation: Before execution, specify the repository, exact issue numbers, target branch, and require explicit confirmation before any push, pull request creation, CI-driven code change, merge, admin merge, or deployment-related step. <br>
Risk: The workflow assumes an authenticated GitHub CLI and repository push permissions. <br>
Mitigation: Use least-privilege credentials scoped to the target repository and review the proposed issue grouping, branch plan, and commands before allowing write operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gdyshi/github-iteration-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline Git and GitHub CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include branch, commit, pull request, CI/CD, deployment, and issue-reporting details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
