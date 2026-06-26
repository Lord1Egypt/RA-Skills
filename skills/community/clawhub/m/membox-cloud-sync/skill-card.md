## Description: <br>
Private zero-knowledge encrypted cross-device memory sync, backup, and recovery for OpenClaw. Helps agents install Membox, pair devices, securely sync `MEMORY.md` and `memory/YYYY-MM-DD.md`, and restore encrypted memory while keeping plaintext, passphrases, AMK, and recovery codes local-only. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Pupillen](https://clawhub.ai/user/Pupillen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install and operate Membox-backed encrypted memory sync, backup, pairing, scheduled upload checks, and restore workflows while keeping plaintext memory and recovery secrets local. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plaintext memory, passphrases, recovery codes, AMK, URK, or decrypted recovery bundles could be exposed in chat or sent to a service. <br>
Mitigation: Keep sensitive material in private local files, use strict local file permissions, and do not paste or transmit secrets through the model transcript. <br>
Risk: Unattended sync, pull, or grant approval can fail or run unexpectedly if the vault is locked or managed unlock was not explicitly enabled. <br>
Mitigation: Require a valid session plus a local unlock path or explicit managed-unlock opt-in before scheduling or running unattended memory operations. <br>
Risk: Restore or pull operations could overwrite existing memory files. <br>
Mitigation: Preview changes first and use conflict-safe writes rather than silently replacing `MEMORY.md` or dated memory files. <br>
Risk: The agent could overstate install, pairing, readiness, or version state. <br>
Mitigation: Separate inferred, planned, executed, and verified state, and only claim readiness after checking command or tool results in the current run. <br>


## Reference(s): <br>
- [Membox Workflows](references/workflows.md) <br>
- [Membox API Surface](references/api-surface.md) <br>
- [Distribution and Lazy-User Flow](references/distribution.md) <br>
- [Scheduling and Restore Notes](references/scheduling.md) <br>
- [Membox Cloud Sync on ClawHub](https://clawhub.ai/Pupillen/membox-cloud-sync) <br>
- [Membox service](https://membox.cloud) <br>
- [Membox API base](https://membox.cloud/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, file paths, API endpoints, and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Directs the agent to verify current state before claiming readiness and to keep secret material out of chat.] <br>

## Skill Version(s): <br>
0.1.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
