## Description:

Supports Temu US returns and refunds workflows through LinkFox gateway scripts for after-sales lists, details, return orders, return addresses, labels, signatures, carriers, and label uploads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Temu US sellers, commerce operators, and developers use this skill to query and process returns, refunds, and after-sales return logistics through documented Partner API calls.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The skill handles LinkFox API keys and Temu merchant access tokens.

Mitigation: Install only for trusted LinkFox workflows, avoid passing tokens on command lines when possible, and prefer environment variables or managed store keys with restricted local file permissions.

Risk: Temu access tokens can be stored locally in plaintext under the LinkFox token store.

Mitigation: Restrict permissions on ~/.linkfox or the configured token-store path, rotate exposed tokens, and remove stale store entries.

Risk: Complete API responses are saved locally by default and may contain sensitive commerce or customer return data.

Mitigation: Run scripts from an appropriate workspace, restrict permissions on saved response directories, and clean up response files according to the merchant's data-retention policy.

Risk: Generic proxy helpers and endpoint override environment variables can broaden what the skill sends through LinkFox gateways.

Mitigation: Clear untrusted gateway override environment variables before use and prefer the specific returns/refunds scripts over arbitrary proxy helpers.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-temu-returns-refunds-us)
- [API Reference](references/api.md)
- [Partner US Returns and Refunds Catalog](references/partner-us-catalog.md)
- [Access Token Guide](references/access-token.md)
- [Authorization Flow](references/authorization-flow.md)
- [Onboarding Guide](references/onboarding.md)
- [Temu Partner US Documentation](https://partner-us.temu.com/documentation?menu_code=d3d2812d87034d35adb016972349fcb0)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API inputs or responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts save complete API responses locally and may print full JSON or summaries depending on response size and inline mode.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
