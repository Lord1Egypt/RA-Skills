## Description: <br>
Audit cancelled and timed-out GitHub Actions runs from JSON exports to surface wasted CI minutes and noisy workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniellummis](https://clawhub.ai/user/daniellummis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to analyze exported GitHub Actions run data, quantify wasted CI time from cancelled or timed-out runs, and prioritize noisy workflows for cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit reads local GitHub Actions run exports, which may contain repository, branch, actor, and workflow metadata. <br>
Mitigation: Review RUN_GLOB before execution so it only matches intended JSON exports, and collect Actions metadata only for repositories that are appropriate to analyze locally. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daniellummis/github-actions-cancel-waste-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Text or JSON reports with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can signal critical waste through exit code 1 when FAIL_ON_CRITICAL=1.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
