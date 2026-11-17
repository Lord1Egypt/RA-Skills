## Description:

Audit GitHub Actions workflow files for hardening gaps (missing timeouts/permissions/concurrency and floating action refs).

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to statically audit GitHub Actions workflow files for CI hardening gaps before risky defaults reach production repositories. It supports local reporting, JSON output, targeted file or event filtering, and optional CI failure on critical workflow findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The static parser can miss some valid GitHub Actions YAML forms.

Mitigation: Confirm important CI policy decisions with a YAML-aware workflow linter or additional security review.

Risk: Audit results may be incomplete if file, event, or allow-list regex filters are too broad or too narrow.

Mitigation: Review filter settings before using results as a CI gate and run an unfiltered audit when establishing repository baselines.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daniellummis/skills/github-actions-workflow-hardening-audit)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain-text or JSON workflow audit reports with shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can exit non-zero when FAIL_ON_CRITICAL=1 and critical workflows are found.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
