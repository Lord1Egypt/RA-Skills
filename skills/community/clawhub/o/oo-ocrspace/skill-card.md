## Description: <br>
OCR.space helps agents run OCR text extraction and conversion-stat lookups through the OOMOL oo CLI instead of calling the OCR.space API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect OCR.space action schemas, extract normalized text from images or Base64 uploads, and check OCR.space conversion statistics through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses sensitive account credentials through an OOMOL-connected OCR.space integration. <br>
Mitigation: Do not request or expose raw API keys; use the configured OOMOL connection and review payloads before running actions. <br>
Risk: OCR runs can fail when the oo CLI is missing, the user is not signed in, the OCR.space connection is expired, or billing is stopped. <br>
Mitigation: Inspect the live connector schema before each run and use the documented setup or recovery steps only after a matching command failure. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/oomol/oo-ocrspace) <br>
- [OCR.space homepage](https://ocr.space) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing payloads; OCR results depend on OCR.space and the connected OOMOL account.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
