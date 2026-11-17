## Description:

Log vehicle mileage, review driving trends, and export trip reports for tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents can use this skill to record mileage-related entries, review status and summary statistics, search activity, and export local reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is advertised as vehicle mileage tracking, while security evidence says it can retain broader personal home-management notes under the mileage label.

Mitigation: Review intended commands before use and avoid storing sensitive travel, schedule, cost, household, or unrelated personal information unless that local retention is acceptable.

Risk: The skill stores searchable and exportable local data under ~/.local/share/mileage without a documented cleanup or retention workflow.

Mitigation: Manage local file permissions, review exported files before sharing them, and manually delete retained data when it is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/mileage)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [shell commands, text, files, configuration]

**Output Format:** [Command-line text with local log files and JSON, CSV, or plain-text exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores data locally under ~/.local/share/mileage.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
