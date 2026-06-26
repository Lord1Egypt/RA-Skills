## Description: <br>
Provides base64 encoding, decoding, validation, URL-safe conversion, buffer support, and file encode/decode utilities for data handling workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to encode, decode, validate, detect, and transform base64 data in local data handling workflows, including URL-safe strings, JSON payloads, buffers, data URIs, and files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: File encode and decode helpers can read from or write to paths supplied by an agent. <br>
Mitigation: Only allow file operations on intended inputs and destinations; do not point the skill at secrets, system files, or important output paths unless that access is explicitly intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/jpeng-base64-toolkit) <br>
- [Publisher profile](https://clawhub.ai/user/jpengcheng523-netizen) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Code] <br>
**Output Format:** [JavaScript module exports and CLI text or JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [File helpers can read from or write to local paths supplied by the caller.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
