## Description: <br>
Audit manual GitHub Actions trigger dependence by workflow/event to flag automation gaps and intervention risk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniellummis](https://clawhub.ai/user/daniellummis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and DevOps engineers use this skill to audit exported GitHub Actions run data for workflows that rely heavily on manual triggers instead of automated CI events. It helps identify automation gaps, recent manual-trigger streaks, and critical operational risks that may need follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit can include unintended local run exports if RUN_GLOB is too broad. <br>
Mitigation: Point RUN_GLOB only at the GitHub Actions run JSON files intended for the audit. <br>
Risk: Fail-on-critical mode can block automation when critical manual-trigger dependence is detected. <br>
Mitigation: Set FAIL_ON_CRITICAL=1 only when CI or release workflows are expected to fail on critical results. <br>
Risk: Findings depend on the completeness and consistency of the exported GitHub Actions run JSON. <br>
Mitigation: Collect run exports with the documented GitHub CLI fields before interpreting the report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daniellummis/github-actions-manual-trigger-audit) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Shell commands, JSON] <br>
**Output Format:** [Text report or JSON report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exit code 1 is used only when FAIL_ON_CRITICAL=1 and one or more audited groups are critical.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
