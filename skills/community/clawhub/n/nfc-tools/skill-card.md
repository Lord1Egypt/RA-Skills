## Description: <br>
NFC tag discovery, inspection, and cautious write workflows using libnfc/nfc-utils; trigger when the user asks to read tags, inspect NDEF payloads, write or update NFC data, or automate tag batches with a PN532/ACR122 reader. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ppopen](https://clawhub.ai/user/ppopen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect NFC readers and tags, plan NDEF or block-level payloads, and perform guarded read, write, erase, or format workflows with libnfc-compatible hardware. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: NFC write, erase, format, or reset commands can permanently change a physical tag. <br>
Mitigation: Require the exact confirmation gate, verify the reader, tag, payload, and rollback dump first, then re-read the tag after the operation. <br>
Risk: Tag UIDs and dumps can expose sensitive identifiers or access data. <br>
Mitigation: Redact UIDs in user-visible output by default and keep tag dumps private unless disclosure is operationally required. <br>
Risk: Reader setup can require elevated OS permissions or udev changes. <br>
Mitigation: Review sudo and udev setup before use and run the provided NFC environment check before touching hardware. <br>


## Reference(s): <br>
- [NFC hardware fallback guide](references/fallback.md) <br>
- [ClawHub skill page](https://clawhub.ai/ppopen/nfc-tools) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and file references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit confirmation before NFC write, erase, format, or reset commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
