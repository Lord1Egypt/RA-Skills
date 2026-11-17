## Description:

Use when ordering 蜜雪冰城 (Mixue) drinks from the terminal — list shops, read the menu, place an order, check the pickup number. Checkout is gift-card only; requires the user's own login token captured from their own traffic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzzhe2333](https://clawhub.ai/user/zzzhe2333)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to find Mixue stores and drinks, check gift-card balances, and place or track orders on the user's own account. The agent must get explicit approval before purchases or cancellations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that some outputs can expose full gift-card numbers despite the documented masking.

Mitigation: Use a release that fixes gift-card masking before agent use; keep order and error output out of shared chats and logs.

Risk: The bundled shared signing key has unverified provenance, and login credentials can authorize account operations.

Mitigation: Protect the user's token and capture files, use only the user's own account, and verify or replace the signing key before use.

Risk: Some commands change cart or order state, and quote operations still make network requests.

Mitigation: Explain networked effects, confirm cart changes with the user, and obtain explicit approval before purchases or cancellations.

## Reference(s):

- [ClawHub release](https://clawhub.ai/zzzhe2333/skills/mixuebingcheng-cli-1-11-1)
- [Protocol details](artifact/references/protocol.md)
- [Mixue service endpoint](https://mxsa.mxbc.net)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [CLI commands and JSON or human-readable menu, quote, order, and status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the user's Mixue account; network calls may occur for quotes and lookups, while purchases and cancellations require explicit approval.]

## Skill Version(s):

1.11.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
