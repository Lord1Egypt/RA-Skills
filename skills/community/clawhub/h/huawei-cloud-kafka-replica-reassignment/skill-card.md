## Description:

Plans Kafka replica expansion from topic and broker spreadsheets and produces validated partition reassignment files for operator review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Kafka operators use this skill to plan replica additions against broker disk capacity and generate staged, validated reassignment JSON for review before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The unauthenticated web interface can expose shared uploads and generated Kafka artifacts.

Mitigation: Prefer the CLI; otherwise bind the UI to localhost, add authentication for remote access, and isolate each user's jobs.

Risk: Unescaped spreadsheet or filename values may render unsafe content in the web interface.

Mitigation: Escape displayed spreadsheet and filename values before using the web interface with untrusted inputs.

Risk: Unpinned dependencies and sensitive Kafka topology or capacity data increase deployment risk.

Mitigation: Pin dependencies and review the deployment environment before processing real cluster data.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-kafka-replica-reassignment)
- [Execution safety](artifact/references/execution-safety.md)
- [Validation rules](artifact/references/validation-rules.md)

## Skill Output:

**Output Type(s):** [JSON reassignment files, Spreadsheet reports, Guidance]

**Output Format:** [JSON and XLSX files with human-readable validation reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reassignment plans require operator review before Kafka execution.]

## Skill Version(s):

1.0.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
