## Description: <br>
Detect GitHub Actions workflow groups that stopped running on their normal cadence using median run intervals and current inactivity gap. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniellummis](https://clawhub.ai/user/daniellummis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and platform engineers use this skill to audit GitHub Actions run exports for workflows that have stopped running on their expected cadence, then review text or JSON results for CI checks and automation guardrails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A critical result can fail automation when FAIL_ON_CRITICAL=1 is enabled. <br>
Mitigation: Review RUN_GLOB filters, regex scope, and warning or critical thresholds before using the fail gate in CI. <br>
Risk: The audit depends on local JSON exports and can miss workflows that are absent from the selected files. <br>
Mitigation: Confirm the exported run set covers the repositories, workflows, branches, events, run IDs, and run URLs being audited. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daniellummis/github-actions-run-gap-audit) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, text, json, shell commands, configuration] <br>
**Output Format:** [Text report or JSON summary of stale workflow groups, including severity, gap metrics, filters, and critical group details.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can exit nonzero when FAIL_ON_CRITICAL=1 and one or more workflow groups are critical.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
