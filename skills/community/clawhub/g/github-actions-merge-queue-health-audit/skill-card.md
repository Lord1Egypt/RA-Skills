## Description: <br>
Audit GitHub merge queue workflow health with failure-rate, queue-latency, and stale-success risk scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniellummis](https://clawhub.ai/user/daniellummis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and release engineers use this skill to analyze exported GitHub Actions run JSON for merge queue workflow health, rank risky repository/workflow groups, and optionally fail CI when critical groups are found. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reports may print repository, workflow, run ID, and URL details to stdout. <br>
Mitigation: Run the skill only on intended GitHub Actions exports and treat generated reports as potentially repository-sensitive operational data. <br>
Risk: The shell command analyzes files matched by RUN_GLOB, so an overly broad glob can include unintended JSON exports. <br>
Mitigation: Set RUN_GLOB to the specific exported GitHub Actions run files that should be reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daniellummis/github-actions-merge-queue-health-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Text report or JSON summary produced by a shell command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can exit with status 1 when FAIL_ON_CRITICAL=1 and critical merge queue health groups are detected.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
