## Description:

Fetches the current public details of a single Etsy listing from a direct product URL, including listing content, pricing, media, variants, shop, delivery, and aggregate review signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, e-commerce researchers, and developers use this skill to inspect one known Etsy listing URL for current product-page details, competitor-page audits, and listing-content extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security verdict is suspicious because the package includes account onboarding, billing, credential, local-storage, and automatic feedback behavior beyond the Etsy lookup.

Mitigation: Install only after reviewing the security summary, use the skill only with a trusted LinkFox publisher account, and confirm any auth or billing action before proceeding.

Risk: The skill handles LinkFox API keys and may guide users through SMS-code login or paid-credit purchase flows.

Mitigation: Treat generated API keys as secrets, prefer a real secret store over shell startup files, and avoid entering SMS codes or making payment selections through an agent unless the publisher is trusted.

Risk: Custom LINKFOX_* endpoint environment variables can redirect network requests away from the default LinkFox services.

Mitigation: Do not use custom LINKFOX_* endpoint variables unless their destinations have been explicitly reviewed and approved.

Risk: Public Etsy page structure changes can cause missing, empty, or misidentified fields in the returned listing data.

Mitigation: Present missing or implausible fields as extraction uncertainty and avoid silently repairing, normalizing, or extrapolating product details.

## Reference(s):

- [Etsy product detail API reference](references/api.md)
- [Authentication and billing onboarding](references/onboarding.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and JSON API output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes full API responses to local JSON files; large responses are summarized unless inline output is requested.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
