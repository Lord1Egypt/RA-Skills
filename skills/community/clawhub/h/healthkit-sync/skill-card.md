## Description: <br>
iOS HealthKit data sync CLI commands and patterns. Use when working with healthsync CLI, fetching Apple Health data (steps, heart rate, sleep, workouts), pairing iOS devices over local network, or understanding the iOS Health Sync project architecture including mTLS certificate pinning, Keychain storage, and audit logging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mneves75](https://clawhub.ai/user/mneves75) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and engineers use this skill to operate or explain the HealthSync CLI for pairing a Mac with an iOS device, fetching Apple HealthKit data, and understanding the local-network security model. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HealthKit exports and terminal output may contain private health records. <br>
Mitigation: Treat CSV and JSON outputs as sensitive health data, store them only in trusted locations, and avoid sharing terminal transcripts that include fetched samples. <br>
Risk: Pairing on untrusted networks or with untrusted devices could expose sensitive workflows. <br>
Mitigation: Pair only trusted devices on trusted local networks and verify the healthsync CLI source before use. <br>
Risk: Clipboard-based QR troubleshooting can expose unrelated sensitive clipboard contents. <br>
Mitigation: Avoid clipboard debug modes when sensitive clipboard data may be present; prefer scanning a known QR image file when possible. <br>


## Reference(s): <br>
- [HealthKit Sync ClawHub Release](https://clawhub.ai/mneves75/healthkit-sync) <br>
- [CLI Reference](references/CLI-REFERENCE.md) <br>
- [Security Patterns](references/SECURITY.md) <br>
- [Architecture](references/ARCHITECTURE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash, JSON, and CSV examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include healthsync CLI commands, configuration paths, troubleshooting steps, and security guidance for local HealthKit synchronization.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
