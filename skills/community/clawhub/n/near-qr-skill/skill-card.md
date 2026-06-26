## Description: <br>
Generate QR codes for NEAR addresses and payment requests, and read NEAR QR codes from images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ussyalfaks](https://clawhub.ai/user/ussyalfaks) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and NEAR users use this skill to generate local QR-code images for account addresses or payment requests and to decode NEAR QR-code images into structured data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment QR codes may encode an incorrect recipient, amount, memo, or output path if the user provides the wrong command inputs. <br>
Mitigation: Review the recipient, amount, memo, and output file path before generating or sharing payment QR codes. <br>
Risk: Dependency drift can affect reproducibility because requirements specify minimum package versions rather than pinned versions. <br>
Mitigation: Install in a trusted Python environment and use pinned dependencies or a lockfile when reproducibility matters. <br>
Risk: QR decoding depends on the zbar system library being installed. <br>
Mitigation: Install zbar before using the read command and verify decoding in the target runtime. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ussyalfaks/near-qr-skill) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell commands, plus generated PNG files and JSON decoded QR data when the commands are run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated payment QR codes can encode recipient, amount, and optional memo values; reading QR codes requires the zbar system library.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, and molthub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
