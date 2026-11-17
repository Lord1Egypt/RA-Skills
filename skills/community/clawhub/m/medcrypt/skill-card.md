## Description:

Demonstrates client-side encryption and decryption for medical message content using AES-256-GCM, PBKDF2-derived keys, encrypted audit logging, key rotation, and emergency key shares.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[cryptoreumd](https://clawhub.ai/user/cryptoreumd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and healthcare security reviewers can inspect a compact Python demo for encrypting patient-physician messages before sending over consumer messaging channels. It is suitable for evaluating cryptography concepts, not for production medical messaging or compliance assurance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security and compliance claims may exceed what the demo implementation proves.

Mitigation: Treat the artifact as a cryptography demo and require independent security, privacy, and compliance review before any patient-data use.

Risk: Production medical messaging, audit logging, and emergency recovery require operational controls beyond the included script.

Mitigation: Do not deploy for clinical workflows until key management, logging durability, access recovery, and regulatory controls are redesigned and validated.

Risk: The demo includes local sample execution behavior that is not a complete secure messaging system.

Mitigation: Review the Python script before running it, use synthetic data during evaluation, and replace demo flows before integration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cryptoreumd/skills/medcrypt)
- [ClawHub publisher profile](https://clawhub.ai/user/cryptoreumd)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and Python code references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and the cryptography package; outputs should be reviewed before use with patient data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
