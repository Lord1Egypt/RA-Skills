## Description: <br>
Audit GitHub Actions workflow permission scope drift to enforce least-privilege token access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniellummis](https://clawhub.ai/user/daniellummis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security engineers use this skill to audit GitHub Actions workflows for over-broad GITHUB_TOKEN permissions, missing explicit permissions policies, and pull_request_target workflows with write-token risk before CI policy gates are enforced. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit runs local Bash and Python over repository workflow files. <br>
Mitigation: Install only when local script execution is acceptable and keep WORKFLOW_GLOB scoped to the workflow files intended for review. <br>
Risk: Audit reports can expose repository workflow names, event triggers, permission scopes, and line-level findings. <br>
Mitigation: Review reports before sharing them outside the repository or team. <br>
Risk: Enabling FAIL_ON_CRITICAL can intentionally fail CI or automation when critical permission findings are detected. <br>
Mitigation: Enable FAIL_ON_CRITICAL only after the team is ready to enforce the policy gate. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/daniellummis/github-actions-permission-scope-audit) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Text report or JSON summary with ranked workflow findings and critical workflow details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash and python3; can exit nonzero when FAIL_ON_CRITICAL=1 and critical workflows are found.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
