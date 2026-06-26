## Description: <br>
Audit GitHub Actions run reliability by actor to surface high-risk contributors and flaky automation owners. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniellummis](https://clawhub.ai/user/daniellummis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to analyze exported GitHub Actions run data, rank actors or actor-workflow groups by reliability, and identify contributors or automation owners that may need CI triage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reports can include actor, repository, run ID, and URL details from selected GitHub Actions exports. <br>
Mitigation: Point RUN_GLOB only at exports intended for analysis and review generated reports before sharing them. <br>
Risk: Critical findings can fail a CI job or automation step when FAIL_ON_CRITICAL is enabled. <br>
Mitigation: Enable FAIL_ON_CRITICAL only when the workflow is intended to enforce reliability gates. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/daniellummis/github-actions-actor-reliability-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Text report or JSON summary with ranked actor groups and critical findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May exit with code 1 when FAIL_ON_CRITICAL=1 and critical actor groups are detected.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
