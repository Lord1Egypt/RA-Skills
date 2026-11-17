## Description:

Guides authorized Wi-Fi and Bluetooth checks, phone safety reviews, and manual inspections for suspected hidden cameras or tracking devices, then helps summarize findings in a plain-language report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samjoeyang](https://clawhub.ai/user/samjoeyang)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and people checking a room or personal device use this skill to review authorized network and Bluetooth findings, follow manual inspection and phone safety steps, and understand the results in a plain-language report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A scan may exceed the authorized network range or probe devices without permission.

Mitigation: Confirm the exact scan range and authorization before running active network probes.

Risk: Users may misunderstand wireless checks as passive when they transmit probes.

Mitigation: Describe wireless scan behavior accurately and disclose active probe transmissions before running them.

Risk: Uninstalling apps or resetting a phone can destroy evidence or personal data.

Mitigation: Preserve relevant evidence and backups before removing apps or considering a reset.

Risk: Reports may contain information about other people's devices.

Mitigation: Keep reports private and limit their use to the user's personal security review.

Risk: Unreviewed dependencies may introduce unwanted behavior or exposure.

Mitigation: Review the full dependency list before approving installation.

## Reference(s):

- [Manual inspection, phone forensics, and authorization checklist](artifact/references/manual_checklist.md)
- [Phone safety checks and evidence guidance](artifact/references/phone_check.md)
- [Platform capability and alternatives guide](artifact/references/platforms.md)
- [Device vendor, port, and tracker identification references](artifact/references/vendors_ports.md)
- [ClawHub skill page](https://clawhub.ai/samjoeyang/skills/hidden-camera-scanner)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown, JSON, Shell commands]

**Output Format:** [Plain-language Markdown reports and JSON scan summaries, with shell commands and checklists when useful.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings depend on authorized scans and user observations; reports should identify untested stages and method limitations.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata; bundled SKILL.md declares 1.2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
