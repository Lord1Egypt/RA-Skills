## Description:

HDL Skills Hub coordinates authenticated HDL API skills for login, request signing, product lookup, shopping cart updates, home selection, and smart-home device control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superzhangquansong](https://clawhub.ai/user/superzhangquansong)

### License/Terms of Use:

MIT-0

## Use Case:

External HDL users and agents use this skill to safely navigate HDL smart-home and commerce workflows that require authentication, signed API requests, product search, cart changes, and device control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles passwords, app secrets, access tokens, refresh tokens, and request signatures.

Mitigation: Use a secure secret-input or login handoff flow, protect .env storage, avoid chat transcript storage of passwords, and redact tokens, signatures, secrets, and IDs from user-visible output.

Risk: The skill can change shopping carts and control real-world smart-home devices.

Mitigation: Require explicit user confirmation before cart changes or device-control actions, and scope HDL tokens to the minimum permissions needed.

Risk: API responses may contain sensitive internal identifiers and home or device metadata.

Mitigation: Return descriptive names and operation results only; do not expose home IDs, device IDs, SKU IDs, project IDs, ERP numbers, secret keys, local secrets, or request signatures.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/superzhangquansong/skills/hdl-skills-hub)
- [HDL Skills Hub Source](artifact/SKILL.md)
- [User Authentication API Skill](artifact/user-auth-api/SKILL.md)
- [Sign Encryption API Skill](artifact/sign-encryption-api/SKILL.md)
- [Product Query API Skill](artifact/product-query-api/SKILL.md)
- [Shopping Cart API Skill](artifact/shopping-cart-api/SKILL.md)
- [Device Control API Skill](artifact/device-control-api/SKILL.md)
- [Home Management API Skill](artifact/home-management-api/SKILL.md)
- [API Specification Skill](artifact/api-spec/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown responses with structured API request and response guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires authenticated HDL context and careful redaction of tokens, signatures, secrets, and internal IDs.]

## Skill Version(s):

1.2.0 (source: artifact frontmatter; release metadata version is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
