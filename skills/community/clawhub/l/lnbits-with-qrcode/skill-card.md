## Description:

Manage LNbits Lightning Wallet (Balance, Pay, Invoice).

This skill is ready for commercial/non-commercial use.

## Publisher:

[jamestsetsekas](https://clawhub.ai/user/jamestsetsekas)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to manage an LNbits Lightning wallet through an assistant, including checking balances, creating invoices with QR codes, decoding invoices, creating wallets, and sending payments after confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send real Lightning payments using an LNbits admin key.

Mitigation: Use a dedicated wallet with limited funds and supervise every payment request.

Risk: Payment confirmation is enforced by the assistant protocol rather than by the CLI command itself.

Mitigation: Treat the explicit yes/no payment approval prompt as mandatory, decode invoices first, and check balance before payment.

Risk: A broad admin key and weak endpoint scoping can expose funds if configured against an untrusted LNbits URL.

Mitigation: Configure only a trusted HTTPS LNbits base URL and avoid pasting admin keys or wallet identifiers into chat.

## Reference(s):

- [LNbits](https://lnbits.com)
- [LNbits demo server](https://legend.lnbits.com)
- [ClawHub skill page](https://clawhub.ai/jamestsetsekas/skills/lnbits-with-qrcode)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown responses with inline shell commands, JSON CLI output, Bolt11 invoice text, and MEDIA file paths for QR PNGs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces QR code PNG files under ./.lnbits_qr and expects LNBITS_API_KEY and LNBITS_BASE_URL environment variables.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
