## Description:

Manage and track plants and gardens with care schedules, growth monitoring, and detailed records for watering, fertilizing, pruning, harvesting, and related care.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johstracke](https://clawhub.ai/user/johstracke)

### License/Terms of Use:


## Use Case:

External gardeners, indoor plant keepers, and small garden managers use this skill to maintain plant inventories, record care actions, search plant records, and export plant data for backup or review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The export command can write Markdown files across broad areas of the user's home directory and may overwrite unintended files.

Mitigation: Use exports only with explicit Markdown paths in ~/.openclaw/workspace or a dedicated exports directory, and review any existing target file before running export.

## Reference(s):

- [Plant Tracker on ClawHub](https://clawhub.ai/johstracke/skills/plant-tracker)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with shell command examples and generated Markdown exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores plant records as JSON in the OpenClaw workspace and can export selected records to Markdown.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
