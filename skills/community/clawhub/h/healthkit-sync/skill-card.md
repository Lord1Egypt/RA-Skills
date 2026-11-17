## Description:

iOS HealthKit data sync CLI commands and patterns for working with the healthsync CLI, fetching Apple Health data, pairing iOS devices over a local network, and understanding the iOS Health Sync security architecture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mneves75](https://clawhub.ai/user/mneves75)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and engineers use this skill to operate and troubleshoot the healthsync CLI for local Apple HealthKit data transfer between an iPhone and a Mac. It helps users pair devices, fetch health data as CSV or JSON, understand configuration, and reason about mTLS, certificate pinning, Keychain storage, and audit logging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HealthKit exports can contain sensitive personal health data, especially when written to CSV or JSON files.

Mitigation: Store only the minimum exported data needed, avoid shared or cloud-synced folders when possible, and delete exports when finished.

Risk: Pairing and data fetches depend on a local iOS device connection and can fail if the devices are not on the same trusted local network.

Mitigation: Use the documented discovery, status, and dry-run commands before fetching data, and confirm that both devices are on the same Wi-Fi network.

Risk: A certificate mismatch can indicate a regenerated server certificate or a potential local-network interception attempt.

Mitigation: Reject mismatched connections and re-pair only after confirming the iOS device identity and expected certificate fingerprint.

## Reference(s):

- [CLI Reference](references/CLI-REFERENCE.md)
- [Security Architecture](references/SECURITY.md)
- [Project Architecture](references/ARCHITECTURE.md)
- [HealthKit Sync on ClawHub](https://clawhub.ai/mneves75/skills/healthkit-sync)
- [mneves75 ClawHub Profile](https://clawhub.ai/user/mneves75)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash, JSON, and CSV examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill provides documentation and command patterns; it does not execute the healthsync CLI on its own.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
