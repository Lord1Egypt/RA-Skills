## Description: <br>
Audit GitHub Actions reliability by commit SHA to surface risky commits causing repeated workflow failures across branches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniellummis](https://clawhub.ai/user/daniellummis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and CI maintainers use this skill to analyze exported GitHub Actions run data, group failures by repository and commit SHA, and identify commits that may need rollback, revert, or targeted fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local GitHub Actions JSON exports selected by RUN_GLOB, so an overly broad glob can include runs the user did not intend to analyze. <br>
Mitigation: Set RUN_GLOB only to the GitHub Actions JSON export path intended for the audit. <br>
Risk: Enabling FAIL_ON_CRITICAL can intentionally fail CI when critical commit-risk results are found. <br>
Mitigation: Enable FAIL_ON_CRITICAL only when critical commit-risk findings should block the workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daniellummis/github-actions-commit-health-audit) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Text report or JSON summary with scored commit-risk groups] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports filters, severity thresholds, top-N ranking, and optional CI fail-gating.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
