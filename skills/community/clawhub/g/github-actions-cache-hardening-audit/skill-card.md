## Description: <br>
Audit GitHub Actions workflow cache usage for poisoning, keying, and secret-path risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniellummis](https://clawhub.ai/user/daniellummis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security engineers use this skill to statically inspect GitHub Actions workflows for risky cache patterns before merging or releasing CI changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit script reads local files matched by WORKFLOW_GLOB, so an overly broad glob can expose more repository content than intended. <br>
Mitigation: Keep WORKFLOW_GLOB scoped to GitHub Actions workflow files unless intentionally auditing another file set. <br>
Risk: Enabling FAIL_ON_CRITICAL can fail CI when critical cache-hardening findings are detected. <br>
Mitigation: Enable FAIL_ON_CRITICAL only after the team is ready for this audit to gate builds. <br>
Risk: The skill reports static cache-risk signals and does not prove whether a workflow has been exploited. <br>
Mitigation: Review reported workflows and confirm remediation in the repository's security and CI context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daniellummis/github-actions-cache-hardening-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Text report or JSON with summary, flagged workflows, and critical workflows.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads workflow files matched by WORKFLOW_GLOB and can exit nonzero when FAIL_ON_CRITICAL is enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
