## Description: <br>
Manage an LNbits Lightning wallet for balance checks, invoice creation with QR codes, invoice decoding, and confirmed payments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JamesTsetsekas](https://clawhub.ai/user/JamesTsetsekas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an assistant interact with an LNbits Lightning wallet, including receiving payments through Bolt11 invoices and QR codes and sending payments only after balance checks and explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The assistant receives access to an LNbits admin key and can initiate Lightning payments. <br>
Mitigation: Use a dedicated low-balance wallet, keep the admin key out of chat and shared terminals, and require decoded invoice review plus explicit user confirmation before payment. <br>
Risk: The skill sends requests to the LNbits server configured by LNBITS_BASE_URL. <br>
Mitigation: Set LNBITS_BASE_URL only to the intended LNbits instance and verify the configured server before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/JamesTsetsekas/lnbits-with-qrcode) <br>
- [LNbits](https://lnbits.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with inline shell commands, JSON CLI results, and MEDIA file paths for generated QR images.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, qrcode[pil], LNBITS_API_KEY, and LNBITS_BASE_URL; QR PNG files are written under ./.lnbits_qr and old files are cleaned up after about five minutes.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
