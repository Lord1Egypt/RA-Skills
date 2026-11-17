## Description:

Private zero-knowledge encrypted cross-device memory sync, backup, and recovery for OpenClaw. Helps agents install Membox, pair devices, securely sync `MEMORY.md` and `memory/YYYY-MM-DD.md`, and restore encrypted memory while keeping plaintext, passphrases, AMK, and recovery codes local-only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pupillen](https://clawhub.ai/user/pupillen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install and pair Membox, sync selected local memory files across devices, schedule protected uploads, and restore encrypted memory without exposing secrets in chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install an external Membox plugin and enable persistent sync behavior around sensitive memory files.

Mitigation: Require the agent to show the exact plugin version and source, then get explicit confirmation before installing components or scheduling unattended sync.

Risk: Managed unlock, account deletion, recovery rotation, restore, and grant approval can affect access to encrypted memory data.

Mitigation: Require explicit user confirmation before enabling managed unlock or invoking restore, deletion, recovery rotation, or trusted-device approval actions.

Risk: Passphrases, AMK, recovery codes, or decrypted recovery material could be exposed if handled in chat.

Mitigation: Keep secrets in private local files, use restrictive file permissions where supported, and do not paste secret material into the chat transcript.

Risk: Pull or restore operations can overwrite local memory files.

Mitigation: Preview restore results and use conflict-safe writes before replacing `MEMORY.md` or dated memory files.

## Reference(s):

- [Membox Cloud Sync on ClawHub](https://clawhub.ai/pupillen/skills/membox-cloud-sync)
- [Membox service](https://membox.cloud)
- [Membox API base](https://membox.cloud/api/v1)
- [Membox Workflows](references/workflows.md)
- [Distribution and Lazy-User Flow](references/distribution.md)
- [Membox API Surface](references/api-surface.md)
- [Scheduling and Restore Notes](references/scheduling.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, local file path guidance, API endpoint references, and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to use local private files for passphrases and recovery material, and to verify installation, pairing, sync, and restore state before reporting success.]

## Skill Version(s):

0.1.12 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
