## Description:

Locally scans untrusted text and documents to detect prompt injection, jailbreak, data exfiltration, social engineering, and related agent-safety threats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jtil4201](https://clawhub.ai/user/jtil4201)

### License/Terms of Use:

Source-available

## Use Case:

Developers and agent integrators use Guardian Shield to scan untrusted user messages, web fetch results, pasted content, and documents before an agent processes them. It returns clean, suspicious, or threat verdicts with scores and categories so integrations can warn or block risky content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner can warn by default instead of automatically blocking dangerous content, so an agent may continue processing a detected threat if the integration ignores the verdict.

Mitigation: Configure blocking behavior or make the integration stop processing whenever the verdict is threat.

Risk: Optional dependencies and model files affect document parsing, ML scoring, and runtime coverage.

Mitigation: Pin and install required dependencies for the target environment, then verify scanner status before deployment.

## Reference(s):

- [Guardian Shield ClawHub page](https://clawhub.ai/jtil4201/skills/guardian-shield)
- [Fallen Angel Systems](https://fallenangelsystems.com)

## Skill Output:

**Output Type(s):** [Text, JSON, Code, Shell commands, Configuration]

**Output Format:** [Terminal text, JSON, and Python ScanResult objects containing verdicts, scores, categories, and threat details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally; configurable warning and blocking thresholds use 0-100 scores.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
