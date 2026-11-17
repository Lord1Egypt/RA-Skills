## Description:

Fetches public OpenReview paper metadata, reviews, comments, rebuttals, decisions, and meta-reviews, then synthesizes reviewer feedback into a structured report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vectorsss](https://clawhub.ai/user/vectorsss)

### License/Terms of Use:


## Use Case:

Researchers, students, reviewers, and developers use this skill to retrieve public OpenReview review data for a paper and turn it into a concise synthesis of scores, consensus points, disagreements, rebuttals, decisions, and meta-review information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fetched OpenReview discussion data is left in a predictable shared /tmp JSON file.

Mitigation: Run the skill only in trusted, non-privileged environments and remove the generated /tmp/openreview_<forum_id>.json file when it is no longer needed.

Risk: Predictable /tmp output paths can expose data or overwrite writable files through symlinks in shared-user environments.

Mitigation: Avoid shared or privileged environments until output handling uses private temporary directories, restrictive permissions, validated forum IDs, and cleanup or opt-in persistence.

## Reference(s):

- [OpenReview website](https://openreview.net)
- [OpenReview API v2 notes endpoint](https://api2.openreview.net)
- [OpenReview API v1 notes endpoint](https://api.openreview.net)
- [Report Template](references/report-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown synthesis report with supporting JSON review data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Matches the user's language and summarizes public OpenReview review data, including scores, confidence, consensus, disagreements, rebuttals, decisions, and meta-reviews when available.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
