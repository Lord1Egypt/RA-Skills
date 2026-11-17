## Description:

Audit rerun debt by commit SHA to find commits that repeatedly burn CI minutes across workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and CI maintainers use this skill to analyze GitHub Actions run exports, identify commit SHAs associated with repeated reruns or failures, and optionally gate CI on critical rerun debt.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes GitHub Actions run exports that may include private repository CI data.

Mitigation: Review RUN_GLOB before running the skill and point it only at the intended JSON exports.

Risk: A CI job can fail when FAIL_ON_CRITICAL=1 and the configured thresholds classify SHA groups as critical.

Mitigation: Run in report mode first, tune thresholds for the repository, and enable FAIL_ON_CRITICAL only after reviewing expected findings.

Risk: Malformed or incomplete run exports can produce parse errors or incomplete audit results.

Mitigation: Collect exports with the documented GitHub CLI fields and review parse_errors in the report output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daniellummis/skills/github-actions-sha-rerun-debt-audit)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands; runtime output is plain text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The audit can exit non-zero when FAIL_ON_CRITICAL=1 and critical SHA groups are found.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
