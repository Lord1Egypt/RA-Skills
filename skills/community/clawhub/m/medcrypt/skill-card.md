## Description: <br>
Helps agents work with a local Python prototype for AES-256-GCM encryption, decryption, audit logging, key rotation, and emergency key recovery for medical messaging workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CryptoReuMD](https://clawhub.ai/user/CryptoReuMD) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Healthcare developers, security reviewers, and agent operators can use this skill to inspect and run a local encryption prototype for protecting message payloads before they are copied into consumer messaging channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release overstates regulatory compliance and safety for sending patient medical data through Telegram, WhatsApp, or similar consumer messaging apps. <br>
Mitigation: Treat the artifact as a local encryption prototype and require legal, security, and organizational review before using it with protected health information. <br>
Risk: Client-side encryption does not by itself address metadata exposure, device compromise, backups, recipient identity, retention, auditing, or consent. <br>
Mitigation: Approve the full workflow, including endpoint security, platform policy, identity checks, retention controls, audit requirements, and patient consent, before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CryptoReuMD/medcrypt) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>
- [Artifact medcrypt.py](artifact/medcrypt.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local command examples and healthcare security caveats.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
