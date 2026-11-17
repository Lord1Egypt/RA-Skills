## Description:

Manage CloudRobo robot registrations, status and metadata, access certificate exports, and robot SDK package information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations teams use this skill to register and manage CloudRobo robot assets, check their status, export access credentials, and retrieve robot SDK package information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Robot registration, update, deletion, and certificate export can change robot state or create a sensitive credential file.

Mitigation: Confirm the target robot and operation with the user before each mutation; verify the robot’s current state before export, and store exported ZIP credentials in a protected location.

Risk: Bundled lifecycle tests may change or delete robot registrations, and telemetry setup installs software whose data handling was unavailable for inspection.

Mitigation: Run lifecycle tests only against disposable registrations. Make telemetry installation opt-in, verify a pinned release before running it, and review its data handling before enabling reports.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-cloudrobo-robot)
- [Publisher profile](https://clawhub.ai/user/huaweicloudskill)
- [CLI Installation Guide](references/cli-installation-guide.md)
- [IAM Policies](references/iam-policies.md)
- [Verification Method](references/verification-method.md)
- [Robot Config Catalog](references/robot-config-catalog.md)
- [Validation Rules](references/validation-rules.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance, Files]

**Output Format:** [Markdown guidance, command examples, JSON results, and an exported ZIP credential bundle]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Robot status and metadata; exported credential bundles require secure storage.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
