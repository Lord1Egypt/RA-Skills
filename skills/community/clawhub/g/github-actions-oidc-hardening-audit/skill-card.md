## Description: <br>
Audit GitHub Actions cloud auth workflows for OIDC hardening gaps like missing id-token write permissions, static cloud secrets, and floating auth action refs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniellummis](https://clawhub.ai/user/daniellummis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, DevOps engineers, and security teams use this skill to audit GitHub Actions workflows for cloud OIDC hardening gaps before identity or secret exposure issues reach CI/CD environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit reads workflow files selected by WORKFLOW_GLOB and optional regex filters. <br>
Mitigation: Keep WORKFLOW_GLOB and file filters scoped to repositories and workflow files intended for inspection. <br>
Risk: The package is not from the trusted @openclaw publisher and has no server-resolved GitHub import provenance. <br>
Mitigation: Review the Bash/Python script before deployment when provenance matters. <br>
Risk: Findings are static-analysis signals and can require context-specific interpretation. <br>
Mitigation: Review flagged workflows before changing permissions, action refs, or cloud authentication settings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daniellummis/github-actions-oidc-hardening-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Text or JSON audit report with workflow counts, flagged workflows, severity scores, issue codes, and optional CI fail-gate exit status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output is controlled by environment variables including WORKFLOW_GLOB, TOP_N, OUTPUT_FORMAT, WARN_SCORE, CRITICAL_SCORE, WORKFLOW_FILE_MATCH, WORKFLOW_FILE_EXCLUDE, ALLOW_REF_REGEX, and FAIL_ON_CRITICAL.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
