## Description: <br>
Detect branch-level GitHub Actions reliability drift by comparing failure and runtime deltas against a mainline baseline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniellummis](https://clawhub.ai/user/daniellummis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and release engineers use this skill to audit exported GitHub Actions runs for branch-specific reliability and runtime drift before issues reach the mainline release flow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper reads files matched by RUN_GLOB. <br>
Mitigation: Keep RUN_GLOB scoped to intended GitHub Actions export files. <br>
Risk: Critical drift findings can fail a pipeline when FAIL_ON_CRITICAL is enabled. <br>
Mitigation: Enable FAIL_ON_CRITICAL only when the pipeline should block on critical branch drift. <br>
Risk: Drift reports may influence CI triage or release decisions. <br>
Mitigation: Review generated text or JSON reports before acting on the findings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daniellummis/github-actions-branch-drift-audit) <br>
- [Publisher profile](https://clawhub.ai/user/daniellummis) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [Text report or JSON report from a Bash/Python command-line helper] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can exit nonzero when FAIL_ON_CRITICAL=1 and critical drift is detected.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
