## Description: <br>
MTProto 2.0 protocol implementation guidance for Telegram backend developers implementing encryption, handshake, message serialization, TL language support, or Telegram-compatible servers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhihang9978](https://clawhub.ai/user/zhihang9978) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill as a non-authoritative learning aid when studying MTProto 2.0 handshakes, encryption, message formatting, TL serialization, and Telegram-compatible backend behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unsafe or contradictory cryptography guidance could mislead production MTProto implementations. <br>
Mitigation: Use the skill only as a non-authoritative learning aid; cross-check every protocol detail against Telegram official documentation and audited implementations. <br>
Risk: Implementation mistakes around Auth Key ID derivation, random generation, padding, message-key verification, AES-IGE assumptions, or bounds checks could compromise security. <br>
Mitigation: Require expert cryptography review, official test vectors, and rigorous buffer, offset, and bounds testing before handling real keys or production traffic. <br>


## Reference(s): <br>
- [Handshake Details](references/handshake.md) <br>
- [Encryption Algorithm](references/encryption.md) <br>
- [Message Format](references/message-format.md) <br>
- [TL Language](references/tl-language.md) <br>
- [Security Notice](references/security-notice.md) <br>
- [MTProto Official](https://core.telegram.org/mtproto) <br>
- [TL Schema](https://core.telegram.org/schema) <br>
- [Telegram API](https://core.telegram.org/api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown guidance with inline Go and TL code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; no tools or commands are executed by the skill.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
