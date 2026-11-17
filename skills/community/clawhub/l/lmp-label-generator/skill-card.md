## Description:

Generate professional labels in LMP format from natural language descriptions. By default saves only locally; cloud preview runs only when the user explicitly sets config.apiEndpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lams001](https://clawhub.ai/user/lams001)

### License/Terms of Use:

MIT-0

## Use Case:

External users, designers, operators, and developers use this skill to turn natural-language label requests into printable LMP JSON files for product, shipping, asset, price, barcode, QR code, and compliance-style label layouts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically writes generated .lmp files to the user's Downloads folder.

Mitigation: Install only when local file creation is expected, and review generated files before opening, sharing, or uploading them.

Risk: Generated labels may contain sensitive names, addresses, phone numbers, barcodes, or product details.

Mitigation: Keep apiEndpoint empty for local-only use unless the user accepts that the full label contents may leave the local environment.

Risk: When cloud preview is enabled, label contents are posted to the configured endpoint and the returned preview link may be viewable by anyone who has it.

Mitigation: Use only a verified HTTPS LabelMake Pro endpoint or another trusted endpoint, and treat preview links as shareable rather than private.

Risk: Compliance-style labels are layout and field references, not a legal determination.

Mitigation: Verify generated FDA, EU, China, UK, or supplement labels against current local regulations and qualified review before market use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lams001/skills/lmp-label-generator)
- [LMP Protocol](https://github.com/lams001/lmp-protocol)
- [LabelMake Pro](https://labelmakepro.com)
- [Compliance Guide](COMPLIANCE.md)
- [Product Label Example](references/examples/product-label.json)
- [Asset Label Example](references/examples/asset-label.json)
- [Shipping Label Example](references/examples/shipping-label.json)
- [Report Issues](https://github.com/lams001/lmp-protocol/issues)
- [FDA Nutrition Facts: 21 CFR 101.9](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-B/part-101/subpart-A/section-101.9)
- [FDA Supplement Facts: 21 CFR 101.36](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-B/part-101/subpart-A/section-101.36)
- [EU Regulation 1169/2011](https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX%3A32011R1169)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Files, API Calls, Guidance]

**Output Format:** [Markdown response with LMP JSON saved as a .lmp file and an optional preview link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Always saves a local .lmp file; optionally posts generated label content to a configured HTTPS preview endpoint.]

## Skill Version(s):

1.5.5 (source: SKILL.md frontmatter, clawhub.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
