## Description: <br>
Measure GitHub Actions failure recovery latency and unresolved incident age by workflow group. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniellummis](https://clawhub.ai/user/daniellummis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and CI maintainers use this skill to audit GitHub Actions run exports, compare workflow recovery latency, identify unresolved failure incidents, and optionally gate CI when critical recovery thresholds are exceeded. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Limited server-resolved provenance may make upstream source review harder. <br>
Mitigation: Review the publisher profile and release page before installing or promoting the skill. <br>
Risk: GitHub Actions exports can contain repository and workflow information that should not be analyzed unintentionally. <br>
Mitigation: Keep RUN_GLOB scoped only to the export files intended for the audit and handle generated reports according to the repository's data policy. <br>
Risk: The documented gh run view collection command uses the currently authenticated GitHub CLI permissions. <br>
Mitigation: Run collection commands from the intended GitHub account or automation identity and collect only the fields needed for the audit. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/daniellummis/github-actions-recovery-latency-audit) <br>
- [Publisher profile](https://clawhub.ai/user/daniellummis) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Text report or JSON report with summary, ranked recovery-risk groups, and critical groups.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can exit with status 1 when FAIL_ON_CRITICAL=1 and one or more groups are critical.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
