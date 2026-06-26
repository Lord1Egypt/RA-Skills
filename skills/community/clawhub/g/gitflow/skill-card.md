## Description: <br>
Automatically push code and monitor CI/CD pipeline status across GitHub and GitLab in one place. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okoddcat](https://clawhub.ai/user/okoddcat) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use GitFlow to push local commits and monitor GitHub or GitLab CI/CD pipeline status without switching to separate pipeline dashboards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can push commits or rerun CI jobs using the user's GitHub or GitLab access. <br>
Mitigation: Require explicit confirmation before any git push or CI rerun, and verify the remote, branch, and target repository first. <br>
Risk: CI logs can expose sensitive build details or secrets to the agent session. <br>
Mitigation: Fetch full or failed-job logs only when the user confirms the contents are appropriate to share in the session. <br>
Risk: Broad GitHub or GitLab credentials can increase the impact of accidental commands. <br>
Mitigation: Use least-privilege tokens and repository-scoped access where possible. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose git push, gh, and glab commands; require confirmation before executing state-changing commands.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
