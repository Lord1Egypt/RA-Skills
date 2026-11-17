## Description:

Hardware Inspector helps an agent collect privacy-safe, read-only hardware, driver, firmware, accelerator, runtime, and resource-limit reports for local systems or explicitly requested SSH and Kubernetes targets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dancher00](https://clawhub.ai/user/dancher00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect local or explicitly named remote compute environments, summarize CPU, memory, storage, accelerator, driver, toolkit, and runtime evidence, and distinguish physical hardware from container, scheduler, or process-level resource limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local hardware probes, especially full inspection, may initialize accelerator runtimes or briefly consume accelerator resources.

Mitigation: Use the default report for normal inspection and reserve full inspection for cases where peripheral or ML-framework readiness evidence is needed.

Risk: Remote inspection uses existing SSH or Kubernetes access to connect to a named target.

Mitigation: Run remote inspection only after an explicit request for a specific target, preserve normal authentication and host-key verification, and do not broaden permissions or create remote resources.

Risk: Hardware reports and transport errors may still contain identifying or organization-specific details even with default redaction.

Mitigation: Review reports and errors before sharing them, and disable redaction only when the user explicitly requests an unredacted report and accepts the exposure.

## Reference(s):

- [Platform interpretation notes](references/platform-notes.md)
- [Remote inspection](references/remote-inspection.md)
- [NVIDIA Jetson device skills](https://github.com/NVIDIA-AI-IOT/jetson-device-skills)
- [Hardware report JSON schema](https://raw.githubusercontent.com/dancher00/hardware-inspector/main/schema/hardware-report.schema.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, plus JSON or Markdown hardware reports when the bundled collector is run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are read-only snapshots with privacy redaction enabled by default; remote reports include transport context when SSH or Kubernetes inspection is used.]

## Skill Version(s):

0.1.0 (source: server release evidence and bundled collector scripts)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
