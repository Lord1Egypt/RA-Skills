## Description:

Track water and sleep with JSON file storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[litiao1224](https://clawhub.ai/user/litiao1224)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to track water intake and sleep events in a local JSON file and view simple daily summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided cup counts are substituted into executable Node commands.

Mitigation: Validate that cup counts are positive numeric values and pass them as command arguments before execution.

Risk: Update and delete actions modify the latest water record.

Mitigation: Ask for confirmation before overwriting or deleting health records.

Risk: Health activity is stored in a local JSON log.

Mitigation: Store the file in an appropriate user-controlled directory and tell the user where records are kept.

## Reference(s):

- [Healthcheck Litiao ClawHub page](https://clawhub.ai/litiao1224/skills/healthcheck-litiao)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files]

**Output Format:** [Plain text responses, inline bash commands, and JSON file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes health-data.json under the configured baseDir.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
