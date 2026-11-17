## Description:

Offline assistant for FDM 3D printer troubleshooting, maintenance guidance, image analysis, calibration G-code, profile management, and log export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redtechsupplylabs](https://clawhub.ai/user/redtechsupplylabs)

### License/Terms of Use:

MIT-0

## Use Case:

3D printer owners, operators, and support technicians use this skill for local troubleshooting, maintenance planning, failed-print analysis, calibration G-code drafting, profile management, and CSV maintenance-log export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated G-code or maintenance instructions may be incompatible with a specific printer, material, firmware, or operating condition.

Mitigation: Treat outputs as advisory and review printer compatibility, temperatures, motion commands, and file destinations before use.

Risk: The inspected package appears incomplete because most action, workflow, and prompt files are empty.

Mitigation: Verify installed artifact contents and test each workflow locally before relying on the skill.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Text or Markdown guidance, with G-code/configuration-style output and CSV log output when implemented]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally through OpenClaw/Ollama according to the artifact documentation; current release evidence says most action, workflow, and prompt files are empty.]

## Skill Version(s):

1.0.0 (source: release evidence and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
