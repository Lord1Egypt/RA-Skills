## Description:

Systematically QA tests a web application, fixes discovered bugs in source code with atomic commits, re-verifies fixes, and reports health scores, evidence, and ship readiness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loocor](https://clawhub.ai/user/loocor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run browser-based QA on web applications, document reproducible issues, apply scoped source fixes, and produce QA reports for release readiness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can edit source code and create git commits while fixing QA findings.

Mitigation: Run it on a clean branch, review each commit, and keep the target app and fix scope explicit before execution.

Risk: QA flows may require authentication and could expose sensitive credentials if handled carelessly.

Mitigation: Use test accounts where possible, avoid production credentials unless necessary, and redact secrets from reports.

Risk: Browser-driven testing and generated reports may create local artifacts such as screenshots and QA reports.

Mitigation: Review generated artifacts before sharing and remove sensitive application data from screenshots or reports.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, concise status text, shell commands, and source code changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create QA report files, screenshots, and atomic git commits when fixes are applied.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
