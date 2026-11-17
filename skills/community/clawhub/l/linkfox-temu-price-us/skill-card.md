## Description:

Helps agents manage Temu US product pricing through LinkFox, including price order queries, recommended supply price lookups, base price estimates, and batch SKU base price changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Temu sellers and operations agents use this skill to query pricing records, estimate or retrieve recommended supply prices, and prepare controlled SKU base-price changes for US listings.

### Deployment Geography for Use:

Global, for use with Temu US and Partner US pricing workflows.

## Known Risks and Mitigations:

Risk: Temu and LinkFox account tokens can grant access to seller operations and are sent through LinkFox gateway calls.

Mitigation: Use dedicated low-privilege Temu tokens where possible, grant only needed permissions, and keep environment variables and the local token store private.

Risk: The skill can change live SKU base prices and query sensitive pricing data for Temu US listings.

Mitigation: Review goods IDs, SKU IDs, currencies, and requested prices before running price-change scripts; query pricing again after changes to confirm results.

Risk: Full API responses and locally saved Temu tokens may persist on disk.

Mitigation: Run in a trusted workspace, protect the Temu token store and generated response files, and avoid sharing saved outputs that may contain store or pricing data.

Risk: Gateway URL overrides can redirect requests containing credentials or business data.

Mitigation: Avoid using gateway override environment variables with real credentials unless the endpoint is explicitly trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-temu-price-us)
- [LinkFox Temu US pricing API reference](references/api.md)
- [Temu access token authorization](references/access-token.md)
- [Partner US price API catalog](references/partner-us-catalog.md)
- [Price API document index](references/apis/README.md)
- [Temu Partner US documentation](https://partner-us.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples, Python script invocations, and JSON API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full API responses are written to local JSON files; small responses print JSON and large responses print summaries unless inline output is requested.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
