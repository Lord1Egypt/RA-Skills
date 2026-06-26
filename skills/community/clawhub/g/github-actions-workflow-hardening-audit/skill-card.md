## Description: <br>
Audit GitHub Actions workflow files for hardening gaps (missing timeouts/permissions/concurrency and floating action refs). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniellummis](https://clawhub.ai/user/daniellummis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and CI maintainers use this skill to statically review GitHub Actions workflow files for hardening gaps before production workflows rely on risky defaults. It supports targeted triage with file and event filters and can optionally fail a CI gate when critical issues are found. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit reads local files matched by WORKFLOW_GLOB, so an overly broad glob can include files beyond GitHub Actions workflows. <br>
Mitigation: Keep WORKFLOW_GLOB scoped to workflow files unless broader local review is intentional. <br>
Risk: FAIL_ON_CRITICAL can cause the command to fail a CI job. <br>
Mitigation: Enable FAIL_ON_CRITICAL only when failing the pipeline on critical workflow hardening findings is desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daniellummis/github-actions-workflow-hardening-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Text report or JSON report with summary, ranked workflow risks, and critical workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local workflow files matched by WORKFLOW_GLOB and can exit nonzero when FAIL_ON_CRITICAL=1.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
