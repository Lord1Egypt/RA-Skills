## Description:

Audit GitHub Actions artifact storage usage from JSON exports so bloated artifacts are flagged before they inflate CI cost.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and CI maintainers use this skill to audit GitHub Actions artifact JSON exports, identify oversized or stale artifacts, and support cleanup decisions with configurable thresholds and filters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports may include repository names, workflow run IDs, and artifact download URLs from private repository exports.

Mitigation: Keep ARTIFACT_GLOB limited to intended GitHub artifact exports and avoid sharing reports from private repositories broadly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daniellummis/skills/github-actions-artifact-budget-audit)
- [Publisher profile](https://clawhub.ai/user/daniellummis)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration]

**Output Format:** [Text or JSON report with optional bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can exit nonzero when FAIL_ON_CRITICAL=1 and critical artifacts are found.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
