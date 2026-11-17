## Description:

MTProto 2.0 protocol implementation guidance for Telegram backend development, covering encryption, handshake flow, message serialization, TL language, and security considerations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhihang9978](https://clawhub.ai/user/zhihang9978)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review MTProto 2.0 implementation guidance for Telegram-compatible backends, including handshake, encryption, TL serialization, and message formatting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security-critical examples may contain contradictory or incorrect protocol and cryptography guidance.

Mitigation: Check the official Telegram specification, known-good libraries, and independent cryptographic review before using the guidance for production implementation.

Risk: Example code may be copied into production without validating randomness, buffer sizing, Auth Key ID handling, or error handling.

Mitigation: Apply the security notice checklist before deployment, including crypto/rand usage, 8-byte Auth Key ID validation, official vectors, buffer-size checks, and expert review.

## Reference(s):

- [Handshake Details](references/handshake.md)
- [Encryption Algorithm](references/encryption.md)
- [Message Format](references/message-format.md)
- [TL Language](references/tl-language.md)
- [Security Notice](references/security-notice.md)
- [Telegram MTProto Documentation](https://core.telegram.org/mtproto)
- [Telegram API Documentation](https://core.telegram.org/api)
- [Telegram TL Schema](https://core.telegram.org/schema)
- [Telegram TL Language Specification](https://core.telegram.org/mtproto/TL)
- [Go crypto/rand Package](https://golang.org/pkg/crypto/rand/)
- [Go Constant-Time Comparison](https://pkg.go.dev/crypto/subtle#ConstantTimeCompare)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands]

**Output Format:** [Markdown with Go, TL, and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; examples require independent security review before production use.]

## Skill Version(s):

1.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
