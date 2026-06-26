## Description: <br>
Generate QR codes from text, URLs, or images. Use when users ask to 'generate QR code', 'create QR', or 'make QR code for'. Supports text content, URLs, and local images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nbf819-web](https://clawhub.ai/user/nbf819-web) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to generate scannable QR code images from text, URLs, or intentionally selected local files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The image path input can read and encode arbitrary small local files, which may include secrets or private documents. <br>
Mitigation: Only pass paths to files that are intentionally meant to be converted into a scannable QR code; avoid secrets, keys, configuration files, and private documents. <br>
Risk: The image behavior is described as image-only and auto-compressed, but the security summary says arbitrary small local files may be embedded and compression is not clearly performed. <br>
Mitigation: Validate the selected file type and contents before use, and review generated QR outputs before sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nbf819-web/pr-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, Guidance] <br>
**Output Format:** [JSON-style response containing a generated image path, error, or message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes generated QR code PNG files to the system temporary directory.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
