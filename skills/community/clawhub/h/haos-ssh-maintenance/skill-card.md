## Description:

Home Assistant OS SSH maintenance for config files, YAML, custom components, shell troubleshooting, or interactive ha CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nextaltair](https://clawhub.ai/user/nextaltair)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Home Assistant maintainers use this skill when API-based inspection is insufficient and they need SSH-guided maintenance of Home Assistant OS configuration, YAML, custom components, logs, or ha CLI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SSH maintenance and direct Home Assistant storage edits can affect sensitive home-control behavior, including locks, alarms, access control, or physical entry.

Mitigation: Use the skill only for intentional Home Assistant OS maintenance; review sensitive changes, start read-only, back up direct .storage edits, and prefer minimal edits with verification.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and configuration paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes safety-oriented maintenance steps and rollback guidance for direct .storage edits.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
