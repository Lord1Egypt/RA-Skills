## Description: <br>
Audit GitHub Actions workflow files for secret exposure risks like pull_request_target secret usage, secret echo commands, and unpinned action secret passing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniellummis](https://clawhub.ai/user/daniellummis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security engineers use this skill to audit GitHub Actions workflow YAML for risky secret handling before credentials leak or unsafe token use reaches CI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated audit reports may include real secret-looking workflow lines from the repository. <br>
Mitigation: Treat reports as sensitive and avoid publishing or storing them in public logs. <br>
Risk: Over-broad file matching could scan files outside intended GitHub Actions workflow YAML. <br>
Mitigation: Keep WORKFLOW_GLOB scoped to workflow YAML and use WORKFLOW_FILE_MATCH or WORKFLOW_FILE_EXCLUDE when narrowing the audit. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daniellummis/github-actions-secret-exposure-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Text report or JSON summary with ranked workflow findings and optional CI fail gate.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash and python3; configurable with WORKFLOW_GLOB, OUTPUT_FORMAT, score thresholds, filters, and FAIL_ON_CRITICAL.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
