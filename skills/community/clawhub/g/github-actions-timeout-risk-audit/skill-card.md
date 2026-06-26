## Description: <br>
Audit GitHub Actions job runtime risk against timeout thresholds so near-timeout jobs get fixed before they fail CI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniellummis](https://clawhub.ai/user/daniellummis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and CI maintainers use this skill to audit GitHub Actions run exports for jobs near timeout thresholds, prioritize fixes, and optionally gate CI when critical timeout risks appear. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CI gating can fail pipelines when critical timeout findings are present. <br>
Mitigation: Enable FAIL_ON_CRITICAL only when critical timeout findings should block the pipeline, and review timeout thresholds before using the skill as a gate. <br>
Risk: Broad input globs can process unintended JSON files. <br>
Mitigation: Keep RUN_GLOB limited to GitHub Actions run export files. <br>
Risk: Incomplete run exports can reduce report accuracy. <br>
Mitigation: Collect GitHub Actions JSON that includes job startedAt, completedAt, and conclusion fields. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daniellummis/github-actions-timeout-risk-audit) <br>
- [Publisher profile](https://clawhub.ai/user/daniellummis) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Text report or JSON object] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can exit with status 1 when FAIL_ON_CRITICAL=1 and critical timeout findings are present; requires bash and python3.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
