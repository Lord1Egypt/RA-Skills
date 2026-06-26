## Description: <br>
Checks remote pull request CI status, diagnoses failures, applies a one-time rerun policy for likely flaky runs, and reports whether the PR can be merged. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chinasilva](https://clawhub.ai/user/chinasilva) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and maintainers use this skill to gate pull request merges by checking required CI status, diagnosing failed jobs from logs, and deciding whether to fix code or perform one confirmed rerun for likely transient failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses the local GitHub CLI login to inspect pull request checks and failed workflow logs. <br>
Mitigation: Confirm the GitHub CLI account and repository scope are appropriate before use, and review any accessed CI evidence before acting on it. <br>
Risk: Rerunning a workflow changes remote CI state and can hide flaky behavior if treated as a fix. <br>
Mitigation: Require confirmation before rerunning, limit reruns to one clearly transient failure, and do not treat a successful rerun as root-cause remediation. <br>
Risk: Incorrect CI diagnosis could lead to merging with unresolved required-check failures. <br>
Mitigation: Require job or log evidence for each failed item and default to not skipping required checks. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with GitHub CLI command examples and CI gate conclusions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs merge readiness conclusions such as can merge or cannot merge, with evidence from jobs or logs when failures exist.] <br>

## Skill Version(s): <br>
1.1.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
