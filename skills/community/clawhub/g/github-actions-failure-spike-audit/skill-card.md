## Description: <br>
Detect sudden GitHub Actions failure-rate spikes by workflow group using recent-vs-baseline run windows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniellummis](https://clawhub.ai/user/daniellummis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and release engineers use this skill to audit exported GitHub Actions run history, identify workflow groups with recent failure-rate spikes, and gate CI when critical regressions are found. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reports can expose repository, branch, workflow, run URL, and failure-trend details from local GitHub Actions exports. <br>
Mitigation: Keep RUN_GLOB scoped to a dedicated export folder and review generated reports before sharing them. <br>
Risk: The optional GitHub CLI export can collect run data from repositories and workflow runs outside the intended audit scope. <br>
Mitigation: Use the GitHub CLI export only for repositories and workflow runs the operator intends to audit. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daniellummis/github-actions-failure-spike-audit) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Text report or JSON summary emitted by a shell script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can return exit code 1 when FAIL_ON_CRITICAL=1 and critical workflow groups are detected.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
