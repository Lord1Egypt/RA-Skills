## Description:

Audit manual GitHub Actions trigger dependence by workflow/event to flag automation gaps and intervention risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to audit exported GitHub Actions run data for workflows that depend heavily on manual triggers. It helps identify automation gaps, recent manual-trigger streaks, and critical groups that can gate follow-up automation work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the audit executes a local bash wrapper and embedded Python over files matched by RUN_GLOB.

Mitigation: Review the script before use and keep RUN_GLOB scoped to the intended GitHub Actions run export directory.

Risk: A broad or customized RUN_GLOB can include unrelated JSON files and produce misleading audit results or parse errors.

Mitigation: Use the default artifacts/github-actions/*.json pattern or an equivalently constrained path containing only expected run exports.

## Reference(s):


## Skill Output:

**Output Type(s):** [analysis, text, json, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands; runtime reports are text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The shell script reads GitHub Actions run JSON exports, ranks workflow groups, and can exit nonzero when FAIL_ON_CRITICAL=1 and critical groups are found.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
