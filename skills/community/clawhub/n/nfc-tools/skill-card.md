## Description:

NFC tag discovery, inspection, and cautious write workflows using libnfc/nfc-utils; trigger when the user asks to read tags, inspect NDEF payloads, write or update NFC data, or automate tag batches with a PN532/ACR122 reader.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ppopen](https://clawhub.ai/user/ppopen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect NFC readers and tags, plan NDEF or sector payloads, and run guarded read, write, erase, or format workflows with libnfc/nfc-utils. It is also useful for offline preparation when NFC hardware or drivers are unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: NFC write, erase, format, or reset operations can irreversibly change tag contents.

Mitigation: Require exact confirmation text before destructive operations, preview payload bytes, preserve a pre-write dump, and re-read the tag after writing.

Risk: Tag UIDs and identifiers can expose sensitive device or access-token metadata in logs or user-visible output.

Mitigation: Redact UIDs by default and reveal them only when the operation explicitly requires it.

Risk: Local setup commands may require elevated permissions for NFC utilities, udev rules, or reader configuration.

Mitigation: Review sudo setup commands before running them and install only when local NFC reader support is needed.

## Reference(s):

- [NFC hardware fallback guide](references/fallback.md)
- [NFC CLI sanity-check script](scripts/check-nfc.sh)
- [ClawHub skill page](https://clawhub.ai/ppopen/skills/nfc-tools)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown with inline shell commands and procedural checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes confirmation gates for destructive NFC operations and UID redaction guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
