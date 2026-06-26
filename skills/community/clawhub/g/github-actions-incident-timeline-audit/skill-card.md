## Description: <br>
Cluster failed GitHub Actions runs into incident windows by repo to expose outage duration, impact scope, and escalation severity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniellummis](https://clawhub.ai/user/daniellummis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, CI maintainers, and release engineers use this skill to turn failed GitHub Actions run exports into incident windows for reliability reviews, dashboards, and optional CI fail gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The input glob can include unintended JSON files if RUN_GLOB is too broad. <br>
Mitigation: Set RUN_GLOB to the intended GitHub Actions export directory or file pattern before running the script. <br>
Risk: Generated reports may expose repository, branch, workflow, run ID, and run URL details. <br>
Mitigation: Handle text and JSON reports as potentially sensitive CI data and share them only with appropriate reviewers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daniellummis/github-actions-incident-timeline-audit) <br>
- [Publisher profile](https://clawhub.ai/user/daniellummis) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [Plain text report or JSON object containing summary data, ranked incidents, all incidents, and critical incident details.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can exit with status 1 when FAIL_ON_CRITICAL=1 and critical incidents are found.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
