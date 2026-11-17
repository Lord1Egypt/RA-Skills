## Description:

Automatically scans Windows Start Menu shortcuts and opens applications by name with fuzzy matching on user command.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flychicks](https://clawhub.ai/user/flychicks)

### License/Terms of Use:

MIT-0

## Use Case:

Windows users use this skill to let an agent refresh a cached Start Menu shortcut list and open installed applications from natural-language app names.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ambiguous fuzzy matching can open an unintended application.

Mitigation: Confirm the matched application name before launching when the requested name is short or ambiguous.

Risk: The skill needs filesystem access to scan Start Menu shortcut directories and maintain a local cache.

Mitigation: Limit use to trusted Windows environments and keep the scan scope to Start Menu shortcut locations.

Risk: The published artifact appears incomplete because the manifest points to main.ps1 but the artifact only includes documentation and schema files.

Mitigation: Verify that the executable PowerShell entrypoint is present before relying on the skill in an agent workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flychicks/skills/openstartmenuink)
- [Publisher profile](https://clawhub.ai/user/flychicks)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Windows-only; depends on PowerShell and filesystem access to Start Menu shortcut directories.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.schema.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
